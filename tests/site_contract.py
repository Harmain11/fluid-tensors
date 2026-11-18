"""Static deployment contracts for the free GitHub Pages research site."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


DOCS = Path(__file__).resolve().parents[1] / "docs"


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


def elements(path):
    collector = Elements()
    collector.feed(path.read_text(encoding="utf-8"))
    return collector.nodes


def by_attr(nodes, tag, key):
    return [attrs for node_tag, attrs in nodes if node_tag == tag and key in attrs]


class SiteContractTests(unittest.TestCase):
    def test_home_explains_data_with_switchable_conditions_and_non_js_fallback(self):
        nodes = elements(DOCS / "index.html")
        sections = {attrs.get("id") for tag, attrs in nodes if tag == "section"}
        self.assertTrue({"overview", "explore", "evidence", "limitations"}.issubset(sections))
        ids = {attrs["data-wording"] for attrs in by_attr(nodes, "button", "data-wording")}
        self.assertEqual(ids, {"original", "reworded", "formal", "terse"})
        self.assertIn("dataset-fallback", {attrs.get("id") for attrs in by_attr(nodes, "table", "id")})
        self.assertIn("study-data.mjs", (DOCS / "index.html").read_text(encoding="utf-8"))

    def test_home_gallery_preserves_all_six_figure_outputs(self):
        nodes = elements(DOCS / "index.html")
        image_names = {Path(attrs.get("src", "")).name for attrs in by_attr(nodes, "img", "src")}
        expected = {
            "figure01_wording_mean_with_ci.png",
            "figure02_direction_control.png",
            "figure03_question_level_paired_effects.png",
            "figure04_factorial_response_heatmaps.png",
            "figureS1_bootstrap_distribution.png",
            "figureS2_prompt_token_diagnostics.png",
        }
        self.assertTrue(expected.issubset(image_names), expected - image_names)

    def test_article_deep_dive_navigation_and_eight_figure_dialogs(self):
        article = DOCS / "papers" / "one-frozen-edit.html"
        html = article.read_text(encoding="utf-8")
        nodes = elements(article)
        self.assertIn('class="article-mini-toc"', html)
        ids = {attrs.get("id") for _, attrs in nodes}
        self.assertTrue({"methods", "figures", "limitations", "replication"}.issubset(ids))
        self.assertEqual(len(by_attr(nodes, "button", "data-figure-open")), 8)
        self.assertEqual(len(by_attr(nodes, "dialog", "id")), 1)
        self.assertIn('src="../site.js"', html)
        self.assertIn("10.5281/zenodo.24338059", html)
        self.assertNotIn("REPLACE_", html)

    def test_article_preserves_six_historical_and_two_confirmation_figures_and_boundaries(self):
        article = DOCS / "papers" / "one-frozen-edit.html"
        nodes = elements(article)
        self.assertEqual(len([tag for tag, _ in nodes if tag == "figcaption"]), 8)
        image_names = {Path(attrs.get("src", "")).name for attrs in by_attr(nodes, "img", "src")}
        self.assertTrue({"p1_confirmation_condition_contrasts.png", "p1_confirmation_matched_vs_raw.png"}.issubset(image_names))
        html = article.read_text(encoding="utf-8")
        for caveat in ["32 question", "reasoning breakthrough", "no length- and position-matched", "not external-model or independent-lab replication"]:
            self.assertIn(caveat.lower(), html.lower())


    def test_version_three_figures_are_visible_in_main_readme(self):
        readme = (DOCS.parent / "README.md").read_text(encoding="utf-8")
        for figure in ("p1_confirmation_condition_contrasts.png", "p1_confirmation_matched_vs_raw.png"):
            self.assertIn(f"](docs/assets/{figure})]", readme)
            self.assertTrue((DOCS / "assets" / figure).is_file())
        self.assertIn("Zenodo Version 3", readme)
        self.assertIn("10.5281/zenodo.24338059", readme)

    def test_new_gpu_figures_appear_early_in_published_story(self):
        home = (DOCS / "index.html").read_text(encoding="utf-8")
        self.assertIn("Zenodo Version 3", home.split('class="paper-hero"', 1)[1].split("</section>", 1)[0])
        self.assertLess(home.index('<section id="confirmation"'), home.index('<section id="explore"'))
        article = (DOCS / "papers" / "one-frozen-edit.html").read_text(encoding="utf-8")
        hero = article.split('class="article-hero"', 1)[1].split("</section>", 1)[0]
        self.assertIn("Zenodo Version 3", hero)
        self.assertIn("../assets/p1_confirmation_condition_contrasts.png", hero)
        update_notes = (DOCS.parent / "paper1-confirmation-2026-11-18" / "README.md").read_text(encoding="utf-8")
        self.assertIn("10.5281/zenodo.24338059", update_notes)
        self.assertNotIn("DOI is pending", update_notes)


if __name__ == "__main__":
    unittest.main()
