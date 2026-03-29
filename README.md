# Recherche_Tool

Automatisierte Internet-Recherche mit Web-UI. Durchforstet Hacker News, Reddit, ArXiv, GitHub Trending und RSS Feeds nach relevanten IT-Themen und generiert einen aufbereiteten Tagesreport.

## Schnellstart

```bash
# Dependencies installieren
pip3 install -r requirements.txt

# Sofort-Recherche (alle Quellen, Report generieren)
python3 recherche.py --now

# Web-UI starten und Report durchblaettern
python3 recherche.py --web
# -> http://localhost:5050
```

## Features

- **5 Quellen**: Hacker News, Reddit, ArXiv, GitHub Trending, RSS Feeds
- **5 Themengebiete**: AI/ML, Apple/Hardware, Software Engineering, IT Business, IT Security
- **Web-UI**: Dark-Theme Dashboard zum Durchblaettern, Filtern, Markieren
- **Artikel merken**: Stern-Button zum Speichern interessanter Artikel
- **Gelesen-Status**: Artikel als gelesen markieren (werden ausgegraut)
- **macOS Notification**: Benachrichtigung wenn Report fertig
- **Auto-Scheduling**: LaunchAgent fuer taegliche automatische Recherche
- **Keine API-Keys**: Alle Quellen sind oeffentlich zugaenglich

## Modi

```bash
# Sofort alle Quellen abrufen und Report generieren
python3 recherche.py --now

# Web-UI starten (http://localhost:5050)
python3 recherche.py --web

# Nacht-Daemon (sammelt 22:00-07:00, Report um 06:30)
python3 recherche.py --daemon

# Optionen
python3 recherche.py --web -p 8080    # Anderer Port
python3 recherche.py --now -v         # Verbose/Debug-Logging
```

## Automatischer Taeglicher Lauf

```bash
# macOS LaunchAgent installieren (laeuft jeden Tag um 06:00)
bash install_scheduler.sh

# Status pruefen
launchctl list | grep recherche

# Deaktivieren
launchctl unload ~/Library/LaunchAgents/com.klincov.recherche.plist
```

## Quellen

| Quelle | API | Was |
|:-------|:----|:----|
| Hacker News | Firebase API | Top 50 Stories |
| Reddit | JSON API | 8 Subreddits (ML, Security, Programming, ...) |
| ArXiv | Atom API | Neue Papers in cs.AI, cs.LG, cs.CR, cs.CL |
| GitHub Trending | HTML Scraping | Trending Repos in Python, Rust, TS, Swift, Go |
| RSS Feeds | feedparser | TechCrunch, Ars Technica, Heise, Krebs, The Register |

## Themengebiete & Keywords

Konfigurierbar in `config.py`:

- **AI / Machine Learning** — LLMs, Training, Inference, Modelle, Frameworks
- **Apple / Hardware** — Apple Silicon, ANE, Chips, GPUs, WWDC
- **Software Engineering** — Rust, Kubernetes, APIs, DevOps, Architektur
- **IT Business / Startups** — Funding, Launches, SaaS, Markt-Trends
- **IT Security** — CVEs, Hacks, Ransomware, Zero-Days, Compliance

## Projektstruktur

```
recherche.py              # Hauptskript (CLI: --now, --daemon, --web)
web.py                    # Flask Web-UI
config.py                 # Konfiguration (Themen, Quellen, Scoring)
analyzer.py               # Relevanz-Scoring & Kategorisierung
report.py                 # Markdown-Report-Generator
scheduler.py              # Nacht-Scheduling
install_scheduler.sh      # macOS LaunchAgent Setup
collectors/               # Quellen-Module
  hackernews.py
  reddit.py
  arxiv.py
  github_trending.py
  rss_feeds.py
templates/                # Web-UI Templates (Jinja2)
static/                   # CSS
reports/                  # Generierte Reports (pro Tag .md)
bookmarks.json            # Gemerkte/gelesene Artikel
```

## Zukunft

- Integration mit Geofrey.ai (Knowledge-Base, LinkedIn-Posts)
- Claude API fuer intelligentere Zusammenfassungen
- Trend-Erkennung ueber mehrere Tage
