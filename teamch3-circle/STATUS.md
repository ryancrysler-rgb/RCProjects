# TeamCH3 · where we left off

Updated October 23, 2026. The invite and sign-up flow is waiting on one last test sign-up.

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
  Its welcome email wasn't confirmed yet: Gmail's search was behind.
- **Sign-up fields reworked.** Date of birth is now three required dropdowns: Date of birth: day / month / year
  (ids 7123603, 7123604, 7123605). The year runs from 2013 back to "1964 or earlier", and each January needs a new
  year added. Home city is now Circle's platform location field (7040786, relabelled), which has place search and
  so corrects typos. It is required, and shown only at sign-up and in Edit profile. The old free-text Date of birth
  (7040793) and Home city (7064457) fields are archived.

## Next steps, in order

1. **Confirm the welcome email.** "Welcome to TeamCH3 Premier" should be in Ryan's Gmail, sent to
   ryancrysler+test2@gmail.com. Check the wording.
2. **Sidebar and form tidy-up.**
   - Done: Circle AI removed "Download the mobile app" from the checklist, and "Messages" is gone from Links.
   - Done: Premier Sessions is published, so "Premier + Elite → Join a space" should be gone. Premier members were
     already members of it through their access group, but it was a draft. It now has a "Start here" module with one
     published "Premier Sessions: coming soon" session (comments off). The Premier + Elite space group is now hidden
     from non-members.
   - To do: Ryan checks where the "Course archive" and "Live recordings" sidebar links point, and probably deletes
     both.
   - To do: move the three Date of birth dropdowns to the top of the sign-up form, before Age group (Circle AI or by
     hand).
   - To do: re-upload the Ask CH3 guide, since its Premier Sessions line changed.
3. **Optional junior test** with ryancrysler+junior1@gmail.com through the TeamFLO junior link. Use it to check the
   new date and city fields.
4. **Delete the test account** Ryan Crysler Tester 2 October.
5. **Send the tester invites:** `onboarding/TeamCH3 - beta tester invite.txt`. Remove its ON HOLD line first.

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
