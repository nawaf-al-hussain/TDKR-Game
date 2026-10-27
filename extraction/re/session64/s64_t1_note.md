# SESSION 64 — T1: the 13 residual template fails CLOSED (engine-true); closure exact 588/653 (90.05%), pass 648 (99.23%), fail 0

## Root cause of all 13 OOB fails (one cause, code-proven)
The s63 SlowMotion (list5) element spec carried a spurious trailing int ("param") that
has NO counterpart in the engine. CContainerStateAnimation::Load is ONE function
(0x3b45f4..0x3b6498; single push/pop pair):
- Sound list inline from 0x3b4610 (STR + count + tracks STR,i,i,i,i)
- Script from ~0x3b4bb8 (inline ldrb @0x3b57dc)
- TrackEffectEvent loop 0x3b5d0c..0x3b6008 (count @0x3b5d18, tracks i,i,STR,i,c;
  stream ldrb @0x3b5fd4)
- Effect loop 0x3b600c..0x3b61e8 (count @0x3b600c, tracks i,i,STR,STR,c; ldrb @0x3b61b8)
- SlowMotion: LIST count @0x3b61ec, per element ReadInt(k) @0x3b62a0, then k x
  [ReadInt, ReadInt, ReadFloat, ReadFloat, ReadInt, ldrb @0x3b643c, ldrb @0x3b6450]
  = (i,i,f,f,i,c,c) 22 B - and RETURN at 0x3b6494. NO per-element param read exists.
The s63 "param" was a solver artifact that cancelled on the calibration set (whose
templates have SlowMotion count = 0) and bit the 13 behaviour payloads (the first
templates with SlowMotion count > 0). Walk-verified by hand on Enemy_Melee_Movement
state 1 and Batman_30 state 0: tracks decode to real floats (1.0/0.2, 0.4/1.0, 3.0/2.0)
and consecutive string indices (0x596..0x59a) with the no-param shape.

## Two more code-derived fixes (bounds -> exact, +20 templates)
- CameraParams (0x7d561d33, reader 0x3bf038..0x3bf184): the s63 spec missed TWO stream
  bytes (c,c) between the 3rd head int and the first STR (stream ldrb pair
  @0x3bf0e0/@0x3bf0f4). 77 -> 79 B. Fixes ALL 18 tail:2 Camera_* templates.
- Glide (0x0110ce1f, reader 0x3c0938..0x3c0a5c): stream = i + 21xReadFloat + i = 92 B
  (read-site census; matches the independent s55 decode). s63 had 20 floats (88 B).
  Fixes Glider + Glider_Plunge (tail:4).

## Closure (denominator 653; engine-true specs only, zero fitted rules)
- exact 588/653 (90.05%), bounds-pass 60, pass 648/653 (99.23%), fail 0, na 5.
- s62 -> s63 -> s64 exact trajectory: 313 -> 552 -> 588; fails 13 -> 0.
- Remaining 60 bounds-pass = per-component trailing under-reads, NOT a common trailer:
  tail:4 x27 across >= 6 distinct readers (census: Collectible 0x28091330 x6,
  ActorSpecialEffects 0x592ce07c x4, BuiltinBox 0x729ec572 x2, BatpodHandle
  0x0d1839c4 (BatPod), TheBatHandle 0x222500f6 (TheBatDrive), VehicleSoundEvents
  0x4de3f7c4 x2, + singletons); tail:16 x7 (Batarang family), tail:8 x5, others
  1-3 templates. Tail VALUES vary (ffffffff / 503.0f / string indices / 0) = real
  trailing fields per reader, fixable by the same read-site census method
  (~0.25-0.5 session for the tail:4 class).

## Calibration and nulls (all PASS)
- Calibration: every previously-exact template still exact (552 -> 588 adds only);
  fail = 0.
- NULL-perm (shuffled id->spec): exact 24 (real 588).
- NULL-rot7 (payload rotate 7): exact 367.
- NULL-ss-swap (l2/l3 shapes swapped): exact 0; all content templates fail.
- NULL-param-restored (deliberately re-inserting the s63 param): content templates
  (Batman_01_Movement, Enemy_Melee_Movement) FAIL again = the wrong shape is rejected.
- NULL-cam-revert: 0/8 Camera templates exact when the c,c fix is reverted.
- NULL-glide-revert: 0/2 when the 21st float is removed.

## Artifacts
s64_t1_faildump.py/.json (instrumented OOB positions), s64_t1_ccstrace.py (state-level
tracer), s64_t1_rawdump.py (string-annotated dumps), s64_t1_l5variants.py (3-shape
comparison: no-param 568/0 vs s63 552/13 vs param-after-list 473/97),
s64_t1_closure.py, s64_t1_closure2.py -> s64_t1_closure.json + s64_t1_final_specs.json
(the fixed table), s64_t1_tails.py (tail census), s64_t1_readcensus.py (reader
read-site census). capstone reinstalled in the fresh environment.
