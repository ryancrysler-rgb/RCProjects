# Content that is not in the weekly Drive docs: month framing, front matter, Week 37, and Month 8 (Weeks 29-32).
# Month 8 has no blueprint in Drive. Its weeks follow last season's themes (Qualifier, PGA Championship, U.S. Open,
# Road Warrior) and are built from Crucible drills already used earlier in the season.

def d(cat, name, hiit, drill, cons, src=None):
    rows = [['HIIT', hiit], ['Do or Die', drill], ['Consequence', cons]]
    return {'cat': cat, 'name': name, 'rows': rows, 'extra': [], 'from': src}

MONTHS = [
    {'n': 1, 'phase': 'Phase 1 · The Foundation of Performance', 'title': 'Foundational Control & Consistency', 'weeks': ['1', '1B', '2', '3', '4'],
     'intro': 'Establish a baseline of precision before adding power. Control comes first: start line, strike, landing spot, and a pre-shot routine you can trust when your heart rate is up.'},
    {'n': 2, 'phase': 'Phase 1 · The Foundation of Performance', 'title': 'Power Generation & Speed', 'weeks': ['5', '6', '7', '8'], 'intro_key': '2'},
    {'n': 3, 'phase': 'Phase 1 · The Foundation of Performance', 'title': 'Pressure Inoculation & Scrambling', 'weeks': ['9', '10', '11', '12'], 'intro_key': '3'},
    {'n': 4, 'phase': 'Phase 2 · The Strategist & the Shot Maker', 'title': 'Strategic Decision Making', 'weeks': ['13', '14', '15', '16'],
     'intro': 'Replace hope with data. Learn your real carry numbers and dispersion, then play the percentages like a course manager: aggressive swings to conservative targets.'},
    {'n': 5, 'phase': 'Phase 2 · The Strategist & the Shot Maker', 'title': 'Adversity Acclimation & Shot Shaping', 'weeks': ['17', '18', '19', '20'],
     'intro': 'Become an all-weather player. Control trajectory and spin, flight it down in the wind, and curve the ball both ways on command.'},
    {'n': 6, 'phase': 'Phase 2 · The Strategist & the Shot Maker', 'title': 'Competitive Sharpening & Mental Fortitude', 'weeks': ['21', '22', '23', '24'], 'intro_key': '6'},
    {'n': 7, 'phase': 'Phase 3 · The Championship Run', 'title': 'Major Prep: The Masters', 'weeks': ['25', '26', '27', '28'], 'intro_key': '7'},
    {'n': 8, 'phase': 'Phase 3 · The Championship Run', 'title': 'Road Warrior: PGA Championship & U.S. Open', 'weeks': ['29', '30', '31', '32'],
     'intro': 'May and June. The majors move on the road: long irons and heat at the PGA Championship, narrow fairways and thick rough at the U.S. Open, and tournament weeks that mean travel and limited practice. This month uses drills from the whole season, themed to the championships. Pars are sacred and nothing gets a second chance.'},
    {'n': 9, 'phase': 'Phase 3 · The Championship Run', 'title': 'Scoring Optimization & Performance Analytics', 'weeks': ['33', '34', '35', '36', '37'], 'intro_key': '9'},
]

FRONT = {
    'premise': 'Make practice harder than the tournament. Standard practice breeds passive mechanics that fall apart under pressure. By adding physical fatigue and mental stress to every session, players build motor patterns and emotional resets that hold up on Sunday.',
    'architecture': [
        ('Pairing', 'Every session pairs up to 6 HIIT exercises with 6 "Do or Die" golf drills across Short Game, Full Swing and Visualization.'),
        ('Heart rate', '45 to 60 seconds of max-effort work drives the heart rate up before every shot.'),
        ('Transition', 'Within 15 seconds of the HIIT, step up, breathe through your pre-shot routine and hit the shot.'),
        ('Why', 'Physical fatigue exposes your fundamentals. Mental fatigue tests your commitment.'),
    ],
    'principles': [
        ('Process over outcome', 'Results follow the routine. Focus on target, breath and commitment.'),
        ('Extreme ownership', 'No excuses for weather, bounces or fatigue. Every shot is yours.'),
        ('Discipline equals freedom', 'Structure in practice gives you freedom under pressure.'),
        ('Chaos management', 'Adapt to bad lies, bad bounces, a racing heart and noise.'),
    ],
    'rules': [
        ('Count resets', 'If a drill needs 5 in a row and you miss on #4, the count goes back to 0.'),
        ('Physical consequences', 'Fail a gate and pay the penalty before you go again: 10 burpees, a 45-second wall sit, a 60-second plank or 15 squat jumps, unless the drill says otherwise.'),
        ('The 24-second rule', 'After any miss you have 24 seconds to release it, get back to neutral and start the next routine.'),
    ],
    'safety': 'Coaches set every load and every rep count. Juniors use bodyweight or light options for any loaded exercise, and anyone can swap an exercise for a safe alternative. Hydrate between blocks.',
}

W29 = {'n': 29, 'title': "The Qualifier's Mindset", 'src': 'Month 8',
       'mission': 'Road to the PGA Championship. A qualifier gives you one ball on every shot. This week every drill is scored on the first attempt only: no mulligans, no second chances.',
       'sections': [{'h': None, 'items': [
           d('Full Swing', 'The "One Shot" Qualifier', 'Explosive Broad Jumps (60s).',
             'Place a single ball on the tee and define a 30-yard fairway. This is the 18th hole of a qualifier. You get one shot to find the fairway.',
             'You must succeed 3 times in a row. A miss resets the count to zero and costs 10 burpees.', 'Week 1B'),
           d('Short Game', 'The "Make the Cut" Par Putt', 'Wall Sit (hold until failure).',
             'Place a ball 6 feet from the hole. You just hit a poor chip and this putt decides whether you make the cut.',
             'You must make 5 consecutive putts. A single miss resets the count to zero.', 'Week 27'),
           d('Visualization', 'Your Name on the First Tee', 'High Knees in Place (60s).',
             'Hear the starter announce your name on the first tee of a qualifier. Feel the nerves. Run your full pre-shot routine in your mind and see the ball land in the fairway.',
             'Hold the routine with total clarity. If your mind wanders, restart. Perform 3 times.', 'Weeks 1 and 21'),
           d('Short Game', 'The Playoff Scramble', "Heavy Farmer's Carry (as far as possible in 60s).",
             'Set up the hardest up-and-down you can find. You get one attempt to get up and down and earn a spot in the playoff.',
             "If you fail, re-do the Farmer's Carry, then complete the same up-and-down 2 times in a row.", 'Week 8'),
           d('Full Swing', 'The First-Attempt Iron', 'Burpees (60s).',
             'Pick three greens at about 130, 155 and 180 yards. You get one ball to each. All three must finish on the green.',
             'Only the first attempt counts. A single miss means you re-do the HIIT and restart all three.', 'New'),
           d('Visualization', 'The Bad Break', 'Box Breathing (90s).',
             'Visualize a perfect drive that kicks into a divot. Feel the anger. Use the 24-second rule: release it, get back to neutral, and plan the smartest shot from the divot.',
             'You must be neutral and committed within 24 seconds. Perform 3 times.', 'Week 4'),
       ]}]}

W30 = {'n': 30, 'title': 'The PGA Championship Test', 'src': 'Month 8',
       'mission': 'The PGA Championship is a long, hot ball-striker\'s major. This week trains long irons into firm greens, endurance through 18 holes, and aggressive scoring when the window opens.',
       'sections': [{'h': None, 'items': [
           d('Full Swing', 'The Long Iron Gate', 'Kettlebell Swings (60s) (safe weight).',
             'With a 4-iron (or your longest iron or hybrid), hit to a green 190 to 210 yards away. The ball must land on the green.',
             'You must land 5 consecutive shots on the green. A miss resets the count to zero and costs 5 burpees.', 'New'),
           d('Short Game', 'The Lag Putt Gauntlet', 'Max Repetition Burpees (60s).',
             'From 50 feet, you must two-putt. Immediately after, you must make an extra 4-foot "comebacker."',
             'You must succeed 3 consecutive times. A three-putt or a missed comebacker resets the count and costs a 30-second plank.', 'Week 21'),
           d('Full Swing', 'Driving in the Heat', 'Sprint 50 yards, jog back (repeat for 90s).',
             'Hit 10 drivers at full speed into a 30-yard corridor. Stay hydrated and keep your tempo as you fatigue.',
             'You must hit 8 of 10 inside the corridor. Failure means you re-do the sprints and the full set.', 'Week 7'),
           d('Short Game', 'The Thick Collar Chip', 'Mountain Climbers (60s).',
             'From 15 to 20 yards in thick rough around the green, you must get up and down.',
             'You must succeed on 6 of 10 attempts. Failure means a 60-second plank before restarting the 10-ball set.', 'Week 33'),
           d('Visualization', 'The Birdie Window', 'Medicine Ball Slams (60s).',
             'Visualize the back nine of a major. Pick the two holes where you will attack and the holes where par is a great score. Plan each one: club off the tee, leave yardage and target.',
             'Your plan must be decisive, with no second-guessing. Perform 3 times.', 'Week 35'),
           d('Full Swing', 'The 72nd-Hole Long Iron', 'Man-Makers (90s). Final gut check.',
             'Exhausted, hit one 4-iron or hybrid into a green from 200 yards, then two-putt for par.',
             'One ball. A miss means you re-do the HIIT and the shot until you succeed.', 'Week 27'),
       ]}]}

W31 = {'n': 31, 'title': 'The U.S. Open Grind', 'src': 'Month 8',
       'mission': 'At the U.S. Open, par is a great score. Narrow fairways, thick rough and firm greens test your patience. Your job is to protect par, avoid hero shots and never make a double.',
       'sections': [{'h': None, 'items': [
           d('Full Swing', 'The Narrow Fairway', 'Lateral Skater Jumps (60s).',
             'Define a 25-yard fairway. With driver or 3-wood, you must find it.',
             'You must hit 5 consecutive fairways. A miss resets the count to zero and costs 10 squat jumps.', 'Week 7'),
           d('Short Game', 'The Thick Rough Escape', "Heavy Farmer's Carry (60s).",
             'Drop 6 balls in deep rough 10 to 25 yards from the green. Every shot must finish within 12 feet of the hole.',
             'You must succeed on 5 of 6. Failure means a 45-second wall sit and a restart.', 'Week 9'),
           d('Full Swing', 'The Chop Out', 'Medicine Ball Rainbow Slams (45s).',
             'From deep rough 150 yards or more out, take a wedge or short iron and advance the ball to a safe lay-up zone at your favorite wedge number. No hero shots.',
             'You must find the zone 3 times in a row. Going for the green is a failure even if it works.', 'Week 3'),
           d('Short Game', 'The "No Three-Putt" Zone', 'Alternating Split Squat Jumps (45s).',
             'On the fastest putts you can find, from 40 feet, your only goal is to get the first putt to finish within 3 feet of the hole.',
             'You must succeed 5 times in a row. A putt outside 3 feet resets the count and costs 10 squat jumps.', 'Week 22'),
           d('Visualization', 'Pars Are Sacred', 'Plank (hold for 90s).',
             'Visualize missing three greens in a row. On each hole, accept bogey as your worst score and plan the safest route to a 5-foot par putt.',
             'You must complete all three holes with zero hero thoughts. Any thought of forcing a birdie means you restart.', 'Week 14'),
           d('Short Game', 'Par Preservation', 'Burpees (60s).',
             'Pick 6 different spots around the green: thick rough, bunker, tight lie, downhill, short-sided and long. One ball from each. Get up and down.',
             'You must save 4 of 6. Any spot where you take 4 or more shots is a "double" and you restart all 6.', 'Week 10'),
       ]}]}

W32 = {'n': 32, 'title': 'Final Exam: The Road Warrior', 'src': 'Month 8',
       'mission': 'Tournament weeks mean travel, hotel rooms and limited practice. This exam proves your preparation travels: equipment-free conditioning, a restricted bag and a 6-hole test. The HIIT needs no gym, and the bag has 8 clubs only: driver, hybrid or 4-iron, 7-iron, 9-iron, pitching wedge, sand wedge, lob wedge and putter.',
       'sections': [{'h': None, 'items': [
           d('Hole 1', 'The Opening Par 4', 'Burpees (60s).',
             'Driver into a 35-yard fairway, an approach to the green, then two-putt. Par is 4.',
             'Keep score against par. Your goal is to finish the 6 holes at Even Par or better.', 'Week 24'),
           d('Hole 2', 'The Long Par 3', 'Squat Jumps (45s).',
             'From 190 yards with your hybrid or 4-iron, you must hit the green. A miss requires an up-and-down to save par. Par is 3.',
             'Track your score.', 'Week 30'),
           d('Hole 3', 'The No 3-Wood Par 5', 'Mountain Climbers (60s).',
             'After your drive, there is no 3-wood in the bag. Lay up with your 7-iron to a full wedge number, then attack the pin. Par is 5.',
             'Track your score. Birdie is the goal.', 'Week 35'),
           d('Hole 4', 'Between Clubs', 'Wall Sit (hold until failure).',
             'From 140 yards, the club you want is not in the bag. Hit a 3/4 knockdown with the longer club or a full shot with the shorter club. You must hit the green. Par is 3.',
             'Track your score.', 'Week 17'),
           d('Hole 5', 'The Rough Par 4', 'Plank with Alternating Shoulder Taps (60s).',
             'Your tee shot is in thick rough (drop it there). Decide: chop out to your wedge number or go for the green. Execute your choice.',
             'A smart bogey beats a double. Track your score.', 'Week 31'),
           d('Hole 6', 'The Finishing Par 4', 'High Knees in Place (90s).',
             'Full pre-shot routine on every shot. Drive, approach, and finish with the putt you leave yourself. Par is 4.',
             'Tally your 6-hole score. Over par means you have failed the exam. Re-do the simulation on your next practice day. You do not pass the month until you pass this test.', 'Week 24'),
       ]},
           {'h': 'On the road: hotel room circuit', 'items': [
               {'cat': 'No gym needed', 'name': 'The Travel Crucible', 'from': 'Weeks 33-34', 'extra': [], 'rows': [
                   ['HIIT', '3 rounds of 45 seconds each: bodyweight squats, push-ups, alternating lunges, plank with shoulder taps, mountain climbers and a wall sit.'],
                   ['Do or Die', 'After each round, putt on the carpet: hole 3, 5 and 7-foot putts in sequence (use a cup or a coin as the hole). Then run 3 full pre-shot routines for tomorrow\'s first tee shot.'],
                   ['Consequence', 'A single miss resets the putting sequence. Complete the full circuit without a gym, range or green.']]},
           ]}]}

W37 = {'n': 37, 'title': 'The Crucible Culmination', 'src': 'master.txt',
       'mission': 'Championship Readiness Exam. The 37-week synthesis: physical HIIT stress, multi-trajectory shot shaping, data-driven decisions and tournament readiness. Run Phase A stations back to back with 15 seconds between them.',
       'sections': [
           {'h': 'Phase A: Physical & Technical Battery', 'items': [
               {'cat': 'Station 1', 'name': 'Heart-Rate Gate Putting', 'extra': [], 'rows': [['HIIT', '60 seconds of max-effort burpees.'], ['Do or Die', 'Step directly to 6 feet. Sink 5 consecutive putts.'], ['Consequence', 'Any miss resets the count to 0 and adds 10 burpees.']]},
               {'cat': 'Station 2', 'name': 'The Multi-Trajectory Iron Challenge', 'extra': [], 'rows': [['HIIT', '60 seconds of mountain climbers.'], ['Do or Die', 'Hit 3 consecutive 5-irons at 165 yards: a low stinger, a high soft draw and a mid fade. All three must land on the green.'], ['Consequence', 'A missed shape or green costs 15 push-ups per missed shot. Re-attempt the station.']]},
               {'cat': 'Station 3', 'name': 'Pressure Driver Corridor', 'extra': [], 'rows': [['HIIT', '60 seconds of high knees.'], ['Do or Die', 'Hit 4 drivers on a 15-second shot clock per ball. Each must carry 250+ yards inside a 25-yard fairway gate.'], ['Consequence', 'You must hit 4 of 4. A miss costs 20 squat jumps and a full restart.']]},
               {'cat': 'Station 4', 'name': 'Emergency Scrambling Circuit', 'extra': [], 'rows': [['HIIT', '60 seconds of plyometric lunge jumps.'], ['Do or Die', 'Get up and down from 3 brutal lies: a deep divot, a fried-egg bunker and short-sided rough. You must convert 3 of 3.'], ['Consequence', 'A 45-second wall sit for every missed save.']]},
               {'cat': 'Station 5', 'name': 'Distance Wedge Matrix', 'extra': [], 'rows': [['HIIT', '60 seconds of lateral speed skaters.'], ['Do or Die', 'A partner calls 4 random distances (for example 45, 65, 85 and 105 yards). Every shot must finish within 7 feet of the target.'], ['Consequence', 'You must hit 4 of 4. Failure costs a 60-second plank.']]},
               {'cat': 'Station 6', 'name': 'The Championship Visual', 'extra': [], 'rows': [['HIIT', '60-second wall sit or plank.'], ['Do or Die', 'While holding, rehearse a championship final round: 2 bad bounces, a double-bogey threat saved for bogey, and your 72nd-hole winning pre-shot routine.'], ['Consequence', 'Keep total focus and steady breathing through the full 60 seconds.']]},
           ]},
           {'h': 'Phase B: The Zero-Double-Bogey Championship Test', 'items': [
               {'cat': 'Final test', 'name': '18-Hole Simulated Match or 6-Hole Live Course Test', 'extra': [], 'rows': [
                   ['Rules', 'No double bogeys on the scorecard. 100% pre-shot routine compliance on every shot: breath, visual, target callout, commitment.'],
                   ['Consequence', 'A double bogey or a broken routine fails the Culmination. Take 3 days to recover, then re-test before your next tournament.'],
                   ['Graduation', 'Completing Week 37 means you have graduated from the Crucible: fully conditioned, mentally inoculated and tournament ready.']]},
           ]}]}

COMPOSED = {'29': W29, '30': W30, '31': W31, '32': W32, '37': W37}
