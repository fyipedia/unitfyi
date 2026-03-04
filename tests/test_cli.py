"""Tests for the unitfyi CLI."""

from typer.testing import CliRunner

from unitfyi.cli import app

runner = CliRunner()


def test_convert_celsius_to_fahrenheit() -> None:
    result = runner.invoke(app, ["convert", "100", "celsius", "fahrenheit"])
    assert result.exit_code == 0
    assert "212" in result.output
    assert "Formula" in result.output


def test_convert_meters_to_feet() -> None:
    result = runner.invoke(app, ["convert", "1", "meter", "foot"])
    assert result.exit_code == 0
    assert "3.2808" in result.output


def test_convert_invalid_number() -> None:
    result = runner.invoke(app, ["convert", "abc", "meter", "foot"])
    assert result.exit_code == 1
    assert "Invalid" in result.output


def test_convert_unknown_unit() -> None:
    result = runner.invoke(app, ["convert", "100", "nonexistent", "meter"])
    assert result.exit_code == 1
    assert "Unknown" in result.output


def test_convert_incompatible() -> None:
    result = runner.invoke(app, ["convert", "100", "meter", "kilogram"])
    assert result.exit_code == 1
    assert "Cannot convert" in result.output


def test_table_command() -> None:
    result = runner.invoke(app, ["table", "kilometer", "mile"])
    assert result.exit_code == 0
    assert "km" in result.output
    assert "mi" in result.output


def test_categories_command() -> None:
    result = runner.invoke(app, ["categories"])
    assert result.exit_code == 0
    assert "length" in result.output.lower()
    assert "temperature" in result.output.lower()


def test_units_command() -> None:
    result = runner.invoke(app, ["units", "length"])
    assert result.exit_code == 0
    assert "meter" in result.output.lower()
    assert "kilometer" in result.output.lower()


def test_units_empty_category() -> None:
    result = runner.invoke(app, ["units", "nonexistent"])
    assert result.exit_code == 1
    assert "No units" in result.output
