"""Reference manager — manage BibTeX entries and reaction citations."""


class ReferenceManager:
    """Manage chemistry references in BibTeX format."""

    def __init__(self):
        self.entries = []

    def add_article(self, key, authors, title, journal, year, volume=None, pages=None, doi=None):
        entry = {
            "type": "article", "key": key, "authors": authors, "title": title,
            "journal": journal, "year": year, "volume": volume, "pages": pages, "doi": doi,
        }
        self.entries.append(entry)
        return entry

    def to_bibtex(self):
        lines = []
        for e in self.entries:
            authors = " and ".join(e["authors"]) if isinstance(e["authors"], list) else e["authors"]
            lines.append(f"@article{{{e['key']},")
            lines.append(f"  author = {{{authors}}},")
            lines.append(f"  title = {{{e['title']}}},")
            lines.append(f"  journal = {{{e['journal']}}},")
            lines.append(f"  year = {{{e['year']}}},")
            if e.get("volume"):
                lines.append(f"  volume = {{{e['volume']}}},")
            if e.get("pages"):
                lines.append(f"  pages = {{{e['pages']}}},")
            if e.get("doi"):
                lines.append(f"  doi = {{{e['doi']}}},")
            lines.append("}")
        return "\n".join(lines)

    def acs_format(self):
        lines = []
        for e in self.entries:
            authors = ", ".join(e["authors"]) if isinstance(e["authors"], list) else e["authors"]
            ref = f"{authors}. {e['title']} {e['journal']} "
            if e.get("year"):
                ref += f"{e['year']}"
            if e.get("volume"):
                ref += f", {e['volume']}"
            if e.get("pages"):
                ref += f", {e['pages']}"
            ref += "."
            if e.get("doi"):
                ref += f" DOI: {e['doi']}."
            lines.append(ref)
        return "\n\n".join(lines)

    def list_entries(self):
        return list(self.entries)
