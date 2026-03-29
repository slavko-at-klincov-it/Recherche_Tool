"""Collector modules for different sources."""

from .hackernews import collect as collect_hackernews
from .reddit import collect as collect_reddit
from .arxiv import collect as collect_arxiv
from .github_trending import collect as collect_github
from .rss_feeds import collect as collect_rss

ALL_COLLECTORS = [
    ("Hacker News", collect_hackernews),
    ("Reddit", collect_reddit),
    ("ArXiv", collect_arxiv),
    ("GitHub Trending", collect_github),
    ("RSS Feeds", collect_rss),
]
