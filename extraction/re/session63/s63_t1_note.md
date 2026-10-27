# SESSION 63 — T1: CContainerStateAnimation CLOSED (engine-true, zero fitted rules)

## Headline
The s62 residual (6 StateSet templates, CContainerStateAnimation::Load body open) is CLOSED.
Closure re-run (s63_t1_closure3.py, denominator 653): **exact 552/653 (84.5%), pass 635/653
(97.2%), fail 13, na 5** — vs s62: exact 473 (+79), and the pass mix changed HONESTLY (below).

## The decoded reader (all from disassembly + byte-verified against payloads)
- CComponentStateSet::Load (0x3b8e9c..0x3b9018): `i(count)`, count x CContainerState::Load,
  then STR x7, RETURN (nothing after the 7 strings).
- CContainerState::Load (0x3b85e8..0x3b8988): **82-B head** =
  `STR(name), i, i, c7, f, f, i, f7, c, f, i, i, i, c2, i(animN)`,
  then animN x CContainerStateAnimation::Load (stride 0x40),
  then `i(nT)`, nT x **trigger = [i6, f, i2, STR, i]** (44 B; vector stride 0x2c).
  The s62 "+82 first CAS name" anchor = the head is exactly 82 B and CAS's first read is a STR.
  s62's "f10 at +0x17" was really [f, f, i, f7] (the i at +27 read as a 0.0 float in data).
- CContainerStateAnimation::Load (0x3b45f4..0x3b7928, 13.1 KB - the symbol table LIES at
  0x3b555c; the fill paths extend to 0x3b7928): `STR(animName)` + FIVE lists, each
  `i(count)` + count x element:
  1. Sound: element `[STR name, i k, k x (STR, i, i, i, i)]` (20-B tracks; vector16)
  2. Script: element `[STR name, i k, k x (i, i, STR, c)]` (13-B tracks - ONE INLINE ldrb @0x3b57dc)
  3. element `[i k, k x (i, i, STR, i, c)]` (17-B tracks; inline ldrb @0x3b5fd4)
  4. element `[i k, k x (i, i, STR, STR, c)]` (17-B tracks; inline ldrb @0x3b61b8)
  5. element `[i count, i param, count x (i, i, f, f, i, c, c)]` (22-B tracks; TWO inline
     ldrb @0x3b643c/@0x3b6450; stream layout count-then-tracks-then-param is byte-identical
     to param-first - closed as [count, rep, param] for 'last' semantics; the CContainerTracks_
     {Sound,Script,Effect} copy-ctors at 0x3b7928+ confirm the three track families)
- **The s62 blocker dissolves**: the trigger element [i6, f, i2, STR, i] = 44 B is REAL and
  lives AFTER the CAS list (the s62 confusion came from wrong state boundaries: the 82-B head
  is NOT 4-aligned, so states pack at 2-mod-4 offsets; s62's "110-B BatPod states" and the
  "compiler-reordered inline trigger loop" were artifacts of 4-aligned reading).

## Tooling corrections that made this work
- The s62 CFG tracer followed fall-through only and died on revisits; the s62 skeleton scan
  hardcoded stream-register r4 (CAS uses r6 in later loops) and a 12-instruction provenance
  window, which MISSED the five inline ldrb byte-reads. Both fixed (s63_t1_inline.py +
  grep-level scan of the full 13.1 KB disasm): exactly FIVE stream byte-reads exist.
- State boundaries come from the walk itself (byte-packed), not signature scanning.

## Closure detail
- The 6 s62 OOB fails: Helicopter, Helicopter_Bane, Military_Heli, Test_Object -> **EXACT**
  (SS walk + all remaining components close the payload byte-exactly, tail 0).
  BatPod, TheBatDrive -> bounds-pass with the DOCUMENTED tail:4 class (last component
  under-reads 4 B; same class as the existing 27 tail:4 templates; SS part exact at 252 B).
- +75 previously "bounds with huge tails" templates (Batman_*/Enemy_* behaviour payloads
  whose StateSet was comp0 and flat-read as 32 B) now walk DEEP: most close EXACT.
- Remaining 13 fails (up from 6 because the nested spec EXPOSES content the flat spec
  silently under-read): Batman_01_Movement, Batman_02_Flying, Batman_04_Combat,
  Batman_08_Takedown, Batman_30/31/32/33_Combat_*, Batman_39_Combat_CounterStrike,
  Enemy_Melee_Attack, Enemy_Melee_Hurt, Enemy_Melee_Movement, Enemy_Ranged_Hurt.
  ONE cause: deep multi-element CAS track content in the behaviour payloads (the walk
  consumes 27+/55 states in Batman_01_Movement before hitting a list5-class variant).
  Est. 0.25-0.5 session with the same data+code method (the failing offsets are pinpointed).
- na 5 = empty component lists (unchanged, by construction).

## Calibration and nulls (all PASS)
- Calibration: count=0 StateSet templates still close (the nested spec reduces to the flat
  form); no previously-exact template regressed.
- NULL-perm (shuffled id->spec): exact 24 (real 552) - discriminative.
- NULL-rot7 (payload rotate 7): exact 347 (real 552).
- NULL-ss-swap (swap list2/list3 shapes inside the StateSet spec): the 4 content templates
  drop to exact 0 (pass 2 = the empty-CAS BatPod/TheBatDrive, order-insensitive as expected).
- Track-shape search: 48 shape combos close the 6 SS payloads byte-wise; the ENGINE-TRUE
  combo is pinned by the five inline ldrb sites (field types + order are code-derived).

## Artifacts
s63_t1_dump_states.py, s63_t1_cas_skeleton.py/.txt, s63_t1_solve.py, s63_t1_statespec.py,
s63_t1_search.py, s63_t1_verbose.py, s63_t1_helidump*.py, s63_t1_inline.py/.txt,
s63_cas_full.txt, s63_t1_make_closure.py -> s63_t1_closure3.py -> s63_t1_closure.json +
s63_t1_final_specs.json (the nested StateSet spec is now in the id->spec table).
