# s48 T2 — non-empty-texel enrichment over all segments: HONEST NEGATIVE (metric has no power; calibrated)

## Run as prescribed

- Population: 1,521 of 1,526 GothamCity segments (5 dropped: no TC0 declaration in
  their material's batch_info or misaligned vb/stride), 69 distinct bound diffuse
  textures, vertex TC0 samples per segment (END-offset declarations).
- Mask (per texture): alpha<64 (SPLIT alpha.pvr, upsampled to rgb dims) OR near-black
  (mean rgb < 16). Per-texture uniform-random-UV non-empty rate from 20,000 samples.
- Metric per segment: observed non-empty rate of its UV samples on the bound diffuse
  / the texture's random-UV rate. Family aggregate: vertex-weighted mean.
- Null: 64 label-shuffle permutations of the material->diffuse binding; per-family
  z = (real - null_mean)/null_std.

## Result: NO family beats the shuffled-binding null

| family | segs | verts | real enr | null mean+/-std | z | log2 ratio | verdict |
|---|---|---|---|---|---|---|---|
| billboard | 183 | 24,767 | 1.157 | 1.310+/-0.141 | -1.09 | -0.18 | not decisive |
| facade | 342 | 312,403 | 0.950 | 0.950+/-0.087 | +0.00 | +0.00 | silent |
| other | 107 | 67,981 | 0.959 | 0.921+/-0.056 | +0.67 | +0.06 | not decisive |
| props | 278 | 81,284 | 0.940 | 1.115+/-0.149 | -1.17 | -0.25 | not decisive |
| road | 157 | 67,767 | 1.137 | 1.530+/-0.322 | -1.22 | -0.43 | not decisive |
| rooftop | 173 | 74,428 | 1.061 | 1.054+/-0.148 | +0.04 | +0.01 | not decisive |

## Calibration (ground rule 2) — the metric fails on a KNOWN-GOOD binding

seg 695 (roads_details; its UVs are the s46 GLB-bit-exact ones, s46 render matched the
deployed street at corr 0.97): observed rate 1.000 vs own-texture random rate 0.993
-> enrichment 1.007, z vs 89 other textures +0.53. roads_details is 99.3% non-empty at
the near-black threshold — the "opaque full-bleed pages are silent by construction"
caveat applies to essentially the WHOLE population, not a few families: the vertex-UV
non-empty rate is dominated by texture layout, not binding correctness. Even where the
mask has structure (Street_Alpha SPLIT: the decal's UVs land at rate 0.24 vs random
0.43 — BELOW random, by design: it is a cutout decal sampling its own opaque region),
"more non-empty than random UVs" is simply not a property of correct bindings on this
data set. Threshold tuning to make it pass would be p-hacking and was not done.

## What does carry population-scale binding evidence

- Render-level (spatial) test with power: s47 T3 5-block gate — real-binding renders
  separate from shuffled-texture AND random-texture nulls by 2-8x TV on all 5
  declaration classes, corr(JS, Python) 1.0000/0.9998. That test uses the full
  triangle-coverage spatial signal, which is where the discrimination lives.
- Engine-vs-authoring table agreement (s47 T1: 301/301 names, 299/301 rows exact).
- The s48 T6 zone render (all segments, engine bindings) pixel-correlated against the
  Python render extends the render-level check to the whole zone.

Verdict: the prescribed enrichment metric is UNINFORMATIVE on this data (calibrated
honest negative); it must not be cited as either support or refutation of the binding.

## Artifacts

s48_t2_enrich.py (+ s48_t2_enrich.json), s48_t2_calib.py (+ s48_t2_calib.json).
Bug fixed en route: SPLIT alpha mask OR'ed against rgb dims without resampling
(ValueError on 2048 vs 1024) — alpha upsampled xN to rgb dims in both scripts.
