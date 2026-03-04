---
name: unit-tools
description: Convert between 200 measurement units across 20 categories with precision.
---

# Unit Tools

Unit conversion powered by [unitfyi](https://unitfyi.com/) -- a pure Python conversion engine covering 200 units across 20 categories with zero dependencies.

## Setup

Install the MCP server:

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

## Available Tools

| Tool | Description |
|------|-------------|
| `convert_unit` | Convert a value from one unit to another |
| `conversion_table` | Generate a conversion table for a unit across common values |
| `list_categories` | List all 20 unit categories (length, mass, temperature, etc.) |
| `list_units` | List all available units in a specific category |

## When to Use

- Converting between metric and imperial units
- Building conversion tables for reference
- Converting temperature, length, mass, volume, speed, and more
- Looking up available units in any measurement category

## Links

- [Unit Converter](https://unitfyi.com/) -- Convert any measurement unit
- [API Documentation](https://unitfyi.com/developers/) -- Free REST API
- [PyPI Package](https://pypi.org/project/unitfyi/)
