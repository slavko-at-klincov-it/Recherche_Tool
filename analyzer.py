"""Relevanz-Scoring und Kategorisierung der gesammelten Artikel."""

import logging
from config import TOPICS, KEYWORD_MATCH_SCORE, KEYWORD_BODY_SCORE, MIN_RELEVANCE_SCORE

log = logging.getLogger(__name__)


def analyze(items: list[dict]) -> dict[str, list[dict]]:
    """Score, categorize, deduplicate, and sort items by topic.

    Returns dict mapping topic name -> list of scored items, sorted by relevance.
    """
    # Deduplicate by URL
    seen_urls = set()
    unique_items = []
    for item in items:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_items.append(item)

    log.info("Deduplicated: %d -> %d items", len(items), len(unique_items))

    # Score and categorize each item
    categorized = {topic: [] for topic in TOPICS}

    for item in unique_items:
        title = item.get("title", "").lower()
        summary = item.get("summary", "").lower()
        best_topic = None
        best_score = 0

        for topic_name, topic_config in TOPICS.items():
            score = 0
            for keyword in topic_config["keywords"]:
                kw = keyword.lower()
                if kw in title:
                    score += KEYWORD_MATCH_SCORE
                if kw in summary:
                    score += KEYWORD_BODY_SCORE

            if score > best_score:
                best_score = score
                best_topic = topic_name

        if best_topic and best_score >= MIN_RELEVANCE_SCORE:
            item["relevance_score"] = best_score
            item["topic"] = best_topic
            categorized[best_topic].append(item)

    # Sort each topic by relevance score (descending)
    for topic in categorized:
        categorized[topic].sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    total = sum(len(v) for v in categorized.values())
    log.info("Categorized %d relevant items across %d topics", total, len(TOPICS))
    for topic, items_list in categorized.items():
        if items_list:
            log.info("  %s: %d items", topic, len(items_list))

    return categorized
