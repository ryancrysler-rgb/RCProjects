# TeamCH3 TeamFLO games and drills: the content, rebranded from the TeamFLO "Golf Blueprint" sheets in Google Drive.
MANO = "In match play it's mano y mano, and you will learn so much more about yourself and the person you are competing against."
FLAGS = ("Flags", "White flags down. Green flags back.")
EW_TEES = ("Tees", "Furthest east and west side possible, without disrupting play.")
SAND = "Sand your divots."
STRESS = "We are adding stress and an elevated heart rate to your practice and decision-making."
HEART = "Putting with an elevated heart rate happens all the time in tournaments. Let's make it normal."
DEPOT = "The depot is a great place to balance technique and skill with the stated objective."
SAVE = "Driving and saving shots around the green under stress in practice isn't normal. Make it normal."
DONE = "We are done with doubles."
TS_ADVICE6 = "Playing well despite swinging poorly is a skill."

C = {}
def card(key, eyebrow, title, sub=None, body=(), advice=None, boxes=(), img=None, meta=None, note=None):
    C[key] = dict(eyebrow=eyebrow, title=title, sub=sub, body=list(body), advice=advice, boxes=list(boxes), img=img, meta=meta, note=note)

# ---- Harmon matches
card('hm-a', 'Harmon Match · "A" Day', '1 Up & 1 Down', None,
     ["With another player, play a singles or standard team match. Once on the green, the winner picks the hardest up and down, and the closest to the pin picks up an extra half point. If the hole is tied, decide as a group where to chip."],
     MANO, [FLAGS, ("Tees", "Tee markers.")], note=SAND)
card('hm-a-team', 'Harmon Match · "A" Day', '1 Up & 1 Down', None,
     ["Against your teammates or coaches, play a singles or standard team match. Once on the green, the winner picks the hardest up and down from the short side, and the closest to the pin picks up an extra half point."],
     MANO, [FLAGS, ("Tees", "Tee markers.")])
card('hm-b', 'Harmon Match · "B" Day', 'Cuts Galore', None,
     ["Against another player, play a singles or standard team match. Depending on pace of play, play two shots: one from the east side and one from the west. Each shot that cuts earns an extra half point. Double-crosses are minus a half point."],
     MANO, [FLAGS, EW_TEES], note=SAND)
card('hm-c-team', 'Harmon Match · "C" Day', 'Cuts Galore', None,
     ["Against your teammates or coaches, play a singles or standard team match. Depending on pace of play, play two shots: one from the east side tees and one from the west. Each shot that cuts earns an extra half point."],
     MANO, [FLAGS, EW_TEES])
card('hm-fade', 'Harmon Match · "B" Day', 'Fade Masterson', None,
     ["Against another player, play a singles or standard team match. Depending on pace of play, play two shots: one from the east side and one from the west. Each shot that fades earns an extra half point. Double-crosses are minus a half point."],
     MANO, [FLAGS, EW_TEES], note=SAND)
card('hm-c', 'Harmon Match · "C" Day', 'Halfsies', None,
     ["Against another player, play a singles or standard team match. Depending on pace of play, play each hole from about half its posted distance, or from the other side of the rough or water. Every hole is a par 2."],
     MANO, [FLAGS, EW_TEES], note=SAND)
card('hm-d', 'Harmon Match · "D" Day', 'Back It Up One Less', None,
     ["Against another player, from the very back of each tee, take one less club than normal and flight your shot. A properly executed shot earns a half point on top of the result of the hole."],
     None, [FLAGS, ("Tees", "As far back as the tee markers allow.")], note=SAND)
card('hm-d-team', 'Harmon Match · "A" Day', 'Back It Up One Less Flighter', None,
     ["In a match play format with your teammates or coaches, from the very back of each tee, take one less club than normal and flight your tee shot. A properly executed shot earns a half point on top of the result of the hole."],
     "Having \"stock\" feels lets you build a base to work from. The best wedge players in the world control their trajectory and spin.",
     [FLAGS, ("Tees", "As far back as the tee markers allow.")])
card('hm-e', 'Harmon Match · "Evil" Day', 'One Ball Egg Carry', None,
     ["You have one ball for the day. The first match is on The Harmon. Decide the game. Go!"],
     None, [FLAGS, ("Tees", "The match decides.")], note=SAND)
card('hm-f', 'Harmon Match · "F" Day', 'Draw Masterson', None,
     ["Against another player, play a singles or standard team match. Depending on pace of play, play two shots: one from the east side and one from the west. Each shot that draws earns an extra half point. Blocks or fades are minus a half point."],
     MANO, [FLAGS, EW_TEES], note=SAND)
card('hm-63', 'Harmon Match', 'Race to 63', None,
     ["With one ball in the bag, the goal is to play seven straight rounds without losing your ball. The group decides the match."],
     "We are playing seven rounds to walk about 7,700 yards on The Harmon.",
     [FLAGS, ("Tees", "Try to create seven different tee shots for each hole. Be creative!")], note=SAND)
card('hilo', 'Harmon Match', 'HI-LO', 'Going high. Going low.',
     ["With another player, play a singles or standard team match. From the tee, hit a high shot and a significantly lower shot. Failing to hit the called shot correctly is a half-stroke penalty."],
     "The challenge is to fit shots onto the green that don't match your instincts, especially when the wind adds to the difficulty.",
     [FLAGS, ("Tees", "The group decides.")], note=SAND)
card('rights-lefts', 'Harmon Match', 'Rights and Lefts', None,
     ["Once the teams are decided, throw a tee to determine which side of the green your team must favor, right or left, regardless of the pin location. Lose half a shot for finishing on the wrong side of the green."],
     "Hitting to specific targets that aren't the pin is one way to swing aggressively at conservative targets.", [])
card('intentional-miss', 'Harmon Match', 'Intentional Miss', None,
     ["On either the Harmon loop or the short course, decide the match. From there, any shot that hits the green in regulation is a one-stroke penalty. You must miss the green on purpose."],
     "This is a great game of chess and helps you focus on where to put the ball.", [])
card('harmon-rules', 'The Harmon', 'Harmon Course Rules', None,
     ["Play with another player.", "Walk.", "Repair pitch marks.", "Find a weed and tee it up.", "Sand Patrol Thursdays."],
     None, [FLAGS, ("Tees", "The match decides.")], note=SAND)
card('survivor', 'Course Game', 'Survivor', 'Win or go home.',
     ["On either course, set your teams. A bogey knocks you out of the match. But if you make a birdie before a bogey, you get an extra life.",
      "Make a double or worse and you walk in.",
      "When you're back at the practice tee, you serve 10 minutes of Ping Pong Purgatory, followed by an up-and-down match against the next player who walks in."],
     "Protect the ball!", [("Timer", "None, unless you're in the Ping Pong penalty box.")])

# ---- Putting
card('good-zones', 'Putting Studio · Middle Tier', 'The Good Zones', None,
     ["By yourself or against another player, take five balls and try to form a perfect line inside the good zone, using the dotted-line putting zones. You may need to roll the lines to take out the slope."],
     MANO, [], img='goodzones.png')
card('beehives', 'Putting Studio · Top Tier to Bottom Tier', 'Beehives', None,
     ["Against another player, take the same number of putts from a spot on the top tier to the beehives below. The center hive with the Titleist hoop is worth 500."],
     MANO, [], img='beehives.png')
card('all22', 'Putting Studio · Top Tier', 'All-22', None,
     ["There are 22 starting dots on the top tier, running east to west. Place a ball on each starting dot and record how many you make."],
     "The putting studio roller smooths out the surface. Roll it for a couple of minutes if you want precise feedback.",
     [("Record", "16 / 22"), ("PGA Tour make rate", "3 ft: 99.4%\n6 ft: 70.2%\n10 ft: 41.3%\n11-15 ft: 30%")], img='all22.png')
card('putting-100', 'Putting', 'The Putting 100', None,
     ["At the specially marked hole, hit 100 putts, one foot at a time. The goal is to get through the drill in 35 minutes without a three-putt. Three-putt and you start over."],
     "Time plays an interesting role in putting. Does faster help or hurt? We'll find out.", [("Timer", "35 minutes.")])
card('putting-50x2', 'Putting', 'Putting 50x2', 'Start big or start small.',
     ["Like the Putting 100, this mind test has two 50-foot ladders: one starts 50 feet away and the other starts one foot away. Work every foot toward 50 feet or toward one foot without a three-putt. Three-putt and you start over."],
     "Hopefully this makes you allergic to three-putts!", [("Timer", "None.")])
card('putting-50', 'Putting', 'Putting 50', 'Start big or start small.',
     ["Like the Putting 100, this mind test is a 50-foot ladder. Start at 50 feet or at one foot, and work every foot toward the other end without a three-putt. Three-putt and you start over."],
     "Hopefully this makes you allergic to three-putts!", [("Timer", "None.")])
card('b-putting', '"B" Day', 'Putting', 'Tee Ball, Fax Machine, 6 + 12',
     ["Tee Ball: put one tee in the ground. Walk two paces and put down another tee, then two more paces and another. Drop two balls at the two-pace tee. You have two chances to hit the first tee. If you do, move to the four-pace tee. If you don't, restart until you hit both tees within two tries.",
      "Fax Machine: one of the best putting tips I ever received was don't use a putter. Roll putts hitting the belly of the ball with your pitching wedge. It keeps you athletic and reactive.",
      "6 + 12: just like Tee Ball, but now you're putting to a cup, and it looks huge. Same game. Roll it confidently."],
     "Technical putting is important, but speed control and start line are the foundations of being a world-class putter!",
     [("Timer", "Tee Ball: 6 minutes.\nFax Machine: none.\n6 + 12: 6 minutes.")])

# ---- Short game
card('trail-mix', 'Short Game Warm-Up', '9 Iron Trail Mix', None,
     ["Take 20 practice balls and throw them around a chipping area. Playing each ball as it lies, use your 9 iron to solve each shot. Choose a different target for every shot."],
     "A great drill to warm up your creative short game and technique. Use the design of the 9 iron to challenge your creative instincts.",
     [("Scoring", "Count how many shots finish inside 8 feet.")])
card('sg-100', 'Short Game', 'The Short Game 100', 'Two Butch B buckets and the microphone.',
     ["Around the short game green, take a full bucket (about 50 balls) and hit 100 different chips. Count the makes.",
      "Then move to the wedge stones and hit two buckets, to a different stone every time. Count the hits."],
     "Putting the emphasis on makes within a set number takes the technique away and puts the focus on the shot. Let the tension build. Execute.",
     [("Timer", "None.")])
card('bunker-course', 'Short Game', 'The Bunker Course', 'Welcome to the beach.',
     ["Starting on the first hole, create a good lie in a bunker and play through each hole. Make these nine shots as challenging as you like. No two bunker shots will be the same! Par is 18.",
      "Individual stroke play game."],
     "Nobody has ever created a bunker course, so why not now!", [("Timer", "None.")])
card('halfsies-alt', 'Short Course', 'Halfsies Alt Shot', "Don't let your team down.",
     ["Playing from half the posted distance on each par 3, pick your odd and even tee shots and play alternate shot."],
     "It's always hard to find a rhythm in foursomes. Figure out a way.", [])
card('halfsies-hilo', 'Short Course', 'Halfsies HI/LO', 'Two shots.',
     ["Playing from half the posted distance on each par 3, hit a high shot and a low shot, using either technique or a different club."],
     "Let's find two solutions to the puzzle.", [])
card('chip-off', 'Short Game', 'Chip-Off Race', 'First to 5.',
     ["In the Chip-Off Race against a teammate, grab a Butch B bucket and hit a different shot every time around the chipping green. The first player to chip in five times wins. There's a 20-minute time limit: if neither player makes five, you're both out of the competition."],
     "Like the Short Game and Putting 100, this challenge is more about extending your focus.", [("Timer", "20 minutes, then reset.")])
card('b-sprinklers', '"B" Day Short Game', 'Sprinklers!', None,
     ["From left to right: sprinkler 4, 1, 3, 2.",
      "With a 9 iron, hit 4 shots: a low runner and a high shot that lands soft. Move to your right.",
      "With your gap wedge, hit 4 shots: a low runner and a \"stock\" chip. Move to your right.",
      "With your sand wedge, hit 4 shots: a low runner and a \"stock\" shot."],
     "The best players in the world have a package of shots with different clubs. The 9 iron and 50-degree help you work the bounce. The 56 gives you new shots.",
     [("Timer", "108 shots. No time limit.")])

# ---- Full swing
card('4x4', 'Ball Striking', '4x4', '13 clubs. 4 different shots.',
     ["With 52 balls, hit four different shots to one target with each club in the bag. Choose a different target for each club. Give yourself a point for each called shot you execute and take a point away for each one you miss.",
      "Take your three best irons to The Harmon for a three-club challenge."],
     "Understanding and accepting what you have for the day is critical to consistent scores and a positive attitude.", [("Timer", "None.")])
card('4x4-relay', 'Ball Striking', '4x4 Relay', '13 clubs. 4 different shots.',
     ["With 52 balls, hit four different shots to one target with each club in the bag. Choose a different target for each club. Give yourself a point for each called shot you execute and take a point away for each one you miss.",
      "Take your three best irons to The Harmon for a three-club challenge relay: continuous alternate shot as one team."],
     "Understanding and accepting what you have for the day is critical to consistent scores and a positive attitude.", [("Timer", "None.")])
card('b-wedges', '"B" Day Wedges', '50, 80, 75', None,
     ["Using your \"stock\" club for these numbers, hit 3 balls at each target with the same club, focusing on the window and trajectory.",
      "Next round, hit 3 balls at each target with one more club.",
      "Final round, hit 3 balls at each target with two more clubs than \"stock\". Repeat for the allotted time."],
     "Having \"stock\" feels lets you build a base to work from. The best wedge players in the world control their trajectory and spin.",
     [("Timer", "8-minute phone timer.\nNo scoring needed.")])
card('b-money', '"B" Day Money Makers', '110, 125', None,
     ["Choose the right clubs for the 110- and 125-yard shots. Hit 2 balls at each target to confirm the club for the wind.",
      "Using your 125-yard club, hit 5 shots to the 125-yard pin. Using your 110-yard club, hit 5 shots to the 110-yard green.",
      "For the last round, flight your 125-yard club to the 110-yard green."],
     "Tour best from 100-125 yards is 88%. Tour average is 74%. Were you more accurate with the 110-yard club, or the 125 at 110?",
     [("Timer", "8-minute phone timer."), ("Track", "Note your scoring average with your \"stock\" club vs one up.")])
card('b-ballstrikers', '"B" Day Ball Strikers', '160, 195, 230', 'Short iron, mid iron, full send.',
     ["Find YOUR shot shape that you can repeat consistently for these numbers. It doesn't matter what the player next to you is doing. Figure out how you compete and score.",
      "From 160: hit 5 fades that start well left of the target and land left of the pin. From 195: hit 5 draws that land right of the pin. From 230: hit the green."],
     "Push yourself to play out of \"bad\" lies and uncomfortable positions. Tour average from 150-175: 64%. 175-200: 54%. 200+: 44%.",
     [("Timer", "10-minute phone timer."), ("Ask yourself", "What is your \"million-dollar shot\"?")])
card('b-driving', '"B" Day Driving', 'High Bombs + Low Bullets', None,
     ["This is your chance to work on both speed and accuracy. Becoming an elite driver of the ball doesn't happen by accident: to hit it high and far on the course under the gun, you have to work on it in practice.",
      "After a few warm-up shots, tee up 5 drivers in a row and hit them as high and far as possible. Dispersion is secondary.",
      "Next, hit 5 low bullets that find the fairway. Repeat."],
     "Having these two drives in the bag gives you shot-making you can attack courses with. The high bomb works speed and power, and the bullet is an everyday shot in Florida.",
     [("Timer", "20 drivers: 10 bombs, 10 bullets.")])
card('driving-50', 'Driving', 'Driving 50', '40 full speed + 10 routine.',
     ["Hit 40 drivers at full speed. No targets, no judgement.",
      "Then hit 10 drivers into a specific target fairway, with your full routine and tournament focus."],
     "This speed drill is probably something you need to do every day, with quality golf balls. Speed training is a daily chore: knock it out and raise the floor of your stock driver speed.",
     [("Timer", "35-minute phone timer."), ("Track", "How many of the 10 found the fairway?")])
card('iron-testing', 'Ball Striking', 'Iron Testing', '10 shots. 10 calls.',
     ["Using 10 different targets and irons, guess how far each ball traveled and how wide the miss is from the target line."],
     "We are dialing in awareness of contact and conditions.", [("Timer", "None."), ("Track", "How many of the 10 calls were right on?")])
card('driving-angles', 'Driving', 'Driving Angles', '10 minutes west side. 10 minutes east side.',
     ["For 10 minutes, full-send drivers to the set angle on the east and west sides of the practice tee."],
     "Analytics tells us that taking the better angle into a green is actually a myth... but we can practice taking aggressive angles off the tee!", [("Timer", "20 minutes.")])
A_META = "Learning type: variable · Trackman: optional"
card('flight-467', '"A" Day · Wedges', 'Flight 467', '41, 65, 76 yards.',
     ["Using your gap wedge (50 or 52), warm up by hitting 3 balls to each number: 41, 65 and 76. Then hit 2 balls at each number in reverse order: 76, 65 and 41.",
      "Once you have hit all 15 shots, move to your sand wedge (54 or 56) and repeat the same process."],
     "This warm-up game does two things. First, you begin by seeing flighted wedges. Second, you work on alignment by moving your targets around the range.",
     [("Track", "30 shots. No scoring required.")], meta=A_META)
card('a-money', '"A" Day · Wedges', 'Money Makers', '104, 113',
     ["These are your money-maker numbers. You just hammered a drive into a par 4, or laid up on a par 5, and you're looking at a great scoring chance.",
      "Using the right club, hit 5 shots into the green at 113. Repeat with the same club to the 104-yard pin.",
      "Next, hit 4 shots to 104. On the 5th ball you are \"live\": hit it within 15 feet and you move on. If not, repeat the game until time is up."],
     "Dialing in your \"stock\" shot at your money-maker number gives you confidence in scoring. To push yourself, take one more club and hit three-quarter shots, controlling trajectory and spin.",
     [("Track", "10 shots to dial in your feel. 3 minutes to complete the 5-ball game.")], meta=A_META)
card('par3-scoring', '"A" Day · Approach', 'Par 3 Scoring', '154, 185, 226',
     ["Research shows the golf ball performs differently off the turf than off a tee. Do you know how yours does?",
      "Tee the ball up and, with your full routine, hit a shot at 154. Repeat twice more.",
      "With the ball on the turf and your full routine, hit a shot at 185. Repeat twice more.",
      "Finally, tee the ball up and hit 5 shots at 226."],
     "There are no right answers, but finding how YOU score is what matters most. Note how you perform off the tee and off the turf. From 210+ yards, anything on the green is a \"good\" shot.",
     [("Track", "12 minutes. No scoring required.")], meta=A_META)
card('22s', '"A" Day · Driving', "22's", None,
     ["Congratulations, you just qualified for the U.S. Open! The average U.S. Open fairway is roughly 22-25 yards wide. There are two schools of thought. One is bomb and gouge: if fairways are that tight, even the best drivers will miss them, but they'll be hacking out and unable to reach greens. Bryson dominated Winged Foot with this strategy. Or you can look at club pro Michael Block, who has less than 160 ball speed and drove it down the middle at the PGA...",
      "You are playing Oakmont. You have 20 balls. Hit 10 as hard as you can. Hit 10 within a 22-yard-wide grid. Which is better?"],
     "To succeed at the highest levels, you have to know YOUR game. Choosing a strategy and sticking to it, even when others are playing completely differently, is challenging, but it's what it takes to be great!",
     [("Track", "20 balls.")], meta=A_META)
card('kauai-cuts', '"A" Day · Driving', 'Kauai Cuts', None,
     ["Doc lived on Kauai, where one hole needed a low, bullet cut. It was badly exposed to the wind, and anything that got above the tree line would be blown into the Pacific. You couldn't draw it: it had to fade, or it ran into a bunker.",
      "Choose two targets 40 yards apart. Tee the ball up and go through your full driver routine. Hit 15 drivers into the \"fairway\". A successful shot stays below the tree line and fades."],
     "Holes that demand a certain shot shape might not be the most entertaining, but they give you the problem to solve. If you can execute, you're rewarded!",
     [("Track", "15 balls. How many found the fairway?")], meta=A_META)

# ---- Driving drills doc (5-10 handicap)
card('pincher', 'Driving Drills · 5-10 Handicap', 'The Pincher', None,
     ["Tee up a ball low, as if you were hitting a fairway wood, then hit your driver.",
      "Most coaches teach you to maximize distance by hitting up and swinging fast. But on a must-hit fairway, the low tee with a driver gives a lower, shorter-flight shot that gets down quickly with the speed of a normal tee shot. It feels like you're pinching the ball off the tee into the ground. Most drivers from the last five years will flight lower and fade with little extra spin."],
     "It's a predictable shot, but it takes a little practice to embrace the change. This will put your driving on autopilot.", [])
card('cruise-control', 'Driving Drills · 5-10 Handicap', 'Cruise Control', None,
     ["On the practice tee, find an angle between two targets that represent your fairway (at TeamFLO we use a gap about 30 yards wide between columns of greens and bunkers).",
      "Take 30 balls in three groups of 10. First group: swing at 100% and grade your accuracy. Take a two-minute break. Second group: swing at 150%, all out, and grade your accuracy. Third group: swing smooth, about 90%, and grade your accuracy.",
      "Which set was most accurate? That's your Cruise Control setting."],
     None, [("Track", "Accuracy grade for each set of 10.")])
card('no-pin-nine', 'Driving Drills · 5-10 Handicap', 'No-Pin Nine', 'Improving iron play.',
     ["Take the ego (the hole location) out and put the back edge of the green in. Delete the pin sheet, look at the sprinkler head (or your Arccos Caddie) and choose the yardage to the back center of the green.",
      "At our team facility, we play 9 holes without pins, and players must play to the back-of-green yardage. We put the pin back in as players arrive and finish the hole."],
     "The number one reason golfers miss greens is not enough club, a mishit, or both. This drill solves that problem in a hurry.", [])
card('hyped-4-doc', 'Driving Drills · 5-10 Handicap', 'Hyped 4-Footer', 'Three-putt avoidance.',
     ["A team rule: make every putt (100%!) inside four feet.",
      "By yourself: make 10 spots in a circle four feet from a hole. Make all 10. If you don't, run 500 yards, come back and try again.",
      "With your best friend: using two holes, make 10 spots in a circle four feet from each hole. You must both make all 10. If either of you misses, you both run 500 yards."],
     "When you live and die as a team, you'll be surprised how much more pressure you feel not to let your teammate down. That carries onto the course in a hurry.", [])

# ---- Fitness
card('the-josh', 'Fitness', 'The Josh', "Josh's 35-minute training circuit.",
     ["Warm-up, 10 reps each: toe taps (lie on your back, arms out like a cross; cross a straight leg over and tap the ground), reverse toe tap / scorpion, Y upper-body roll-over, cat-dog, kneeling hip flexor stretch, fire hydrants.",
      "Circuit, 10 reps each, back to back: push-ups, plank elbows to hands, mountain climbers, burpees, jumping jacks, one-foot jumps forward and back, one-foot jumps side to side. Then balance 15 seconds with eyes open doing forward arm circles, and 15 seconds with eyes closed doing backward arm circles. Break 90 seconds.",
      "Reverse weighted lunges (10 reps, 2 sets), jumping lunges (10 reps, 2 sets), shot put throws (10 reps each arm, heavy and light ball). Break 90 seconds.",
      "Weighted side lunges (10 reps, 1 set each side), lateral jumps (15 reps), throw 8 lb and 4 lb balls like a golf swing to each other (10 reps left and right). Break 90 seconds.",
      "Swing the fans left and right 10 times, Happy Gilmore style. Swing a shaft left and right 10 times, fast."],
     "Bring the right shoes.", [("Timer", "35-minute phone timer. No scoring.")])

# ---- Standards and culture
card('tourn-std', 'Standards', 'Tournament Standards', 'How to prepare for round defense.',
     ["1. Pre-write a thank-you note to the tournament host pro.", "2. Protect your ball.", "3. Play responsibly.", "4. Accept what you bring.", "5. Build momentum."],
     "Playing well despite thoughts on technique is a standard of true professionals.", [("Timer", "30 seconds per routine or less.")])
card('tourn-std6', 'Standards', 'Tournament Standards', 'How to prepare for round defense.',
     ["1. Pre-write a thank-you note to the tournament host pro.", "2. Protect your ball.", "3. Play responsibly.", "4. Accept what you bring.", "5. Build momentum.", "6. Play better."],
     TS_ADVICE6, [("Timer", "30 seconds per routine or less.")])
card('flo-why', 'FLOmandments', 'Our Why', None,
     ["Claude has worked with players who have won 8 of the last 52 majors, with 60 other major tour victories since 2011.",
      "Why? Why not more? Let's find out together.",
      "In other sports there are teams with one vision and shared goals. In golf, we think an hour lesson, or separate coaching in a silo, is the path. We tend to think it's technique more than execution. We neglect how we actually play the game.",
      "Doc Nico will revolutionize how we train. Claude will share what works. I'm going to help facilitate it all, because it's my job to make everyone around me successful.",
      "We are going to take knowledge from the most successful organizations and teams and implement it here. We will start small and grow together. This is not just about golf: it's about building successful, great people who play golf."], None, [])
card('flo-amb', 'FLOmandments', 'Ambassadorship', None,
     ["As an ambassador on TeamFLO, we are responsible for the care of our training facility and Learning Center, the Harmon Course and the Fazio Course. Whatever the coaches, greenkeepers and players need, we all deliver. The quality of our training areas reflects on us and gives us the greatest chance to succeed."], None, [])
card('flo-vision', 'FLOmandments', 'Vision', None,
     ["As an ambassador on TeamFLO, you are charged with:", "a. Sharing the vision of constant learning, growth, trust and unlimited potential.",
      "b. Doing what is best for the team while encouraging your own personal growth.", "c. Focusing on the chase, as it is better than the capture.", "d. Understanding that it's a sacrifice, not just work."], None, [])
card('flo-team', 'FLOmandments', 'Team', None,
     ["We train together. If you're the only team member here and there's a coach available, or another player or Floridian member between lessons, you are obligated to convince them to join you."], None, [])
card('flo-walk', 'FLOmandments', 'We Walk', None,
     ["Whenever possible on The Harmon, The Fazio, field trips and events, we walk."], None, [])

# ---- Bootcamp missions
card('bc1-walk', 'Bootcamp 1', 'The Walk', 'Grab sand.',
     ["Your first task with your partner is to walk the entire Fazio Course, starting on #3. Bring a sand bottle. Fill divots. Pick up broken tees. Fulfill your role as an ambassador when you meet groups on the course."],
     "Golf tournaments are walking only. We walk.", [("Timer", "None, but you have a ton of work to complete.")])
card('bc1-strike5', 'Bootcamp 1', 'Strike on #5', 'Protect your ball.',
     ["Your next task with your partner is to run to Harmon #5 and make par or better. Don't make par? Play Harmon #6, and now you must play these two holes until you make back-to-back pars. You're running, so you might take only a few clubs. Protect your ball. Both players must make pars. Help each other."],
     STRESS, [("Timer", "None, but you've got other tasks.")])
card('bc1-hyped4', 'Bootcamp 1', 'The Hyped 4-Footer', None,
     ["At the specially marked hole, hit 10 putts from 4 feet. You and your partner must make all 10 without a miss. If you don't, run to Harmon #1: make par to come back to the circle. Bogey or worse moves you to #2. Make par there and come back to finish 10 in a row. Bogey or worse on #2 and you're in a 20-minute time-out. After the time-out, back to Harmon #1: make par, or you're in purgatory until you do."],
     HEART, [])
card('bc1-last', 'Bootcamp 1', 'The Last Up and Down', 'Up and down to win.',
     ["Your last task of the day is an up and down from the specially marked spot. You and your partner must both get up and down. Fail and the penalty is 10 push-ups. Repeat until you get up and down."],
     "That tension you feel in your arms is what you want to feel, because it means you care.", [("Timer", "None.")])
card('bc2-walk', 'Bootcamp 2', "Today's Walk", 'Grab sand.',
     ["Your first task with your partner is to walk the Harmon Course and the front nine of the Fazio. Bring a sand bottle. Fill divots. Pick up broken tees. Fulfill your role as an ambassador when you meet groups on the course."],
     "We had 36 holes plus walking last week, second only to PGA Tour players in Hawaii.", [("Timer", "None, but you have a ton of work to complete.")])
card('bc2-scramble', 'Bootcamp 2', 'Scramble to Harmon #3', 'Play responsibly.',
     ["Your next task with your partner is to run to Harmon #3 and make birdie or better in a scramble. No birdie? Play Harmon #4. Par or worse? Play Harmon #5. Par or worse? Head to the basketball court, where you must both make a free throw to go back to Harmon #3 and continue the scramble.",
      "You're running, so you might take only a few clubs. Protect your ball. Help each other."],
     STRESS, [("Timer", "None, but you've got other tasks.")])
card('bc2-vietnam', 'Bootcamp 2', 'Vietnam', 'The jungle.',
     ["There are six holes on the putting green, with a white ball marker at each starting position. You and your partner keep scrambling. The team target is 5 under: 5 makes out of 12. Fewer than 5? Run to Harmon #2 and make birdie or better. No birdie? Return to the putting green, but the target is now 6 under. Miss 6 under and you're in a 15-minute time-out, and the target goes back to 5 under."],
     HEART, [])
card('bc2-cannon', 'Bootcamp 2', 'Load Up the Cannon', 'Drive responsibly.',
     ["Each teammate hits two drives from five tee boxes, at each corner of the practice tee and the center. Six of the 10 drives must land inside the target area. Either player can contribute, or one player can carry the team.",
      "Fewer than 6? Run a lap around the Learning Center, then head to the bunker, where both players must get up and down."],
     SAVE, [("Timer", "None.")])
card('bc2-bike', 'Bootcamp 2', 'The Bike Ride', 'Ride responsibly.',
     ["In the putting studio there are 22 putts near the garage door (consult the map). One player must make 15 putts or more while the other rides a mile on the assault bike. Then switch. If you make 30 or more between you, the task is complete. Fewer than 30: repeat the task."],
     SAVE, [("Timer", "None.")])
card('bc3-walk', 'Bootcamp 3', "Today's Walk", "Let's go backwards.",
     ["Your first task with your partner is to walk the Fazio course backwards, starting on hole #2. Bring a sand bottle. Fill divots. Pick up broken tees. Fulfill your role as an ambassador when you meet groups on the course.",
      "Today's goal is to build ball inventory and complete the final task: playing the Harmon. You start with one ball. Let's go!"],
     "We had 36 holes plus walking last week, second only to PGA Tour players in Hawaii.", [("Timer", "None, but you have a ton of work to complete.")])
card('bc3-mogul', 'Bootcamp 3', 'Mogul Depot', 'Watch for enemy fire.',
     ["You and your partner head to the stones and hit from the set tee. You have one ball. Hit at a stone, run to retrieve your ball, and come back. There are 9 stones. Every stone you hit adds one ball to your inventory for the day. The two back-row stones are worth four balls. Stay on this mission as long as you like to build inventory."],
     STRESS, [("Timer", "None, but you've got other tasks.")])
card('bc3-ring', 'Bootcamp 3', 'Ring of Fire', None,
     ["There are three rings of fire on the putting green, at 3, 4 and 5 feet: 30 putts in all. Your team objective is for each of you to make 25. Make 26 and add a ball to your inventory, plus one ball for each make after 26.",
      "Make fewer than 25 and run to Harmon #1 and play alternate shot with one of your balls. Make par to come back to the ring of fire. No par: your team loses a ball and moves to #2, where one chosen player must make par. No par: move to #3. Out of ammo? Back to the Mogul Depot."],
     HEART, [])
card('bc3-storm', 'Bootcamp 3', 'Desert Storm', 'Harmon holes 4, 5 and 6.',
     ["You and your partner move to holes 4, 5 and 6 on the Harmon. On each hole, hit a bunker shot and get up and down. Only one of you needs to get up and down to advance, but failing costs a ball of inventory. To build inventory, head back to the Mogul Depot."],
     SAVE, [("Timer", "None.")])
card('bc3-march', 'Bootcamp 3', 'The March', None,
     ["Using only four clubs and your remaining ball inventory, you and your partner play alternate shot from Harmon #1. The task is to finish all nine holes before anyone else. Out of balls? Back to the Mogul Depot to earn inventory."],
     "Saving shots around the green under stress in practice isn't normal. Make it normal.", [("Timer", "None.")])
card('bc4-walk', 'Bootcamp 4', "Today's Walk", 'Grab a weight.',
     ["Your first task with your partner is to walk the Fazio course backwards, starting on hole #2. You and your partner must carry an object chosen by RC from a lineup."],
     "Walking 18 holes carrying extra weight is normal for the Army or a SWAT team.", [("Timer", "None, but you have a ton of work to complete.")])
card('bc4-drive', 'Bootcamp 4', 'Driving Depot', None,
     ["You and your partner head to the helipad and hit drives into a specific window. Hit three drives in a row into the window to earn one ball of ammo for future missions."],
     DEPOT, [("Timer", "None, but you've got other tasks.")])
card('bc4-pitch', 'Bootcamp 4', 'Pitching Depot', None,
     ["You and your partner head to one of the 55-yard pitching areas. Get up and down to earn one ball of ammo."],
     DEPOT, [("Timer", "None, but you've got other tasks.")])
card('bc4-trapped', 'Bootcamp 4', 'Trapped Six', None,
     ["There are 6 putts set up on the putting green. Your partner is trapped. To free your partner, you must complete all 6 putts at 2 under par or better. When one player finishes the course, the other player is trapped. Both players must complete the challenge, which earns two balls of inventory."],
     "You must save your partner to advance.", [])
card('bc4-rescue', 'Bootcamp 4', 'Rescue Mission', 'Hostages held on #6.',
     ["Your partner is a hostage on the Harmon #6 tee with both of your bags. Your mission: use whatever tools are in the Titleist Studio, limited to two clubs of your choice, and whatever ammo you have. The rescue requires you to hit every green in a row on Harmon holes 1-5 to reach the 6th tee. Use the mat tee boxes. Miss a green and start over on #1.",
      "Once contact is made, both players play #6. Play both balls, scoring +1 or better to advance, or the other partner becomes the hostage."],
     "This is a problem-solving game and a waiting game. The hostage must carry both bags to the #6 tee.", [("Timer", "None.")])
card('bc5-run', 'Bootcamp 5', "Today's Run", 'Two options.',
     ["1. Run the Harmon twice to inoculate yourself from bogeys for the rest of the day. You must stay on the cart path.",
      "2. Or roll the dice: for every shot over par today, you run the Harmon that many times."], DONE, [])
card('bc5-suicide', 'Bootcamp 5', 'Putting Suicide', None,
     ["There are three 4-foot stations of 10 putts. You must make 10 in a row at each station.",
      "Miss a putt and you can either ride 5 miles on the assault bike or start over. This station must be completed, or you can escape with the 5-mile assault bike ride."], DONE, [])
card('bc5-course', 'Bootcamp 5', 'On Course 9 and 9+', None,
     ["The Harmon Game: amateurs have a full set of clubs; pros have three clubs. If you've been inoculated for bogeys, there's nothing to worry about. If you haven't... DON'T MAKE A BOGEY. Every stroke over par is a run. MAKE BIRDIES.",
      "The Fazio Game: depending on timing, play 9 or 18 holes. The game is simple: shoot under par after 9 or 18 and you win. Same bogey rules: every stroke over par is a run."],
     DONE, [("Tees on the Fazio", "Par 3s: all play #1 tee.\nPar 4s: all play #3 tee.\nPar 5s: all play #4 tee.")])

# ---- Packs (multi-page sessions) and single cards
SINGLES = [
 ('Harmon Matches', ['hm-a','hm-b','hm-fade','hm-c','hm-d','hm-e','hm-f','hm-63','hilo','harmon-rules','survivor']),
 ('Putting Studio', ['good-zones','beehives','all22']),
 ('Short Game and Putting', ['trail-mix','sg-100','putting-100']),
 ('Ball Striking and Driving', ['4x4','4x4-relay']),
 ('Fitness and Standards', ['the-josh','tourn-std']),
]
PACKS = [
 ('Session Days', 'Harmon Match Day', '1 Up & 1 Down', None, ['hm-a-team','hm-c-team','hm-d-team','b-ballstrikers','b-driving','b-sprinklers','b-putting']),
 ('Session Days', 'TeamFLO "A" Day', 'Plan for 7/31/23',
  ['Practice tee: Flight 467 (41, 65, 76) · Money Makers (104, 113) · Par 3 Scoring (154, 185, 226) · Driving: 22\'s and Kauai Cuts',
   'Harmon Course: "A" tees · White pins down, green pins back · Blind-draw match play'],
  ['flight-467','a-money','par3-scoring','22s','kauai-cuts']),
 ('Session Days', 'TeamFLO "B" Day', 'October 23', None, ['b-wedges','b-money','4x4-relay','b-ballstrikers','b-driving','b-sprinklers','b-putting']),
 ('Session Days', 'Stations Day', None, None, ['the-josh','driving-50','putting-100','4x4']),
 ('Session Days', 'Nico Sans Nico Day', None, None, ['rights-lefts','iron-testing','driving-angles','driving-50','intentional-miss']),
 ('Session Days', "RC's Short Game Circus 126", None, None, ['bunker-course','halfsies-alt','chip-off','putting-50x2']),
 ('Session Days', "RC's Short Game Buff n' Shine", None, None, ['bunker-course','halfsies-hilo','putting-50']),
 ('Bootcamps', 'Bootcamp 1', "Practice until you can't get it wrong.", None, ['bc1-walk','bc1-strike5','bc1-hyped4','bc1-last','tourn-std']),
 ('Bootcamps', 'Bootcamp 2', 'Confident execution of your plan.', None, ['bc2-walk','bc2-scramble','bc2-vietnam','bc2-cannon','bc2-bike','tourn-std']),
 ('Bootcamps', 'Bootcamp 3', "This We'll Defend.", ['The motto of the U.S. Army.'], ['bc3-walk','bc3-mogul','bc3-ring','bc3-storm','bc3-march','tourn-std6']),
 ('Bootcamps', 'Bootcamp 4', 'Servare Vitas.', ['The motto of the FBI Hostage Rescue Team: "Save Lives."'], ['bc4-walk','bc4-drive','bc4-pitch','bc4-trapped','bc4-rescue','tourn-std6']),
 ('Bootcamps', 'Bootcamp 5', 'Hell Week.', ["We are done with doubles after today.", "Complete today's blueprint in this order."], ['bc5-run','bc5-suicide','bc5-course','tourn-std6']),
 ('Drills', 'Driving Drills', '5-10 handicap', ['Improving your accuracy off the tee comes down to technique and execution, but few golfers practice execution. When it comes to playing golf, not playing golf swing, you simply need to get the ball in the fairway by whatever means necessary.'], ['pincher','cruise-control','no-pin-nine','hyped-4-doc']),
 ('Team', 'FLOmandments', 'Our why and how we train.', None, ['flo-why','flo-amb','flo-vision','flo-team','flo-walk']),
]
