import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def front_matter(path):
    text = read(path)
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[4:end] if end != -1 else ""


def hex_to_rgb(value):
    value = value.strip().lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    channels = []
    for channel in rgb:
        channel = channel / 255
        if channel <= 0.03928:
            channels.append(channel / 12.92)
        else:
            channels.append(((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first, second):
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)
    light = max(first_luminance, second_luminance)
    dark = min(first_luminance, second_luminance)
    return (light + 0.05) / (dark + 0.05)


class SiteQualityTests(unittest.TestCase):
    def test_demo_content_is_not_published_from_source(self):
        demo_paths = [
            "content/event/example",
            "content/courses/example",
            "content/slides/example",
        ]

        for path in demo_paths:
            self.assertFalse((ROOT / path).exists(), f"Remove demo content: {path}")

    def test_theme_links_are_readable_on_white_cards(self):
        theme = read("data/themes/minimal.toml")
        primary = re.search(r'^primary\s*=\s*"([^"]+)"', theme, re.MULTILINE)

        self.assertIsNotNone(primary)
        ratio = contrast_ratio(hex_to_rgb(primary.group(1)), (255, 255, 255))
        self.assertGreaterEqual(ratio, 4.5)

    def test_contact_metadata_has_no_template_or_broken_links(self):
        params = read("config/_default/params.yaml")
        profile = read("content/authors/admin/_index.md")
        experience = read("content/home/experience.md")

        self.assertNotIn("description: ''", params)
        self.assertNotIn("echo123", params)
        self.assertNotIn("keybase.io", params)
        self.assertNotIn("discourse.gohugo.io", params)
        self.assertIn("mailto:ngugi.mburu@ku.ac.ke", profile)
        self.assertNotIn("/#ngugi.mburu@ku.ac.ke", profile)
        self.assertNotIn("company_url: www.", experience)

    def test_netlify_branch_deploy_url_is_valid(self):
        netlify = read("netlify.toml")

        self.assertNotIn("https.www.", netlify)

    def test_publication_front_matter_has_no_duplicate_keys_or_template_tags(self):
        publication_files = sorted((ROOT / "content/publication").rglob("*.md"))

        for path in publication_files:
            with self.subTest(path=path.relative_to(ROOT)):
                frontmatter = front_matter(path.relative_to(ROOT))
                keys = [
                    match.group(1)
                    for match in re.finditer(r"^([A-Za-z0-9_-]+):", frontmatter, re.MULTILINE)
                ]
                duplicates = {key for key in keys if keys.count(key) > 1}

                self.assertFalse(duplicates, f"Duplicate front matter keys: {duplicates}")
                self.assertNotIn("abstract: ---", frontmatter)
                self.assertNotIn("Source Themes", frontmatter)

    def test_publication_summaries_are_polished(self):
        content = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "content/publication").rglob("*.md"))

        self.assertNotIn("abstract: he African", content)
        self.assertNotIn("As a results", content)
        self.assertNotIn("AfCFTA is likely to income inequality", content)

    def test_homepage_source_has_no_inactive_template_placeholders(self):
        content = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "content/home").rglob("*.md"))

        for placeholder in ["Photography", "Emojiness", "provider: formspree", "id: test"]:
            self.assertNotIn(placeholder, content)

    def test_author_education_matches_resume(self):
        profile = read("content/authors/admin/_index.md")

        self.assertIn("year: 2018 - Present", profile)
        self.assertIn("year: Dec. 2017", profile)
        self.assertIn("year: Dec. 2014", profile)
        self.assertNotIn("year: 2008", profile)

    def test_experience_dates_and_titles_match_resume(self):
        experience = read("content/home/experience.md")

        self.assertIn("title: Research Economist and Project Officer", experience)
        self.assertNotIn("Research Economist and Project Officer On the Co-Impact Project", experience)
        self.assertIn('date_start: "2024-02-01"', experience)
        self.assertIn('date_end: "2025-06-30"', experience)
        self.assertIn('date_end: "2021-12-31"', experience)
        self.assertIn('date_start: "2017-01-01"', experience)
        self.assertIn('date_end: "2019-07-31"', experience)

    def test_professional_training_matches_resume_and_current_site(self):
        accomplishments = read("content/home/accomplishments.md")
        expected_training = [
            "StEPPFoS Summer School 2026: Advanced Economic Modelling for FNSSA in Africa",
            "GTAP Firm Heterogeneity Course",
            "Non-Tariff Measures and Data Collection 2019",
            "Treatment/Impact evaluation models Theory and Application",
            "Certified Securities and Investment Analyst (Section I and II)",
        ]

        for title in expected_training:
            with self.subTest(title=title):
                self.assertIn(title, accomplishments)

        self.assertIn('date_start: "2026-05-25"', accomplishments)
        self.assertIn('date_end: "2026-05-29"', accomplishments)
        self.assertIn("https://steppfos.faraafrica.org/2026/03/27/steppfos-summer-school-2026-advanced-economic-modelling-for-fnssa-in-africa/", accomplishments)


if __name__ == "__main__":
    unittest.main()
