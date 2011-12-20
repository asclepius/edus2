#!/bin/bash

if [ $# -ne 2 ]; then
  echo $#
  echo "Usage $0 '<infile>' '<outfile>'"
else
  ffmpeg -vf "crop=520:430:80:24, scale=-1:480, drawtext=fontfile=/opt/local/share/fonts/dejavu-fonts/DejaVuSans.ttf: text='Copyright (c) 2011 Paul Kulyk, Paul Olszynski':x=5: y=450: fontsize=16: fontcolor=white@0.8: box=1: boxcolor=black@0.8" -sameq -i "$1"  "$2"
  #ffmpeg -vf "crop=520:430:80:24, drawtext=fontfile=/opt/local/share/fonts/dejavu-fonts/DejaVuSans.ttf: text='Copyright (c) 2011 Paul Kulyk, Paul Olszynski':x=5: y=415: fontsize=13: fontcolor=white@0.8: box=1: boxcolor=black@0.8" -sameq -i "$1"  "$2"
  #ffmpeg -vf "crop=520:430:80:24, scale=-1:720" -sameq -i "$1"  "$2"
#  mencoder "$1" -o "$2" -vf crop=520:430:80:24 -ovc x264 -x264encopts subq=6:partitions=all:8x8dct:me=umh:frameref=5:bframes=3:weight_b
fi
