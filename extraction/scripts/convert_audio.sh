#!/bin/bash
# Convert all MS ADPCM wav chunks to OGG (parallel). Private research use.
SRC="/home/z/my-project/download/TDKR_assets/raw/sounds"
DST="/home/z/my-project/download/TDKR_assets/audio_ogg"
mkdir -p "$DST"
cd "$SRC"
ls *.wav | xargs -P 8 -I{} sh -c 'ffmpeg -hide_banner -loglevel error -y -i "$1" -c:a libvorbis -q:a 3 "$2" 2>/dev/null || echo "FAIL $1"' _ {} "$DST/{}.ogg"
echo "DONE: $(ls "$DST" | wc -l) ogg files"
