"""Scrapes and indexes offline framework documentation."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:  # pragma: no cover - optional
    import requests  # type: ignore
    _REQ = True
except Exception:  # pragma: no cover
    _REQ = False


@dataclass
class DocPage:
    url: str
    title: str
    content: str
    links: list[str] = field(default_factory=list)


@dataclass
class DocIndex:
    root_url: str
    pages: list[DocPage] = field(default_factory=list)
    by_keyword: dict[str, list[str]] = field(default_factory=dict)

    def search(self, keyword: str) -> list[DocPage]:
        return [p for p in self.pages if keyword.lower() in p.content.lower()]


class DocumentationScraper:
    """Fetches and indexes framework documentation for offline use."""

    def __init__(self, cache_dir: str = "database/docs_cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, url: str) -> DocPage | None:
        if not _REQ:
            return None
        try:  # pragma: no cover - network
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            html = resp.text
            title = self._extract_title(html)
            content = self._strip_html(html)
            links = self._extract_links(url, html)
            return DocPage(url=url, title=title, content=content, links=links)
        except Exception:
            return None

    def crawl(self, root_url: str, max_pages: int = 50) -> DocIndex:
        index = DocIndex(root_url=root_url)
        visited: set[str] = set()
        queue = [root_url]
        while queue and len(index.pages) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)
            page = self.fetch(url)
            if not page:
                continue
            index.pages.append(page)
            self._cache(page)
            for link in page.links:
                if link not in visited and root_url in link:
                    queue.append(link)
        return index

    def _cache(self, page: DocPage) -> None:
        safe = re.sub(r"[^\w]", "_", page.url)[:80]
        (self.cache_dir / f"{safe}.txt").write_text(
            f"# {page.title}\n{page.url}\n\n{page.content}", encoding="utf-8")

    def _extract_title(self, html: str) -> str:
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else "Untitled"

    def _strip_html(self, html: str) -> str:
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_links(self, base: str, html: str) -> list[str]:
        from urllib.parse import urljoin
        links = re.findall(r'href=["\']([^"\']+)["\']', html)
        return [urljoin(base, l) for l in links if not l.startswith(("#", "mailto:"))]
