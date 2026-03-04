"""Command-line interface for unitfyi.

Requires: pip install unitfyi[cli]

Usage::

    unitfyi convert 100 celsius fahrenheit
    unitfyi table kilometer meter
    unitfyi categories
    unitfyi units length
"""

from decimal import Decimal, InvalidOperation

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="unitfyi",
    help="Unit conversion engine -- 200 units, 20 categories, Decimal precision.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def convert(
    value: str = typer.Argument(help="Numeric value to convert"),
    from_unit: str = typer.Argument(help="Source unit slug (e.g., celsius, kilometer)"),
    to_unit: str = typer.Argument(help="Target unit slug (e.g., fahrenheit, meter)"),
) -> None:
    """Convert a value between two units."""
    from unitfyi import IncompatibleUnitsError, UnknownUnitError
    from unitfyi import convert as do_convert

    try:
        dec_value = Decimal(value)
    except InvalidOperation:
        console.print(f"[red]Invalid number: {value}[/]")
        raise typer.Exit(1) from None

    try:
        result = do_convert(dec_value, from_unit, to_unit)
    except (UnknownUnitError, IncompatibleUnitsError) as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1) from None

    console.print(
        f"[green]{result.value} {result.from_symbol} ({result.from_name}) "
        f"= {result.result} {result.to_symbol} ({result.to_name})[/]"
    )
    console.print(f"[dim]Formula: {result.formula_text}[/]")


@app.command("table")
def table_cmd(
    from_unit: str = typer.Argument(help="Source unit slug"),
    to_unit: str = typer.Argument(help="Target unit slug"),
) -> None:
    """Show a conversion table for a unit pair."""
    from unitfyi import IncompatibleUnitsError, UnknownUnitError, conversion_table

    try:
        rows = conversion_table(from_unit, to_unit)
    except (UnknownUnitError, IncompatibleUnitsError) as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1) from None

    from unitfyi import get_unit

    from_info = get_unit(from_unit)
    to_info = get_unit(to_unit)
    from_sym = from_info.symbol if from_info else from_unit
    to_sym = to_info.symbol if to_info else to_unit

    table = Table(title=f"{from_unit} to {to_unit}")
    table.add_column(from_sym, style="cyan", justify="right")
    table.add_column(to_sym, style="green", justify="right")

    for val, result in rows:
        table.add_row(str(val), str(result))

    console.print(table)


@app.command()
def categories() -> None:
    """List all 20 unit categories."""
    from unitfyi import get_ordered_categories

    table = Table(title="Unit Categories")
    table.add_column("#", style="dim", justify="right")
    table.add_column("Slug", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Base Unit", style="yellow")

    for cat in get_ordered_categories():
        table.add_row(str(cat["order"]), cat["slug"], cat["name"], cat["base_unit"])

    console.print(table)


@app.command()
def units(
    category: str = typer.Argument(help="Category slug (e.g., length, temperature)"),
) -> None:
    """List all units in a category."""
    from unitfyi import get_category_units

    unit_list = get_category_units(category)
    if not unit_list:
        console.print(f"[red]No units found for category: {category}[/]")
        raise typer.Exit(1)

    table = Table(title=f"Units in {category}")
    table.add_column("Slug", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Symbol", style="yellow")

    for u in unit_list:
        table.add_row(u.slug, u.name, u.symbol)

    console.print(table)
