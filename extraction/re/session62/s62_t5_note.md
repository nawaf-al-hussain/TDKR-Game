# SESSION 62 — T5: CContainerStateAnimation::Load decode — PARTIAL (2 structural findings landed, exact body open)

## What was attempted
Close the s62 T1 residual: the 6 StateSet templates with count>0 (BatPod, Helicopter,
Helicopter_Bane, Military_Heli, Test_Object, TheBatDrive) blocked by the undecoded
CContainerStateAnimation::Load body. Symbols located: CContainerState::Load = 0x3b85e8,
CContainerStateAnimation::Load = 0x3b45f4 (14 KB, inlined vector-growth paths).
Tooling added: s62_t5_cfg_trace.py (execution-order CFG tracer), s62_t5_dump.py /
s62_t5_scan.py / s62_t5_states.py (residual payload dumpers), s62_t5_decode.py
(CAS candidate sweep). Gate harness: s62_t4_gate.py etc. (see T4 note).

## FINDING 1 (solid, corrects the s61/s62 reader model): payload STR = u32 string-table INDEX
CMemoryStream::ReadString (0x33a0d4) has TWO modes selected by stream flags: the gol-mode
path (0x33a2f0) reads ReadInt() and bounds-checks idx < (end-start)>>2 into the WIRED
string table ([stream+0x28], s61 GOM::Load) - i.e. a 4-byte INDEX, not [len][bytes].
Data-proof: the 6 residual StateSet payloads contain sequential string indexes where
state/animation/script names read: Helicopter reads 0x0fcc..0x0fd1 in ascending payload
order = 'Idle_To_Propeller_Spin', 'propeller_start', 'function Templ313124_1_0_0_0_OnScrip...',
'Propeller_Spin_Idle', 'propeller_rotate', ... (the table itself is written in read order).
NO inline ASCII exists in any residual payload. SIZE-COMPATIBLE with the closure
(STR = 4 B either way) -> the 473/653 exact + 642/653 pass numbers STAND; the s61 note's
"STR" readers (BeastObjectComponent, Destroyable, Motion, Trail...) are index-reads too.

## FINDING 2 (solid): state boundaries + a fixed +82 anim-name anchor
StateSet = [i(count), rep(count: CCS), S x7]; state starts are directly observable via
the name indexes. Helicopter (13 states): state sizes 159/175/131/154/175/131/159/... B;
BatPod: 2 states x 110 B + S x7 tail (7 consecutive 'Idle' idx=75 at the tail - the
count-0 'flat form' was actually reading this tail region). EVERY state in BOTH
templates reads its first CAS name at EXACTLY offset +82 ('-- NONE --' idx 195 for Idle
states, 'propeller_rotate'/'fly'/'land' for the motion states) -> the CCS fixed head is
82 B: [S(name), i, i, c7, f10, ...19 B...]. The f10 block is byte-verified sane on both
templates: [0,0,0,0,1,1,1,0,0,20.0] at payload +0x17 (floats are byte-consecutive, no
alignment padding; the c7 bools at +0x10).

## What blocks the exact body
With head=82 the per-state remainder (28..77 B) cannot fit the address-order trigger
element [i6, f, i2, S, i] = 44 B (e.g. state 'Propeller_Spin_Idle' = 131 B = 82 + CAS +
n2*44 must hold animName@82 AND scriptName@110 -> the trigger's S would need offset 28
inside a 44 B element that starts BEFORE the anim at 82). Conclusion: the inlined
trigger/anim loop BLOCKS are compiler-reordered in the 0x3b88cc..0x3b8974 region
(address order != payload order there), so the element layout needs a real CFG trace of
the loop bodies (the s62_t5_cfg_trace.py walk stops at the vector-fill noise; loop
iteration-2 semantics not yet handled). CAS itself contains further nested string lists
(trace groups: [S,i], loop[S,i], loop[S,i,i,i,i], i, loop[S,i,[i,i,S]], i, i...).

## Status
- T1 residual NOT closed: exact stays 473/653 (72.4%), pass 642/653 (98.3%), 6 fails.
- Findings 1+2 are prerequisite corrections any follow-up session needs (est. 0.25-0.5:
  CFG-trace the trigger loop bodies at 0x3b88cc..0x3b8988, then sweep CAS against the
  6 payloads with the +82 anchor and the sequential-name constraint net).
- No closure/spec changes were committed for T5 (zero speculative rules - the project's
  zero-fitted-rules discipline holds).
