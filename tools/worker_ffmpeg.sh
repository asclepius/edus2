#!/bin/bash

# EXAMPLE: find ./rawscans/ -name "*.mp4" -print0 | xargs -0 -n 1 ./worker.sh

FILE=$1


BASE=`basename "$FILE" | sed 's/\ /\_/g' | sed 's/\:/\_/g'`

./ffmpeg_crop_and_copyright.sh "$FILE" "/Volumes/voyager2/edus2/edus2_$BASE"
