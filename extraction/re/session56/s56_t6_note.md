# s56 T6 — combat slice, data first: enemy component decode (Melee_Enemy_Merc + family)

## Component-id resolution (two independent anchors each, per ground rules)
| component | class id | anchor A | anchor B |
|---|---|---|---|
| CComponentHealth | **0x0ddcd6c4** | Load @0x2d7bf0 (symbol) disasm: ReadFloat->[this+4], ReadChar->bool [this+8], ReadInt->[this+0xc], ReadInt->[this+0x10] (bl targets 0x339b94/0x3395d8/0x339914 = CMemoryStream::ReadFloat/ReadChar/ReadInt by nm) | s30 readseq {f:1, c:1, i:2} - exact match |
| CComponentAwareness | **0x6754056b** | Load @0x3bbb68 (symbol): 16x ReadFloat | s30 readseq {f:16} - exact match |
| CComponentMotion | 0x592ce07c (candidate) | Load @0x2d79ec = 3-insn tailcall to a shared reader @0x33a0d4 writing [this+4]; reader is not a Read* wrapper - field count NOT pinned this session | readseq {raw:1, f:4} - suggestive, not exact |
| CActorBaseComponent | 0x54989cb1 | named in the s30 meta.loop_specs | present in all enemy templates |
vtable layout confirmed for all three classes (+0x10 New, +0x14 Clone, +0x18 Load).

## Payload decode (gol.bin template payloads; big-endian per the s54 glide precedent; lvc.js
Reader semantics: STR = 4-byte string-table index, rep count = last field, fat = (kind,size))
Method: the 19-comp payload has 5 comps with no s30 readseq spec (0x5441a117, 0x3ef5108d,
0x44c6e9e5, 0x3e2bb040, 0x40c6b80a) = gap bytes; the single gap BEFORE Health is derived
from the sane-health pattern (f in [1..10000], c<=1, ints bounded); Awareness follows after
the two spec'd comps between them. Melee_Enemy_Merc: gap0 = 37 B, Health @121, Awareness @154.

## Decoded value table (Melee_Enemy_Merc, gol template 0x000c351d, 683 B payload)
| field | value | interpretation |
|---|---|---|
| health | **120.0** | CComponentHealth float @+4 (HP) |
| health.flag | 0 | bool @+8 |
| health.int1/int2 | -1 / -1 | ints @+0xc/+0x10 (unset markers) |
| aware f0 | 11.0 | radius pair 1 (u) |
| aware f1 | 17.0 | radius pair 1 far |
| aware f2/f3 | 0 / 0 | |
| aware f4/f5 | 2.0 / 5.0 | radius pair 2 |
| aware f6/f7 | 0 / 0 | |
| aware f8/f9 | 1.5 / 6.0 | radius pair 3 |
| aware f10/f11 | 0 / 0 | |
| aware f12 | 1.1 | movement/turn scale |
| aware f13 | **160.0** | FOV (degrees) |
| aware f14 | 2.7 | hearing/aggro scale |
| aware f15 | 1.5 | global default (1.5 in ALL 37 templates) |

## Cross-template validation (s56_t6_enemy_decode.json; 37 of 50 Health+Awareness carriers decoded)
- Range checks: all decoded health in [2, 1400]; all 592 awareness floats finite and in
  [0, 500]; the FOV-like field f13 takes ONLY authored values {45, 120, 160, 180}.
  The zero-hit control (s53-era garbage at the unshifted offset: NaN/1e38 values) fails
  every check - the comparison moves.
- Shuffled-template null: health values across the 37 templates, mean 239.5, sd 462.2;
  Melee_Enemy_Merc 120.0 -> z = -0.26, permutation two-sided p ~ 0.836 (1000 shuffled draws,
  seed 56). Sign convention: health = CComponentHealth float @+4, higher = more HP;
  z = (x - mean)/sd over templates. The Merc's health is UNREMARKABLE against the template
  population (expected - the null shows the value carries no template identity by itself).
- Structural signal (stronger than the health z): the awareness vectors cluster by BEHAVIOR
  family - Melee_Enemy_Merc == Melee_Enemy_Pit == Melee_Enemy_Test == Police_Officer_Melee
  exactly [11,17,...,1.1,160,2.7,1.5]; the boss family (LeadMerc, Bane, Turhan, Miranda =
  1400 HP) shares [11,17,...,1.3,180,3.0,1.5]; civilians (NPC/NPC_Female/Pit_Prisoner,
  60 HP) share [10,15,5,7,...,1.2,180,2.0,1.5]; vehicles carry health=2 with the sensor-only
  vector [0 x13, 45, 500, 0.5]. Wrong-position decodes (the s53-era offsets) produce no
  such clustering - the shuffled/null control moves the comparison.
- Health table highlights: Knife_Enemy 150, Crowbar_Enemy (not decoded - no sane window:
  different comp order), Police_Officer 150, Sniper/Ranged_Disarm_Dummy skipped (unknown
  comp between Health and Awareness), Bane 1400, Tumbler/Generic_Car 2.

## Clips and damage (from s55 scoping, unchanged)
- State-table combat states: core[10] = Enemy_Combat_Idle / Knife_Combat_Idle /
  Enemy_Idle_Aim (s36 mechanism, lua_uses 4); clip families in batman_anims.bdae (921 clips):
  attack 33, counter 20, takedown 14, hit 9, block 10 (s55_t6_clipfams.json).
- Lua call volume: NPCAttackTarget 529, SetActorSpeed 291, GiveDamage 146, ActorIsAttacked 73,
  SetActorHealth 63 (game_config.gla occurrence counts). Damage NUMBERS not decoded this
  session (GiveDamage argument extraction from Lua bytecode = future work).

## Verdict vs acceptance
- ONE enemy template decoded with component payloads from gol.bin and floats named from the
  Load functions: **MET** (Health: 4 fields byte-mapped; Awareness: 16 floats; ids resolved
  with two anchors each).
- Clips bound to states: MET at the s55-scoping level (families + core states); per-clip
  state bindings for ENEMY skeletons are the bdae anim_pack gap (s36 standing issue).
- Damage values: NOT MET (Lua GiveDamage args undecoded) - PARTIAL overall on that sub-item.
- Validation: MET (range checks + shuffled-template null + structural family clustering).
- Implementation: none beyond the data table (per brief; no time remained for a viewer page).
