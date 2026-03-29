#!/usr/bin/env python3
"""Recherche_Tool — Automatisierte Internet-Recherche.

Usage:
    python recherche.py --now       # Sofort alle Quellen abrufen und Report generieren
    python recherche.py --daemon    # Nacht-Modus (22:00-07:00, Report um 06:30)
"""

import argparse
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import LOG_FILE
from collectors import ALL_COLLECTORS
from analyzer import analyze
from report import generate
from scheduler import run_daemon


def setup_logging(verbose: bool = False):
    """Configure logging to file and console."""
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def collect_all() -> list[dict]:
    """Run all collectors and return combined items."""
    all_items = []

    for name, collector in ALL_COLLECTORS:
        logging.info("Collecting from %s...", name)
        try:
            items = collector()
            all_items.extend(items)
            logging.info("  -> %d items", len(items))
        except Exception as e:
            logging.error("  -> FAILED: %s", e)

    logging.info("Total collected: %d items", len(all_items))
    return all_items


def run_and_report(items: list[dict]) -> str:
    """Analyze items and generate report. Returns report path."""
    total = len(items)
    categorized = analyze(items)
    return generate(categorized, total)


def main():
    parser = argparse.ArgumentParser(
        description="Recherche_Tool - Automatisierte Internet-Recherche",
    )
    parser.add_argument("--now", action="store_true",
                        help="Sofort alle Quellen abrufen und Report generieren")
    parser.add_argument("--daemon", action="store_true",
                        help="Nacht-Modus (22:00-07:00)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Debug-Logging aktivieren")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.daemon:
        logging.info("=== Recherche_Tool - Nacht-Daemon ===")
        run_daemon(
            collect_fn=collect_all,
            report_fn=lambda items: run_and_report(items),
        )
    elif args.now:
        logging.info("=== Recherche_Tool - Sofort-Modus ===")
        items = collect_all()
        path = run_and_report(items)
        print(f"\nReport generiert: {path}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
