"""Konfiguration für das Recherche-Tool."""

import os

# --- Themengebiete mit Keywords ---

TOPICS = {
    "AI / Machine Learning": {
        "emoji": "\U0001f916",
        "keywords": [
            "llm", "large language model", "gpt", "claude", "gemini", "transformer",
            "neural network", "deep learning", "machine learning", "fine-tuning",
            "training", "inference", "diffusion", "reinforcement learning",
            "natural language", "computer vision", "multimodal", "rag",
            "embedding", "tokenizer", "lora", "quantization", "gguf", "mlx",
            "ollama", "hugging face", "openai", "anthropic", "mistral", "llama",
            "stable diffusion", "midjourney", "ai agent", "mcp", "tool use",
        ],
    },
    "Apple / Hardware": {
        "emoji": "\U0001f34e",
        "keywords": [
            "apple", "iphone", "ipad", "mac", "macbook", "apple silicon",
            "m4", "m5", "a18", "neural engine", "ane", "coreml", "metal",
            "wwdc", "ios", "macos", "swift", "swiftui", "xcode", "vision pro",
            "gpu", "cpu", "chip", "semiconductor", "tsmc", "arm", "risc-v",
            "nvidia", "amd", "intel", "qualcomm",
        ],
    },
    "Software Engineering": {
        "emoji": "\U0001f4bb",
        "keywords": [
            "rust", "golang", "typescript", "python", "kubernetes", "docker",
            "microservices", "api", "graphql", "grpc", "database", "postgres",
            "redis", "kafka", "ci/cd", "devops", "gitops", "terraform",
            "serverless", "edge computing", "wasm", "webassembly",
            "framework", "library", "open source", "developer tools",
            "testing", "performance", "scalability", "architecture",
        ],
    },
    "IT Business / Startups": {
        "emoji": "\U0001f4c8",
        "keywords": [
            "startup", "funding", "series a", "series b", "ipo", "acquisition",
            "valuation", "venture capital", "vc", "saas", "b2b", "b2c",
            "product launch", "pivot", "growth", "revenue", "market",
            "competition", "disruption", "unicorn", "techcrunch",
            "layoffs", "hiring", "remote work",
        ],
    },
    "IT Security": {
        "emoji": "\U0001f512",
        "keywords": [
            "security", "vulnerability", "cve", "exploit", "ransomware",
            "malware", "phishing", "zero-day", "0day", "breach", "hack",
            "cybersecurity", "encryption", "authentication", "oauth",
            "ssl", "tls", "firewall", "pentest", "bug bounty",
            "supply chain attack", "backdoor", "apt", "threat",
            "data leak", "privacy", "gdpr", "compliance",
        ],
    },
}

# --- Quellen-Konfiguration ---

HACKERNEWS_TOP_N = 50
HACKERNEWS_API = "https://hacker-news.firebaseio.com/v0"

REDDIT_SUBREDDITS = [
    "MachineLearning", "LocalLLaMA", "netsec", "programming",
    "apple", "startups", "artificial", "cybersecurity",
]
REDDIT_TOP_N = 25  # pro Subreddit

ARXIV_QUERIES = [
    "cat:cs.AI",
    "cat:cs.LG",
    "cat:cs.CR",
    "cat:cs.CL",
]
ARXIV_MAX_RESULTS = 30

GITHUB_LANGUAGES = ["python", "rust", "typescript", "swift", "go"]

RSS_FEEDS = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Heise", "https://www.heise.de/rss/heise-atom.xml"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
    ("Hacker News (RSS)", "https://hnrss.org/newest?points=100"),
    ("The Register", "https://www.theregister.com/headlines.atom"),
]

# --- Scoring ---

KEYWORD_MATCH_SCORE = 10       # pro Keyword-Match im Titel
KEYWORD_BODY_SCORE = 3         # pro Keyword-Match im Body/Summary
MIN_RELEVANCE_SCORE = 5        # Minimum um in den Report zu kommen
MAX_ITEMS_PER_TOPIC = 15       # Max Artikel pro Themengebiet im Report

# --- Scheduler ---

SCHEDULE_START_HOUR = 22       # 22:00 Uhr
SCHEDULE_END_HOUR = 7          # 07:00 Uhr
COLLECTION_INTERVAL_MIN = 30   # Alle 30 Minuten neue Runde
REPORT_GENERATION_HOUR = 6
REPORT_GENERATION_MIN = 30     # Report um 06:30 generieren

# --- Pfade ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOG_FILE = os.path.join(BASE_DIR, "recherche.log")

# --- HTTP ---

REQUEST_TIMEOUT = 30  # Sekunden (ArXiv braucht oft laenger)
USER_AGENT = "Recherche_Tool/1.0 (github.com/slavko-at-klincov-it/Recherche_Tool)"
