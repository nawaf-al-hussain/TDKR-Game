# RE Session 14 — verification round 2: ZNCC retracted, batch_info layout SOLVED, site deploy guarded

## Trigger
Outside-AI round-2 review of the session-13 skyline result + batch_info
evidence. Every point executed.

## 1. ZNCC "+0.66" — RETRACTED (the reviewer's broad-ridge worry was right)

Ran the requested ±100u sweep (float64, masked, σ=1.5 @ 1u cells, whole
plane): **ZNCC at the record TRS = +0.08**, landscape max +0.19 at an
unrelated offset (+635,+158), ±100u window = broad plateau, rotation
response flat (±5°). No sharp peak anywhere near the record.

Then bisected the session-13 +0.66: it reproduces ONLY under zncc13b's
exact framing (sky local, grid = union(street, sky-local) + 340 margin,
read at the record index). Same data/math under the shipped framing gives
+0.156; the **direct windowed Pearson over the sky support (the
convention-free definition) gives +0.0284** at the record, 0.00 identity,
−0.07 v13, +0.12 at the sweep argmax. Cause: the FFT-ZNCC normalizes over
the shifted-grid-intersection window whose extent depends on arbitrary
framing; it mostly measures "does the sky blob sit on the city" — that is
why it could read +0.66 at the record and ~0 at identity.

**What the placement evidence actually is** (all in
`extraction/re/skyline_verify14.json`):
- the engine record itself (0x14051 @ GothamCity.lvc 0x55545, disasm-proven
  read path, explicit TRS + mesh name) — the game's own data;
- per-prim nearest-centroid correspondence FP1/FP2/FP3 vs the assembly:
  mean |d| 0.96 / 1.55 / 2.23 u, max 3.81/4.37/10.95 u, and the **mean
  delta vector ≈ 0** (0.19/0.13/1.10 u) — a wrong frame would shift every
  prim coherently;
- raw binary overlap: record 13,776 cells vs v13 offset 7,406 vs identity
  **0**. Corroborates at large displacement; within ±60u it is plateau-like
  (argmax +40,+45 at 112% of record) — density metrics cannot do better,
  as the reviewer suspected.

Scripts: `zncc_sweep14.py` (sweep + PNGs), `zncc_repro13.py` (arbitration),
`zncc_bisect14.py` (config isolation), `zncc_direct14.py` (ground truth),
`skyline_verify14.py` (consolidated, committed JSON).

## 2. Skyline material bindings — engine-level closure

`ground_truth.parse_file` on all 8 LongDist bdaes (island1+2, LOW
variants): **every material has LightMap texIdx = 0xFFFFFFFF (UNBOUND)**;
4-5 LightMapDC materials + 1 StandardDiffuseDC (monorail) per unit. The
engine itself renders Diffuse × white × 2.0 → the shipped GLB material
names `<page>|2x` / `<tex>|d` are exact parity. No viewer change needed.

## 3. Island-2 removal + site integrity

- manifest v14 has no island-2 skyline GLBs ✓; viewer logic never needed
  them in the single-level view ✓.
- Stale app.js boot comment (v13 offset) corrected to the record TRS.
- `GC_Railway_Island2_LongDist` (hero tier, OFF by default) overlaps the
  island-1 area by 21k u² at local coords — documented, stays a research
  toggle until the generic-object records are decoded.

## 4. Deploy pipeline — the gh-pages branch was STALE (v13 served!)

The live site was still v13 (45 GLBs, wrong skyline offset, island-2
GLBs present) because session 13 patched main:gh-pages but never pushed
the gh-pages BRANCH. Fixed:
- incremental sync main:gh-pages → gh-pages worktree (protected
  style.css/skybox.jpg/.nojekyll which only exist on the branch),
- deleted the 5 island-2 skyline GLBs, committed, pushed (gh-pages
  @ 7c8eda6 + manifest-bytes fix).
- **post-deploy smoke test** `extraction/scripts/site_smoke_test.py`:
  infra files (index/style/app.js/skybox/.nojekyll), index wiring,
  manifest parse + version + tiers, all 40 GLBs (status + Content-Length
  vs manifest bytes), all 51 textures, island-2 absence. **53/53 PASS**
  against the live URL. It caught two real bugs: restored index.html
  never linked style.css (it is self-contained; style.css is a root
  sentinel — test adjusted), and manifest v14 carried pre-patch GLB byte
  sizes (fixed + redeployed).

## 5. batch_info.bin — LAYOUT SOLVED

- **`batch_info.bin = u32(197) + M × 197-byte records`, one record per
  material.** M = 307 (island1) / 196 (island2) = EXACTLY the material
  counts of the zones' materials bdae (source.dae library_materials;
  regenerated the zone_materials JSONs to confirm — session 10's
  "305+195" was slightly off).
- **Record m's first byte = m** (material index): 307/307 and 196/196
  (mod 256 for m ≥ 256).
- The leading u32 197 = record stride, NOT a count. **stream_info.bin
  decoded: `[6 × f32 streaming bbox][u32 X][u32 197]`** — the same 197
  appears as the zone constant; X = 234,466 / 303,832 (open).
- The old session-13 "197 records / 307-196 B records / drifting
  template" observations were artifacts of slicing at the wrong stride:
  the "drift" was each record's material-index byte landing one byte
  later in the mis-gridded view (body[197k] == k held 195/195 island2).
- Slot bytes (196 per record): 0xFF 13.4% (12–13 runs), 0x00 68%, values
  0..254 saturating; adjacent slots highly correlated; f32 groups
  (UV-rect-like: 3.6e-4, 1.8e-4, 0.48, −2.59 …) at in-record offsets
  ~75–115. NOT monotone per record; per-record max sums (74,934/47,949)
  match no known count; u16 reading is not clean. Value semantics OPEN.
- Engine side: name table @0xb40704 has NO absolute pointers anywhere
  (full-file literal scan ±0x800) — reached via computed base + enum
  index. `CLevelStreaming_DB::Load` @0x406dfc orchestrates; parse is in
  non-exported helpers (bl 0x3dac58 ×8, 0x42e2bc ×7, 0x455e2c ×6);
  0x4043f8 = CLevel::LoadGlobalObjects.
- Evidence pack for the collaborator (hexdumps, lod_table rows, material
  name order): `extraction/re/batch_info_evidence14.md` +
  `batch_info_material_names14.txt`.

## Shipped (committed)

- extraction/re/: zncc_sweep14.py, zncc_repro13.py, zncc_bisect14.py,
  zncc_direct14.py, skyline_verify14.py + skyline_verify14.json,
  batch_info_matrix14.py, batch_info_deep14.py, batch_info_evidence14.md,
  batch_info_material_names14.txt, RE_NOTES_session14.md
- extraction/scripts/site_smoke_test.py
- gh-pages/app.js (boot comment corrected)
- gh-pages/models/manifest.json (bytes fields corrected)
- CLAUDE_HANDOFF.md (session-14 state: retraction, material closure,
  deploy guard, batch_info solved layout)

## Next (ordered)

1. batch_info value semantics: engine reader via the enum-index path in
   PrepareFiles/Load helpers (0x3dac58/0x42e2bc/0x455e2c), or the
   collaborator's read of the evidence pack.
2. Generic-object records (CreateObject component loop) → hero unit TRSs
   (bridges/monorail/railway), incl. GC_Railway_Island2 (currently an
   off-default research toggle overlapping island-1 by 21k u²).
3. Ground fidelity split + near-field density (blocker C) — unblocked by
   batch_info once slot semantics are known.
