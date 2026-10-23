# s55 T2 — glide fidelity second signal: float naming, s_glide* verdict, trajectory comparison

## (a) CComponentGlide float naming (21 floats; Glider values 4,16,14,4,16,1,6,0,2,16,-45,-60,30,35,1.25,0.05,45,0.5,30,30,40)

Layout (s54, confirmed): [vptr@0][int1@4][f0..f20 @8..0x58][int2@0x5c].

| f# | value | read site (ARM, libKRHP.so) | meaning | evidence |
|----|-------|------------------------------|---------|----------|
| f0 | 4 | RefreshForcesGlide 0x383704 `vldr s15,[r6,#8]` | sink at level flight (u/s) | PROVEN: sink = f0 + (f1-f0)*(2/pi)*abs(pitch_rad) (0x38370c-0x38371c, pool 2/pi 0.63662 @0x3839f8) |
| f1 | 16 | RefreshForcesGlide 0x383708 `vldr s14,[r6,#0xc]` | sink at steepest pitch (u/s) | PROVEN (same block) |
| f2 | 14 | not read by the 6 glide functions | (unused by physics; s54 guess n/a) | site-scan negative |
| f3 | 4 | not read | (unused) | site-scan negative |
| f4 | 16 | RefreshForcesGlide 0x3836e4 `vldr s11,[r3,#0x18]`, r3=[r4+4] | pitch source: [r4+4]-object field, degrees (pitch_rad = f4*(pi/180), pool 0.0174533 @0x3839f4) | PROVEN formula; holder object = actor component at CActorBaseComponent+4 (not the gadget) |
| f5 | 1 | RefreshForcesGlide 0x38374c `vldr s20,[r6,#0x1c]` | forward speed at level pitch (u/s) | PROVEN: speed = f5 + (f6-f5)*(2/pi)*abs(pitch_rad) + GetGliderGravityHelper() (0x38374c-0x383784) |
| f6 | 6 | RefreshForcesGlide 0x383750 `vldr s13,[r6,#0x20]` | forward speed at steepest pitch | PROVEN (same block) |
| f7 | 0 | 0x38375c `vldr s21,[r6,#0x24]` | proximity-blend min | PROVEN: blend = f7 + (f8-f7)*(1 - dist/f9), dist = |deltapos| (0x383780-0x3837cc) |
| f8 | 2 | 0x383760 `vldr s15,[r6,#0x28]` | proximity-blend max | PROVEN |
| f9 | 16 | 0x383798 `vldr s12,[r6,#0x2c]` | proximity-blend distance divisor (u) | PROVEN (s15 = sqrt(...)/f9 @0x3837cc) |
| f10 | -45 | SetInitialGlideAngle 0x380e78 `ldr r1,[r0,#0x30]`; StartGlide 0x3806xx `ldreq r1,[r0,#0x30]`; StartGlideFromGrapnel | initial pitch, DEGREES, stored at [actor+0x558] | PROVEN; engine hard default -30.0 (0xc1f00000 @0x380e6c) when [actor+0x4fc]!=1 |
| f11 | -60 | StartGlide (n=2), StartGlideFromGrapnel 0x380axx `ldr r3,[r3,#0x34]` | initial vertical-speed magnitude factor (dive entry) | SITE-ATTESTED (role: paired with f10 in entry setup) |
| f12 | 30 | not read by the 6 functions | (unused) | site-scan negative |
| f13 | 35 | StartGlideFromGrapnel 0x380axx `ldr r5,[...]` | grapple->glide entry parameter | SITE-ATTESTED |
| f14 | 1.25 | StartGlide rw (n=3, str r0,[r4,#0x40]) | runtime state field written at glide start (timer/phase scale) | SITE-ATTESTED (written, not read, in these blocks) |
| f15 | 0.05 | StartGlide w | runtime state field zeroed/updated at start | SITE-ATTESTED |
| f16 | 45 | not read by the 6 functions | (unused) | site-scan negative |
| f17 | 0.5 | not read | (unused) | site-scan negative |
| f18 | 30 | SetInitialGlideAngle 0x380e34 pool-annotated `ldr r3,[pc,#0x50]` = 0x8871e0 GOT chain (NOT a component read - annotation artifact) | (not a component float read) | corrected |
| f19 | 30 | not read | (unused) | site-scan negative |
| f20 | 40 | StartGlideFromGrapnel `ldr r2,[r2,#0x58]` | grapple-entry clamp (speed cap?) | SITE-ATTESTED |

int2 = 600 (s54) — not consumed by the 6 functions.

Engine-implied glide at pitch0 = -45 deg, no upgrade:
speed = 1 + 5*(2/pi)*(45*pi/180) = 3.5 u/s; sink = 4 + 12*(2/pi)*(45*pi/180) = 10.0 u/s;
altitude lost per metre = 10/3.5 = 2.857 m/m.

## (b) Trajectory comparison (live integration_lazy ?s5=1, real zip, 60 samples / 983 ms)

| measure | staged (decoded ?s5=1) | staged (?s5legacy=1) | engine-implied |
|---|---|---|---|
| mean horizontal speed | 16.016 u/s | 16.02 u/s | 3.5 u/s |
| mean vz | -13.42 u/s | -10.084 u/s | -10.0 u/s |
| altitude lost per metre | 0.531 | 0.580 | 2.857 |
| alt lost / horiz dist | 8.35 u / 15.73 u | 8.66 / 14.93 | - |
| landMs | 1000 | 950 | - |

FINDINGS (fidelity gaps in the staged slice, exact fixes):
1. Staged sink = f0 + (f1-f0)*|pitch_rad| = 4+12*0.7854 = 13.42 (matches measured -13.42 exactly) —
   the page is MISSING the engine's (2/pi) normalization: engine sink at -45deg = 10.0.
2. Staged forward speed is a constant 16 u/s (s53 placeholder value = f1, the MAX SINK field,
   misused as speed). Engine speed = f5 + (f6-f5)*(2/pi)*|pitch_rad| = 1..6 u/s.
3. Clip lengths: glide span 983 ms vs _057_glide_idle 2167 ms (loopable - benign);
   landing excerpt 450 ms of _065_glide_idle_to_run 667 ms (engine transition, kept).

## (c) Wrong-parameter control: PASS
decoded vs legacy placeholders move every measure (vz 13.42 vs 10.08, alt/m 0.531 vs 0.580,
landMs 1000 vs 950) — the comparison metrics are parameter-sensitive (not saturated).

## s_glide* .bss statics: RESOLVED — DEAD (no writer AND no reader)

Correction of the s54 record ("GOT-indirect, 7-13 read sites each"): those site counts came
from a decoding artifact (full 32-bit word treated as the pc-relative offset — a real
`ldr rX,[pc,#imm]` word 0xE59Fxxxx can never match; the 94-97 'sites' were instruction
words whose value coincidentally landed in the window).

Exhaustive search (scripts s55_t2_glide_naming.py / _writer_final*.py / _final6.py):
- B1 pool-absolute words == any s_glide* address anywhere in .text: 0
- B2 movw/movt building any base in [0xc16000,0xc19000]: 0
- B3/B4 two-step GOT chains (`ldr rD,[pc,#imm]` + `ldr rE,[pc,rD]`, got = site+8+W):
  160 REAL chains into the CLevel-static window — g_sceneManager 97, s_batpodSounds 18,
  s_thebatSounds 18, joystick statics 1-2 each — but ZERO chains for the s_glide* slots
  (0xc080c8..0xc080ec) and ZERO str landing on s_glide* via any neighbor pointer.
  Scanner validated positively: it finds the real accessors of neighboring statics.
- k_glideWallEvadeDistance/Min/MaxAngle (.data, values 6.0/1.0/10.0): whole-file word scan
  finds references ONLY in DWARF debug metadata (0xd06678+0x10k) — code-dead too.

VERDICT: all ten CLevel::s_glide* floats and the three k_glide* constants are DEAD symbols.
.bss = zero-init, never written, never read => runtime values 0.0 forever; they CANNOT
affect glide physics. The engine glide model is fully determined by the 21 CComponentGlide
floats (above). The s54 open item closes with no further RE needed (0.25-0.5 session
estimate freed).

## Required slice fix (exact)
- sink: 4 + 12*(2/pi)*abs(pitch_rad)          [add the (2/pi) factor]
- fwd speed: 1 + 5*(2/pi)*abs(pitch_rad) + upgrade(0)   [replace constant 16]
- at pitch0=-45deg: speed 3.5, sink 10.0, alt/m 2.857
Not applied to any deployed page this session (analysis-only task).
