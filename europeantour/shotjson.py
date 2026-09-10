"""Schema-agnostic tools for finding and flattening shot data in JSON payloads.

The DP World Tour feed is undocumented and its field names change between
seasons, so nothing here hard-codes a schema. We score payloads by how much
shot-shaped vocabulary they contain, then flatten whatever record arrays we
find into tidy rows.
"""
from __future__ import annotations

from typing import Any, Iterator

# Weighted vocabulary. Keys are compared lowercased with separators stripped,
# so "shotNumber", "shot_number" and "ShotNumber" all collapse to "shotnumber".
SHOT_KEY_WEIGHTS: dict[str, int] = {
    "shots": 6,
    "shotnumber": 6,
    "shottracker": 6,
    "shotdata": 5,
    "shot": 4,
    "strokenumber": 4,
    "club": 4,
    "clubused": 4,
    "trajectory": 4,
    "ballposition": 4,
    "fromlocation": 4,
    "tolocation": 4,
    "distancetopin": 4,
    "distancetohole": 4,
    "carry": 3,
    "lie": 3,
    "surface": 3,
    "coordinates": 3,
    "latitude": 2,
    "longitude": 2,
    "elevation": 2,
    "scorecard": 2,
    "holes": 2,
    "holenumber": 2,
    "strokes": 2,
    "par": 1,
    "round": 1,
    "roundnumber": 1,
    "playerid": 1,
    "x": 1,
    "y": 1,
    "z": 1,
}

# A record array must have at least this much vocabulary overlap to count as
# a candidate shot table.
MIN_ARRAY_SCORE = 6


def norm_key(key: str) -> str:
    return "".join(ch for ch in key.lower() if ch.isalnum())


def walk_keys(obj: Any) -> Iterator[str]:
    """Yield every dict key appearing anywhere in the structure."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from walk_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_keys(item)


def score_payload(obj: Any) -> tuple[int, list[str]]:
    """Rate how likely a payload is to contain shot-level data.

    Each distinct vocabulary key counts once, so a huge leaderboard array does
    not outrank a compact shot feed just by repeating itself.
    """
    seen = {norm_key(k) for k in walk_keys(obj)}
    matched = sorted(k for k in seen if k in SHOT_KEY_WEIGHTS)
    return sum(SHOT_KEY_WEIGHTS[k] for k in matched), matched


def _is_ancestor(parent: str, child: str) -> bool:
    return child.startswith(parent + ".") or child.startswith(parent + "[")


def find_record_arrays(
    obj: Any, path: str = "$", context: dict[str, Any] | None = None
) -> Iterator[tuple[str, list[dict], dict[str, Any]]]:
    """Yield (json_path, rows, context) for every list-of-dicts with shot vocabulary.

    ``context`` carries scalar fields inherited from enclosing objects, so a
    nested Shots array still knows its player, round and hole.
    """
    context = context or {}
    if isinstance(obj, list):
        dicts = [item for item in obj if isinstance(item, dict)]
        if dicts:
            keys = {norm_key(k) for row in dicts for k in row}
            score = sum(SHOT_KEY_WEIGHTS[k] for k in keys if k in SHOT_KEY_WEIGHTS)
            if score >= MIN_ARRAY_SCORE:
                yield path, dicts, context
        for index, item in enumerate(obj):
            yield from find_record_arrays(item, f"{path}[{index}]", context)
    elif isinstance(obj, dict):
        # Scalars on this object describe everything nested beneath it.
        child_context = dict(context)
        child_context.update(
            {k: v for k, v in obj.items() if not isinstance(v, (dict, list))}
        )
        for key, value in obj.items():
            yield from find_record_arrays(value, f"{path}.{key}", child_context)


def flatten(obj: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten nested dicts to dotted keys; scalar lists become joined strings."""
    flat: dict[str, Any] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            flat.update(flatten(value, f"{prefix}.{key}" if prefix else str(key)))
    elif isinstance(obj, list):
        if all(not isinstance(item, (dict, list)) for item in obj):
            flat[prefix] = "|".join("" if v is None else str(v) for v in obj)
        else:
            for index, item in enumerate(obj):
                flat.update(flatten(item, f"{prefix}[{index}]"))
    else:
        flat[prefix] = obj
    return flat


def to_rows(payload: Any, keep_ancestors: bool = False) -> list[dict[str, Any]]:
    """Flatten the deepest shot arrays into tidy, context-carrying rows.

    A hole object and the Shots array inside it both match the vocabulary, so
    by default we keep only the leaf arrays -- otherwise every shot would be
    emitted twice, once inline on its hole row.
    """
    found = list(find_record_arrays(payload))
    if not keep_ancestors:
        paths = [path for path, _, _ in found]
        found = [
            entry for entry in found
            if not any(_is_ancestor(entry[0], other) for other in paths)
        ]

    rows: list[dict[str, Any]] = []
    for path, records, context in found:
        for index, record in enumerate(records):
            row: dict[str, Any] = {"_source_path": path, "_row_index": index}
            row.update(flatten(context))
            row.update(flatten(record))  # record fields win on collision
            rows.append(row)
    return rows
