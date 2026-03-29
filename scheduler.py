"""Nacht-Scheduler: Sammelt zwischen 22:00 und 07:00, generiert Report um 06:30."""

import logging
import time
from datetime import datetime
from config import (
    SCHEDULE_START_HOUR, SCHEDULE_END_HOUR,
    COLLECTION_INTERVAL_MIN, REPORT_GENERATION_HOUR, REPORT_GENERATION_MIN,
)

log = logging.getLogger(__name__)


def is_collection_window() -> bool:
    """Check if current time is within the collection window (22:00-07:00)."""
    hour = datetime.now().hour
    return hour >= SCHEDULE_START_HOUR or hour < SCHEDULE_END_HOUR


def is_report_time() -> bool:
    """Check if it's time to generate the final report (06:30)."""
    now = datetime.now()
    return now.hour == REPORT_GENERATION_HOUR and now.minute >= REPORT_GENERATION_MIN


def run_daemon(collect_fn, report_fn):
    """Run the overnight daemon.

    Args:
        collect_fn: Function that collects and returns all items.
        report_fn: Function that takes items and generates a report.
    """
    log.info("Daemon started. Waiting for collection window (%02d:00-%02d:00)...",
             SCHEDULE_START_HOUR, SCHEDULE_END_HOUR)

    all_items = []
    report_generated = False
    last_collection = 0

    while True:
        now = datetime.now()

        if is_collection_window():
            elapsed = time.time() - last_collection

            if elapsed >= COLLECTION_INTERVAL_MIN * 60:
                log.info("Collection round at %s", now.strftime("%H:%M"))
                new_items = collect_fn()
                all_items.extend(new_items)
                last_collection = time.time()
                log.info("Total items collected: %d", len(all_items))

            if is_report_time() and not report_generated:
                log.info("Generating final report...")
                report_fn(all_items)
                report_generated = True
                log.info("Report generated. Daemon will exit.")
                break

        time.sleep(60)  # Check every minute
