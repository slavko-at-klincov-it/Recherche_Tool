"""Web UI for browsing Recherche reports."""

import json
import os
import glob
from datetime import datetime
from flask import Flask, render_template, request, jsonify

from config import REPORTS_DIR, TOPICS, BASE_DIR

app = Flask(__name__)

BOOKMARKS_FILE = os.path.join(BASE_DIR, "bookmarks.json")


def load_bookmarks() -> dict:
    if os.path.exists(BOOKMARKS_FILE):
        with open(BOOKMARKS_FILE, "r") as f:
            return json.load(f)
    return {"starred": [], "read": []}


def save_bookmarks(data: dict):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def parse_report(filepath: str) -> dict:
    """Parse a markdown report into structured data."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    report = {
        "date": "",
        "stats_line": "",
        "topics": {},
        "raw": content,
    }

    # Extract date from filename
    basename = os.path.basename(filepath).replace(".md", "")
    report["date"] = basename

    # Parse stats
    for line in lines:
        if line.startswith("> Automatisch generiert"):
            report["stats_line"] = line.lstrip("> ").strip()
        if "Artikel gesammelt" in line:
            report["collected_line"] = line.lstrip("> ").strip()

    # Parse topics and articles
    current_topic = None
    current_article = None
    topic_config = {v["emoji"]: k for k, v in TOPICS.items()}

    for line in lines:
        # Topic header: ## 🤖 AI / Machine Learning (15 Artikel)
        if line.startswith("## ") and not line.startswith("###"):
            for emoji, topic_name in topic_config.items():
                if emoji in line:
                    current_topic = topic_name
                    # Extract count
                    count = ""
                    if "(" in line and "Artikel" in line:
                        count = line.split("(")[1].split(" ")[0]
                    report["topics"][current_topic] = {
                        "emoji": emoji,
                        "count": count,
                        "articles": [],
                    }
                    current_article = None
                    break

        # Article header: ### [Title](url)
        elif line.startswith("### ") and current_topic:
            if current_article:
                report["topics"][current_topic]["articles"].append(current_article)

            title = line[4:]
            url = ""
            if title.startswith("[") and "](" in title:
                title_part = title.split("](")
                title = title_part[0][1:]
                url = title_part[1].rstrip(")")

            current_article = {
                "title": title,
                "url": url,
                "summary": "",
                "meta": "",
                "id": hash(url or title) & 0xFFFFFFFF,
            }

        # Summary/meta lines (start with >)
        elif line.startswith("> ") and current_article:
            text = line[2:]
            if text.startswith("Quelle:"):
                current_article["meta"] = text
            else:
                if current_article["summary"]:
                    current_article["summary"] += " "
                current_article["summary"] += text

    # Don't forget last article
    if current_article and current_topic and current_topic in report["topics"]:
        report["topics"][current_topic]["articles"].append(current_article)

    return report


def get_available_reports() -> list[str]:
    """Get list of available report dates, newest first."""
    pattern = os.path.join(REPORTS_DIR, "*.md")
    files = glob.glob(pattern)
    dates = [os.path.basename(f).replace(".md", "") for f in files]
    dates.sort(reverse=True)
    return dates


@app.route("/")
def index():
    dates = get_available_reports()
    selected = request.args.get("date", dates[0] if dates else None)
    topic_filter = request.args.get("topic", "all")

    report = None
    if selected:
        filepath = os.path.join(REPORTS_DIR, f"{selected}.md")
        if os.path.exists(filepath):
            report = parse_report(filepath)

    bookmarks = load_bookmarks()

    return render_template(
        "index.html",
        dates=dates,
        selected=selected,
        report=report,
        topic_filter=topic_filter,
        topics=TOPICS,
        bookmarks=bookmarks,
    )


@app.route("/api/bookmark", methods=["POST"])
def bookmark():
    data = request.get_json()
    action = data.get("action")  # "star" or "read"
    article_id = str(data.get("id"))
    article_url = data.get("url", "")
    article_title = data.get("title", "")

    bookmarks = load_bookmarks()
    key = "starred" if action == "star" else "read"

    entry = {"id": article_id, "url": article_url, "title": article_title,
             "date": datetime.now().isoformat()}

    # Toggle
    existing_ids = [str(b["id"]) for b in bookmarks[key]]
    if article_id in existing_ids:
        bookmarks[key] = [b for b in bookmarks[key] if str(b["id"]) != article_id]
        state = False
    else:
        bookmarks[key].append(entry)
        state = True

    save_bookmarks(bookmarks)
    return jsonify({"ok": True, "state": state})


@app.route("/starred")
def starred():
    bookmarks = load_bookmarks()
    return render_template("starred.html", bookmarks=bookmarks, topics=TOPICS)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
