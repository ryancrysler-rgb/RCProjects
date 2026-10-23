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

- **Paste the latest file.** `membership-page/teamch3-membership-circle.html` has all three academy photos, the head
  coaches (Mike Bolt, Joe Marshall, Ryan Crysler) and the range photo. Ryan still needs to paste it into
  Pages → TeamCH3 Preview → Custom HTML and Publish.
- **Open: "On the range" copy is still the mock-up.** That's "Cam Smith × Claude", the shot numbers, "Claude's cue"
  and the ticker's "NEW: CAM SMITH RANGE SESSION ON FORESIGHT". Is there a real session, or should it be retitled
  (e.g. "On the range at CH3 Dubai")?
- **Open: the TeamFLO and range photos are low resolution** (477 and 399 px wide). Ask for the originals.
- **Open: who is in the range photo?** The alt text is neutral for now.
- **Open: the Live Recordings card says "ALL TIERS"** and some feature cards say "PREMIER +". Relabel?
- **Open: photo rights.** The hero is an agency-style photo with a tour player, and the junior group photo needs
  parental consent for a public page.

## Later

- **Ask CH3:** re-upload `ask-ch3/Ask CH3 - TeamCH3 community guide.txt` to its knowledge.
- **Payments:** after the LLC, bank and Stripe are set up, paste Part 2 of the Circle AI brief (8 paywalls). Then make
  the checkout links and point the membership page buttons at them.
- **Before launch:** delete the test accounts: Test Junior, Test Junior Two, Test Adult, the old Test Parent (on
  rcrysler+…@floridian.cc), Ryan Junior (ryancrysler+junior1@gmail.com) and Test Parent (ryancrysler@gmail.com,
  formerly Ryan Tester).
- **Riverside Grow is a free trial**, ending about October 30 (Riverside's email of October 23). Wednesday's show
  is covered. Start paying for Grow before the trial ends to keep live streaming and custom destinations.
- **Junior Events:** tick "Hide attendees" on each new one.
- **When teamch3.com is live:** update the ch3.circle.so references and recheck the tester links.
