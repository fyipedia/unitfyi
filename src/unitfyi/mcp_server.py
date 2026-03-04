"""MCP server for unitfyi — unit conversion tools for AI assistants.

Requires: pip install unitfyi[mcp]

Configure in claude_desktop_config.json::

    {
        "mcpServers": {
            "unitfyi": {
                "command": "python",
                "args": ["-m", "unitfyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("unitfyi")


@mcp.tool()
def convert_unit(value: str, from_unit: str, to_unit: str) -> str:
    """Convert a value between two measurement units.

    Supports 220 units across 20 categories (length, weight, temperature,
    volume, speed, etc.) with Decimal precision.

    Args:
        value: Numeric value to convert (e.g., "100", "3.14").
        from_unit: Source unit slug (e.g., "celsius", "kilometer", "pound").
        to_unit: Target unit slug (e.g., "fahrenheit", "meter", "kilogram").
    """
    from unitfyi import IncompatibleUnitsError, UnknownUnitError, convert

    try:
        dec_value = Decimal(value)
    except InvalidOperation:
        return f"Invalid number: {value}"

    try:
        result = convert(dec_value, from_unit, to_unit)
    except UnknownUnitError as e:
        return str(e)
    except IncompatibleUnitsError as e:
        return str(e)

    return (
        f"{result.value} {result.from_symbol} ({result.from_name}) "
        f"= {result.result} {result.to_symbol} ({result.to_name})\n"
        f"Formula: {result.formula_text}\n"
        f"Category: {result.category_name}"
    )


@mcp.tool()
def conversion_table(from_unit: str, to_unit: str) -> str:
    """Show a conversion table for a unit pair.

    Generates a table with common values converted between two units.

    Args:
        from_unit: Source unit slug (e.g., "kilometer").
        to_unit: Target unit slug (e.g., "mile").
    """
    from unitfyi import IncompatibleUnitsError, UnknownUnitError, get_unit
    from unitfyi import conversion_table as get_table

    try:
        rows = get_table(from_unit, to_unit)
    except (UnknownUnitError, IncompatibleUnitsError) as e:
        return str(e)

    from_info = get_unit(from_unit)
    to_info = get_unit(to_unit)
    from_sym = from_info.symbol if from_info else from_unit
    to_sym = to_info.symbol if to_info else to_unit

    lines = [
        f"## {from_unit} to {to_unit}",
        "",
        f"| {from_sym} | {to_sym} |",
        "|--------|--------|",
    ]
    for val, result in rows:
        lines.append(f"| {val} | {result} |")

    return "\n".join(lines)


@mcp.tool()
def list_categories() -> str:
    """List all 20 unit measurement categories.

    Returns categories like length, weight, temperature, volume, speed, etc.
    """
    from unitfyi import get_ordered_categories

    lines = [
        "## Unit Categories",
        "",
        "| # | Slug | Name | Base Unit |",
        "|---|------|------|-----------|",
    ]
    for cat in get_ordered_categories():
        lines.append(f"| {cat['order']} | {cat['slug']} | {cat['name']} | {cat['base_unit']} |")

    return "\n".join(lines)


@mcp.tool()
def list_units(category: str) -> str:
    """List all units in a measurement category.

    Args:
        category: Category slug (e.g., "length", "temperature", "weight").
    """
    from unitfyi import get_category_units

    units = get_category_units(category)
    if not units:
        return f"No units found for category: {category}"

    lines = [
        f"## Units in {category}",
        "",
        "| Slug | Name | Symbol |",
        "|------|------|--------|",
    ]
    for u in units:
        lines.append(f"| {u.slug} | {u.name} | {u.symbol} |")

    return "\n".join(lines)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
