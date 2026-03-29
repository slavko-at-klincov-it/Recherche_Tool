"""RSS/Atom feed collector."""

import logging
import feedparser
from config import RSS_FEEDS

log = logging.getLogger(__name__)


def collect() -> list[dict]:
    """Collect articles from RSS/Atom feeds."""
    items = []

    for feed_name, feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            if feed.bozo and not feed.entries:
                log.warning("RSS: Feed %s returned error: %s", feed_name, feed.bozo_exception)
                continue

            for entry in feed.entries[:20]:  # Max 20 per feed
                title = entry.get("title", "").strip()
                link = entry.get("link", "")
                summary = entry.get("summary", entry.get("description", ""))

                # Clean HTML from summary
                if summary and "<" in summary:
                    from bs4 import BeautifulSoup
                    summary = BeautifulSoup(summary, "html.parser").get_text()
                summary = (summary or "")[:400].strip()

                # Timestamp
                published = entry.get("published", entry.get("updated", ""))

                items.append({
                    "title": title,
                    "url": link,
                    "source": feed_name,
                    "summary": summary,
                    "score": 0,
                    "timestamp": published,
                    "meta": {
                        "feed": feed_name,
                        "author": entry.get("author", ""),
                    },
                })

        except Exception as e:
            log.warning("RSS: Failed to parse %s: %s", feed_name, e)
            continue

    log.info("RSS: Collected %d articles from %d feeds", len(items), len(RSS_FEEDS))
    return items
