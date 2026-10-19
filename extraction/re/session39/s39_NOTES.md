# Session 39 (round 29) notes

## State on entry
Remote: main fbadb25, gh-pages 39298a4 (v21 LIVE), gh-pages-staged 39298a4,
essentials-s36 7c8defc — all as expected; bundles_s38 redundant (not re-verified).
No credentials -> no push; local commits + verified bundles.

## T1 (44cd719) — LIVE verification: PASS
All metrics on the PUBLIC URLs (no local copies): IoU 0.9421 (lying null
0.0229, wrong-pose 0.89, shifted 0.002); aspect 1.312 vs 1.279; feet 0.095 m;
albedo-to-texture 5.0 (grey 155.1); texture presence std 21.1/28.2; UV seams
48.9% integer-offset pairs at 100% texel match (shuffled null 25.6%); FK parity
idle@0.5 0.015 cm / idle@2.0 0.025 / run@0.1 0.005 / run@0.5 0.006 cm (wrong-
time nulls 30.0/157.8 cm); idle+run advancing (30/158 cm deltas); console
errors 0; network 8/8 200. pipeline.html LIVE + real 895 MB zip: READY 20.5 s,
0 errors, 5/5 200. GATE extended: texture presence + advancing (vertex-delta
0.293 m real vs 0 null); silhouette-level advancing check measured INSENSITIVE
(t2-vs-truth 0.940 == wrong-pose 0.89) and is reported, not gated.

## T2 (ef3e8cb) — PARTIAL: the .tga format is NOT PVRTC
CRACKED at structure level: 8 B per 4x4 block, LINEAR order; bytes0-2 = RGB888
endpoint A; byte3 = flags (44 uniq, mean 8.0); bytes4-7 = 16x2-bit modulation
(hist [0.61,0.12,0.12,0.15]; checkerboards). Explains all prior failures (see
s39_t2_FINDINGS.md). Named next: caller @0x800f84 disasm (start found; Thumb
awareness needed) + mod-weight fit from uniform-mod blocks; then JS/Py decoders
+ street patch. The engine-vs-file mismatch is now PROVEN, not assumed.

## T3 (2f012ab) — shortfalls documented
s38 per-object test reproduced verbatim (n=19, real-inside 0.286 vs null
0.0000, rank 0.024) — discriminative but n<<100. NEW: 230 GetDistFromMC
comparison sites in gol.bin templates, 21 unique thresholds [5..700],
pcts [5,7,20,50,400] vs trigger rxy-half p50 0.71 m -> script radii are
AI-awareness distances, NOT volume radii (independent negative).
LNObject enum NOT achieved: repaired walk dump has LOAD-ORDER ids (0 overlap
with game object ids); positions not captured. Named next: rerun the walk with
TObjectData id+TRS capture. Volume model: unvalidated, engine-derived only.

## T4 (1a7ab6d) — static evidence table
16 constant-like names in the 541 scripts; 7 as .so strings; FACE_* family
shares one literal pool (0xc0b018-0xc0b050) = registration table EXISTS.
MC_MAX_DISTANCE: ZERO pool refs (4th independent negative) -> ASSUMED=10.0.
Runtime hook BLOCKED: Lua glue is Thumb; needs a Thumb LDR-literal xref scan.
The 100-script fengari comparison is DONE (s38: 100/100 + math.random shim).

## T5 (1c66c1e main, f223bb1 gh-pages staged) — 2/4 classes validated
PROPER permutation test (200 label shuffles): IDLE xy_rate 0.270 vs null 0.553
p=0.000; AIR zr 1.44 vs 0.45 p=0.000; LOCO p=0.33 and TURN p=0.41 NOT
validated (reported per-item). v1 test was void by design (pass rate invariant
under pairing shuffle) — caught by rule 2, replaced. PAGE WIRED: states
resolve through the gol.bin table with embedded-clip fallbacks; speed only
selects the STATE. Gate regression PASS.

## T6 — not re-attempted (time-box spent on T2/T3/T5)
s38 banked the negative: clearance-weighted A* + clearest-of-8 steering =
13/40 (baseline 12/40) -> "missing agent-radius clearance" REFUTED; failures
stuck_wall 14, fell 6, step_too_high 5, no_ground 1 = collision-layer/data
issues (missing walkable flags, step geometry). NAMED NEXT (different follower
strategy): analytic wall-slide (project the desired velocity on the collision
plane) + contiguous bug-walk around obstacles, then >=40 routes; plus the
data-layer fixes.

## T7 (8de935b main mirror, a1bf3b1 gh-pages staged)
Clear input errors: APK detection, non-TDKR zip, v1.1.6b layout check.
BANKED from s38: 6/6 skeleton digests; lazy memory 13.1 MB heap peak
(target <300 MB met); Firefox/WebKit not installed (Chromium only).

## T8 — migration plan (see s39_t8_migration.md)

## T9 — delivery
main: 44cd719, ef3e8cb, 2f012ab, 1a7ab6d, 1c66c1e, 8de935b (+ T8/T9 commits).
gh-pages staged: f223bb1 (T5), a1bf3b1 (T7) on top of 39298a4 (v21 LIVE).
PUSH REQUIRES FRESH TOKEN (none supplied this session).
