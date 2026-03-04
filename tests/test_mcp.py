"""Tests for the unitfyi MCP server."""

from unitfyi.mcp_server import (
    conversion_table,
    convert_unit,
    list_categories,
    list_units,
)


def test_convert_unit_celsius_fahrenheit() -> None:
    result = convert_unit("100", "celsius", "fahrenheit")
    assert "212" in result
    assert "Formula" in result
    assert "Temperature" in result


def test_convert_unit_kilometers_miles() -> None:
    result = convert_unit("1", "kilometer", "mile")
    assert "0.621371" in result


def test_convert_unit_invalid_number() -> None:
    result = convert_unit("abc", "meter", "foot")
    assert "Invalid" in result


def test_convert_unit_unknown_unit() -> None:
    result = convert_unit("100", "nonexistent", "meter")
    assert "Unknown" in result


def test_convert_unit_incompatible() -> None:
    result = convert_unit("100", "meter", "kilogram")
    assert "Cannot convert" in result


def test_conversion_table() -> None:
    result = conversion_table("kilometer", "mile")
    assert "kilometer" in result
    assert "mile" in result
    assert "km" in result
    assert "mi" in result


def test_list_categories() -> None:
    result = list_categories()
    assert "Unit Categories" in result
    assert "length" in result
    assert "temperature" in result
    assert "weight" in result


def test_list_units_length() -> None:
    result = list_units("length")
    assert "meter" in result.lower()
    assert "kilometer" in result.lower()


def test_list_units_empty() -> None:
    result = list_units("nonexistent")
    assert "No units" in result
