# unitfyi

Pure Python unit conversion engine — 200 units, 20 categories, Decimal precision. Zero dependencies core.

## Install

```bash
pip install unitfyi              # Core (zero deps)
pip install "unitfyi[cli]"       # + CLI (typer, rich)
pip install "unitfyi[mcp]"       # + MCP server
pip install "unitfyi[all]"       # Everything
```

## Quick Start

```python
from decimal import Decimal
from unitfyi import convert, get_unit, get_category_units, get_ordered_categories

# Convert 100 Celsius to Fahrenheit
result = convert(Decimal("100"), "celsius", "fahrenheit")
result.result          # Decimal('212')
result.formula_text    # '°F = (°C × 9/5) + 32'

# Convert 5 kilometers to miles
result = convert(Decimal("5"), "kilometer", "mile")
result.result          # Decimal('3.1069')

# Look up a unit
unit = get_unit("meter")
unit.name              # 'Meter'
unit.symbol            # 'm'
unit.category          # 'length'

# List categories
categories = get_ordered_categories()
len(categories)        # 20

# List units in a category
units = get_category_units("temperature")
[u.name for u in units]  # ['Celsius', 'Fahrenheit', 'Kelvin', 'Rankine']
```

## Features

- **200 units** across 20 measurement categories
- **Decimal precision** — no floating-point drift
- **Linear + non-linear** — temperature uses function-based formulas
- **Smart rounding** — magnitude-aware precision
- **Zero dependencies** — pure Python standard library only
- **Fully typed** — PEP 561 py.typed, mypy strict

## Categories

Length, Weight, Temperature, Volume, Area, Speed, Time, Data Storage,
Pressure, Energy, Frequency, Force, Power, Angle, Fuel Economy,
Data Transfer Rate, Density, Torque, Cooking, Typography

## CLI

```bash
unitfyi convert 100 celsius fahrenheit
unitfyi table kilometer mile
unitfyi categories
unitfyi units length
```

## MCP Server

Add to your Claude Desktop config:

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

Tools: `convert_unit`, `conversion_table`, `list_categories`, `list_units`

## API Client

```python
from unitfyi.api import UnitFYI

with UnitFYI() as client:
    result = client.convert("100", "celsius", "fahrenheit")
    categories = client.categories()
    units = client.units("length")
```

## License

MIT
