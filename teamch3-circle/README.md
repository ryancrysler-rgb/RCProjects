# TeamCH3 · Circle head snippet

`circle-head-snippet-v3.html` (v3.2) is the code pasted into Circle at **Site › Code snippets › head** for
ch3.circle.so. It applies the TeamCH3 brand kit (navy + orange, Anton + Barlow Condensed) to Circle's web
app and adds the basecamp pills, basecamp header cards, sidebar codes, FEATURED bars, quote cards, the
row under "Start a post" and the community-rules pop-up before a member's first post.

- Web and desktop only; the Circle mobile app ignores code snippets.
- Hooks are Circle's own `data-circle` attributes and CSS variables, read from the live feed on
  Oct 12 2026. If a Circle update breaks part of the look, turn the snippet off in the same screen.
- Basecamp ids, pill labels and header copy live in the `BASECAMPS` array at the top of the script.
- `GREENLIGHT_URL` is empty on purpose: "Send your golf data to RC Greenlight" shows as a label until
  an address is set.

The running list of things to paste or click in Circle admin is in Google Drive:
"TeamCH3 Circle - copy-paste list v2.txt". Membership is one access group per basecamp and tier
(chosen at checkout), so no Circle automations handle access.

## Membership page (Circle website builder)

`membership-page/teamch3-membership-circle.html` is the TeamCH3 membership site as one paste-ready block for a
custom HTML section in Circle's website builder. It is plain HTML and CSS scoped under `#ch3-site`, plus an
optional script for the clocks, the countdowns and the range-session player; everything else works without it.

- Built from the design file "TeamCH3_Membership_Site_1.html" (`design-template.html` is its page template)
  by `build_paste.py`: `python3 -I build_paste.py design-template.html teamch3-membership-circle.html`.
- Copy changes from the design (pricing, nearest-basecamp grouping, the real Global Basecamp view) are in the
  `EDITS` list and the data block at the top of `build_paste.py`.
- Images are hosted on Circle (assets-v2.circle.so) and attached to the Global Basecamp draft post
  "Membership page images (keep as a draft)" so Circle keeps them.
- Buttons marked `data-checkout="pod|junior|premier|elite"` point to `#tiers` until the paywalls exist.

## Ask CH3 (Circle AI agent)

`ask-ch3/` turns Circle's "Ask a Coach" AI agent into Ask CH3, a member-facing AI coach trained on the
Son of a Butch transcripts and Claude Harmon III's coaching PDFs. Circle has no API for AI agents, so the setup
is done by hand in Circle admin.

- `Ask CH3 - Circle AI agent setup.txt`: name, instructions (under Circle's ~1,500-character box), knowledge
  sources, audience, touchpoints, Pause AI keywords and a test list.
- `Ask CH3 - voice and coaching guide.txt`: uploaded to the agent's knowledge. It carries the coaching style and
  rules that don't fit in the instructions box. Built from the CH3 Lesson Playbook.
- `Ask CH3 avatar.png`: the agent's avatar.
- The transcripts come from the Colab notebook "Sonofabutchtranscriptharness.ipynb" (Whisper `base.en`), one
  .txt per episode in the Drive folder "Son of a Butch Podcast Transcripts". Episodes with Ryan Crysler are skipped.
