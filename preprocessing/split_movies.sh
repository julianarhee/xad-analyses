#!/usr/bin/env bash

srcdir="$1"

#shopt -s dotglob nullglob
shopt -s globstar 

echo "Processing $srcdir"

for f in $srcdir/*.MOV; do
  d=${f%.MOV} # get movie filename to make subdir
  b=$(basename -s .MOV "$f") # get file basename without ext

  # make dir, then save 10min segments to subdir 
  if mkdir -p "$d"; then
    ffmpeg -i "$f" -c copy -map 0 -segment_time 00:10:00 -f segment -reset_timestamps 1 "$d/${b}_%03d.MOV"
  else
    printf 'could not mkdir %s\n' "$d"
  fi
done


