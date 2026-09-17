#!/usr/bin/env python3
"""Which tournament we are pulling, and where its captures live.

One place to change when the tour moves on. Everything else -- the capture,
the spreadsheet build, the API fetch -- reads the answer from here, so a new
week is a one-line edit (or just a different URL typed at the prompt).

Captures are filed per tournament. That is not tidiness: a shot record carries
a hole and a stroke but no tournament, and every event has a round 1, so
building a spreadsheet from a folder holding two tournaments silently
interleaves them.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
CAPTURED = HERE / "captured"

BASE_SITE = "https://www.europeantour.com"


@dataclass
class Tournament:
    slug: str
    name: str
    event_id: str | None = None   # the tour API's id; sniffed live when unknown

    @property
    def url(self) -> str:
        return f"{BASE_SITE}/dpworld-tour/{self.slug}/leaderboard?round=1"

    @property
    def captured_dir(self) -> Path:
        return CAPTURED / self.slug


# This week.
CURRENT = Tournament(
    slug="bmw-pga-championship-2026",
    name="BMW PGA Championship 2026",
)

# Captures made before runs were filed per tournament are all from this one.
LEGACY = Tournament(
    slug="amgen-irish-open-2026",
    name="Amgen Irish Open 2026",
    event_id="2026135",
)

REMEMBERED = HERE / "current_tournament.json"


def slug_from_url(url: str) -> str | None:
    """The tournament slug in a leaderboard URL, e.g. bmw-pga-championship-2026."""
    match = re.search(r"/dpworld-tour/([^/?#]+)", url)
    return match.group(1) if match else None


def titleise(slug: str) -> str:
    return slug.replace("-", " ").title().replace("Bmw", "BMW").replace("Pga", "PGA")


def from_url(url: str) -> Tournament:
    """A tournament for whatever leaderboard URL was actually used."""
    slug = slug_from_url(url)
    if not slug or slug == CURRENT.slug:
        return CURRENT
    if slug == LEGACY.slug:
        return LEGACY
    return Tournament(slug=slug, name=titleise(slug))


def remember(url: str) -> None:
    """Keep the URL that worked, so the next run offers it by default."""
    try:
        REMEMBERED.write_text(json.dumps({"url": url}, indent=2), encoding="utf-8")
    except OSError:
        pass


def default_url() -> str:
    """The URL to offer at the prompt: last one used, else this week's."""
    try:
        url = json.loads(REMEMBERED.read_text(encoding="utf-8")).get("url")
        if isinstance(url, str) and url.startswith("http"):
            return url
    except (OSError, ValueError):
        pass
    return CURRENT.url


EVENT_ID_IN_API_URL = re.compile(r"/Leaderboard/Strokeplay/(\d+)/", re.I)


def event_id_from_api_url(url: str) -> str | None:
    """The tour's event id, as it appears in the calls the leaderboard makes."""
    match = EVENT_ID_IN_API_URL.search(url)
    return match.group(1) if match else None


def event_id_path(tournament: Tournament) -> Path:
    return tournament.captured_dir / "_event.json"


def store_event_id(tournament: Tournament, event_id: str) -> None:
    """Record the id the site used, so later runs need no browser to find it."""
    try:
        tournament.captured_dir.mkdir(parents=True, exist_ok=True)
        event_id_path(tournament).write_text(
            json.dumps({"slug": tournament.slug, "name": tournament.name,
                        "event_id": event_id}, indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass


def known_event_id(tournament: Tournament) -> str | None:
    if tournament.event_id:
        return tournament.event_id
    try:
        value = json.loads(event_id_path(tournament).read_text(encoding="utf-8")).get("event_id")
        return str(value) if value else None
    except (OSError, ValueError):
        return None


def run_dirs(tournament: Tournament | None = None) -> list[Path]:
    """Capture folders for one tournament, newest layout and the old flat one.

    Runs from before tournaments were separated sit directly under captured/
    and belong to LEGACY, which is the only tournament captured back then.
    """
    tournament = tournament or CURRENT
    dirs = sorted(d for d in tournament.captured_dir.glob("run_*") if d.is_dir())
    if tournament.slug == LEGACY.slug:
        dirs += sorted(d for d in CAPTURED.glob("run_*") if d.is_dir())
    return dirs


def captured_tournaments() -> list[Tournament]:
    """Every tournament with captures on disk, so a build can offer a choice."""
    found = []
    for path in sorted(CAPTURED.glob("*")):
        if not path.is_dir() or path.name.startswith("_") or path.name.startswith("run_"):
            continue
        if not any(path.glob("run_*")):
            continue
        slug = path.name
        found.append(CURRENT if slug == CURRENT.slug
                     else LEGACY if slug == LEGACY.slug
                     else Tournament(slug=slug, name=titleise(slug)))
    if any(CAPTURED.glob("run_*")):
        found.append(LEGACY)
    # Same tournament can show up twice: nested folder plus legacy flat runs.
    unique = {t.slug: t for t in found}

    def last_capture(item: Tournament) -> str:
        dirs = run_dirs(item)
        return max((d.name for d in dirs), default="")

    return sorted(unique.values(), key=last_capture, reverse=True)
