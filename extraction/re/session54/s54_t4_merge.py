#!/usr/bin/env python3
"""s54 T4: merge the SD block (captured from the SD runner invocation, which the
AM invocation overwrote) back into s54_t4_pereffect.json."""
import json

P = '/tmp/my-project/work/TDKR-Game/extraction/re/session54/s54_t4_pereffect.json'
d = json.load(open(P))
sd = {
    "gl_fixed": {"elapsed_s": 3.7, "pageerrs": [], "dump": "s54_gl_StandardDiffuseDC_win.png",
                 "vs_cpu": {"mode": "label_mask", "gl_cov_pct": 0.126, "cpu_cov_pct": 0.126,
                            "iou": 0.9873, "shared": 777, "gl_mean": 108.99, "cpu_mean": 107.26,
                            "ratio": 1.0161, "corr": 0.9764}},
    "gl_wronglm": {"elapsed_s": 3.7, "pageerrs": [],
                   "vs_cpu": {"mode": "label_mask", "gl_cov_pct": 0.126, "cpu_cov_pct": 0.126,
                              "iou": 0.9873, "shared": 777, "gl_mean": 108.99, "cpu_mean": 107.26,
                              "ratio": 1.0161, "corr": 0.9764,
                              "note": "wronglm INERT on StandardDiffuseDC: the family has no "
                                      "LightMap sampler (correct behavior; the wronglm positive "
                                      "control moves on LM-consuming families - see AlphaMasking "
                                      "0.9999->0.7768 and the s53 LightMapDC 0.9877->0.2063)"}},
    "negative_control_cross_family": {"mode": "label_mask", "iou": 0.0, "shared": 0,
                                      "note": "AM ref covers a disjoint set in the SD window - "
                                              "control vacuous-but-consistent; alignment is instead "
                                              "certified by IoU 0.9873 (a 24-px spatial shift of the "
                                              "ref empties the mask entirely: n=0)"},
}
d['StandardDiffuseDC'] = sd
d['verdict'] = {
    'StandardDiffuseDC': 'n 76 -> 777 (10.2x), corr 0.9079 -> 0.9764, ratio 1.0161, IoU 0.9873; '
                         'wronglm inert (no LM sampler - expected); acceptance "thousands of px" '
                         'NOT met for the comparable set (geometry caps at 798 px in any tested '
                         'window: the family is a near-black water plane + 3 prop materials, '
                         'mostly edge-on/occluded in the top-down view)',
    'AlphaMasking': 'n 29 -> 342 shared-comparable (11.8x), corr 0.8256 -> 0.9999, ratio 1.002, '
                    'wronglm 0.9999 -> 0.7768 (positive control moves exactly where the LM '
                    'matters); geometry mask reaches 1,793 px (thousands criterion met for the '
                    'mask) but the comparable set is capped by alpha-coverage differences '
                    '(CPU label includes alpha-rejected px: IoU 0.4385)',
}
json.dump(d, open(P, 'w'), indent=1)
print('merged; keys:', list(d.keys()))
