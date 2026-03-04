# unitfyi

[![PyPI](https://img.shields.io/pypi/v/unitfyi)](https://pypi.org/project/unitfyi/)
[![Python](https://img.shields.io/pypi/pyversions/unitfyi)](https://pypi.org/project/unitfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python unit conversion engine for developers. Convert between [200 units](https://unitfyi.com/) across 20 measurement categories with `Decimal` precision, human-readable formula text, and smart magnitude-aware rounding -- all with zero dependencies.

> **Convert between 200 units at [unitfyi.com](https://unitfyi.com/)** -- [unit converter](https://unitfyi.com/tools/converter/), conversion tables, and formula references across length, weight, temperature, volume, and 16 more categories.

## Install

```bash
pip install unitfyi              # Core engine (zero deps)
pip install "unitfyi[cli]"       # + Command-line interface
pip install "unitfyi[mcp]"       # + MCP server for AI assistants
pip install "unitfyi[api]"       # + HTTP client for unitfyi.com API
pip install "unitfyi[all]"       # Everything
```

## Quick Start

```python
from decimal import Decimal
from unitfyi import convert, get_unit, get_category_units, get_ordered_categories

# Convert 100 Celsius to Fahrenheit
result = convert(Decimal("100"), "celsius", "fahrenheit")
result.result          # Decimal('212')
result.formula_text    # '°F = (°C x 9/5) + 32'

# Convert 5 kilometers to miles
result = convert(Decimal("5"), "kilometer", "mile")
result.result          # Decimal('3.1069')

# Look up a unit
unit = get_unit("meter")
unit.name              # 'Meter'
unit.symbol            # 'm'
unit.category          # 'length'

# List all 20 categories
categories = get_ordered_categories()
len(categories)        # 20

# List units in a category
units = get_category_units("temperature")
[u.name for u in units]  # ['Celsius', 'Fahrenheit', 'Kelvin', 'Rankine']
```

## Understanding Unit Systems

The world's measurement systems evolved from diverse historical origins into three main families:

**SI (International System of Units)** -- the modern metric system, used by virtually every country for scientific and most commercial purposes. Built on seven base units (meter, kilogram, second, ampere, kelvin, mole, candela) with decimal prefixes from yocto (10^-24) to yotta (10^24).

**Imperial / US Customary** -- derived from English units. The US and Imperial systems share many unit names (inch, foot, mile, pound) but diverge for volume: a US gallon is 3.785 liters while an Imperial gallon is 4.546 liters. This distinction causes real-world confusion -- always specify which system.

**Historical and domain-specific units** -- troy ounces for precious metals, nautical miles for maritime navigation, astronomical units for solar system distances, light-years for stellar distances. These persist because they map naturally to the scale of their domain.

```python
from decimal import Decimal
from unitfyi import convert

# Metric prefixes follow powers of 10
convert(Decimal("1"), "kilometer", "meter")       # 1000
convert(Decimal("1"), "megabyte", "kilobyte")      # 1024 (binary prefix)

# Imperial/US volume differences require care
convert(Decimal("1"), "us-gallon", "liter")        # 3.7854
```

`unitfyi` uses Python's `Decimal` type throughout the conversion pipeline. This eliminates floating-point drift that plagues `float`-based calculators -- critical for financial calculations (currency amounts), scientific work (precise measurements), and any application where `0.1 + 0.2 != 0.3` would be unacceptable.

## Temperature Conversion

Temperature is the only common measurement category where conversions are non-linear. Length, weight, and volume use simple multiplication by a constant factor (1 km = 1000 m). Temperature requires function-based formulas because the scales have different zero points:

```python
from decimal import Decimal
from unitfyi import convert

# Celsius to Fahrenheit: F = (C x 9/5) + 32
result = convert(Decimal("100"), "celsius", "fahrenheit")
result.result          # Decimal('212')
result.formula_text    # '°F = (°C x 9/5) + 32'

# All temperature conversions go through Kelvin as the base unit internally
# Celsius -> Kelvin -> Fahrenheit
convert(Decimal("0"), "celsius", "kelvin")         # Decimal('273.15')
convert(Decimal("-40"), "celsius", "fahrenheit")   # Decimal('-40') -- the crossover point

# Rankine (absolute scale based on Fahrenheit)
convert(Decimal("100"), "celsius", "rankine")      # Decimal('671.67')
```

Internally, `unitfyi` routes all temperature conversions through Kelvin as the canonical base unit. For linear categories (length, weight, etc.), each unit stores a single conversion factor relative to the base unit, and conversion is a simple division-then-multiplication. For temperature, each unit provides `to_base` and `from_base` functions that encode the non-linear relationship.

## Conversion Tables

```python
from decimal import Decimal
from unitfyi import conversion_table

# Generate a full conversion table
table = conversion_table("kilometer", "mile", count=10)
# Returns list of (input_value, output_value) pairs
# Useful for reference charts and documentation
```

## Command-Line Interface

```bash
pip install "unitfyi[cli]"

unitfyi convert 100 celsius fahrenheit
unitfyi table kilometer mile
unitfyi categories
unitfyi units length
```

## MCP Server (Claude, Cursor, Windsurf)

Add unit conversion tools to any AI assistant that supports [Model Context Protocol](https://modelcontextprotocol.io/).

```bash
pip install "unitfyi[mcp]"
```

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "unitfyi": {
            "command": "python",
            "args": ["-m", "unitfyi.mcp_server"]
        }
    }
}
```

**Available tools**: `convert_unit`, `conversion_table`, `list_categories`, `list_units`

## REST API Client

```python
pip install "unitfyi[api]"
```

```python
from unitfyi.api import UnitFYI

with UnitFYI() as client:
    result = client.convert("100", "celsius", "fahrenheit")
    categories = client.categories()
    units = client.units("length")
```

Full [API documentation](https://unitfyi.com/developers/) at unitfyi.com.

## API Reference

### Core Conversion

| Function | Description |
|----------|-------------|
| `convert(value, from_unit, to_unit) -> ConversionResult` | Convert between units with Decimal precision |
| `conversion_table(from_unit, to_unit, count) -> list` | Generate conversion reference table |

### Unit Queries

| Function | Description |
|----------|-------------|
| `get_unit(slug) -> UnitInfo` | Look up unit by slug (name, symbol, category) |
| `get_category_units(category) -> list[UnitInfo]` | List all units in a category |
| `get_ordered_categories() -> list[str]` | List all 20 measurement categories |

### Exceptions

| Exception | Description |
|-----------|-------------|
| `UnknownUnitError` | Raised when a unit slug is not recognized |
| `IncompatibleUnitsError` | Raised when converting between different categories |

## Categories

Length, Weight, Temperature, Volume, Area, Speed, Time, Data Storage, Pressure, Energy, Frequency, Force, Power, Angle, Fuel Economy, Data Transfer Rate, Density, Torque, Cooking, Typography

## Features

- **200 units** across 20 measurement categories
- **Decimal precision** -- no floating-point drift
- **Linear + non-linear** -- temperature uses function-based formulas
- **Formula text** -- human-readable conversion formulas
- **Smart rounding** -- magnitude-aware precision
- **Conversion tables** -- generate reference charts
- **CLI** -- Rich terminal output with conversion tables
- **MCP server** -- 4 tools for AI assistants (Claude, Cursor, Windsurf)
- **REST API client** -- httpx-based client for [unitfyi.com API](https://unitfyi.com/developers/)
- **Zero dependencies** -- pure Python standard library only
- **Type-safe** -- full type annotations, `py.typed` marker (PEP 561)
- **Fast** -- all conversions under 1ms

## FYIPedia Developer Tools

Part of the [FYIPedia](https://fyipedia.com/) open-source developer tools ecosystem:

| Package | Description |
|---------|-------------|
| [colorfyi](https://pypi.org/project/colorfyi/) | Color conversion, [WCAG contrast](https://colorfyi.com/tools/contrast-checker/), harmonies, shades -- [colorfyi.com](https://colorfyi.com/) |
| [emojifyi](https://pypi.org/project/emojifyi/) | Emoji lookup, search, encoding -- [emojifyi.com](https://emojifyi.com/) |
| [symbolfyi](https://pypi.org/project/symbolfyi/) | Symbol encoding, Unicode properties -- [symbolfyi.com](https://symbolfyi.com/) |
| [unicodefyi](https://pypi.org/project/unicodefyi/) | Unicode character info, 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| [fontfyi](https://pypi.org/project/fontfyi/) | Google Fonts metadata, CSS, pairings -- [fontfyi.com](https://fontfyi.com/) |
| [distancefyi](https://pypi.org/project/distancefyi/) | Haversine distance, bearing, travel times -- [distancefyi.com](https://distancefyi.com/) |
| [timefyi](https://pypi.org/project/timefyi/) | Timezone ops, time differences, business hours -- [timefyi.com](https://timefyi.com/) |
| [namefyi](https://pypi.org/project/namefyi/) | Korean romanization, Five Elements -- [namefyi.com](https://namefyi.com/) |
| **[unitfyi](https://pypi.org/project/unitfyi/)** | **Unit conversion, 200 units, 20 categories -- [unitfyi.com](https://unitfyi.com/)** |
| [holidayfyi](https://pypi.org/project/holidayfyi/) | Holiday dates, Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |

## Links

- [Unit Converter](https://unitfyi.com/tools/converter/) -- Convert between 200 units
- [REST API Documentation](https://unitfyi.com/developers/) -- Free API
- [npm Package](https://www.npmjs.com/package/unitfyi) -- TypeScript version
- [Source Code](https://github.com/fyipedia/unitfyi) -- MIT licensed

## License

MIT
