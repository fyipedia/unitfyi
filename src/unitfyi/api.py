"""HTTP API client for unitfyi.com REST endpoints.

Requires: pip install unitfyi[api]

Usage::

    from unitfyi.api import UnitFYI

    with UnitFYI() as client:
        result = client.convert("100", "celsius", "fahrenheit")
        print(result)
"""

from __future__ import annotations

from typing import Any

import httpx


class UnitFYI:
    """API client for the unitfyi.com REST API."""

    def __init__(
        self,
        base_url: str = "https://unitfyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    def convert(self, value: str, from_unit: str, to_unit: str) -> dict[str, Any]:
        """Convert a value between two units via the API.

        Args:
            value: Numeric value as string (e.g., "100").
            from_unit: Source unit slug (e.g., "celsius").
            to_unit: Target unit slug (e.g., "fahrenheit").

        Returns:
            Dict with conversion result including value, result, formula, etc.
        """
        return self._get("/convert/", value=value, from_unit=from_unit, to_unit=to_unit)

    def categories(self) -> dict[str, Any]:
        """List all unit categories.

        Returns:
            Dict with categories list.
        """
        return self._get("/categories/")

    def units(self, category: str) -> dict[str, Any]:
        """List all units in a category.

        Args:
            category: Category slug (e.g., "length", "temperature").

        Returns:
            Dict with units list for the category.
        """
        return self._get(f"/units/{category}/")

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> UnitFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
