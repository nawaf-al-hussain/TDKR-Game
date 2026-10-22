# Session 48 (round 38) — T1-T8 receipts

STATE at start: remote main=58b7f3a, gh-pages=16a22ce (LIVE), gh-pages-staged-s44=62b4ffd,
s41-city-slice=646a267, s40-user-zip-slice=80274a1, essentials-s36=7c8defc, gh-pages-staged=39298a4
(all matching the brief); session 47 was local-only (main 9c663dc, s41-city-slice e791920;
bundles_s47 verified). No token supplied this session -> local commits + verified bundles.
Anomaly found and repaired: committed s47_t3_reference.py cannot regenerate its own committed
JSON (Python-side SPLIT-zip unwrap was lost before the s47 commit; the JS page kept it).

- T1 (04a69ff + correction dc4280f; branch 9c71876 + 4c5651f) PASS with a CORRECTION that
  supersedes s46's effect keying: per-material EFFECTS come from the compiled scene-instance
  table (307 rows x 36 B @0x5fea0 — s47's "301" undercounted; effect URLs == source.dae
  307/307); the s46 260-B records @0x23308 are NOT keyed by material id. Engine math applied:
  LightMapDC roads Color=Diff*(LM*2.0) -> 119.8->32.8 / 124.7->40.6 mean (x0.27: streets ARE
  dark pre-fog; the x2 verified hardcoded in effects.gla); stride28 mat 302 = AlphaMasking
  Color=Diff*(LM*2+Overbright[default 1.0 from AlphaMasking.bdae]) with SPLIT alpha.r discard
  a<0.3 = a LIGHT DECAL (55.1 -> 111.4); mat 300 billboard = SimpleAdditive colored vColor
  (54.8 -> 10.3). Region check: TC1 bbox JS==Python 0.0 diff; roads bake spread 0.79 of the
  Roads0 page; swap-atlas delta 30.7/37.1; sampled-LM enrichment vs uniform 0.95/1.06 (roads
  lit at page-average). Browser gate city_slice6.html: corr 0.9995-1.0 on 5/5, 0 console
  errors. SPLIT restore + regression recorded.
- T2 (c9d3ebc) HONEST NEGATIVE (calibrated): non-empty-texel enrichment over 1,521/1,526 segs,
  69 textures, 64 shuffled-binding perms — NO family beats the null (z in [-1.22,+0.67]);
  calibration on the GLB-proven seg 695 shows the metric is SILENT even there (own rate 1.000
  vs random 0.993 on 99.3%-non-empty roads_details) — full-bleed pages are silent by
  construction across the whole population; binding evidence remains the s47 render-level TV
  separation (2-8x) + engine==authoring table + T6's zone corr. Metric must not be cited
  either way.
- T3 (ab32f38; branch bf24a20) PASS: browser parses the COMPILED binding table
  (city_slice7.html) — canonical digest JS==Python 1d0f1930..., parity vs authoring 307/307
  names + 305/307 rows (only the 2 FX_Coronas diffs), 0 no-scene rows; cost 4.3 ms vs 56.5 ms
  XML = 13.1x faster; 0 console errors.
- T4 (ccfdf9c; branch a7924fc) PASS: s44's 301 strict-smoothness anchor EXACTLY reproduced,
  corrected decode drops it to 197/1,526 (island2 167->156/1,020) and the failing set decodes
  as UNIT NORMALS (median |n|-1 = 0.0000) — the "non-unit normals" interpretation closed (was
  TC1-read-as-normal); remaining fails = unit-but-not-smooth content noise. Declaration-driven
  JS zone decoder (city_slice8.html): f64 canonical digests match Python BYTE-FOR-BYTE on both
  zones (1,526+1,020 segs, 1.2M verts, 8/8 digests, ~1.1 s per zone), shuffled-descriptor null
  changes positions 145/147 of 200 (remainder = identity mappings).
- T5 (feedb98) HONEST NEGATIVE + STOP: trigger gol.bin templates DO carry a BuiltinBox
  component (9803/18250: [0,0x729ec572]) but with flag 0 (record-driven — the task's
  non-zero-flag premise does not apply); GenerateComponentTemplate @0x368ac0 (ARM, 11.3 KB,
  per-class new+ctor switch) has NO branch for BuiltinBox — no template-default sizes; with
  s47's 0 record blocks, no per-instance extents exist anywhere; volume model stays
  "unvalidated, engine-derived only".
- T6 (9604391; branch 08ec3b3) PASS: zone-scale browser render (city_zone.html) — all 1,526
  segs, compiled bindings, ETC1 LRU (cap 20), per-effect shading; 368,749 tris / 346,772 drawn
  in 46 s JS (Python 101 s); painter heads BIT-IDENTICAL; texture binds 30,500 == Python;
  pixel corr 0.9999 vs Python at 1024x605; peak JS heap 1.37 GB; dark by design (pre-fog).
- T7 (e4da015) PASS: LIVE pages verified by public-URL load — walktest 0 errors / 6 reqs /
  no gc_collision.bin; index.html?userfiles=1 0 errors / 11 reqs; RC untouched (no
  instruction).
- T8: bundles in bundles_s48/ (main_s48_inc 58b7f3a..main; branch_s41_s48 e791920..branch);
  >5 MB audit clean per commit; worklogs updated; final ls-remote recorded. NOT pushed (no
  token).

Capability estimate update: NEW this session = engine lightmap/shader chain verified and
applied (per-effect math incl. Overbright and SPLIT alpha), compiled binding table in the
browser (13x faster than XML), whole-zone (1,526-seg) textured render in-browser at corr
0.9999 with LRU ETC1 caching, declaration-driven two-zone decoder digest-proven, smoothness
question closed. Remaining for option (a): fog + vertical fog + tone/post for outdoor
brightness, streaming/culling (bih) + LOD selection, batch addBatch loop + remaining effect
variants (NormalSpecOverbright, glass, LightmapVCBlend), cross-region navigation + mission
flow — consistent with the s46 (a) estimate of 2-3 sessions for a full-city walkable render;
after s48 the first zone-scale slice EXISTS, so ~(a) has 1.5-2 sessions left.
