# Session 35 (round 25) notes

## State
- Remote unchanged: main 8842b35, gh-pages f22b098 (v17 live), gh-pages-staged 9a9fb3b.
- Local main after this session: 9b95005 (28ea343 T1, 50fcede T2, 369c48a T3,
  17fd443 T4, 1d76e43 T5, 9b95005 T6 on top of 93c956c).
- NINE rounds (17-25) now exist only in sandbox bundles. Push requested.
- Bundles: download/bundles_s35/main_s35_inc.bundle (incremental, requires
  8842b35) + bundles_s35/essentials_s35.bundle (small scripts/notes bundle).

## T1 animation — PASS
- r24's 28-B record walk @0xcd00 was MISALIGNED 4 B. True container {663,
  0xccfc} @0xccf4; record = [tickStart][tickEnd][0][0][tablePtr][dist][0];
  663 chunks tile the packed timeline 0..3,394,830 exactly.
- Stream table: entry0 = (nStreams, len0); data base = TBL + (nst+1)*8 - 4;
  663/663 decode.
- CLIP MAPPING (engine-derived): clip windows [ts,te] ARE packed-timeline
  intervals; segments = storage chunks; getBlock walks the block chain by
  time; grab() prefetches the next chunk when clip[8] > seg[4] and WRAPS to
  the chunk covering clipStart (loop). r24's "static-legs run" = seg6 is the
  tail of _004_idle_stand_check1; true run = segs 11+12, walk = seg11.
- Gait battery: walk period 1070 ms (ac 0.75 vs null 0.14), anti-phase
  -0.96 @ lag 500 ms; run period 670 ms (ac 0.75 vs null 0.18), anti-phase
  -0.992 @ 340 ms; foot z 1.10/1.05 m; idle negative control clean.
- Batch: 921/921 clips decode, span-in-window 921/921, smoothness ratio
  median 0.170 (zero > 1), wrap median 0.0 deg.
- batman_s35_anims.glb: 3 chunk-assembled animations; three.js AnimationMixer
  vs numpy row-form FK: REST 0.0002 cm, 12 samples worst 0.0884 cm.

## T2 cape — PASS (absence proven)
- Full-file stride-80 sweep, band-criterion edge score + layout + variance:
  positive control body @0x4b5c (edge 0.414 vs shuffled-null 0.065); all
  394/194-vertex survivors = body-zone aliasing or straddle artifacts with
  periodic bboxes. Gap zone = a table, not vertices. Declared cape streams
  @0x5cc24/0x6901c remain all-zero. Engine: Load = cloth params only;
  skin/updateBuffer = runtime buffers. Cape (394v) + cape_down (194v)
  ABSENT from file = runtime cloth. Confirms r34 with nulls.

## T3 navmesh — PARTIAL (field map solved; portal zone open)
- Counts reconciled: [u16 0x7868][BE f32 soup = 30,905 xyz][marker with cell
  count 0x7b9f = 31,647][31,647 triangle cells x 15 B][portal zone][pad].
  r34's "30,822 cells" = soup float count; the 15-vs-16 B distinction (cells
  are 15 B packed, engine stores into 16-B-stride vectors) is why the field
  map stayed open in r34.
- Field map PROVEN: [v0 v1 v2 | n0 n1 n2 | regionId u16 | char 0];
  0xFFFF = none; symmetry 1.0000 vs null 0.0000; shared-2-vertex 1.0000;
  regionId 0..1020 == exact component partition (two independent signals).
- Routes 0/34 on the cells-only graph: 1,021 regions; cross-region links are
  explicit portal data @0xce337+ (NOT decoded; named resisting block).
  Zero shared/coincident vertices across regions (exact tests).

## T4 triggers — PASS
- r34 demo's "9.5 m inside" = the ASSUMED 10-m half-extent hardcoded in the
  demo (dh < 10); position was data-determined, extents assumed.
- Extents source: OBB at CComponentTrigger+0x58 = 64-B copy from an engine
  global template (GOT slot 0xc07f70, R_ARM_RELATIVE 0xa4d9c, runtime-init).
- Field semantics CORRECTED: f0-f2 = position, f3-f5 = rotation degrees,
  f6-f8 = owner scale (r34's "H field" = scale-x).
- Null profile: spawn-in-volume vs street-in-volume = 17.8% vs 0.4% (39.5x)
  at B=1 m; spawns' nearest-trigger distance median 0.0 m vs street 43.7 m.
  Typical Lua-entry triggers are spawn/encounter-coincident, ~1-2 m at
  scale 1; a few city-scale triggers exist (scale up to 1682).

## T5 Lua — PASS (55 errors = harness bug)
- The 55 "non-string error object" failures = r34 harness bug: value-returning
  stubs pushed results onto the main state L instead of the coroutine Ls;
  fengari returned the C function itself as the result; the script's use of
  that value raised with the FUNCTION OBJECT as the error value; r34's
  lua_typename() printed Uint8Array bytes ('nonstr:102,...' = "function").
- Corrected run: 522/541 = 96.5% complete. 19 remaining errors ALL NAMED
  (9 missing APIs, 8 missing constants MC_MAX_*, 2 structural).
- Three-way: 78 no-stubs-needed / 440 stub-presence / 4 semantic-values / 19.
- 5.1 vs 5.3: construct census = ZERO divergent constructs in all 541 scripts
  (0 tostring, 0 %d, 0 division, 0 unpack/setfenv/os/io; 2 '#') => shim pass
  vacuous by census; probe table recorded.

## T6 first playable — DONE
- gh-pages/playable/ (copy-side only): Batman glb + 12,512-tri collision
  patch + WASD capsule controller + speed blend idle<->run + spatial Lua
  triggers (fengari-web) with the T4 volume model (B=1.5 m declared assumed).
- Headless smoke: 80/80 ground hits; 2 triggers fired naturally
  (405674, 2100005) with real Lua chains (Disable/Disable/HideObject).
- FPS: no real-GPU browser in sandbox; no performance evidence.

## Estimate (evidence-backed)
- IN: walkable world (collision soup, 271,589 tris; patch demonstrated in
  T6), character renderer + idle/run/jump (T1/T6, three.js-verified),
  Lua shim (522/541 scripts complete, T5), positional Lua triggers (T4/T6),
  animation system for all 921 clips via the chunk rule (T1).
- NOT IN: navmesh-driven movement (portal zone open, T3), cape cloth
  (absent from file, T2), glide/grapple/combat/AI/mission flow/audio/UI,
  exact trigger volumes (engine template extents undecoded), FPS evidence
  (no real GPU).
- First playable milestone the evidence supports: walk-as-Batman on the
  collision ground of GothamCity with idle/run blending and positional Lua
  triggers firing real mission-chain scripts — DEMONSTRATED in T6 (patch).
