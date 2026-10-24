# s57 T1 — glide model DECIDED: the accumulator IS the engine model (branch s56-t1-glide @af90aff, NOT deployed)

## The conflict
s55 note: sink = f0+(f1-f0)(2/pi)|p|, fwd = f5+(f6-f5)(2/pi)|p|+helper. s56 re-read: f0/f1 formula =
acceleration rate of an airspeed accumulator [actor+0x53c] clamped [4,16]; f5/f6 family = vertical term.
Both were implemented (?s5=1 s55-note / ?s5acc=1 accumulator). This session resolves it from code.

## (a) Branch arithmetic + acc reader/writer census (ARM, libKRHP.so; s57_t1_disasm.txt)
RefreshForcesGlide 0x3836b0..0x383a08 (r4=actor this, r5=velocity out, r7=this+0x530+0xc=this+0x53c):
- rate s10 = f0+(f1-f0)*(2/pi)*|pitch_rad|  (0x383704..0x38371c; pitch from [[this+4]+0x18] x pi/180)
- pitch<=0 branch @0x3839dc: acc=[r7] read; if f1>acc: acc += s10*dt; store  (vmlagt/vstrgt)
- pitch>0  branch @0x383724: acc=[r7] read; if f0<acc: acc -= s10*dt; store  (vmlsmi/vstrmi)
- dt = [this+0x2a8] (0x3836f0)
- output 0x383858..0x383880: X = -sin(f6*pi/180)*acc*cos(p)*dt; Y = cos(f6*pi/180)*acc*cos(p)*dt;
  Z = (sin(p)*acc - [f5+(f6-f5)(2/pi)|p| + GetGliderGravityHelper()] - max(blend,f7))*dt
  where blend = f7 + (1-|target-pos|/f9)*(f8-f7) from a virtual-call target (0x383788 blx r3).
- the s10 formula appears ONLY in the acc update; the f5/f6 formula ONLY in Z; helper vadd into Z
  @0x383784 (the s55 note's "helper into forward speed" is byte-refuted).
acc census (whole .text; direct imm 0x53c impossible for VFP (vldr max 1020) so bases are computed
via add #0x530 +0xc; scan covered ldr/str/ldrd/strd imm + decoded add immediates):
- WRITE StartGlide 0x3806a8: acc = [comp+0xc] = f1 = 16 (ldr ip,[sl+0xc]; str [r1+0xc], r1=this+0x530)
- WRITE StartGlideFromGrapnel 0x380b80 + 0x380c48: acc = f1 = 16 (both paths)
- WRITE UpdateNavGlide 0x381bc0: acc = |velocity @[this+0x224..0x22c]| (momentum seed)
- READ RefreshForcesGlide 0x38379c (post-update acc -> velocity), 0x383724/0x3839dc (integration)
- READ UpdateNavGlide 0x381c5c
- NO other readers/writers. (0x538/0x539 are BYTE flags cleared by StartGlide/StartFly/FromGrapnel.)
- CActorBaseComponent::SetGlideSpeed(float) @0x38a120 (Lua SetActorSpeedGlide -> CZonesManager::FindActor
  -> [actor+0xb8]) stores its argument at [actor+0x3b8] - a DIFFERENT field (PlayerComponent ctor/ReInit
  write it; CActorBaseComponent::SaveSave + SlideOnCollisions read it) = the SCRIPTED glide speed, not
  the accumulator. SetInitialGlideAngle 0x380e34 re-proves pitch0 = f10 (0x30), hard default -30.0
  (movt 0xc1f0).

## (b) Plausibility (ground rule 3: independent of the disasm reading)
- acc model: fwd = acc*cos(p) with acc in [4,16] -> Glider(-45) 11.314 u/s, Plunge(-60) 8.0 u/s;
  glide angle 52.8/66.4 deg; distinct per gadget; glide FASTER than a run.
- s55-note model: fwd = 3.5 (Glider) / 4.333 (Plunge) CONSTANT - slower than a run, ~70 deg dive for
  BOTH gadgets identically, no acceleration ever, and NO role for the integrated accumulator field.
- wrong-model control: the s55-note model is kept as ?s5sink=1 and reproduces its old numbers exactly
  (fwd 3.5 / vz -10.0), i.e. the comparison moves.
- GetGliderGravityHelper 0x1e1508 = UpgradesManager map key 0x1f -> SUpgrade+0xc (upgrade-scaled,
  runtime value; in-page 0 = no upgrades).

## Decision + gates (s57_t1_gate.json; runner s57_t1_gate.py; 2 cores sequential)
?s5=1 default = accumulator (seed acc=f1=16 per StartGlide byte-proof); ?s5sink=1 = s55-note control;
?s5acc=1 alias of default; ?s5old/?s5legacy unchanged; ?s5ctl rides the acc model.
| config | pass | errs | soup sha256 | nTri | model | landed | landMs |
|---|---|---|---|---|---|---|---|
| default | PASS | 0 | 00ce7970e45adc85 (= LIVE) | 137893 | - | - | - |
| ?s5=1 Glider | PASS | 0 | 00ce7970 | 137893 | acc | True | 417 |
| ?s5=1&s5plunge=1 | PASS | 0 | 00ce7970 | 137893 | acc | True | 467 |
| ?s5=1&s5sink=1 | PASS | 0 | 00ce7970 | 137893 | sink56 | True | 917 |
| ?s5=1&s5ctl=1 | PASS | 0 | 00ce7970 | 137893 | acc+ctl | True | 450 |
Routes 10/10 on every config. fwd EXACT: 11.314 (Glider, n=25 traj samples), 8.0 (Plunge, n=28),
3.5 (sink56 control, n=55); vz = sin(p)*acc - s56(p) - blend(h) within 1.14 u/s worst-sample - the
residual is the declared blend-distance proxy (in-page height-over-nm vs the engine virtual-call
target, not pinned). ctl: pitch ramp -45->-60, head -6.0 deg EXACT (f6 side-slip), fwd = 16*cos(pitch)
sample-exact (e.g. -45.62 deg -> 11.19 = 16*cos(45.62deg)).

## Verdict vs acceptance
- Arithmetic per branch + every store to 0x53c/0x3b8/velocity: DONE (section a).
- acc reader/writer list incl. StartGlide init: DONE (init = f1 = 16; nav seed = |v|).
- Decision with evidence + controls: DONE (accumulator; sink56 kept behind ?s5sink=1 as control).
- Gates (default digest, routes, s5, ctl): DONE (5 configs PASS, digest = LIVE everywhere).
- Trajectories: DONE (fwd exact; vz within the declared blend proxy).
