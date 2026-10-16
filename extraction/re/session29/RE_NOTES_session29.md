# RE Notes — Session 29 (round 19)

## T1: lvc parser finished

### The id-resolution break (corrects session 28's premise)
Session 28 concluded "component ids are runtime name-hashes and never appear as
literals; unknown ids do NOT default to zero reads". Both halves were extraction
artifacts:

1. **The ids ARE literals.** ARM MOVT encodes as `cond 0011 0100 imm4 rd imm12`
   — top-byte mask `0x03400000`, NOT `0x04000000`. With the correct mask a
   whole-.text MOVW/MOVT pair scan resolves every 32-bit component id:
   - `0xC69A6A7`  → factory case @0x369d58 (generic switch, `cmp; bne` form) →
     vt 0xbd0e30 → `CComponentZonesLink::Load` @0x2e7430 (symbol) — spec `[i][i]`
     (two BE i32 = two zone ids)
   - `0x2AD64F3D` → factory case @0x22453c (`cmp; bne`, inline body) + GetType
     thunk @0x2e1db0 returns exactly this value → `CPlaneNodeComponent`
     (Load @0x2a0728) — spec `[f][f][i][i]` (16 B)
   - `0x3377F0E`  → **absent from the entire .so** (no cmp/literal/MOVW-MOVT
     anywhere). Positive controls: the same scan finds 0xC69A6A7, 0x2AD64F3D,
     0x17AC851F, 0x7F88E44E, 0x2888019A, 0x39E32181. Unregistered class →
     CreateObject null-checks GCT's return (@0x367fe4 `subs r3,r0,#0; beq`) and
     skips: 0 reads.
   - Bonus resolutions: `0x7F88E44E` = CComponentBuiltinCollisionBox,
     `0x2888019A` = CComponentBaseWorldBox (Load @0x2e6a08 = `[i][f x6][i]`
     32 B bbox), `0x39E32181` = CComponentMetaZone (Load @0x3c13f8 =
     `[i n] + n x [i]`), `0x10FCFD6` = CDummyComponent (Load @0x22a368 reads
     0 B; session 28's "0x10FF796" was a hex typo), `0x16F31` =
     CComponentNewShopItemProperty, `0x2AD2A046` = CComponentBuiltinCollisionPlane.
   - Session 28's refuted-hypothesis note ("unknown ids do NOT default to zero
     reads") is superseded: ids that HAVE cases have real Loads; ids that are
     absent from the .so are skipped with 0 reads by the CreateObject null-check.

2. **Dispatch completeness.** The generic switch (0x368ac0) and factory switch
   (0x223e3c) use BOTH `cmp; beq` (case body at target) and `cmp; bne`
   (case body inline). Session 25's extractor only matched the first form,
   which is why 0xC69A6A7/0x2AD64F3D/0x7F88E44E looked "absent from both
   switches". dispatch_complete.json now lists 59 factory + 64 generic ids.

### Level status (pure parser, all to table end unless noted)
| level | records | state |
|---|---|---|
| GothamCity | 14313 | OK |
| GothamCity_Island2 | 7474 | OK |
| BatCave | 92 | OK |
| l_menu | 31 | OK |
| Stadion | 274 | OK |
| Police_Station | 653 | OK |
| StockExchange | 2023 | OK |
| Underground | 2653 | OK |
| Military | 773 | OK |
| ThePit | 700 | OK |
| shop | 3778 | PARTIAL: 113/114 records match the native walk 1:1; the tail 0x3ccc..0x40ec contains tids (0x16F3C/41/43/48/4A/53/88 family) that appear NOWHERE in the engine; the s25 walker (GCT-null patched to skip, matching CreateObject's null-check) still cannot frame the tail; parse lands 2 B past the table |
| Test | — | engine-confirmed data anomaly (round 17: bogus STR index 960462848 at rec 13; native tracer agrees) |

### Cinematic class
CCinematicComponent (0x17AC851F) Load itself performs ZERO stream reads; all
reads are inside CComponentCinematic::Load @0x2dce20 (6312 B, head
`[i dur][c][f][c][i n1]`, n1 vector of 16-B elements, n2 12-B-element vector
with the fill-read gate at 0x2dd738 skipping when n2<=0) and the per-element
CContainerTracksAnimatedObject::Load @0x2d9118 (inner tail not fully inverted).
**The class remains span-replayed**: 96 instances banked (34 islands from
round 17 + 62 newly measured natively this session at each component offset).
Grammar derived ~80% from disasm + 34 byte-exact island token streams
(rot/pos event shape `[i id][i 0][i 1][STR interp][i nkeys] + nkeys x [i tick]
[f x][f y][f z]`, anim events `[i n][i id][i ?][STR clip][i ?][f ?]`,
tail counts rot/scale/effect/sound/script) — listed as span-replayed, not PASS.

### LevelInit trailing word (i_nz)
The 0x2657 case's final word: read as part of the record when nonzero
(GC/I2: 31004 = 0x791C, the next record's dedicated tid absorbed), left as a
separate tid-0 skip record when zero (shop). Fitted rule `i_nz` = peek; read
iff nonzero; 3 observations (GC, I2, shop). Implemented in lvc_pure.py and lvc.js.

### Independence
All round-19 component specs come from disassembly + symbols (level-independent
by construction). Spans are per-instance file offsets (no cross-level reuse).
Leave-one-island-out is therefore structural: no island contributed bytes to
any spec; GC parses with zero I2-derived data and vice versa.

### JS vs Python
test_lvc_s29.js: **10/10 levels PASS** — record boundaries AND per-record
SHA1 token streams, JS == Python on GothamCity, GothamCity_Island2, BatCave,
l_menu, Stadion, Police_Station, StockExchange, Underground, Military, ThePit.

### Header count (offset 13)
Round 17 refuted records+links (GC 14313+4407=18720 != 14917) and components
(21003 != 14917); LoadRawLvl @0x4891f8 reads the field into r6 and never uses
it (exporter-side bookkeeping). Round 19 re-fit on all 10 parsed levels:
see s29_header_fit.json — still unexplained.

### Whitelist-off
Round 16's census stands (1474 component runs fault post-read; reads complete
proven by the fault-free pure parser). Round 19 adds: the genuinely-unregistered
ids (0x3377F0E Military, 0x1D50AA73 shop rec 114) take the GCT null path —
CreateObject skips them (0x367fe4), the data after such tids is never read by
the engine.
