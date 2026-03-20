"""HTTP API client for unitfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install unitfyi[api]``

Usage::

    from unitfyi.api import UnitFYI

    with UnitFYI() as api:
        items = api.list_blog/categories()
        detail = api.get_blog/category("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class UnitFYI:
    """API client for the unitfyi.com REST API.

    Provides typed access to all unitfyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://unitfyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://unitfyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_blog/categories(self, **params: Any) -> dict[str, Any]:
        """List all blog/categories."""
        return self._get("/api/v1/blog/categories/", **params)

    def get_blog/category(self, slug: str) -> dict[str, Any]:
        """Get blog/category by slug."""
        return self._get(f"/api/v1/blog/categories/" + slug + "/")

    def list_blog/posts(self, **params: Any) -> dict[str, Any]:
        """List all blog/posts."""
        return self._get("/api/v1/blog/posts/", **params)

    def get_blog/post(self, slug: str) -> dict[str, Any]:
        """Get blog/post by slug."""
        return self._get(f"/api/v1/blog/posts/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> UnitFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
