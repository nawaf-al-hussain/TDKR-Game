# RE Session 22 (round 12) — 2026-10-13

Sandbox reset again (6th round). Nothing since v17 pushed. Rebuilt from the
round-12 briefing + session-18 repo state; raw data re-downloaded (SHA256
verified vs README), restore + texture decode + ZIP_SPLIT re-run. Scripts
persisted under /home/z/my-project/scripts/ (also listed at the end).

## 1. State recovery

- Remote: main @ 3ae66a2, gh-pages @ f22b098 (v17 live). NOTHING pushed
  since v17 — sessions 19-21 never reached the remote; their artifacts
  (harness, raycaster, gate v2, notes, bundles) were LOST with the sandbox.
- download/bundles_s21/ GONE — no bundle verify possible (nothing found).
- Raw data: TDKR_v1.1.6b_APK_OBB.zip 895,253,801 B, SHA256
  0510e54c128de0f52bebc6db41ea3e3a9556f666d5ca5bb09eb39880c213aa6f ✓ README.
- Rebuilt: restore_raw, restore_assets (551 tex), ZIP_SPLIT (26 incl.
  GC_LongDist_* bake pages), zone zips, batch_info/lod bins.

## 2. loadHeadersAndSkipData @0x8e1d34 — harness rebuilt, all 503 records emulated (0 errors)

- Symbol check: .symtab says 0x8e1d34 size 1380 (briefing right); the
  ghidra all_functions.txt entry 0x8f1d34 is a shifted export — the ELF
  prologue sits at 0x8e1d34. Loops at +0x310/+0x35c ✓.
- Engine file format decoded from disasm + emulation:
  [u8][u32le N][N x 12B desc][K+1 x 24B pair][u32 X][seek X*desc0.stride]
  [24B tail {t0, kind, count, ...}][seek table[kind]*count].
  desc = {u32 byteOff; u16 attrId; u16 f2(type); u16 f3; u16 stride}.
  Pair = (vec3f scale, vec3f offset), SCALE FIRST (pre-loop pair + K loop
  iterations; exit `bls` = K iterations total).
- K = popcount(mask & 0xFFFE) is stored by CVertexStreams ctor (+0xc) from
  CVertexStreams::allocate(mask|1) — the engine derives it; the harness
  does NOT provide it. T3 circularity CLOSED (engine-ctor path).
- Pair slot j <-> descriptor j; slot0 = position's pair = zeros.
- 30 attr bytes = CMaterialVertexAttributeMap: attrId -> pairbuf slot
  (0xff = absent). m90: attr0->0, attr1->1, attr2->2, attr16->3.
- vtable slots used by the function: +0xc read, +0x18 seek.
- PLT: 0xa4e1c memcpy, 0xa4e88 memset (native hooks in the harness).
- Pure-Python parser (scripts/batch_parser.py) cross-validated vs the
  emulated engine: 503/503 byte-exact (pair values, slot counts, tails).

## 3. Uniform-commit extension (session-21 stretch goal) — DONE

commitCurrentMaterialAutomaticParameters @0x7e3290 (size 3100): the
auto-param dispatcher reads binding entries {u16 id; ...; u8 type@+8;
u8 attrId@+0xa}; types 0x85-0x8a upload vec4s built at 0x7e3bcc-style
handlers as `vec4(pair[slot(attrId)].scale.xy, pair[slot(attrId)].offset.xy)`
via the 30-byte map; types 0x6f-0x84 upload per-stream scalars via
getStream(E_VERTEX_ATTRIBUTE). Attribute name registry (strings @0xb87518,
sequential ids): 0=Position, 1=TexCoord0, 2=TexCoord1, 16=Normal, 17=Color0.
CONSEQUENCE: engine chain =
  vCoord0 = w3_raw * s109.xy + s121.xy   (diffuse; tiling scales x65535 = 1..52)
  vCoord1 = w4_raw * s133.xy + s145.xy   (lightmap; spans x65535 <= 1.0)
(GL_REPEAT; scale sized for RAW u16 — confirmed by the identity records'
s109 = exactly 1/65535). Shipped chain frac(w3_deq*s121 + s145) is
engine-CONTRADICTED on both channels — PROVEN, no longer inferred.

## 4. T1 — EF2raw falsifiable tests (scripts/t1_tests.py)

| test | EF2raw | shipped | identity | null | verdict |
|---|---|---|---|---|---|
| containment (raw) isl1 | 0.341 | 0.000 | 1.000* | 0.317+/-0.016 (z=+1.51) | at null |
| containment isl2 | 0.259 | 0.000 | 1.000* | 0.274+/-0.021 (z=-0.71) | at null |
| multi-wrap mats isl1 | 0/123 | 122/123 | 0/123 | — | EF2raw physical |
| partition total-area | 4.60x / 2.78x | 1.2e11x / 9.5e10x | 14.6x / 11.8x | (sizes kept: same by construction) | EF2raw ≠ 1.0x |
| partition overlap | 0.653 / 0.687 | 0.728 / 0.783 | 0.985 / 0.945 | 0.560+/-0.039 (z=+2.38) / 0.549+/-0.026 (z=+5.27) | EF2raw WORSE than random |
| spread non-ovl (>=200u) | 0.711 / 0.605 | 0.002 / 0.001 | — | 0.786+/-0.004 (z=-18.3) / 0.472+/-0.008 (z=+16.2) | islands disagree |

*identity containment is vacuous by construction (u16/65535 ∈ [0,1]).

DECISION (per the briefing's rule): containment AND partition did not beat
their nulls -> **EF2raw NOT implemented in the exporter; v17 chain kept;
manifest bumped to v18 only for the skyline fix (T4)**. Honest notes:
the engine chain is now PROVEN engine-true (§3) while failing the
physical-partition hopes — bake pages are REPEATED/tiled per city area
under the engine chain (2.8-4.6x oversubscription, above-random overlap);
round-6's "area bakes with legitimately overlapping tiles" survives in
modified form. m128/m141 compact-rect explanation: plausibility argument,
unproven.

## 5. T2 — classes and exporter damage

- Records (N,K): isl1 (4,2) 276 / (4,1) 9 / (5,2) 9 / (3,1) 11 / (3,0) 1 /
  (1,0) 1; isl2 (4,2) 178 / (4,1) 7 / (5,2) 6 / (3,1) 4 / (1,0) 1.
- Segments: isl1 (4,2) 1092, (4,1) 325, (3,1) 95, (3,0) 5 = 1517; isl2
  (4,2) 658, (4,1) 337, (3,1) 25 = 1020.
- ALL lm-bound street segments are (4,2): the exporter's fixed bytes hit
  the right BYTES everywhere they ship uv1; briefing's "K<2 = m23 and m12"
  was WRONG (m23-isl1 is (4,2); m12-isl1 is (4,1) and not lm-bound).
- TexCoord1's pair is at descriptor index 2 in 285/307 + 184/196 records
  (always byteOff 16 when present); N=3 shifts -12, N=5 +12 ✓.
- Per-class parser = the shipped parser (batch_parser.py) — T1 already
  used per-class selection; re-run under fixed offsets would change only
  the (4,2) chain semantics, which is the §3 contradiction.

## 6. T3 — raycast (scripts/raycast_t3.py)

- Cameras RECONSTRUCTED (session-21's lost): camA = fitCamera proxy
  (fov 55, pos = c + r*(1.05,.62,1.05)); camB/camC = straight-down 120u
  over a Roads0-bound / Crossing-bound segment centroid. Same-camera
  identity NOT provable; the 19.9% coincidence is noted, not claimed.
- camA ground-third: hits 0.184 / void 0.816 (960-ray sampling; class-map
  saved, coarse). Hits by +40: m76 42.4%, m6 11.9%, m23 10.2%, m196 6.8%,
  m70 5.1%, ... (index-level; labels carry nothing). Hit heights median
  7.2u (street level), p90 30.8.
- POSITIVE CONTROL FAILED (rule 8): camB 0.044 hits, 0/71 same-material;
  camC 0.029 hits, 0 same-material. The street archive's floor is sparse —
  triangles under a road segment's centroid belong to other materials —
  the void is largely REAL in the archive. Raycaster NOT certified for
  per-material attribution; certified only for gross hit/void structure
  (and only conditionally).
- Far-LOD slabs (+40 value 34/35, GothamCity_low): 5/6 extents parse to
  garbage (low-archive stride/vertex-format mismatch); one sane slab
  x[-710,0] y[0,2] z[0,779] shows real ground slabs exist. Slab-vs-miss
  coverage NOT established (what the method could not see: the low
  archive's vertex layout). OPEN.
- Verdict: "road-family triangles exist and are intersected" stands;
  "street floor renders near-black / void ~80% of the ground third"
  remains open but is now consistent with genuine archive sparsity.

## 7. Claim status changes (rounds 7-11 -> round 12)

- "m90/m76 exact banked-rect match" (round 7) — RETRACTED in session 21
  (circular); confirmed retracted: no banked rect matches any chain.
- "shipped chain contradicts the engine consumer" (session 21) — UPGRADED
  to PROVEN (uniform-commit path + attr registry + emulation).
- "EF2raw = engine-faithful" (session 21) — CONFIRMED as engine-true
  (w4_raw * s133 + s145; pair slots by descriptor; K from allocate).
- "EF2raw never multi-wraps shows physicality" — held (0/123 multi-wrap)
  but NOT correctness (round rule 3): containment/partition at/worse than
  null.
- "bake pages are area bakes with legitimately overlapping tiles"
  (round 6) — SURVIVES in modified form under the engine chain (2.8-4.6x
  oversubscription, above-random overlap); the round-7 form (shipped
  chain) was based on the wrong chain.
- "K<2 materials are 23 and 12" (round 11 briefing) — REFUTED (m23 is
  (4,2); m12-isl1 is (4,1), not lm-bound).
- "gate v2 asymmetry 0.6 keeps all controls failing" (session 21) —
  CONFIRMED and extended: the mid-load uniform control required a NEW
  night-floor check (near-black >= 0.5); all 6 controls now fail.
- "fingerprint r>=0.5 catches the skyline bug" — DOWNGRADED: r(staged,
  v17-live) = 0.816 >= 0.5 — the fingerprint does NOT catch it;
  stream-complete does.
- "raycast 19.9% road" (session 21) — profile reproduced (0.184 at 960-ray
  sampling) but same-camera identity NOT provable; positive control
  FAILED → per-material attribution uncertified.
- Rounds 7-11 "1517/680 multi-wrap segments" (shipped chain) — superseded
  by material-level: 122/123 lm-bound materials multi-wrap under shipped.

## 8. Deliverables produced this session

Scripts (scripts/): disasm_lhs.py, disasm_fn.py, harness_lhs.py,
batch_parser.py, record_layout_probe.py, record_dump_fit.py, t1_tests.py,
gate_v2.py, gate_controls.py, deploy (repo deploy_site.py reused),
raycast_t3.py, tex_split_convert_tga.py, download_obb.sh.
Artifacts (work/): harness_lhs.json, parser_validation.json, t1_results.json,
t1_run.log, gate_staged_final.json, gate_live.json, gate_deployed.json,
gate_controls.json, gate_noglb.json, fingerprint.json, shot_staged_fixed.png,
shot_v17_live.png, raycast_results.json, ray_classmap_camA.png.
Bundles (download/bundles_s22/): see CLAUDE_HANDOFF.md §22.
