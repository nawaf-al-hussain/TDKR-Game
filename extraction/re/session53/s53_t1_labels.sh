#!/bin/bash
set -e
CPU=/home/z/my-project/scripts/s52_t1_cpu.py
for FX in AlphaMasking SimpleAdditive StandardDiffuseDC other LightMapDC; do
  OUT=s53_lab_${FX}
  if [ ! -f /tmp/my-project/work/city_slice_wt/playable/${OUT}.png ]; then
    echo "=== flat label $FX ==="
    python3 $CPU --flat --zbuf --snap --only $FX --out $OUT
  fi
done
echo ALL_DONE
