# RE Session 26 (round 16) — 2026-10-16

## 0. State recovery
- Sandbox partially reset: download/ survived with bundles_s24 only;
  bundles_s25 was missing from download/ but the previous sandbox's
  /tmp/my-project had a verified copy (SHA256 9047d131...ffe7ed, 1,339,152 B).
- Remote clone: main @ 03ee321, gh-pages @ f22b098 (v17 live),
  gh-pages-staged @ 9a9fb3b (v19). Bundles s24 verified + fetched
  (main_s24_inc 55,644 B SHA256 78357cc0...; ghpages_staged_s24 6,086,056 B
  SHA256 1336093e...). Nothing since v17 is pushed.

## 1. T1 — lvc parse VALIDATED + LIBERATED: PASS
- ENGINE GROUND TRUTH: ran CLevel::LoadNextObject @0x489ecc natively under
  Unicorn over both islands with a natively-populated GOM template map
  (map::operator[] @0x3c6084 + vector::operator= @0x3a6f88 x 653 templates).
- FRAMING CORRECTIONS (vs round-15 walk):
  * 0x2657 LevelInit = 1,339 B via the real dispatcher case (the banked
    parse under-read 4 B; the walk papered over it with a 4-B phantom skip).
  * 0x798f = waypoint Load (67 B) + 3 floats + CComponentBuiltinCylinder::
    Load (45 B) = 128 B; 200 (GC) + 332 (I2) such records. The walk's
    "-1 + float-run" mystery = these chains' tails (the -1s = the waypoints'
    0xffffffff link fields).
  * -1 and unknown tids = 4-B skips, engine-verified (CreateObject
    default-inserts an empty template; LoadZoneFromMemoryStream's loop
    condition is cursor < stream size).
- HEADER COUNT RECONCILED: 14,917 (GC) / 8,214 (I2) = an ENGINE-DISCARDED
  field: CLevel::LoadRawLvl @0x4891f8 reads it into r6 and never uses it;
  the loop bound is the stream size. The exporter counted pre-serialization
  elements (waypoint network links/colliders stored inline). Engine framing
  counts: 14,313 / 7,474.
- VALIDATION: 0 STR-index violations in 24,579 STR reads; 871/873 banked
  boundaries direct + the 2 = the corrected 0x2657 pair; every leading u32
  is a known typeId or an engine-verified skip (733 GC / 1 I2).
- PURE PARSER (extraction/re/session26/lvc_pure.py + lvc_readseq.json):
  54 component classes = 44 fixed + 5 loop specs (collision, smartlight,
  soundlight, npc-list, actorbase incl. inlined-read fat tokens) + 2
  measured-span classes (CCinematicComponent x34, CTrafficSetting x15 --
  the resisting ones). EQUIVALENCE PROVEN: 21,787/21,787 record boundaries
  AND token streams (kind, offset, size, value) on both islands.
- CENSUSES (pure parser): collision 1,238 comps = 271,589 triangles
  (= round-15 exactly); triggers 694 (475 substantive scripts = 560,803 B);
  spawns 317; mesh 62. Lua pool 1,252 strings = 1,639,112 B (session-23's
  1.64 MB reconciled: union = trigger 560,803 + zone/quest/waypoint
  1,078,309). Lua API: 249/747 registry functions used in triggers; top:
  Wait, Enable, ShowMessage, ActorSetState, Disable, ShowObject, HideObject,
  ActorLookTo, StartFadeOut, CameraFollowObject, StartFadeIn, SpawnObject.

## 2. T2 — batman skin: PARTIAL
- 40-vs-80 RESOLVED: data = 116,156 = 1,449 x 80 + 236-B trailer; stride 80
  confirmed by 8 u32 0x50 constants in the data head AND the index buffer
  max = 1,448 = count-1. Index list = 5,430 u16 = 1,810 triangles
  (region header 0x712) after a 225-u16 identity prefix.
- Session-24 "two mirrored 40-B halves" REFUTED: the 80-B vertex carries a
  position-like triple, TWO unit quaternions (|q| = 1.00) and weight data
  (+68; pairwise delta 0.0232 vs 0.49-1.44 for position candidates).
- 67 Bip01 bones enumerated (28 cape CBones). Shuffled null: real med-edge
  0.980 vs null 1.353 — positions appear bone-space; the bind-pose test
  needs the -skin section. RESISTING: the resource-manager cache layer
  (CResFileManager::get) blocks the engine-parse bypass.

## 3. T3 — one clip: PARTIAL
- Channel group = 32 B [timeOff, 1, valOff1, 1, valOff2, 0, 0, 0]
  (session-24's "40 B" wrong), per-clip blocks preceded by [1, 0];
  clip 1 @0xb53c = 78 channels. Offsets are FILE-ABSOLUTE; the time-key
  base = the header word @0x2c = 0x3a5ec: [f32 value][u32 tick] pairs,
  ticks increasing. 1,375 groups = the sum over the 503 clips (2.7 avg).
- Decode of the value streams + skeleton application = NOT completed.

## 4. T4 — housekeeping
- Staged v19 re-verified structurally (cache version 19, skyline boot fix
  present, 41 GLBs on disk, 17 skyline/longdist manifest entries);
  the round-13 gate PASS 26/26 stands (gate_v19_staged.json).
- Skyline placement still rests solely on engine record 0x14051.

## 5. Whitelist-off run (T1 validation d)
- GothamCity: 1,474 component runs faulted under the emulator, all in
  post-Load bookkeeping (CBeastObjectComponent x423, CTriggerComponent x269
  [Lua registration: luaS_newlstr/LoadFromBuffer], 0xc7d8baf x255,
  0x592ce07c x211, CSoundAndLight x176, ...), touching 1,442 records
  (4,889,564 record bytes). With the whitelist off these would report
  failures; the stream reads were already complete -- proven by the pure
  parser (no emulation, no faults) reproducing every boundary and value.
