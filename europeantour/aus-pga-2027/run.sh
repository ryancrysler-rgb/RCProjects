#!/bin/bash
# Cam Smith · Australian PGA (DP World event 2027100) · one round, from the card, vs every finished player. No shot tracker this week.
# usage: run.sh ROUND  -> pulls the leaderboard + finished cards + Cam's card, builds the 2-page report, racing look, PDF.
set -e
P=/home/user/RCProjects/europeantour/aus-pga-2027
R=${1:-1}; T=$(TZ=America/New_York date +%Y%m%d-%H%M)
D=/tmp/claude-0/-home-user/c0cfce94-7d29-53ae-a568-1ec015f2a64a/scratchpad/auspga/r$R-$T; mkdir -p $D
timeout 600 python3 -I $P/pull.py $D finished
python3 -I $P/build.py $D $R $D/cam-smith-aus-pga-r$R.html
node /home/user/rc-greenlight/research/season-2026/players/race.js $D/cam-smith-aus-pga-r$R.html
NODE_PATH=$(npm root -g) node $P/pdf.js $D/cam-smith-aus-pga-r$R.html "$D/Cam Smith Aussie PGA R$R Report.pdf" $D/preview.png
# every data pull is saved the same day (owner 2026-11-19)
mkdir -p /home/user/RCProjects/data/aus-pga-2027 && tar czf /home/user/RCProjects/data/aus-pga-2027/r$R-$T.tgz -C $D leaderboard.json scorecards.json par_row.json
echo "PDF $D/Cam Smith Aussie PGA R$R Report.pdf"
