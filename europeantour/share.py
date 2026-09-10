#!/usr/bin/env python3
"""Collect the interesting captured payloads into a folder that can be shared.

capture_api.py saves every response, most of which is site furniture. This
picks out the golf ones, small enough to commit, so they can be pushed to
GitHub for someone else to look at.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
KEEP_HOSTS = ("europeantour.com", "srarena.io", "imgarena.dev", "imgarena.com")
MAX_BYTES = 2_000_000


def main() -> int:
    manifest_path = HERE / "captured" / "manifest.json"
    if not manifest_path.exists():
        print("No captured/manifest.json -- run START HERE first.")
        input("\nPress Enter to close... ")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out = HERE / "to_send"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()

    index = []
    kept = skipped = 0
    for item in manifest:
        url = item.get("url", "")
        body = Path(item.get("body_file", ""))
        if not any(host in url for host in KEEP_HOSTS) or not body.exists():
            continue
        if body.stat().st_size > MAX_BYTES:
            index.append({"url": url, "note": f"skipped, {body.stat().st_size // 1024} KB"})
            skipped += 1
            continue
        shutil.copy2(body, out / body.name)
        index.append({"url": url, "score": item.get("score"), "file": body.name})
        kept += 1

    (out / "_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Collected {kept} payloads into the 'to_send' folder ({skipped} too big, listed only).")
    print("\nNow in GitHub Desktop: tick the changes, write anything in the summary box,")
    print("click Commit, then Push origin. Claude can read them from there.")
    input("\nPress Enter to close... ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
