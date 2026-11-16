"""Search, sharing, citation, and file integrity contract for GitHub Pages."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import unittest
from xml.etree import ElementTree

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://harmain11.github.io/fluid-tensors/"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


def nodes_of(path):
    parser = Parser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.nodes


class MetadataContractTests(unittest.TestCase):
    def test_pages_have_complete_sharing_and_search_metadata(self):
        for page, url in [(DOCS / "index.html", SITE), (DOCS / "papers/one-frozen-edit.html", SITE + "papers/one-frozen-edit.html")]:
            with self.subTest(page=page):
                content = page.read_text(encoding="utf-8")
                nodes = nodes_of(page)
                metas = {attrs.get("property", attrs.get("name")): attrs.get("content") for tag, attrs in nodes if tag == "meta"}
                links = {attrs.get("rel"): attrs.get("href") for tag, attrs in nodes if tag == "link"}
                self.assertEqual(links.get("canonical"), url)
                self.assertEqual(metas.get("og:url"), url)
                self.assertEqual(metas.get("og:image"), SITE + "assets/social-cover.png")
                self.assertEqual(metas.get("twitter:card"), "summary_large_image")
                self.assertTrue(metas.get("description"))
                self.assertTrue(links.get("icon"))
                self.assertTrue(links.get("manifest"))
                match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', content, re.DOTALL)
                self.assertIsNotNone(match)
                ld = json.loads(match.group(1))
                self.assertIn(ld.get("@type"), {"WebSite", "ScholarlyArticle"})

    def test_brand_assets_and_discovery_files_exist(self):
        with Image.open(DOCS / "assets" / "social-cover.png") as img:
            self.assertEqual(img.size, (1280, 640))
        with Image.open(DOCS / "favicon.ico") as img:
            self.assertIn(img.size, {(48, 48), (64, 64)})
        with Image.open(DOCS / "apple-touch-icon.png") as img:
            self.assertEqual(img.size, (180, 180))
        ElementTree.parse(DOCS / "sitemap.xml")
        self.assertTrue((DOCS / "assets" / "ft-mark.svg").is_file())
        self.assertTrue((ROOT / "GITHUB_ABOUT_SETUP.md").is_file())
        self.assertTrue((DOCS / "site.webmanifest").is_file())

    def test_all_local_web_links_resolve_and_no_placeholders(self):
        for page in (DOCS / "index.html", DOCS / "papers/one-frozen-edit.html"):
            self.assertNotIn("REPLACE_", page.read_text(encoding="utf-8"))
            for tag, attrs in nodes_of(page):
                for key in ("src", "href"):
                    target = attrs.get(key, "")
                    parsed = urlsplit(target)
                    if not target or parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    resolved = (page.parent / unquote(parsed.path)).resolve()
                    self.assertTrue(resolved.is_file(), f"Broken local {key}: {page}: {target}")

    def test_citation_has_minted_doi_and_readme_link(self):
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("10.5281/zenodo.24284827", citation)
        self.assertIn("10.5281/zenodo.24284827", readme)
        self.assertIn(SITE, readme)
        self.assertNotIn("REPLACE_", readme)


if __name__ == "__main__":
    unittest.main()
