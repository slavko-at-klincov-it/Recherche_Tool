# Recherche_Tool

Automatisierte Nacht-Recherche: Durchforstet das Internet nach relevanten IT-Themen und generiert einen Morgen-Report.

## Was es tut

- Sammelt Artikel aus **5 Quellen**: Hacker News, Reddit, ArXiv, GitHub Trending, RSS Feeds
- Kategorisiert in **5 Themengebiete**: AI/ML, Apple/Hardware, Software Engineering, IT Business, IT Security
- Bewertet Relevanz durch Keyword-Matching
- Generiert einen **Markdown-Report** pro Tag

## Schnellstart

```bash
# Dependencies installieren
pip3 install -r requirements.txt

# Sofort-Recherche (alle Quellen, Report generieren)
python3 recherche.py --now

# Report anschauen
open reports/$(date +%Y-%m-%d).md
```

## Nacht-Modus

```bash
# Daemon starten (sammelt 22:00-07:00, Report um 06:30)
python3 recherche.py --daemon
```

## Quellen

| Quelle | API | Beschreibung |
|:-------|:----|:-------------|
| Hacker News | Firebase API | Top 50 Stories |
| Reddit | JSON API | 8 Subreddits (ML, Security, Programming, ...) |
| ArXiv | Atom API | Neue Papers in cs.AI, cs.LG, cs.CR, cs.CL |
| GitHub Trending | HTML Scraping | Trending Repos in Python, Rust, TS, Swift, Go |
| RSS Feeds | feedparser | TechCrunch, Ars Technica, Heise, Krebs, ... |

Keine API-Keys noetig.

## Themengebiete

- **AI / Machine Learning** — LLMs, Training, Inference, neue Modelle
- **Apple / Hardware** — Apple Silicon, ANE, Chips, GPUs
- **Software Engineering** — Frameworks, Tools, DevOps, Architektur
- **IT Business / Startups** — Funding, Launches, Markt-Trends
- **IT Security** — Vulnerabilities, Hacks, CVEs, Compliance

## Konfiguration

Alle Einstellungen in `config.py`:
- Themen-Keywords
- Quellen und Subreddits
- Scoring-Gewichtungen
- Zeitfenster (Standard: 22:00-07:00)
- Max Artikel pro Kategorie

## Projektstruktur

```
recherche.py           # Hauptskript (CLI)
config.py              # Konfiguration
analyzer.py            # Relevanz-Scoring & Kategorisierung
report.py              # Markdown-Report-Generator
scheduler.py           # Nacht-Scheduling
collectors/            # Quellen-Module
  hackernews.py
  reddit.py
  arxiv.py
  github_trending.py
  rss_feeds.py
reports/               # Generierte Reports (pro Tag)
```

## Zukunft

- Integration mit Geofrey.ai (Knowledge-Base, LinkedIn-Posts)
- Claude API fuer intelligentere Zusammenfassungen
- Web-UI zum Durchblaettern
