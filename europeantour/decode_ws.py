#!/usr/bin/env python3
"""Decode captured websocket frames into shot data, without a browser.

The Event Centre streams Snappy-compressed UTF-16LE JSON. Frames are stored
whole, so a capture can be re-decoded any number of times as the parsing
improves -- no need to click through eighteen holes again.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import find_shots
import shotjson
import snappy_lite

HERE = Path(__file__).parent


def decode_entry(entry: dict) -> Any:
    """Recover one frame's JSON, whether it was stored as text or bytes."""
    if entry.get("text"):
        try:
            return json.loads(entry["text"])
        except Exception:
            pass
    blob = entry.get("base64") or entry.get("head_hex")
    if not blob:
        return None
    raw = base64.b64decode(blob) if entry.get("base64") else bytes.fromhex(blob)
    text = snappy_lite.decode_text(raw, partial=True)
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        # A truncated frame leaves invalid JSON; the prefix is still useful.
        return {"_partial_text": text}


def main() -> int:
    logs = sorted((HERE / "captured").glob("run_*/_ws_frames.jsonl"))
    if not logs:
        print("No websocket captures found. Run GET SHOT BY SHOT first.")
        input("\nPress Enter to close... ")
        return 1

    frames, operations = [], {}
    for log in logs:
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                entry = json.loads(line)
            except Exception:
                continue
            payload = decode_entry(entry)
            if payload is None:
                continue
            if entry.get("direction") == "sent" and payload.get("type") == "start":
                operations[str(payload.get("id"))] = payload.get("operationName", "?")
            frames.append((entry.get("operation"), payload))

    # Label received frames by the subscription they answer.
    labelled = []
    for operation, payload in frames:
        if not operation and isinstance(payload, dict):
            operation = operations.get(str(payload.get("id")))
        labelled.append((operation or "unknown", payload))

    print(f"Decoded {len(labelled)} frames from {len(logs)} capture(s).\n")
    counts: dict[str, int] = {}
    for operation, _ in labelled:
        counts[operation] = counts.get(operation, 0) + 1
    for operation, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {count:4d}x  {operation}")

    shotjson.MIN_ARRAY_SCORE = 2
    rows, seen = [], set()
    for operation, payload in labelled:
        for path, records, context_fields in shotjson.find_record_arrays(payload):
            shot_score, _ = find_shots.assess(records)
            text_score, _ = find_shots.assess_commentary(records)
            if not (shot_score or text_score):
                continue
            for record in records:
                row = {"_operation": operation,
                       **shotjson.flatten(context_fields), **shotjson.flatten(record)}
                fingerprint = json.dumps(row, sort_keys=True, default=str)
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                rows.append(row)

    if not rows:
        print("\nNo shot records in the decoded frames.")
        input("\nPress Enter to close... ")
        return 1

    find_shots.write_csv(rows, HERE / "SHOT_BY_SHOT.csv")
    print(f"\n{len(rows)} rows -> SHOT_BY_SHOT.csv")
    input("\nPress Enter to close... ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
