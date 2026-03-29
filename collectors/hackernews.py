"""Hacker News API collector."""

import logging
import requests
from config import HACKERNEWS_API, HACKERNEWS_TOP_N, REQUEST_TIMEOUT, USER_AGENT

log = logging.getLogger(__name__)


def collect() -> list[dict]:
    """Collect top stories from Hacker News."""
    items = []
    headers = {"User-Agent": USER_AGENT}

    try:
        # Get top story IDs
        resp = requests.get(
            f"{HACKERNEWS_API}/topstories.json",
            headers=headers, timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        story_ids = resp.json()[:HACKERNEWS_TOP_N]
    except Exception as e:
        log.error("HN: Failed to fetch top stories: %s", e)
        return items

    for story_id in story_ids:
        try:
            resp = requests.get(
                f"{HACKERNEWS_API}/item/{story_id}.json",
                headers=headers, timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            story = resp.json()
            if not story or story.get("type") != "story":
                continue

            items.append({
                "title": story.get("title", ""),
                "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                "source": "Hacker News",
                "summary": f"{story.get('score', 0)} points, {story.get('descendants', 0)} comments",
                "score": story.get("score", 0),
                "timestamp": story.get("time", 0),
                "meta": {
                    "hn_id": story_id,
                    "comments": story.get("descendants", 0),
                    "by": story.get("by", ""),
                },
            })
        except Exception as e:
            log.warning("HN: Failed to fetch story %s: %s", story_id, e)
            continue

    log.info("HN: Collected %d stories", len(items))
    return items
