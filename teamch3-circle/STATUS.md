# TeamCH3 · where we left off

Updated October 23, 2026. The invite and sign-up flow works end to end, and the tester invites are ready to send.

## Fixed on October 23

- **Default onboarding access now grants nothing.** Circle's default onboarding access had included all 9 access
  groups, so every new member got Junior Basecamp, Parents and Elite on top of their own group. Circle AI removed
  them. Claude confirmed it: a silent test member got no groups, where before the fix all 9 were added within
  2 seconds. Only test accounts were ever affected.
- **Welcome emails have a sender.** They come from "TeamCH3" at rcrysler@email.circle.so, and replies go to
  rcrysler@floridian.cc. They had failed because Email Hub had no sender address.
- **Test accounts deleted.** Ryan Tester October and the silent test members are gone.
- **Re-test passed (memberships).** Ryan Crysler Tester 2 October (ryancrysler+test2@gmail.com, member 99557738)
  got only Premier · TeamFLO and the Beta tester tag, and its sidebar showed no junior spaces or other academies.
  The account has since been deleted.
- **Welcome email confirmed.** The welcome emails first failed for lack of a marketing footer mailing address. Ryan
  added 3700 SE Floridian Dr, Palm City, FL 34990. On re-test, "Welcome to TeamCH3 Premier" arrived in Ryan's
  Gmail (Updates tab) within a minute, word for word as in the brief.
- **How to re-test a welcome email.** Circle skips a workflow if the same member triggers it again within one hour
  ("Duplicate Skipped"), and every skipped re-add restarts the hour. So use a new member, or wait more than an hour
  since the last re-add. The Gmail connector can read mail sent to ryancrysler+…@gmail.com, but its search can lag
  20–30 minutes.
- **Sign-up fields reworked.** Date of birth is now three required dropdowns: Date of birth: day / month / year
  (ids 7123603, 7123604, 7123605). The year runs from 2013 back to "1964 or earlier", and each January needs a new
  year added. Home city is now Circle's platform location field (7040786, relabelled), which has place search and
  so corrects typos. It is required, and shown only at sign-up and in Edit profile. The old free-text Date of birth
  (7040793) and Home city (7064457) fields are archived.

## Next steps, in order

1. **Send the tester invites:** `onboarding/TeamCH3 - beta tester invite.txt`.
2. **Sidebar and form tidy-up.**
   - Done: Circle AI removed "Download the mobile app" from the checklist, and "Messages" is gone from Links.
   - Done: Premier Sessions is published, so "Premier + Elite → Join a space" should be gone. Premier members were
     already members of it through their access group, but it was a draft. It now has a "Start here" module with one
     published "Premier Sessions: coming soon" session (comments off). The Premier + Elite space group is now hidden
     from non-members.
   - Done: the "Course archive" and "Live recordings" sidebar links are deleted. The head snippet's same-window rule
     had been closing their ⋯ menus. v3.12 fixes that and is pasted into Circle.
   - To do: move the three Date of birth dropdowns to the top of the sign-up form, before Age group (Circle AI or by
     hand).
   - To do: re-upload the Ask CH3 guide, since its Premier Sessions line changed.
3. **Junior and parent tests passed (October 23).**
   - The junior **Ryan Junior** (ryancrysler+junior1@gmail.com, member 99568272) signed up through the TeamFLO
     junior link. They got only Junior Basecamp · TeamFLO and the Beta tester tag, and the date of birth dropdowns
     and the Home city location (Stuart, Florida) saved as real places. They landed in Junior Basecamp, and "Welcome
     to the Junior Basecamp" arrived (Gmail filed it in Promotions).
   - The old "Ryan Tester" Pod test account (ryancrysler@gmail.com, member 98567787) was repurposed as **Test
     Parent**: taken out of Pod Community, put in Parents, with Parent of set to Ryan Junior. Its spaces are only
     Parents, Junior Events and Community Rules. Ryan saw the Parents welcome email arrive.
   - The sign-up form order is now day, month, year, Age group, Parent's email, Home city.
4. **Son Of A Butch Live, Wed Oct 28, 12–2pm Eastern (16:00–18:00 UTC).** See the section below.
5. **Coaches and the academy rollout** (see section 8 of the sign-up doc).
   - Done: 3 coach access groups created with their spaces: Coaches · CH3 Dubai (167198), Coaches · CH3 Thailand
     (167199) and Coaches · TeamFLO (167200). The public "Coach" member tag (304513) is created.
   - Done (October 26): **Coaches' Basecamp** (space 2925010, ch3.circle.so/c/coaches) in a new hidden "Coaches"
     space group (1236243). It's in all 3 coach access groups, and Claude Harmon III and Ryan are members. Topics:
     Ask the team, Best practice, Drills and sessions, Juniors. Claude's welcome post with the ground rules is pinned
     (post 37784681). Head snippet v3.13 adds its CB code, COACHES button and header card.
   - Done: head snippet v3.13 is pasted into Circle.
   - Done (checked by Claude): 3 coach welcome workflows, all active. Each starts on its coach access group, sends
     Email F, then adds the Coach tag (304513). Ids: CH3 Dubai 34b24d10-80fc-4c0d-9161-429b3df39b94, CH3 Thailand
     78413f73-2dbc-4b5f-bc01-ff444489212c, TeamFLO 68d130a0-e4e1-4d04-84ed-dee13da7e98f. Circle AI again reported
     things done that weren't (Thailand was a draft with no tag step). Always check through the connector.
   - Tested (October 26): Claude invited one test coach per academy through the connector: Test Coach Dubai,
     Test Coach Thailand and Test Coach TeamFLO (ryancrysler+coach1/2/3@gmail.com, members 99802348, 99802357,
     99802358). Each got only their Coaches membership and its 11 spaces. Circle's invitation arrived within seconds.
     About a minute later, before anyone accepted, Email F arrived (word for word as in the brief) and the Coach
     tag was added. All of it landed in Gmail's Updates tab.
   - Coaches can be added by Ryan in Circle, or by Claude from a list of names, emails and academy. Either way the
     workflow sends Email F and adds the Coach tag. Moderators are set by hand in Circle (or by Circle AI).
   - Changed (October 27, Ryan's call): coaches see every academy and every coach is a moderator. Claude added
     CH3 Dubai, CH3 Thailand and TeamFLO to all 3 Coaches access groups (13 spaces each; Elite Basecamp stays out)
     and checked it on the test coaches. To do (Ryan → Circle AI, after the Dubai coaches are added, so one pass
     covers them all): paste Part 4 of the Circle AI brief. It makes
     every coach a space moderator of the 3 academies and Junior Basecamp, adds that to the coach workflows if
     Circle allows it, and updates Email F's first bullet. Then Claude checks the moderator flags and workflows.
   - Wave 1, CH3 Dubai: Ryan sends the 13 coaches' names and emails and marks the head coach (Mike Bolt). Claude
     invites them with Coaches · CH3 Dubai (the workflow adds the Coach tag), and each coach is made a moderator
     (Part 4, or by hand if Circle can't automate it). Then Mike sends the Junior · CH3 Dubai link to families, and
     Claude invites the parents afterwards.
   - Wave 2 is TeamFLO (coaches, then players). Wave 3 is CH3 Thailand (head coach Joe Marshall).

## Son Of A Butch Live (October 28)

- **The plan:** Riverside records and streams live to an unlisted YouTube video, and members watch it embedded in
  Circle. Circle Live can't take an RTMP feed from outside tools. Riverside webinars, which give an audience link,
  aren't on Ryan's Grow plan.
- **Riverside:** session "Son Of A Butch Live: Claude with Cam Smith and Ryan Crysler" in the Son Of A Butch Podcast
  studio (event id dee77114-0194-4b95-af2e-e9f3dbdcc48a). No guests invited yet. Invites email the guests straight
  away, so get Ryan's go-ahead and the emails first.
- **YouTube:** scheduled stream https://youtube.com/live/rMhYtMJGw3U.
- **Circle event:** in Live Recordings, id 37711750,
  https://ch3.circle.so/c/live-recordings/son-of-a-butch-live-cam-smith. Its location is "virtual" and links to the
  podcast post. The link shows only to members who RSVP, and reminders are on. The event description is still the
  generic original, which the connector can't edit.
- **Circle post:** "Live this Wednesday" in Son Of A Butch Podcast, id 37711755, with the YouTube player embedded and
  questions invited in the comments.
- **To do (Ryan):**
  - fix the YouTube description, which says "Live look-in to a tour player lesson";
  - confirm the stream is Unlisted;
  - connect YouTube in the Riverside Live stream panel, select this broadcast, and do a test stream;
  - send Claude and Cam's emails for the Riverside guest invites.
- **Afterwards:** the same YouTube video is the replay. Optionally add it to Live Recordings, or swap in the edited
  episode later.

## What's in place

No swing videos (Oct 28). For now the coaches take questions, round reports and playing stats, not swing videos:
TeamCH3 coaches how players play the game. The membership page (step 03 and the FAQ, now "What do I need to bring?")
and the Ask CH3 guide say so, and the coaches help players who don't track rounds get set up. To do (Ryan): paste
the new page, re-upload the Ask CH3 guide, and paste Part 6 of the Circle AI brief (the Premier emails' step 2).
Part 4's coach email text was updated too, so paste the current version when the coaches are added.

Welcome workflows. Circle AI built these from `onboarding/TeamCH3 - Circle AI build brief.txt`, and Claude checked
each one through the connector. All are on. Each has the trigger "added to access group" and one Send email action,
with no filter or delay.

| Workflow | Access group (id) | Workflow id |
|---|---|---|
| Welcome · Pod Community | Pod Community (163806) | 282b6e92-d969-40d7-bb00-f931c33eaaf9 |
| Welcome · Junior Basecamp · CH3 Dubai | 164397 | 5f1a608a-9851-4a4c-ab05-41342281c131 |
| Welcome · Junior Basecamp · CH3 Thailand | 164398 | 29009c6e-2c02-4415-8700-f990c76c46b8 |
| Welcome · Junior Basecamp · TeamFLO | 164399 | 02ff927a-1ee0-46f0-bec4-c6cb0d518779 |
| Welcome · Premier · CH3 Dubai | 164400 | 4e2638b2-d879-42fb-9364-85cde0e5afb1 |
| Welcome · Premier · CH3 Thailand | 164401 | 389077d5-f945-48d5-be9b-8772d7b0c8ae |
| Welcome · Premier · TeamFLO | 164402 | d7618f61-a631-43a5-9320-0027150e5ef8 |
| Welcome · Elite | Elite (163809) | 7b3e9e93-4405-480f-bba9-c5976dfe6796 |
| Welcome · Parents | Parents (163974) | 22e5bce6-dffd-41cc-b988-3a09050df0db |

- **Circle AI over-reports.** It said all 9 were built and on when one was missing and one was a draft. Always check
  through the connector, not its summary.
- **The connector can't read the email text.** Each email is a broadcast, which the connector can't open. Check the
  wording from the received email instead.
- **The 16 old workflows** ("Academy · …", "Cleanup · …", "Elite Basecamp", "Podcast basecamp", "Junior Basecamp")
  are off. Leave them.
- **Ryan's admin account** (97652537) has been in Premier · TeamFLO since 21:21 UTC on October 22, from opening the
  tester link while signed in. It's harmless. Leave it: removing it could take spaces away from the admin account.

## Membership page

- **Member badges and Elite (October 28).** Public badges: Coach (304513, orange), Elite (305717, navy), Junior (305721,
  light orange), Son of a Butch (305723, dark, for Pod Community members) and one per academy: CH3 Dubai (305718), CH3 Thailand (305719), TeamFLO (305720). No Premier or Pod badge
  (Ryan's call). Tagged so far: Ryan (TeamFLO), Ryan Junior (Junior, TeamFLO), the test coaches (their academy). To do
  Done (checked by Claude, Oct 28): all 11 welcome workflows add their badges after the email (Junior + academy,
  Premier academy, Coaches Coach + academy, Elite, Pod Son of a Butch). Email D's new line can't be read through the
  connector: check it on the first Elite welcome.
  Elite is now defined as: application only; private coaching with Claude and Ryan; the Elite Basecamp for exclusive
  conferences with the 8 members; RC Greenlight Data Services; plus Son of a Butch and the home academy basecamp. The
  page, FAQ and Ask CH3 guide say so.
- **Sales and SEO pass (October 28, Ryan: "do everything you recommend", paywalls not possible yet, mock data stays).**
  - Beta sign-up: 12 "REQUEST AN INVITE" buttons and 2 "APPLY FOR ELITE", each opening a pre-filled email to
    rcrysler@floridian.cc (the membership is in the subject). One switch (BETA in build_paste.py) flips them to
    "START 2 WEEKS FREE" and the checkout links at launch. A Circle form can replace the email: send Claude its link.
  - Countdowns run off the real Circle calendar (EVENTS in build_paste.py): Son of a Butch Live today, the three
    Basecamp Spotlights and the Junior night; "LIVE NOW" during a session; "new dates soon" after Nov 19. Refresh
    EVENTS before each paste.
  - New order: hero → coaches strip (Claude, Mike Bolt, Joe Marshall, Ryan) → How it works (3 steps) → What's Inside →
    On the range → academies → feed → Son of a Butch → pricing → FAQ (8 questions) → final call to action. Nav and
    footer match, with an FAQ link.
  - Pricing: three cards (Pod, Premier "most popular", Elite) with annual prices, a Junior Basecamp bar under them,
    Elite "Limited to 8 members" and "8 seats in total". Beta copy says membership is by invitation for now.
  - SEO: the H1 now carries "Online golf coaching from Claude Harmon III and the CH3 academies in Dubai, Thailand and
    Florida"; Organization + FAQ structured data; a 1200x630 share image (Circle file 80hq8wshxgnbb7izhorxgb9ynu37).
  - To do (Ryan): paste the page and Publish; set the page settings from "TeamCH3 page settings - SEO.txt" (rename
    from "TeamCH3 Preview", SEO title, description, share image); send Claude's and the coaches' credentials and
    headshots for the coaches strip, and testimonials when there are some.
- **Fixed (October 28): "Hello, world!" text under the footer.** It comes from Circle code boxes saved with Circle's sample code
  (not from our files). Delete them in Site → Code snippets and check the page's own custom code settings.
- **Signed-out landing page (October 27).** Claude set Circle's logged-out landing page to the website page
  "TeamCH3 Preview" (page 76685, ch3.circle.so/settings/pages/edit/76685) through the connector. The community
  stays private. Members still land in the Global Basecamp after signing in. The page's LOG IN links go to
  ch3.circle.so/sign_in. Check it in a private window after each paste and Publish. Ryan checked it in incognito:
  the page loads and the top navigation jumps to each section.
- **Hero photo: CH3 cap (October 27).** Claude's cap in the top photo now carries the CH3 mark where the "P" was,
  tilted to the seam and blended in, and the white logo on the side of the cap is removed. Circle file
  d85q2vrd3kilwhzo17w9x39764zx, kept on the draft images post. `brand/Claude range-side (CH3 cap).jpg` is the edit;
  `brand/Claude range-side.jpg` is the untouched original. Paste the latest membership page file to put it live.
- **Hero line and basecamp box (October 27).** Hero: "Play better golf with Claude and the CH3 coaches from Dubai, Thailand
  and TeamFLO, wherever you live. Then go live with Claude: Son of a Butch recordings and his updates from tour. One
  membership." The "There's a basecamp near you" box now spans the full width under the Junior banner, with
  the same rounded corners and type sizes as the academy cards (it was squeezed into one column).
- **What's Inside, reordered (October 27, Ryan's brief).** First the golf, for Junior, Premier and Elite: 01 Live
  webinars (inside the coaches' minds, for Premier members at every academy and the Junior Basecamp), 02 Premier
  Sessions (lessons from every academy), 03 Basecamp Spotlights (a day inside each academy: practice schedule,
  coaching insights, the experience). Then the cherry on top, for every membership: 04 Live with Claude (the live
  podcast recordings), 05 On tour with Claude (his tour updates, posted in the Global Basecamp). Tier rows now read
  "Global feed + Claude's tour updates" (all) and "Basecamp Spotlights" (not Pod). The Ask CH3 guide's Events
  entry matches: re-upload it to Ask CH3's knowledge.
- **No "Coaches' Room" for members (October 27).** The coaches' own space (the Coaches' Basecamp) stays coaches-only,
  so the page no longer sells it. Card 05 is now Basecamp Spotlights (Claude and each academy's head coach, live, in
  Events), and the tier row reads "On tour with Claude + Basecamp Spotlights" (Junior, Premier, Elite; not Pod).
- **Free trial is 2 weeks (October 27, Ryan's call), not 4.** The page now says "2 weeks free" and "cancel before day
  14" everywhere, and Part 2 of the Circle AI brief (the paywalls, not built yet) asks for a 14-day trial, still none
  for Elite.
- **No course archive (October 27).** The page no longer promises a course archive: the hero line is gone, the
  What's Inside card 02 is now Premier Sessions ("opening soon"), the tier row reads "Live webinars + Premier
  Sessions" and the footer link is Premier Sessions.
- **"Inside TeamCH3" screenshot replaced (October 27).** The old Global Basecamp screenshot (old GP/JP/P1 codes,
  past events) is now Ryan's screenshot of a Premier · CH3 Dubai test member's Feed: GLOBAL, CH3 DUBAI and SON OF A
  BUTCH buttons and the current events. Circle file 3hy9hkputoabzbwq6hcweyd3sw24 (on the draft images post); the frame's
  address now reads ch3.circle.so/feed. Retake it when the feed changes a lot, from a member account, not an admin's.
- **Done: head snippet v3.14 is pasted** (Ryan, October 27). v3.13 showed the basecamp buttons (GB, DU, TH, FL, SB, EB) above
  the membership page for signed-out visitors. v3.14 hides them on that page and leaves members' pages unchanged
  (tested in a browser against v3.13).
- **Paste the latest file.** `membership-page/teamch3-membership-circle.html` has all three academy photos, the head
  coaches (Mike Bolt, Joe Marshall, Ryan Crysler) and, since October 27, the "CH3NologoCoaching" photo from Drive in
  the "On the range" panel (Claude on the putting green; Circle file 7j18iax3nfe4yh5w5pa6k9qt4n59, kept on the
  draft images post). Ryan still needs to paste it into Pages → TeamCH3 Preview → Custom HTML and Publish.
- **Open: "On the range" copy is still the mock-up.** That's "Cam Smith × Claude", the shot numbers, "Claude's cue"
  and the ticker's "NEW: CAM SMITH RANGE SESSION ON FORESIGHT". Is there a real session, or should it be retitled
  (e.g. "On the range at CH3 Dubai")?
- **Open: the TeamFLO photo is low resolution** (477 px wide). Ask for the original.
- **Done: card tags (October 27).** The What's Inside cards for live webinars, Premier Sessions, On tour with Claude
  and Basecamp Spotlights are tagged "JUNIOR · PREMIER · ELITE" (was "PREMIER +"), on their own line above the number.
  Live recordings stays "ALL TIERS", which is true: every membership, Pod included, has it.
- **Open: photo rights.** The hero is an agency-style photo with a tour player, and the junior group photo needs
  parental consent for a public page.

## Later

- **Ask CH3:** re-upload `ask-ch3/Ask CH3 - TeamCH3 community guide.txt` to its knowledge.
- **Payments:** after the LLC, bank and Stripe are set up, paste Part 2 of the Circle AI brief (8 paywalls, 14-day trial). Then make
  the checkout links and point the membership page buttons at them.
- **Before launch:** delete the test accounts: Test Junior, Test Junior Two, Test Adult, the old Test Parent (on
  rcrysler+…@floridian.cc), Ryan Junior (ryancrysler+junior1@gmail.com), Test Parent (ryancrysler@gmail.com,
  formerly Ryan Tester) and the three test coaches (ryancrysler+coach1/2/3@gmail.com).
- **Riverside Grow is a free trial**, ending about October 30 (Riverside's email of October 23). Wednesday's show
  is covered. Start paying for Grow before the trial ends to keep live streaming and custom destinations.
- **Junior Events:** tick "Hide attendees" on each new one.
- **When teamch3.com is live:** update the ch3.circle.so references and recheck the tester links.
