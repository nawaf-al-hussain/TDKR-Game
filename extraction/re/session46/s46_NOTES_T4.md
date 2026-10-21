# s46 T4 — decoded-value parity Python vs JS: PASS on 3 lvc levels; one encoding nuance documented; other decoders audited — PASS

## New: value-level digests (the class where the s45 BE-float bug hid)

Canonical token line `kind|off|value` (floats = raw f64 bits of the f32->f64
widening; strings = latin1 bytes hex; ints/bytes exact). Python (lvc_pure)
vs the SHIPPED lvc.js parseLvc, same dispatch table (re29/lvc_readseq_s30.json)
and gol templates:

| level | tokens | floats | ints | strings | verdict |
|-------|--------|--------|------|---------|---------|
| GothamCity.lvc (7.4 MB) | 1,710,117 | 1,331,305 | 147,757 | 16,731 | sha256 EQUAL |
| GothamCity_Island2.lvc (6.0 MB) | 1,518,149 | 1,253,240 | 75,871 | 7,848 | sha256 EQUAL |
| ThePit.lvc (2.3 MB) | 597,947 | 527,136 | 5,500 | 1,152 | sha256 EQUAL |

New mismatches: NONE.

## Encoding nuance (documented, not a digest mismatch)

lvc.js decodes string-table entries as latin1 (lossless); lvc_pure uses
utf-8/replace. For non-ASCII names the DECODED string values differ between
the shipped pages and the Python reference (bytes identical). The digest
aligns on latin1. Named-next: pick one (latin1) in lvc_pure for consumers.

## Decoder parity audit (what level each already has)

- lvc.js: NOW value-level (this session; was raw-byte/token-hash only).
- animation values: value-level since s35/s38 (npz numeric comparisons).
- skin: value-level (s38 numeric).
- ETC1: pixel-exact 647/647 (s42) + engine-oracle bit-exact + JS-vs-Python
  digest (this session's T2 gate) — value-level x2.
- collision soup: TCS1 byte-identical JS rebuild from user files (s45) —
  stronger than value-level.
- navmesh .nm: counts + raw digest (s44) — decoded-float value digest NOT yet
  covered (fixed-layout BE f32 arrays; low risk; named-next).

## Artifacts
s46_t4_lvc_values.py, s46_t4_js_digest.js, s46_t4_lvc_values.json.
