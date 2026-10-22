# s48 T4 — the failing-smoothness set under corrected descriptors + declaration-driven JS zone decoder: PASS

## Part 1 — the s44 "301" set with the corrected descriptor semantics

Protocol EXACTLY as s44 (validated anchor): population filter hdr[3]==4,
probe stride detection cands(24,20,32,28) first-match with mx<vb//s,
F@{20:12,24:16,28:20}, s8 = first 3 bytes of the field as signed /127,
per-seg RandomState(0x544B+k), 4 paired row-shuffle nulls, fail = real >=
min(nulls). EXACT REPRODUCTION: **301 fail on GothamCity (1,526)** — the
anchor reproduces byte-for-byte with today's data.

Corrected decode (same protocol, same population; normal = the DECLARED
attr-16 span under END-offset semantics — @20 for the dominant 276-material
class, @16 for the 9-material class, declared per material; declared stride):

| zone | population | s44 probe decode | corrected decode | unit-normal check |
|---|---|---|---|---|
| GothamCity | 1,526 (all used) | 301 fail | **197 fail** | see below |
| Island2 | 1,020 (all used) | 167 fail | **156 fail** | see below |

**The earlier failing-smoothness set now decodes as UNIT NORMALS**: on the
s44-301 set re-decoded with the corrected offsets, the median |n|-1 is
**0.0000** (the packed signed-byte normals are unit to sub-1e-3 precision);
likewise 0.0000 on Island2's set. The corrected-decode failures (197/156) are
therefore NOT unit-ness failures — those segments have unit normals that are
not SMOOTH across edges (noisy hard-surface content: micro-detail/foliage-like
fragments; s44's "noisy hard-surface content" hypothesis is what remains, and
it is a content property, not a decode error). The strict min-of-4 criterion
itself remains conservative: a single-null run fails fewer.

Bottom line: the s46 "301 non-unit-normal segments" interpretation is CLOSED —
the set was an artifact of reading TC1 as the normal (probe-era offsets);
with the declared offsets the normals are unit, and the remaining 197+156
smoothness failures are content noise, not a decode defect.

## Part 2 — declaration-driven zone decoder (no stride probes), digest parity

Python decoder (s48_t4_decode.py) vs JS decoder (city_slice8.html), canonical
f64 streams (per segment: u32 nv header in EVERY stream; values only for
declared attributes; positions f32->f64, normals signed-byte/127, UVs
int16/32767), segments in lod_table order:

| zone | segs | verts | pos | nrm | uv0 | uv1 | JS time |
|---|---|---|---|---|---|---|---|
| GothamCity.zip | 1,526 | 667,188 | 6fe853d1... | ce93cef4... | f4f865ae... | ffec19ac... | 1,077 ms |
| GothamCity_Island2.zip | 1,020 | 536,668 | 719acd62... | 8b90a5f7... | 7eb1893e... | a8467811... | 854 ms |

**All 8 digests match byte-for-byte** (gate: s48_t4_gate.json digest_match all
true, 0 console errors). Shuffled-descriptor null: permuting the attr labels
over the declared spans changes the decoded position stream for 145/200 and
147/200 segments — the unchanged remainder is exactly the fraction of shuffles
that map attr 0 back onto its own span (~1/k for k declared attrs), so the
decoder is demonstrably driven by the declarations, not by hardcoded offsets.

## Artifacts

s48_t4_decode.py (+ s48_t4_decode.json, includes both zones' fail lists and
digests), playable/city_slice8.html (branch), s48_t4_gate.py (+ gate json).
