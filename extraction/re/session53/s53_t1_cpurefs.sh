#!/bin/bash
# s53 T1: CPU per-effect references (full-zone camera, zbuf semantics, snap, step4)
# sign convention: outputs are 1024x605 top-down PNGs, pixel = engine shader math
set -e
CPU=/home/z/my-project/scripts/s52_t1_cpu.py
for FX in LightMapDC AlphaMasking SimpleAdditive StandardDiffuseDC other; do
  OUT=s53_ref_${FX}
  if [ ! -f /tmp/my-project/work/city_slice_wt/playable/${OUT}.png ]; then
    echo "=== CPU ref $FX ==="
    python3 $CPU --only $FX --zbuf --snap --step 4 --out $OUT
  else
    echo "skip $FX (exists)"
  fi
done
echo ALL_DONE
