from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List


CLAIM_MARKERS = ("therefore", "shows that", "suggests", "indicates", "we find", "we argue", "because")
ASSUMPTION_MARKERS = ("assume", "assuming", "depends on", "requires", "premise", "given that")
UNCERTAINTY_MARKERS = ("may", "might", "could", "unclear", "uncertain", "limited", "unknown", "risk")
WEAKNESS_MARKERS = ("however", "but", "limitation", "weakness", "bias", "fails", "challenge")
CONTRADICTION_MARKERS = ("contradict", "conflict", "inconsistent", "whereas", "on the other hand")


def sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    clean = [part.strip() for part in parts if len(part.strip()) > 30]
    return clean[:80]


def pick_sentences(text: str, markers: Iterable[str], limit: int) -> List[str]:
    marker_set = tuple(marker.lower() for marker in markers)
    found = [s for s in sentences(text) if any(marker in s.lower() for marker in marker_set)]
    return dedupe(found)[:limit]


def top_terms(text: str, limit: int = 8) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z-]{3,}", text.lower())
    stop = {
        "that",
        "this",
        "with",
        "from",
        "have",
        "their",
        "about",
        "which",
        "would",
        "there",
        "these",
        "those",
        "into",
        "were",
        "been",
        "being",
        "than",
    }
    counts = Counter(word for word in words if word not in stop)
    return [word for word, _ in counts.most_common(limit)]


def dedupe(items: Iterable[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        key = re.sub(r"\W+", " ", item.lower()).strip()
        if key and key not in seen:
            seen.add(key)
            output.append(item)
    return output


def fallback_list(prefix: str, terms: List[str], limit: int) -> List[str]:
    if not terms:
        return [f"{prefix} The document needs more explicit evidence before this can be trusted."]
    return [f"{prefix} {term} appears central and should be examined as a reasoning dependency." for term in terms[:limit]]
