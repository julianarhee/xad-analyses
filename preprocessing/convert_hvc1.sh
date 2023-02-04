#!/usr/bin/env bash

srcdir="$1"

shopt -s globstar 

echo "Converting $srcdir"

for sdir in $srcdir/*/; do
  if [ -d "$sdir" ]; then
    ddir=${sdir%*/}      # remove the trailing "/"
    compressdir="$ddir/compressed"
    for f in $compressdir/*.MOV; do
      parentdir="$(dirname "$f")"
      bname=$(basename "$parentdir")
      #if [ "$bname" != "raw" ]; then
      #  dstdir="$parentdir/compressed"
      #  mkdir -p "$dstdir" 
      b=$(basename -s .MOV "$f")
      echo "$parentdir/${b}q.MOV"
      ffmpeg -i "$f" -c:v copy -tag:v hvc1 "$parentdir/${b}q.MOV"    
      #fi
    done
    echo "Done converting!"
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

