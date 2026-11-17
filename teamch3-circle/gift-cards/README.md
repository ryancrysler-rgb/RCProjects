# TeamCH3 gift card template

One-page gift card, 8.5 x 11, TeamCH3 navy and orange, with the CH3 mark and the Floridian logo.

- `gift-card-template.html` is the template. Edit the text in it: the gift ("One 90-minute lesson"), the coach,
  the location line, the four fill-in labels and the booking note.
- `render.js` makes the PDF: `node render.js "Name of the card.pdf"` (run in this folder; needs Playwright).
  It prints `overflow 0` when everything fits on the page.
- Fonts (Anton, Barlow Condensed) and both logos are in this folder, so it renders without downloads.
- `Claude Harmon III Gift Card - 90 minute lesson.pdf` is the first card made from it (Nov 17, 2026).

Options not on the first card: booking phone or email, expiry date, dollar value, a printed recipient name,
and a white-background version for office printers.
