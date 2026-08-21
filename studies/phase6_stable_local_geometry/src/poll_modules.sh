#!/bin/bash
# Poll for /Users/sam/mathmap_data/all_modules.tsv to stop growing.
# At most 10 checks, 120s apart. Never blocks the foreground.
F=/Users/sam/mathmap_data/all_modules.tsv
LOG=/Users/sam/my-repos/research/Map_Of_Mathematics/studies/phase6_stable_local_geometry/logs/poll_modules.log
mkdir -p "$(dirname "$LOG")"
: > "$LOG"
prev=-1
for i in $(seq 1 10); do
  if [ -f "$F" ]; then
    sz=$(stat -f%z "$F")
    echo "$(date +%H:%M:%S) check $i size=$sz prev=$prev" >> "$LOG"
    if [ "$sz" = "$prev" ]; then
      echo "STABLE size=$sz lines=$(wc -l < "$F")" >> "$LOG"
      exit 0
    fi
    prev=$sz
  else
    echo "$(date +%H:%M:%S) check $i: absent" >> "$LOG"
  fi
  sleep 120
done
echo "TIMEOUT after 10 checks" >> "$LOG"
