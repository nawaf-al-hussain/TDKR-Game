# RE Session 15 — batch_info is a per-material parameter block; segment→material link FOUND (+40); skyline negatives run honestly

## Trigger
Outside-AI round-3 review. Every point executed.

## 1. Skyline — the three (-730,-1250,0) records + two new negatives

- Confirmed the triple: **0x14051 (gc_island1_longdist.bdae)** @lvc 349509 +
  **2× 0x14050 reflections** (gc_footprint_ic_reflection @5064989,
  gc_railway_island1_reflection @5065605) all at EXACTLY (-730,-1250,0).
  They are elements 31/42 of one 56-byte-stride 0x14050 array (~44 records,
  the rest scattered x∈[-930,32] y∈[-1110,-574]).
- **Anchor comparison**: (-730,-1250,0) is NOT a corner/center of
  stream_info.bin bbox (island1: -1620..185, -1313..-247, -27..204 — note
  bih_struct stores the same box permuted (x,z,y), matching
  SAxisMapping<0,2,1>) and not the spawn. Honest reading: it is an authored
  **far-field group origin** (LongDist + its two reflection companions);
  the levelInit/template lvc sections carry no origin.
- **AddLowPolyLongDistanceNode @0x48b140 (symtab-true, 336 B) fully
  decoded: NO second offset.** It creates an identity CEmptySceneNode
  named **"LPLDBatchCollect"**, hangs it off the scene root, reparents the
  record's node; sole caller = CLevel::LoadNextObject (the lvc record
  loop). CreateLowPolyLongDistanceBatch @0x48b290 merges the children via
  updateAbsolutePosition — again no extra transform. The record TRS is
  final. (Name also confirms the far-field batch-collector pipeline.)
- **Roof/road negative test (new)**: engine-derived road classification —
  segment descriptor +40 (see §3) → materials.bdae sampler chain
  (LightMap = BakeGroup_Island1_Roads0 page OR DiffuseMap road-named;
  trunk excluded; |z|<12) → 76,537 road verts. Roofs = GC_island1_LongDist
  XY footprint (dilated 2u mask). Sweep ±60u @2u:
  **@record 0.0276; landscape mean 0.0247; global min 0.0102 @(+60,+46);
  constrained (building-coverage ≥ 90% max) min 0.0231 @(-58,-10)**;
  identity/v13 displace roofs fully off the road network → 0 (degenerate
  direction). **No sharp minimum at the record — the test does not
  independently support the placement**, exactly the blob-overlap failure
  mode the reviewer predicted. Placement rests on the engine record alone;
  skyline_verify14.json/RE_NOTES_session14 wording stands.
- Correction banked: descriptor bounds are NOT the segment bbox (seg2's
  "bounds" span 0.1u); do not use them as geometry bounds.

## 2. batch_info.bin — record = fixed per-material parameter block

Word-position test (batch_words15.py, output banked in
batch_words15_out.txt): record m = byte0 + 196-byte payload = 49×u32.
**The two islands' templates are essentially identical** (same constants,
same high-cardinality columns), M=307/196:

- bytes 0–1: material index (u16 LE; byte1 = m>>8 ∈ {0,1})
- rec 3,4: {1,255}/{2,255} — sampler-ish fields with -1 sentinels
- rec 5–16: **0xffffffff ×3** (12 B, u32-aligned in payload);
  rec 20/21–31/32: another 0xff region + 0x00 — the reviewer's
  "three aligned -1 words" hypothesis CONFIRMED, twice
- rec 33: small int 0..5; rec 41–44: const 0x00060000; w7 const 0xffffff
- rec 45–108: u16-ish small-value array (values ≤ 28; per-record variants
  like (3,20/24,12,16…)) — vertex-stream/declaration-like; open
- **rec 109–156: FOUR 12-byte vec3 f32 groups** (at 109/121/133/145,
  4-byte tails between, usually 0):
  - Animated mats: (scroll-speed-like ~1e-6..1e-5 pairs)
  - 2Sided/Default/Reflection: (scaleU, scaleV)-like (e.g. 42.2, 0.25;
    -2.03, -1.04) + (offsetU, offsetV) ∈ [0,1] (0.895, 0.396; 0.25, 0.25)
  - StandardDiffuseDC: zeros or int pairs (bits 0x00000006 read as 8.4e-45)
  - value sets are ~unique per material (284–291 distinct of 307)
- rec 157+: flags/tail, mostly 0; w45–48 always 0
- BE u32 decode is garbage (BE table in batch_words15_out.txt); the f32
  groups are LE. u16 runs cannot be endianness-probed (values < 256).
- f16 reading tested and rejected (no consistent mapping).
- Technique correlation: materials WITHOUT the float groups = default/
  invalid/Water/ExtraDiffuse/UVAnimCulling etc.; ~95% of textured
  materials carry them → **per-material render/UV parameter block**
  (semantics per-technique; engine consumer identified, see §4).

## 3. **segment→material link FOUND: lod descriptor +40**

Per-segment descriptor field at **+40** (session-9 layout, empirically
re-based: +0 triCount, +4/+44 bounds-like pairs, +28 =4, +32 block count,
+36 near-unique id 0..3772, +68 block[off,4,vBytes,iBytes,fmt1,fmt2],
+204 0xffff0000 terminator):

- island1: all 1,526 segments carry it, **139 distinct values, 0..305 <
  M=307**
- island2: all 1,020 segments, **88 distinct, 4..194 < M=196**
- **Cross-validation: top value 74 (210 segs) = a material whose LightMap
  is BakeGroup_Island1_Roads0** (m11 Street, m90 Railroad also top) — the
  distribution is semantically sensible per height bucket.

**This is the street-tier material binding that Blocker B needed** — the
"dark buildings" can now be bound by descriptor +40 → materials.bdae
order (= batch_info record index). The dark-near-tier fallback in the
exporter can be replaced with engine-true bindings.

+36 (0..3772, near-unique per segment) = open (offset into a shared
table? batch id?). lod_data segment-block headers: no second candidate
field (headers nearly constant).

## 4. Engine chain (symtab-true, all addresses re-verified this session)

- **CLevelStreaming_DB::Load @0x3f6dfc** (session-14's 0x406dfc was stale):
  opens CZipReader over the zone stream and maps members → fields:
  **+0xf0 stream_info, +0xf4 bih_data, +0xf8 bih_struct, +0xfc
  batch_info, +0x100 <zone>_materials.bdae, +0x104 lod_table, +0x108
  lod_data, +0x10c lod_selector.** (First resolver pass was off by one;
  manual pool resolution is authoritative.)
- **bih_struct = CRegularGridStreaming ctor input** @0x45db7c (called
  with (&+0xf8, &+0xf4) = (bih_struct, bih_data)): layout
  **[24 B aabbox3d f32][u32 100][u32 100][u32 1][10001×u32 LE offsets]** —
  a 100×100×1 cell grid; offsets monotone 0..33,461 = exactly the bytes
  after the array (BIH node payload). Session-9's "AABB + BIH nodes" is
  now an exact layout.
- **batch_info's consumer = CDoubleBufferedDynamicBatchMesh ctor
  @0x45c750** (args include stream_info&, batch_info&, materials file):
  ctor reads stream_info [bbox→this+0xac (expanded by ε)][X→this+0x80
  (iota-filled byte array, 234,466/303,832 — meaning still open)][197→
  this+0xa8 = stride], CColladaDatabase over materials, stores batch_info
  IReadFile at this+0xa4. Record-loop parse is deeper (vtable-mediated).
- **getBatchMaterial(SBatch&, uint) @0x44ef08: the uint is UNUSED**;
  SBatch+0x8 = intrusive_ptr<CMaterial>, +0xc = vertex-attribute map —
  materials bind at SBatch construction, not at getBatchMaterial.
- **Session-14's "helpers" 0x3dac58/0x42e2bc/0x455e2c are
  Application::GetInstance / CHUDDisplay::HideHint /
  TrackingManager::AddEvent.constprop — misattributed** (they are just
  common calls inside Load). Corrected here.
- File-name strings (0xb40704 block, dup at 0xb45454) have NO absolute
  pointers, NO movw/movt pairs, NO relocs — the name table is reached via
  GOT-relative thunk (`rsb r1, r1, #0xB4` backwards-index pattern at
  0xc75bc) — enum-index access as suspected in session 14.

## 5. Deploy — stale-branch regression guard (v15 live)

- gh-pages was again behind? No — but the *class* is now guarded:
  **site_release_check.py** (release gate): fails on manifest version
  drift main vs origin/gh-pages, APP_CACHE_VERSION mismatch, missing
  index.html (third-loss guard), GLB inventory drift. PASS after deploy.
- **Cache-busting in app.js**: `APP_CACHE_VERSION='v15'` busts the
  manifest fetch; GLB/texture URLs get `?v=v<manifest.version>`.
- **site_smoke_test.py** extended: live-manifest-version == main, four
  cache-bust hooks, frameWarning surfacing; GLB/tex fetches now use the
  ?v= suffix. **58/58 PASS live (v15)**.
- manifest v15: version 15; **frameWarning added to the three island-2
  -local hero units (GC_Railway_Island2 / GC_Monorail_Island2 /
  GC_Small_Bridge_Island2_LongDist)** — app.js toggleTier surfaces it in
  the status line + console.warn; browser rows show ⚠ with tooltip.
  The railway's 21k u² island-1 overlap can no longer appear silently.

## Shipped (committed)

- extraction/re/: batch_words15.py + batch_words15_out.txt (the
  collaborator data pack), batch_xref15.py (+ per-island JSON),
  batch_srcdae15.py, mat_tex15.py + mat_tex_{island}.json (DiffuseMap/
  LightMap per material), lod_segfield15.py, roof_road_test15.py +
  roof_road_test15.json, disasm15.py, load_openfiles15.py
- extraction/scripts/: site_release_check.py (release gate),
  site_smoke_test.py (extended, 58 checks)
- gh-pages: app.js (cache-bust + frameWarning), models/manifest.json (v15
  + frameWarning fields) — pushed to gh-pages @3bc86ab
- CLAUDE_HANDOFF.md, this file

## Next (ordered)

1. **Bind the dark near-tier by descriptor +40** (exporter): seg→matIdx →
   materials.bdae DiffuseMap/LightMap → engine-true bindings for all
   1,526 street segments. This is Blocker B's payoff — the dark buildings
   are solved at the data level; remaining work is exporter plumbing +
   visual verify.
2. batch_info record semantics via CDoubleBufferedDynamicBatchMesh parse
   (find the record loop — likely in a helper called with this+0xa4; or
   instrument by value-matching the vec3 groups against known UV
   transforms) — now confirmable against +40 material names.
3. +36 field (0..3772) identification; stream_info X (234,466/303,832).
4. Generic-object records → hero unit TRSs (bridges/monorail/railway),
   then the island-2 frameWarning units can be placed or dropped for good.
