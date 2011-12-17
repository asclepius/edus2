#!/bin/bash

# EXAMPLE: find ./rawscans/ -name "*.mp4" -print0 | xargs -0 -n 1 ./worker.sh

FILE=$1


BASE=`basename "$FILE"`

./mplayer_crop.sh "$FILE" "../data/$BASE"
