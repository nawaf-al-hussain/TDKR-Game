# s54 T3 — state-table clip selection for glide/grapple (receipt)

## Sources
- State table: `extraction/re/session36_t3_statetable.json` (s36; mechanism: Lua
  ActorSetState -> engine CAnimationGraph from batman_anims.bdae; the table maps
  state names to clips by name correspondence + Lua usage counts).
- Lua states: `extraction/re/session36_t3_lua_states.json`
  (Glide_Idle 3 uses, Grapnel_Horizontal_To_Glide_Idle 6, Grapnel_Fly_Idle_Horizontal 1,
  Glide_Idle_To_Grapnel_Horizontal, + parachute family).
- s39 per-class clip signature validation stands (sign conventions verified there).

## Table entries relevant to the slice
| state | clips (table) | slice use (s54) |
|---|---|---|
| Glide_Idle | _057_glide_idle (2167 ms), _059_glide_parachute_idle | glide loop = **_057** (unchanged; table #1) |
| Grapnel_Horizontal_To_Glide_Idle | _062 wall_contact_idle_to_glide family, _065_glide_idle_to_run (667 ms) | landing transition = **_065** (NEW this session; was a hard switch to _008_run) |
| Grapnel pull | Lua names Grapnel_Loopable_Pull_Start; battery _089_grapnel_pull (1899 ms), _088_grapnel_shoot (432 ms) | pull = **_089** (unchanged; _088 shoot kept exported, not sequenced in the slice) |

## Change made (staged page, ?s5=1)
- GLB in-page builder clip whitelist += `_065_glide_idle_to_run` (7 clips total now:
  idle/walk/run/glide/pull/shoot/landing).
- Landing sequence: `_065_glide_idle_to_run` (450 ms excerpt of the 667 ms clip)
  then `_008_run` — replaces the immediate `_008_run` hard switch.
- GATE after change: targetReached 0 u, glideClipActive true, landed 1000 ms,
  0 console/page errors (s54_t1_gate.json s5_decoded, re-run after the T3 edit).

## Clip coverage report (of the 104 glide/grapnel clips in the s35 battery)
The state table + Lua reference, by family:
- glide core: _057_glide_idle (slice glide), _059_glide_parachute_idle,
  _065_glide_idle_to_run (slice landing), _062 wall-contact-to-glide family,
  run_jump_to_glide_parachute (3 clips), glide_parachute_stream_jet_air (3),
  fall_to_glide_parachute (2) — 12 named/tabled clips.
- grapple core: _088_grapnel_shoot (exported), _089_grapnel_pull (slice pull),
  _087_idle_to_grapnel, Grapnel_Fly_Idle_Horizontal state — 4 named/tabled clips.
- The remaining ~88 of 104 are enemy/parachute-variant/QTE clips with no state-table
  row in the s36 decode (the bdae anim_pack node bindings remain undecoded — the
  standing declared gap from s36).

## Validation (ground rule 3: two signals)
1. **State-table sign**: the slice's three chosen clips are the table's first-listed
   clips for their states (Glide_Idle -> _057, landing -> _065 from
   Grapnel_Horizontal_To_Glide_Idle), i.e. the same (state -> clip) correspondence
   the engine's Lua uses, not name-similarity picks.
2. **Duration consistency**: _065 (667 ms) is used for a 450 ms transition excerpt —
   shorter than the clip, consistent with a blend-out; _089 (1899 ms) covers the
   1200 ms pull; _057 (2167 ms loop) covers any glide length. A deliberately WRONG
   pick (using _088_grapnel_shoot, 432 ms, for the 1200 ms pull) would stall/loop
   mid-pull — the durations falsify it.
