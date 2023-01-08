#!/usr/bin/env bash

srcdir="$1"

shopt -s globstar 

echo "Compressing $srcdir"

#for dir in $srcdir/*/; do
#  if [ -d "$dir" ]; then
#    dir=${dir%*/}      # remove the trailing "/"
#    for f in $dir/*/*.MOV; do
#      parentdir="$(dirname "$f")"
#      b=$(basename -s .MOV "$f")
#      ffmpeg -i "$f" -vcodec libx265 -crf 28 "$parentdir/${b}_c.MOV"    
#    done
#  fi
#done

for sdir in $srcdir/*/; do
  if [ -d "$sdir" ]; then
    ddir=${sdir%*/}      # remove the trailing "/"
    for f in $ddir/*.MOV; do
      parentdir="$(dirname "$f")"
      bname=$(basename "$parentdir")
      if [ "$bname" != "raw" ]; then
        dstdir="$parentdir/compressed"
        mkdir -p "$dstdir" 
        b=$(basename -s .MOV "$f")
        echo "$dstdir/${b}_c.MOV"
        ffmpeg -i "$f" -vcodec libx265 -crf 28 "$dstdir/${b}_c.MOV"    
      fi
    done
    echo "Done compressing!"
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

