# s48 T3 — browser reads the compiled binding table: PASS (13x faster than XML)

## Correction to the task's numbers (and s47's)

The scene-material instance table is **307 entries x 36 B @0x5fea0** (not 301 —
s47 stopped one row short of the FX tail). All 307 DB materials have instances;
the 'id' word == entry index 0..306. There are NO "materials without entries"
and mat 302 does NOT need a twin fallback: instance row 302 exists and binds
{DiffuseMap: GC_Z1_Props_Street_Alpha.tga, LightMap: BakeGroup_Island1_A0.tga}
with effect AlphaMasking (== source.dae). The s46 260-B effect records @0x23308
are NOT keyed by material id — record 302's effect string ("SimpleAdditive")
actually belongs to a neighboring instance; every per-material effect claim from
that keying is superseded by the instance table (307/307 effect-URL agreement
with the authoring file).

## Parity (JS in-browser parse == independent Python parse == authoring)

- Canonical [name, DiffuseMap tga, LightMap tga] sorted-by-name digest:
  compiled table = **1d0f1930cf10e5d37edccd911472bd8ed5e9660b01c586c7140281bc4cf4dedf**
  (JS == Python byte-for-byte).
- vs source.dae authoring: **307/307 names, 305/307 full rows**; the only 2 row
  diffs are the FX_Coronas materials (engine DiffuseMap = none — the corona
  textures load through the corona system, s47 T1 explanation stands).
- 0 authoring rows without a scene entry (s47's "6 no-scene rows" were the
  undercount artifact).

## Cost (headless Chromium, user zip path, same process, sequential)

- Compiled binary parse: **4.3 ms**, builds 307 rows from the 455 KB member.
- source.dae XML (DOMParser on 2.19 MB): **56.5 ms** — the compiled table is
  **13.1x faster**.
- Memory: performance.memory.usedJSHeapSize deltas measured 0.00 MB for both
  (counter granularity/GC timing — sub-MB); structurally the DOM tree for
  2.19 MB XML is avoided in favor of ~40 KB of row objects over an existing
  455 KB buffer (which the page must load anyway for effects/params).

## Engine semantics exercised by the parse (for T6)

- profile SNewParam blocks: {name*, semantic*, 13, 1, v1, v2=v1+4}; value header
  {1, v1+24}; node at v1+24 = {u32 image_index}; 0xffffffff = none (null sampler).
- image table: 176 x 12 B @0x22a9c {name*, dup, tga*}; pointers are file offsets
  into little_endian_not_quantized.bdae.
- postLoadProcess would patch SImage pointers at load; the browser resolves
  index -> tga directly (same values, no patching needed).

## Gate

s48_t3_gate.py: 0 console errors, 0 page errors, digest_compiled_match,
digest_xml_match, name_match 307/307, row_ok 305/307, no_scene_n 0,
exactly 2 diffs (both FX_Coronas). VERDICT PASS.

## Artifacts

s48_t3_reference.py (+ s48_t3_compiled.json), s48_t3_gate.py (+ s48_t3_gate.json),
playable/city_slice7.html (branch-only, NOT deployed).
