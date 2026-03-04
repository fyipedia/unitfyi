"""Unit conversion engine -- pure Python, Decimal precision, <1ms, DB-free."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext

from unitfyi.data import CATEGORIES, FORMULAS, UNITS, CategoryDef, UnitDef


class IncompatibleUnitsError(ValueError):
    """Raised when trying to convert between incompatible unit categories."""


class UnknownUnitError(ValueError):
    """Raised when a unit slug is not found."""


@dataclass(frozen=True)
class ConversionResult:
    """Result of a unit conversion."""

    value: Decimal
    from_unit: str
    from_symbol: str
    from_name: str
    to_unit: str
    to_symbol: str
    to_name: str
    result: Decimal
    formula_text: str
    category: str
    category_name: str


@dataclass(frozen=True)
class UnitInfo:
    """Information about a single unit."""

    slug: str
    name: str
    symbol: str
    category: str
    description: str
    aliases: list[str]


def convert(value: Decimal, from_slug: str, to_slug: str) -> ConversionResult:
    """Convert a value between two units.

    Supports both linear conversions (via Decimal factors) and non-linear
    conversions (temperature via function-based formulas).

    Args:
        value: The numeric value to convert.
        from_slug: Source unit slug (e.g., "celsius", "kilometer").
        to_slug: Target unit slug (e.g., "fahrenheit", "meter").

    Returns:
        ConversionResult with the converted value and metadata.

    Raises:
        UnknownUnitError: If either unit slug is not found.
        IncompatibleUnitsError: If units belong to different categories.
    """
    from_unit = UNITS.get(from_slug)
    to_unit = UNITS.get(to_slug)
    if from_unit is None:
        raise UnknownUnitError(f"Unknown unit: {from_slug}")
    if to_unit is None:
        raise UnknownUnitError(f"Unknown unit: {to_slug}")
    if from_unit["category"] != to_unit["category"]:
        raise IncompatibleUnitsError(
            f"Cannot convert {from_slug} ({from_unit['category']}) "
            f"to {to_slug} ({to_unit['category']})"
        )

    category = from_unit["category"]

    with localcontext() as ctx:
        ctx.prec = 50

        if category in FORMULAS:
            # Non-linear conversion (temperature, etc.)
            formulas = FORMULAS[category]
            to_base = formulas[from_slug]["to_base"]
            from_base = formulas[to_slug]["from_base"]
            base_value = to_base(value)
            result = from_base(base_value)
        else:
            # Linear conversion: result = value * (from_to_base / to_to_base)
            base_value = value * from_unit["to_base"]
            result = base_value / to_unit["to_base"]

    result = _smart_round(result)

    formula_text = _format_formula(from_slug, to_slug, from_unit, to_unit, category)

    cat_def = CATEGORIES.get(category)
    category_name = cat_def["name"] if cat_def else category

    return ConversionResult(
        value=value,
        from_unit=from_slug,
        from_symbol=from_unit["symbol"],
        from_name=from_unit["name"],
        to_unit=to_slug,
        to_symbol=to_unit["symbol"],
        to_name=to_unit["name"],
        result=result,
        formula_text=formula_text,
        category=category,
        category_name=category_name,
    )


def conversion_table(
    from_slug: str, to_slug: str, values: list[Decimal] | None = None
) -> list[tuple[Decimal, Decimal]]:
    """Generate a conversion table for a unit pair.

    Args:
        from_slug: Source unit slug.
        to_slug: Target unit slug.
        values: List of values to convert. Defaults to common values.

    Returns:
        List of (input_value, converted_value) tuples.
    """
    if values is None:
        values = [Decimal(v) for v in ["1", "5", "10", "25", "50", "100", "250", "500", "1000"]]
    results: list[tuple[Decimal, Decimal]] = []
    for val in values:
        r = convert(val, from_slug, to_slug)
        results.append((val, r.result))
    return results


def get_category_units(category_slug: str) -> list[UnitInfo]:
    """Get all units in a category.

    Args:
        category_slug: Category slug (e.g., "length", "temperature").

    Returns:
        List of UnitInfo objects for all units in the category.
    """
    return [
        UnitInfo(
            slug=slug,
            name=u["name"],
            symbol=u["symbol"],
            category=u["category"],
            description=u.get("description", ""),
            aliases=u.get("aliases", []),
        )
        for slug, u in UNITS.items()
        if u["category"] == category_slug
    ]


def get_unit(slug: str) -> UnitInfo | None:
    """Get a single unit by slug.

    Args:
        slug: Unit slug (e.g., "meter", "celsius").

    Returns:
        UnitInfo if found, None otherwise.
    """
    u = UNITS.get(slug)
    if u is None:
        return None
    return UnitInfo(
        slug=slug,
        name=u["name"],
        symbol=u["symbol"],
        category=u["category"],
        description=u.get("description", ""),
        aliases=u.get("aliases", []),
    )


def get_ordered_categories() -> list[CategoryDef]:
    """Get all categories sorted by display order.

    Returns:
        List of CategoryDef dicts sorted by order field.
    """
    return sorted(CATEGORIES.values(), key=lambda c: c["order"])


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _smart_round(value: Decimal) -> Decimal:
    """Apply appropriate precision based on magnitude."""
    try:
        abs_val = abs(value)
    except InvalidOperation:
        return Decimal("0")
    if abs_val == 0:
        return Decimal("0")
    if abs_val >= 1000:
        return value.quantize(Decimal("0.01"))
    if abs_val >= 1:
        return value.quantize(Decimal("0.0001"))
    if abs_val >= Decimal("0.01"):
        return value.quantize(Decimal("0.000001"))
    return value.quantize(Decimal("0.0000000001"))


def _format_formula(
    from_slug: str,
    to_slug: str,
    from_unit: UnitDef,
    to_unit: UnitDef,
    category: str,
) -> str:
    """Generate human-readable formula text."""
    if category in FORMULAS:
        if category == "temperature":
            return _temperature_formula(from_slug, to_slug, from_unit, to_unit)
        return f"1 {from_unit['symbol']} \u2192 {to_unit['symbol']}"

    from_base = from_unit["to_base"]
    to_base = to_unit["to_base"]
    assert isinstance(from_base, Decimal)
    assert isinstance(to_base, Decimal)
    factor = _smart_round(from_base / to_base)
    return f"1 {from_unit['symbol']} = {factor} {to_unit['symbol']}"


def _temperature_formula(
    from_slug: str,
    to_slug: str,
    from_unit: UnitDef,
    to_unit: UnitDef,
) -> str:
    """Generate temperature conversion formula text."""
    formulas: dict[tuple[str, str], str] = {
        ("celsius", "fahrenheit"): "\u00b0F = (\u00b0C \u00d7 9/5) + 32",
        ("fahrenheit", "celsius"): "\u00b0C = (\u00b0F \u2212 32) \u00d7 5/9",
        ("celsius", "kelvin"): "K = \u00b0C + 273.15",
        ("kelvin", "celsius"): "\u00b0C = K \u2212 273.15",
        ("fahrenheit", "kelvin"): "K = (\u00b0F \u2212 32) \u00d7 5/9 + 273.15",
        ("kelvin", "fahrenheit"): "\u00b0F = (K \u2212 273.15) \u00d7 9/5 + 32",
        ("celsius", "rankine"): "\u00b0R = (\u00b0C + 273.15) \u00d7 9/5",
        ("rankine", "celsius"): "\u00b0C = (\u00b0R \u00d7 5/9) \u2212 273.15",
        ("fahrenheit", "rankine"): "\u00b0R = \u00b0F + 459.67",
        ("rankine", "fahrenheit"): "\u00b0F = \u00b0R \u2212 459.67",
        ("kelvin", "rankine"): "\u00b0R = K \u00d7 9/5",
        ("rankine", "kelvin"): "K = \u00b0R \u00d7 5/9",
    }
    key = (from_slug, to_slug)
    return formulas.get(key, f"1 {from_unit['symbol']} \u2192 {to_unit['symbol']}")
