# TeamCH3 · where we left off

Paused October 22, 2026, in the middle of testing the invite and sign-up flow.

## Blocker: don't send tester links or invite anyone yet

- **Every new member gets all 9 memberships.** Circle's default onboarding access includes every access group, so
  adults are added to Junior Basecamp, Parents and Elite on top of the group their link or invite gives. Circle AI
  confirmed the cause from Ryan Tester October's access history ("granted by Onboarding"). It started after 17:01 UTC
  on October 22. Only test accounts were affected.
- **Welcome emails fail.** All 9 welcome workflows ran, but every Send email failed because TeamCH3 has no sender
  address in Circle's Email Hub.

## Next steps, in order

1. **Ryan → Circle AI:** "Go ahead with step 1: remove all 9 access groups from the default onboarding access so it
   grants none. Change nothing else." The default should grant nothing: links, admin invites and (later) checkouts
   set each member's one membership. Not even Pod Community, which is paid.
2. **Ryan picks the sender** and tells Circle AI. Recommended: name "TeamCH3", address rcrysler@floridian.cc for the
   beta (already the reply-to), then a teamch3.com address once the domain is live. Click Circle's confirmation email
   if it sends one.
3. **Claude checks step 1:** create a silent test member (skip invitation), confirm it gets no access groups within a
   few seconds, then delete it.
4. **Claude deletes Ryan Tester October** (member 99531943, ryancrysler+test1@gmail.com).
5. **Ryan re-tests** in a private window (not signed in as admin), with ryancrysler+test2@gmail.com, through the
   "Beta testers · Premier · TeamFLO" link. Claude checks: only Premier · TeamFLO, the Beta tester tag, lands in the
   TeamFLO space, and "Welcome to TeamCH3 Premier" arrives in Ryan's Gmail (the Gmail connector can read it).
6. Then send the tester invites: `onboarding/TeamCH3 - beta tester invite.txt`.

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
- **Before launch:** delete the test accounts: Test Junior, Test Junior Two, Test Adult, Test Parent, Ryan Tester,
  and Ryan Tester October if still there.
- **Junior Events:** tick "Hide attendees" on each new one.
- **When teamch3.com is live:** update the ch3.circle.so references and recheck the tester links.
