# TeamCH3 · Circle head snippet

`circle-head-snippet-v3.html` is the code pasted into Circle at **Site › Code snippets › head** for
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
"TeamCH3 Circle - copy-paste list.txt".
