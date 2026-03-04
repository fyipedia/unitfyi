"""Tests for the unitfyi conversion engine."""

from decimal import Decimal

import pytest

from unitfyi import (
    ConversionResult,
    IncompatibleUnitsError,
    UnitInfo,
    UnknownUnitError,
    conversion_table,
    convert,
    get_category_units,
    get_ordered_categories,
    get_unit,
)
from unitfyi.engine import _smart_round

# ── Linear conversions ──


def test_convert_meters_to_kilometers() -> None:
    result = convert(Decimal("1000"), "meter", "kilometer")
    assert result.result == Decimal("1")
    assert result.from_symbol == "m"
    assert result.to_symbol == "km"
    assert result.category == "length"


def test_convert_kilometers_to_miles() -> None:
    result = convert(Decimal("1"), "kilometer", "mile")
    # 1 km ≈ 0.6214 miles
    assert Decimal("0.6") < result.result < Decimal("0.7")


def test_convert_kilograms_to_pounds() -> None:
    result = convert(Decimal("1"), "kilogram", "pound")
    # 1 kg ≈ 2.2046 lbs
    assert Decimal("2.2") < result.result < Decimal("2.3")


def test_convert_same_unit() -> None:
    result = convert(Decimal("42"), "meter", "meter")
    assert result.result == Decimal("42")


def test_convert_returns_dataclass() -> None:
    result = convert(Decimal("100"), "meter", "kilometer")
    assert isinstance(result, ConversionResult)
    assert result.value == Decimal("100")
    assert result.from_unit == "meter"
    assert result.to_unit == "kilometer"
    assert result.from_name == "Meter"
    assert result.to_name == "Kilometer"
    assert result.category == "length"
    assert result.category_name == "Length"
    assert result.formula_text  # non-empty string


# ── Temperature (non-linear) ──


def test_convert_celsius_to_fahrenheit() -> None:
    result = convert(Decimal("100"), "celsius", "fahrenheit")
    assert result.result == Decimal("212")


def test_convert_fahrenheit_to_celsius() -> None:
    result = convert(Decimal("32"), "fahrenheit", "celsius")
    assert result.result == Decimal("0")


def test_convert_celsius_to_kelvin() -> None:
    result = convert(Decimal("0"), "celsius", "kelvin")
    assert result.result == Decimal("273.15")


def test_convert_kelvin_to_celsius() -> None:
    result = convert(Decimal("273.15"), "kelvin", "celsius")
    assert result.result == Decimal("0")


def test_convert_celsius_to_rankine() -> None:
    result = convert(Decimal("0"), "celsius", "rankine")
    # 0°C = 273.15K, 273.15 * 9/5 = 491.67°R
    assert abs(result.result - Decimal("491.67")) < Decimal("0.01")


def test_convert_negative_temperature() -> None:
    result = convert(Decimal("-40"), "celsius", "fahrenheit")
    assert result.result == Decimal("-40")


# ── Error cases ──


def test_unknown_from_unit() -> None:
    with pytest.raises(UnknownUnitError, match="nonexistent"):
        convert(Decimal("1"), "nonexistent", "meter")


def test_unknown_to_unit() -> None:
    with pytest.raises(UnknownUnitError, match="nonexistent"):
        convert(Decimal("1"), "meter", "nonexistent")


def test_incompatible_categories() -> None:
    with pytest.raises(IncompatibleUnitsError, match="Cannot convert"):
        convert(Decimal("1"), "meter", "kilogram")


# ── conversion_table ──


def test_conversion_table_default() -> None:
    rows = conversion_table("kilometer", "mile")
    assert len(rows) == 9  # default 9 values
    # First value is 1 km
    assert rows[0][0] == Decimal("1")
    assert rows[0][1] > Decimal("0")


def test_conversion_table_custom_values() -> None:
    rows = conversion_table("meter", "foot", values=[Decimal("1"), Decimal("2")])
    assert len(rows) == 2


# ── get_category_units ──


def test_get_category_units_length() -> None:
    units = get_category_units("length")
    assert len(units) > 5
    slugs = [u.slug for u in units]
    assert "meter" in slugs
    assert "kilometer" in slugs
    assert all(isinstance(u, UnitInfo) for u in units)
    assert all(u.category == "length" for u in units)


def test_get_category_units_empty() -> None:
    units = get_category_units("nonexistent")
    assert units == []


# ── get_unit ──


def test_get_unit_exists() -> None:
    unit = get_unit("meter")
    assert unit is not None
    assert unit.slug == "meter"
    assert unit.name == "Meter"
    assert unit.symbol == "m"
    assert unit.category == "length"
    assert isinstance(unit.aliases, list)


def test_get_unit_not_found() -> None:
    unit = get_unit("nonexistent")
    assert unit is None


# ── get_ordered_categories ──


def test_get_ordered_categories() -> None:
    cats = get_ordered_categories()
    assert len(cats) == 20
    # Check sorted by order
    orders = [c["order"] for c in cats]
    assert orders == sorted(orders)
    # Check first and last
    assert cats[0]["slug"] == "length"
    assert cats[-1]["slug"] == "typography"


# ── _smart_round ──


def test_smart_round_large() -> None:
    assert _smart_round(Decimal("12345.6789")) == Decimal("12345.68")


def test_smart_round_medium() -> None:
    assert _smart_round(Decimal("3.14159265")) == Decimal("3.1416")


def test_smart_round_small() -> None:
    assert _smart_round(Decimal("0.0314159265")) == Decimal("0.031416")


def test_smart_round_very_small() -> None:
    result = _smart_round(Decimal("0.00000314159"))
    assert result == Decimal("0.0000031416")


def test_smart_round_zero() -> None:
    assert _smart_round(Decimal("0")) == Decimal("0")


def test_smart_round_negative() -> None:
    assert _smart_round(Decimal("-1234.5678")) == Decimal("-1234.57")
