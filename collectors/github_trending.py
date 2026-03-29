"""GitHub Trending repos collector via HTML scraping."""

import logging
import requests
from bs4 import BeautifulSoup
from config import GITHUB_LANGUAGES, REQUEST_TIMEOUT, USER_AGENT

log = logging.getLogger(__name__)


def collect() -> list[dict]:
    """Collect trending repositories from GitHub."""
    items = []
    headers = {"User-Agent": USER_AGENT}
    seen_urls = set()

    for lang in GITHUB_LANGUAGES:
        try:
            resp = requests.get(
                f"https://github.com/trending/{lang}?since=daily",
                headers=headers, timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            for article in soup.select("article.Box-row"):
                # Repo name and link
                h2 = article.select_one("h2 a")
                if not h2:
                    continue
                repo_path = h2.get("href", "").strip()
                url = f"https://github.com{repo_path}"

                if url in seen_urls:
                    continue
                seen_urls.add(url)

                name = repo_path.lstrip("/")

                # Description
                desc_el = article.select_one("p")
                description = desc_el.get_text(strip=True) if desc_el else ""

                # Stars today
                stars_today = ""
                spans = article.select("span.d-inline-block.float-sm-right")
                if spans:
                    stars_today = spans[0].get_text(strip=True)

                # Total stars
                total_stars = 0
                star_links = article.select("a.Link--muted")
                if star_links:
                    star_text = star_links[0].get_text(strip=True).replace(",", "")
                    try:
                        total_stars = int(star_text)
                    except ValueError:
                        pass

                # Language
                lang_span = article.select_one("[itemprop='programmingLanguage']")
                language = lang_span.get_text(strip=True) if lang_span else lang

                items.append({
                    "title": name,
                    "url": url,
                    "source": "GitHub Trending",
                    "summary": f"{description} ({stars_today})" if stars_today else description,
                    "score": total_stars,
                    "timestamp": "",
                    "meta": {
                        "language": language,
                        "stars": total_stars,
                        "stars_today": stars_today,
                    },
                })

        except Exception as e:
            log.warning("GitHub: Failed to fetch trending/%s: %s", lang, e)
            continue

    log.info("GitHub: Collected %d trending repos", len(items))
    return items
