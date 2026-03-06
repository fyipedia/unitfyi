---
name: unit-tools
description: Convert between 200 units across 20 measurement categories with Decimal precision. Use when converting temperature, length, weight, volume, or any physical unit, generating conversion tables, or looking up unit metadata.
license: MIT
metadata:
  author: fyipedia
  version: "0.1.1"
  homepage: "https://unitfyi.com/"
---

# UnitFYI -- Unit Conversion Tools for AI Agents

Pure Python unit conversion engine. Convert between 200 units across 20 categories with `Decimal` precision, human-readable formula text, and smart magnitude-aware rounding -- all with zero dependencies.

**Install**: `pip install unitfyi` -- **Web**: [unitfyi.com](https://unitfyi.com/) -- **API**: [REST API](https://unitfyi.com/developers/) -- **npm**: `npm install unitfyi`

## When to Use

- User asks to convert between measurement units (km to miles, Celsius to Fahrenheit, kg to lbs)
- User needs a conversion table or reference chart for documentation
- User asks about unit metadata (symbol, category, aliases)
- User needs precise Decimal-based conversion (financial, scientific)
- User wants to list available units in a category or all 20 categories

## Tools

### `convert(value, from_slug, to_slug) -> ConversionResult`

Convert a value between two units with Decimal precision.

```python
from decimal import Decimal
from unitfyi import convert

result = convert(Decimal("100"), "celsius", "fahrenheit")
result.result          # Decimal('212')
result.formula_text    # '°F = (°C x 9/5) + 32'
result.from_name       # 'Celsius'
result.to_name         # 'Fahrenheit'
result.category_name   # 'Temperature'

result = convert(Decimal("5"), "kilometer", "mile")
result.result          # Decimal('3.1069')
result.formula_text    # '1 km = 0.6214 mi'
```

### `conversion_table(from_slug, to_slug, values) -> list[tuple[Decimal, Decimal]]`

Generate a conversion reference table for a unit pair.

```python
from unitfyi import conversion_table

table = conversion_table("kilometer", "mile")
# [(Decimal('1'), Decimal('0.6214')), (Decimal('5'), Decimal('3.1069')), ...]
# Default values: 1, 5, 10, 25, 50, 100, 250, 500, 1000
```

### `get_unit(slug) -> UnitInfo | None`

Look up a single unit by slug.

```python
from unitfyi import get_unit

unit = get_unit("meter")
unit.name        # 'Meter'
unit.symbol      # 'm'
unit.category    # 'length'
unit.aliases     # ['meters', 'metre', ...]
```

### `get_category_units(category_slug) -> list[UnitInfo]`

List all units in a category.

```python
from unitfyi import get_category_units

units = get_category_units("temperature")
[u.name for u in units]  # ['Celsius', 'Fahrenheit', 'Kelvin', 'Rankine']
```

### `get_ordered_categories() -> list[CategoryDef]`

List all 20 measurement categories sorted by display order.

```python
from unitfyi import get_ordered_categories

categories = get_ordered_categories()
len(categories)  # 20
```

## REST API (No Auth Required)

```bash
curl https://unitfyi.com/api/convert/100/celsius/fahrenheit/
curl https://unitfyi.com/api/unit/meter/
curl https://unitfyi.com/api/category/length/
curl https://unitfyi.com/api/categories/
curl https://unitfyi.com/api/table/kilometer/mile/
```

Full spec: [OpenAPI 3.1.0](https://unitfyi.com/api/openapi.json)

## Categories Reference

| Category | Example Units | Count |
|----------|--------------|-------|
| Length | meter, kilometer, mile, foot, inch, yard | 15+ |
| Weight | kilogram, pound, ounce, gram, ton | 12+ |
| Temperature | celsius, fahrenheit, kelvin, rankine | 4 |
| Volume | liter, us-gallon, cup, milliliter | 15+ |
| Area | square-meter, acre, hectare | 10+ |
| Speed | km-per-hour, mile-per-hour, knot | 8+ |
| Time | second, minute, hour, day, week | 8+ |
| Data Storage | byte, kilobyte, megabyte, gigabyte | 10+ |
| Pressure | pascal, bar, psi, atmosphere | 8+ |
| Energy | joule, calorie, kilowatt-hour, btu | 10+ |
| Frequency | hertz, kilohertz, megahertz, gigahertz | 6+ |
| Force | newton, pound-force, dyne | 5+ |
| Power | watt, horsepower, kilowatt | 6+ |
| Angle | degree, radian, gradian | 4+ |
| Fuel Economy | km-per-liter, miles-per-gallon | 4+ |
| Data Transfer Rate | bit-per-second, megabit-per-second | 8+ |
| Density | kg-per-cubic-meter, g-per-ml | 5+ |
| Torque | newton-meter, foot-pound | 4+ |
| Cooking | teaspoon, tablespoon, cup, pinch | 8+ |
| Typography | point, pica, pixel, em | 5+ |

## Demo

![UnitFYI demo](https://raw.githubusercontent.com/fyipedia/unitfyi/main/demo.gif)

## Utility FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [UnitFYI](https://unitfyi.com), [TimeFYI](https://timefyi.com), [HolidayFYI](https://holidayfyi.com), [NameFYI](https://namefyi.com), [DistanceFYI](https://distancefyi.com).
