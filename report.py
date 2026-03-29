"""Markdown report generator."""

import logging
import os
from datetime import datetime
from config import TOPICS, MAX_ITEMS_PER_TOPIC, REPORTS_DIR

log = logging.getLogger(__name__)


def generate(categorized: dict[str, list[dict]], total_collected: int) -> str:
    """Generate a Markdown report from categorized items.

    Returns the file path of the generated report.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"{today}.md")

    total_relevant = sum(len(v) for v in categorized.values())

    lines = []
    lines.append(f"# Recherche Report \u2014 {today}")
    lines.append("")
    lines.append(f"> Automatisch generiert am {datetime.now().strftime('%d.%m.%Y um %H:%M')}")
    lines.append(f"> {total_collected} Artikel gesammelt, {total_relevant} als relevant eingestuft")
    lines.append("")
    lines.append("---")
    lines.append("")

    for topic_name, topic_config in TOPICS.items():
        emoji = topic_config["emoji"]
        items = categorized.get(topic_name, [])[:MAX_ITEMS_PER_TOPIC]

        lines.append(f"## {emoji} {topic_name} ({len(items)} Artikel)")
        lines.append("")

        if not items:
            lines.append("_Keine relevanten Artikel gefunden._")
            lines.append("")
            continue

        for item in items:
            title = item.get("title", "Ohne Titel")
            url = item.get("url", "")
            source = item.get("source", "")
            summary = item.get("summary", "")
            relevance = item.get("relevance_score", 0)
            meta = item.get("meta", {})

            # Title as link
            if url:
                lines.append(f"### [{title}]({url})")
            else:
                lines.append(f"### {title}")

            # Summary
            if summary:
                # Truncate long summaries
                if len(summary) > 250:
                    summary = summary[:247] + "..."
                lines.append(f"> {summary}")

            # Metadata line
            meta_parts = [f"Quelle: **{source}**"]
            meta_parts.append(f"Relevanz: {relevance}")

            if item.get("score"):
                meta_parts.append(f"Score: {item['score']}")

            if meta.get("comments"):
                meta_parts.append(f"Kommentare: {meta['comments']}")

            if meta.get("stars"):
                meta_parts.append(f"\u2b50 {meta['stars']}")

            if meta.get("language"):
                meta_parts.append(f"Sprache: {meta['language']}")

            if meta.get("authors"):
                authors = ", ".join(meta["authors"][:3])
                meta_parts.append(f"Autoren: {authors}")

            if meta.get("pdf"):
                meta_parts.append(f"[PDF]({meta['pdf']})")

            lines.append(f"> {' | '.join(meta_parts)}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Footer
    lines.append(f"_Generiert von [Recherche_Tool](https://github.com/slavko-at-klincov-it/Recherche_Tool)_")

    content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    log.info("Report written to %s (%d lines)", filepath, len(lines))
    return filepath
