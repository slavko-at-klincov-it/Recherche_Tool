"""Reddit JSON API collector (no OAuth needed)."""

import logging
import time
import requests
from config import REDDIT_SUBREDDITS, REDDIT_TOP_N, REQUEST_TIMEOUT, USER_AGENT

log = logging.getLogger(__name__)


def collect() -> list[dict]:
    """Collect top posts from relevant subreddits."""
    items = []
    headers = {"User-Agent": USER_AGENT}

    for sub in REDDIT_SUBREDDITS:
        try:
            resp = requests.get(
                f"https://www.reddit.com/r/{sub}/hot.json?limit={REDDIT_TOP_N}",
                headers=headers, timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()

            for post in data.get("data", {}).get("children", []):
                p = post.get("data", {})
                if p.get("stickied"):
                    continue

                items.append({
                    "title": p.get("title", ""),
                    "url": p.get("url", ""),
                    "source": f"r/{sub}",
                    "summary": (p.get("selftext", "") or "")[:300],
                    "score": p.get("score", 0),
                    "timestamp": int(p.get("created_utc", 0)),
                    "meta": {
                        "subreddit": sub,
                        "comments": p.get("num_comments", 0),
                        "author": p.get("author", ""),
                        "permalink": f"https://reddit.com{p.get('permalink', '')}",
                    },
                })
        except Exception as e:
            log.warning("Reddit: Failed to fetch r/%s: %s", sub, e)
            continue

        # Rate limiting
        time.sleep(1)

    log.info("Reddit: Collected %d posts from %d subreddits", len(items), len(REDDIT_SUBREDDITS))
    return items
