#!/bin/bash

if [ $# -ne 2 ]; then
  echo $#
  echo "Usage $0 '<infile>' '<outfile>'"
else
  mencoder "$1" -o "$2" -vf crop=520:430:80:24 -ovc x264 -x264encopts subq=6:partitions=all:8x8dct:me=umh:frameref=5:bframes=3:weight_b
fi
