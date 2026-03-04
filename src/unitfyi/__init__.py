"""unitfyi -- Pure Python unit conversion engine for developers.

220 units across 20 measurement categories with Decimal precision.
Zero dependencies.

Basic usage::

    >>> from unitfyi import convert, get_unit, get_category_units
    >>> from decimal import Decimal
    >>> result = convert(Decimal("100"), "celsius", "fahrenheit")
    >>> result.result
    Decimal('212')
    >>> unit = get_unit("meter")
    >>> unit.name
    'Meter'
"""

from unitfyi.engine import (
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

__version__ = "0.1.0"

__all__ = [
    # Data types
    "ConversionResult",
    "UnitInfo",
    # Exceptions
    "IncompatibleUnitsError",
    "UnknownUnitError",
    # Core conversion
    "convert",
    "conversion_table",
    # Unit queries
    "get_unit",
    "get_category_units",
    "get_ordered_categories",
]
