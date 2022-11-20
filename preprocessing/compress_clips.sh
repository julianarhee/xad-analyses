#!/usr/bin/env bash

srcdir="$1"
dstdir="$2"

shopt -s globstar 

echo "Processing $srcdir"

for dir in $srcdir/*/; do
  if [ -d "$dir" ]; then
    dir=${dir%*/}      # remove the trailing "/"
    for f in $dir/*/*.MOV; do
      parentdir="$(dirname "$f")"
      b=$(basename -s .MOV "$f")
      ffmpeg -i "$f" -vcodec libx265 -crf 28 "$parentdir/${b}_c.MOV"    
    done
  fi
done



#for f in $srcdir/**/*.MOV; do
#  d=${f%.MOV}
#  b=$(basename -s .MOV "$f")
# 
#  ffmpeg -i "$f" -c copy -map 0 -segment_time 00:10:00 -f segment -reset_timestamps 1 "$d/${b}_%03d.MOV"
#  else
#    printf 'could not mkdir %s\n' "$d"
#  fi
#
#  for f in $d/*.MOV; do
#    echo "$f"
#    b=$(basename "$f")
#    ffmpeg -i "$f" -vcodec libx265 -crf 28 "$dstdir/$b"
#
#done
#
#done
#

