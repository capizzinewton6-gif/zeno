"""
actions - web_search
=====================
Google/Bing search with summarisation.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import re
import urllib.parse
from typing import Any, Dict, Optional

from core.capability import Capability

try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    _HAS_REQUESTS = False


class WebSearch(Capability):
    """Google/Bing search with summarisation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "web_search"
        self.description = "Google/Bing search with summarisation."
        self.timeout = int(self.config.get("timeout", 10))

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        query = self._extract_query(task)
        if not query:
            return self.error("No search query found in task.")
        if not _HAS_REQUESTS:
            return self.error("requests is not installed. Run: pip install requests")
        results = self._search(query)
        if not results:
            return self.error(f"No results found for: {query}")
        lines = [f"Search results for '{query}' ({len(results)} found):"]
        for i, (title, url, snippet) in enumerate(results, 1):
            lines.append(f"{i}. {title}\n   {snippet}\n   {url}")
        return self.ok("\n".join(lines), query=query, count=len(results))

    def _extract_query(self, task: str) -> str:
        task = task.strip()
        for prefix in ("search for:", "search:", "look up:", "find online:", "google:"):
            if task.lower().startswith(prefix):
                return task[len(prefix):].strip().strip("\"'")
        return task.strip().strip("\"'")

    def _search(self, query: str):
        """Scrape DuckDuckGo HTML results (no API key required)."""
        url = "https://html.duckduckgo.com/html/"
        try:
            resp = requests.post(
                url,
                data={"q": query},
                headers={"User-Agent": "Mozilla/5.0 (compatible; PaperclipAI/1.0)"},
                timeout=self.timeout,
            )
            resp.raise_for_status()
        except Exception as exc:
            return [(f"Search request failed: {exc}", "", "")]

        results = []
        # Result titles and snippets are in <a class="result__a"> and <a class="result__snippet">
        title_re = re.compile(r'class="result__a"[^>]*>(.*?)</a>', re.S)
        snippet_re = re.compile(r'class="result__snippet"[^>]*>(.*?)</a>', re.S)
        href_re = re.compile(r'class="result__a"\s+href="([^"]+)"', re.S)
        titles = [self._clean(t) for t in title_re.findall(resp.text)]
        snippets = [self._clean(s) for s in snippet_re.findall(resp.text)]
        hrefs = [self._clean_url(h) for h in href_re.findall(resp.text)]
        for i in range(min(len(titles), 8)):
            results.append((
                titles[i] if i < len(titles) else "(no title)",
                hrefs[i] if i < len(hrefs) else "",
                snippets[i] if i < len(snippets) else "",
            ))
        return results

    @staticmethod
    def _clean(text: str) -> str:
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"&[a-z]+;", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _clean_url(href: str) -> str:
        # DuckDuckGo wraps URLs in a redirect like //duckduckgo.com/l/?uddg=...
        m = re.search(r"uddg=([^&]+)", href)
        if m:
            return urllib.parse.unquote(m.group(1))
        return href
