"""ArXiv API collector for research papers."""

import logging
import xml.etree.ElementTree as ET
import requests
from config import ARXIV_QUERIES, ARXIV_MAX_RESULTS, REQUEST_TIMEOUT, USER_AGENT

log = logging.getLogger(__name__)

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def collect() -> list[dict]:
    """Collect recent papers from ArXiv."""
    items = []
    headers = {"User-Agent": USER_AGENT}

    query = " OR ".join(ARXIV_QUERIES)

    try:
        resp = requests.get(
            ARXIV_API,
            params={
                "search_query": query,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": ARXIV_MAX_RESULTS,
            },
            headers=headers, timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()

        root = ET.fromstring(resp.text)

        for entry in root.findall("atom:entry", NS):
            title = entry.findtext("atom:title", "", NS).strip().replace("\n", " ")
            summary = entry.findtext("atom:summary", "", NS).strip().replace("\n", " ")
            published = entry.findtext("atom:published", "", NS)

            # Get PDF link
            pdf_url = ""
            for link in entry.findall("atom:link", NS):
                if link.get("title") == "pdf":
                    pdf_url = link.get("href", "")
                    break

            # Get main link
            main_url = ""
            for link in entry.findall("atom:link", NS):
                if link.get("rel") == "alternate":
                    main_url = link.get("href", "")
                    break

            # Authors
            authors = [
                a.findtext("atom:name", "", NS)
                for a in entry.findall("atom:author", NS)
            ]

            # Categories
            categories = [
                c.get("term", "")
                for c in entry.findall("atom:category", NS)
            ]

            items.append({
                "title": title,
                "url": main_url or pdf_url,
                "source": "ArXiv",
                "summary": summary[:400],
                "score": 0,  # ArXiv has no score
                "timestamp": published,
                "meta": {
                    "authors": authors[:5],  # First 5 authors
                    "categories": categories,
                    "pdf": pdf_url,
                },
            })

    except Exception as e:
        log.error("ArXiv: Failed to fetch papers: %s", e)

    log.info("ArXiv: Collected %d papers", len(items))
    return items
