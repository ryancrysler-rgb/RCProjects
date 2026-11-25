"""Australian PGA 2027100: the leaderboard + every scorecard, read through the site's own pages in Chromium.
usage: pull.py OUTDIR [all|finished]   (finished = only players through 18 in the current round, plus Cam Smith)"""
import sys, json, time, os
sys.path.insert(0, '/home/user/RCProjects/europeantour')
from playwright.sync_api import sync_playwright
import auto_capture as ac
EV = "2027100"; URL = "https://www.europeantour.com/dpworld-tour/bmw-australian-pga-championship-2027/leaderboard"
out = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else "finished"
os.makedirs(out, exist_ok=True)
with sync_playwright() as pw:
    b = ac.launch(pw, True); c = ac.new_context(b); p = c.new_page()
    p.goto(URL, wait_until="domcontentloaded", timeout=60000); p.wait_for_timeout(6000)
    get = lambda path: p.evaluate("u => fetch(u, {headers:{Accept:'application/json'}}).then(r => r.ok ? r.json() : null)", path)
    lb = get(f"/api/sportdata/Leaderboard/Strokeplay/{EV}/type/load")
    json.dump(lb, open(f"{out}/leaderboard.json", "w"))
    # the Par row, as the site prints it on an opened scorecard
    try:
        p.get_by_text("SMITH, Cam").first.click(timeout=15000); p.wait_for_timeout(4000)
        t = " ".join(p.inner_text("body").split()); i = t.find("Par ", t.find("Cam SMITH"))
        json.dump({"text": t[i:i+120]}, open(f"{out}/par_row.json", "w"))
    except Exception as e:
        json.dump({"error": str(e)[:200]}, open(f"{out}/par_row.json", "w"))
    cards = {}
    for pl in lb["Players"]:
        name = f"{pl.get('LastName','')}, {pl.get('FirstName','')}"
        done = pl.get("HolesPlayed") == 18 or bool(pl.get("IsFinished"))
        if mode == "finished" and not done and "SMITH" not in name.upper(): continue
        cards[pl["PlayerId"]] = get(f"/api/sportdata/Scorecard/Strokeplay/Event/{EV}/Player/{pl['PlayerId']}")
        time.sleep(0.3)
    json.dump(cards, open(f"{out}/scorecards.json", "w"))
    print(len(lb["Players"]), "players;", len(cards), "scorecards")
    b.close()
