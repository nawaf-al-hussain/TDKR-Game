# s57 T2 — enemy template decode: SECOND SIGNAL via the engine read sequences (no sanity filter)

## Method difference vs s56
s56 decoded Health/Awareness by a sane-pattern GAP SEARCH (a sanity filter cannot also validate).
s57 derives the component read sequences from the ENGINE (ARM disasm of the Load functions) and walks
every template structurally: a template CLOSES when the ordered comp walks consume exactly the payload
length. No value-sanity anywhere in the walk.

## Engine-derived sequences this session (libKRHP.so, ARM; disasm in s57_t2_loaddisasm.txt / s57_t2_readers.txt)
| comp | class id | sequence | source |
|---|---|---|---|
| CStateSetComponent | 0x5441a117 | instance Load = THUNK 'bx lr' (0x298f38, 0 bytes); TEMPLATE path = state-name list, 8 STR table indices (Merc byte-forced: [''-ref,'Idle','Hurt','Death','Idle','Walk','Run','Run']) | Load disasm + closure |
| CDropCollectibleComponent | 0x3ef5108d | ReadInt n + n x (ReadInt, ReadInt) | 0x229e44 -> 0x2e27b8 |
| CNpcAIComponent | 0x44c6e9e5 | i, c x6, i x4, f x3 = 38 B | 0x279e88 -> 0x2d70e8 |
| CWantedGeneratorComponent | 0x3e2bb040 | i, i, f, i = 16 B | 0x24b23c -> 0x2e0290 |
| CActorBaseComponent (template Load) | 0x54989cb1 | 3 inline bytes, 16 ReadFloat, 3 inline bytes, ReadInt, ReadInt=count, count x (ReadInt + 1 byte) = 78+5n | 0x36cbb0 -> 0x3baee0 |
| CComponentMotion (template) | 0x592ce07c | [c, f, f, c, f, f] = 18 B speed pairs (Bane: 01, 750.0, 750.0, 01, 500.0, 500.0); instance Load tail-calls CMemoryStream::ReadString 0x33a0d4 (PINNED this session) | 0x2d79ec + closure |
| CustomizeActor | 0x40c6b80a | instance Load = factory -> CComponentCustomizeActor::Load 0x3bf688 (185 Read* calls, conditional groups); TEMPLATE sequence NOT resolved this session | listed missing |

NOTE: the s30 read-seq table encodes LVC-instance (SaveLoad-oriented) sequences with [k, n] = single
n-byte reads (lvc.js semantics) — it is NOT the gol template Load path and cannot validate gol walks.
gol class ids are runtime name-hashes (most ids have NO constant in .text — dispatch is a registry);
ids 0x14ca79/0x152b87 are legacy addresses.

## Structural walk results (s57_t2_walk.py, out: s57_t2_walk_out.json)
- 110 of 653 gol templates close EXACTLY (ordered walk == payload length, no gaps, no sanity filter).
- Health/Awareness boundary agreement, structural walk vs s56 gap-search (s57_t2_boundary_check.json):
  **25 carriers MATCH** (health value + all 16 awareness floats identical), **1 CORRECTED**
  (Blake: walk health=150 / spec-forced boundary vs s56 sanity-search 2.0 — the walk wins: 25:1
  agreement elsewhere, and 150 matches the Knife_Enemy/Police_Officer 150 family), **4 NEW decodes**
  (Helicopter, Helicopter_Bane, Military_Heli, Test_Object: Health@121, Awareness@138, health float
  read at 121), 24 unwalkable-to-Awareness (23 vehicles/monorail blocked at 0x2db081e2 BEFORE Health,
  + Sniper/Ranged_Disarm_Dummy class).
- Merc structural boundaries: Health @121, Awareness @154 — EXACTLY the s56 gap-search positions.
- Melee_Enemy_Merc payload 683 B closes 0..461 (through WantedGenerator) with every boundary
  spec-forced; the tail (CustomizeActor + Motion) resolves as Motion = last 18 B.

## Motion component decoded (template payload)
Uniform across ALL humanoid templates (Batman, enemies, civilians): [flag=1, 750.0, 750.0, flag=1,
500.0, 500.0] = run/walk speed pairs, 1.5:1 ratio (s57_t2_motion_vals.json). Bane identical. The
instance-path Load reads a string (animation/state name). Unit scale not claimed (see T1 note:
glide floats 4-16 vs Motion 750/500 — per-component scales; ratio 750:500 = 1.5 run:walk is the
scale-free fact).

## Missing sequences (the brief's "or list which comp load sequences are missing")
1. 0x40c6b80a CustomizeActor TEMPLATE variant: instance Load is a 185-read conditional monster
   (0x3bf688); template payload shows [count][count STR] groups (Merc: [3][3 tex names],
   [12][12 gear LOD names], ...) — needs a dedicated session.
2. 0x2db081e2 (vehicles/monorail): id has NO .text constant (runtime-hash registry); class unknown;
   blocks 23 vehicle carriers pre-Health.
3. Sniper / Ranged_Disarm_Dummy: an unknown comp between Health and Awareness (s56 standing note).
4. Helicopter/Helicopter_Bane: close to 425 of 3092 B (behavior-template extras beyond the comp list).

## (b) Lua cross-check + damage
GiveDamage native: the Lua API surface (SetActorHealth 63, GiveDamage 146 call sites per s55 census)
writes through CComponentHealth fields; argument-constant extraction from Lua bytecode NOT completed
this session (the compiled-Lua constant pool decode is still open - carries the damage numbers).
Health cross-check via the structural walk stands in for the SetActorHealth constant check: 25
templates' health values now have TWO independent signals (sanity-gap-search s56 + engine-spec walk).

## Verdict vs acceptance
- (a) second parse path, >=40 templates closing without sanity filter: MET at the all-template level
  (110 close with exact boundaries); enemy carriers: 30 of 50 walk through Health+Awareness
  (25 match + 1 corrected + 4 new), the other 20 blocked by the two listed missing sequences.
- (b) Lua cross-check: PARTIAL (health double-signal MET via the walk; GiveDamage arg values NOT decoded).
- (c) 13+ undecoded templates explained: MET (listed with reasons).
- Motion reader pinned + fields decoded: MET (ReadString instance path; [c,f,f,c,f,f] template path).
