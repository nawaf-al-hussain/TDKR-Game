# Session 40 (round 30) notes

## State on entry
Remote: main bd7c709, gh-pages a1bf3b1 (v21.1 LIVE), gh-pages-staged 39298a4,
essentials-s36 7c8defc — all as expected. Local repo survived; one untracked
s39c file committed. Credentials: leftover git credential-store file
(/home/z/.git-credentials, mode 600, 75 bytes) DELETED at session start and
`credential.helper = store` removed from ~/.gitconfig. No token this session
-> no push; local commits + verified bundles.

## T1 (bf71bae gh-pages, main mirror) — PASS: ETC1 PROVEN, JS DECODER, STREET PATCH
1. Header format-code histogram over ALL 910 texture chunks in the 7 tex
   archives: 862 valid PVR-v2-LE headers + 48 ZIP-split stream continuations
   (PK zip signature, "SPLIT" member). Codes (flags & 0xff): 0x36 x647 (ETC1),
   0x13 x205 (RGB565), 0x15 x8 (RGB888), 0x12 x2 (RGBA8888). NO other code.
2. Engine mapping (disassembly): CImageLoaderPVR::loadTextureHeader reads the
   52 B LE header, magic 'PVR!', then dispatches on flags&0xff through a
   97-entry jump table -> E_PIXEL_FORMAT in STextureDesc+4. Code 0x36 -> enum
   29; pixel_format::decompress @0x800f84 special-cases fmt 29 = ETC1 (before
   the PFDTable size checks) -> decompressETC1 (statics: modifierTable
   @0xb88710, tableCWShift [5,2,2,8], tableCWMask [7,2], differentialMode
   [0x2,0x2], modeBit [0x2,0x1], flipBit [0x1,0x1,0x0,0x1000000] — all
   consistent with the file layout: t1 bits 7-5, t2 bits 4-2, diff bit 1,
   flip bit 0 of byte3).
   PVRTC ROUTE RETIRED WITH NUMBERS: PVRTCDecompress @0x744148 has exactly TWO
   call sites, both inside pixel_format::decompress, reachable only for
   fmt in {21,22}; the loader produces enum 22 only from header codes 0x0c/0x18
   and enum 21 from none — ZERO occurrences in the OBB. So the engine's
   PVRTC decoder is dead code for every texture in the game. Positive control
   answered in the negative by exhaustive xref (ARM BL any-cond + Thumb BL/BLX
   + literal pools; scanner validated against the two known call sites).
3. Decode: Python reference decoder (calibrated against texture2ddecoder with
   synthetic probes, which is pixel-exact vs the pool PNGs on 17 spot checks
   incl. 2048^2 street atlases) decodes 647/647 ETC1 textures BIT-EXACT.
   Nulls (Gargoyle / BakeGroup_Island1_A0 / Roads0): real 0.00% mismatch vs
   col-major block order 87.3/96.7/94.2%, shuffled blocks 93.7/97.9/97.6%,
   s39-style word-swap 99.98/99.82/99.78% (mean |err| 50-76 vs 0).
   BYTE LAYOUT: b0-2 = RGB (diff: base5=b>>3, delta3=b&7 SIGNED color2-only;
   individual: 4444), b3 = [t1:3][t2:3][diff:1][flip:1], b4-7 = 16 2-bit
   modifiers as TWO BIT-PLANES: planeH = LE u16 of b4,b5 (texel col order
   [2,3,0,1]), planeL = u16 with b7 as LOW byte (col order [0,1,2,3]);
   mod = L + 2*H; out = clamp(expand(c) + MOD[t][m], 0, 255) with expand5 =
   (v<<3)|(v>>2), expand4 = (v<<4)|v; flip=0: x<2 uses color1/t1, flip=1: y<2.
   MODIFIER TABLES = the ENGINE's 8 tables (32 entries @0xb88710) = the
   STANDARD ETC1 intensity modifier tables [CORRECTED s41 T1: rows 5-7 are
   {24,80},{33,106},{47,183} exactly as in the ETC1 spec; the earlier claim
   that they "DIFFER from the ETC2-spec punchthrough numbers" was WRONG —
   74/109/159 was a misreading, and using it broke 521/647 textures
   precisely because the engine/files use the standard table].
4. JS decoder playable/etc1_tdkr.js: node parity 647/647 SHA256-exact (5.8 s).
5. pipeline.html: street patch BakeGroup_Island1_Roads0.tga (2048^2, chunk
   @11,198,218 in l_gothamcity_tex.gla) stream-inflated from the USER's zip and
   decoded in-browser (63 ms), SHA256 in-page == Python reference
   (52fcbf32...), textured ground patch + 2D preview, 0 console errors,
   READY ~1.5 s.
6. s39 FINDINGS RECLASSIFIED (PVRTC route retired):
   - "555 packing / colA bit15 flags" (s39 part 8): ARTIFACT — those fields
     belong to the engine's PVRTC word layout, not the file; the file has no
     555 fields at all (bytes 0-2 are per-channel base|delta).
   - "transposed Morton addressing" (s39 part 8): ARTIFACT of block-order
     confusion; blocks are LINEAR row-major (null: col-major 87-97% wrong).
   - "8x4 texel cells / anisotropic corners": ARTIFACT — ETC1 is 4x4; the
     apparent anisotropy came from decoding ETC mod data as PVRTC bilinear
     weights.
   - "byte3 bit1 always set, values {2,3,6,7,22,23,26,27,43,0b}" (s39): STILL
     VALID and now EXPLAINED — bit1 = diff flag (1 = diff mode), bits 7-5/4-2
     = modifier table indices (3-bit, 8 tables).
   - "bytes 4-7 = 16x2-bit modulation, hist [0.61,0.12,0.12,0.15]" (s39): STILL
     VALID (it IS the modulation), but the s39 bit->texel map was not.
   - "engine PVRTCDecompress expects [4B mod][2B][2B]" (s39 part 2): STILL
     VALID as a statement about the engine, now MOOT (never called for files).
   - "u32swap TV 34.2 vs null 64.4" (s39): ARTIFACT (partial-overlap
     coincidence; word-swap decode = 99.8% wrong).
   - Mod-weight fit / midpoint probing from s39: MOOT (weights are the standard
     per-table modifiers; no uniform-mod fit needed).
7. LIVE PAGE HAD A REAL BUG (found by the gate): s39 T7 (a1bf3b1) introduced
   `const names` redeclaration (module SyntaxError) + Object.keys() on a Map
   (always [] -> every input guard broken). The live pipeline page could not
   load ANY file since v21.1 shipped. Fixed (single [...dir.keys()]).
8. Batman RGB888 path: memory order is B,G,R — verified pixel-exact vs the
   pool on all 8 bpp=24 textures; the live page swapped R/B (invisible on the
   grey suit). Fixed; also height(+4)/width(+8) field order fixed.

Artifacts: extraction/re/session40/s40_t1*.{py,js,json} + this file.

## T2 (c68bbbb) — coverage characterized; volume model stays engine-derived-only
Union position table = trigger class 938977454 (440 records, pos+half; 435/440
ids re-derived straight from the lvc = independent confirmation) + pure-parser
token TRS patterns [B][i][9f] (907 hits, 883 more ids, both islands). Script-id
resolution: callees 44/96, owners 52/84. Real both-positioned pairs: 19 (14
same-class) — STILL << 100. Blockers, precisely: (a) only the trigger class
carries half-extents; (b) generic 0x14CA79 (3,905 records) ids do NOT land in
the script id space (engine-walk toks are fault-truncated: 0 contiguous
[B][i][9f] hits); (c) the remaining 52 callees need the unicorn engine-walk
rerun WITH TObjectData id+TRS capture (beyond this session's time-box). The
test at n=14 still discriminates: inside 0.286 vs null 0.0007 (1,400 same-class
nulls), dn median 6.60 vs 363.2, per-pair rank median 0.0099.

## T3 (cba42a0) — FACE_* RESOLVED; MC_MAX_DISTANCE fifth negative
Thumb-2 LDR-literal xref scanner (39,427 pool targets; validated on the two
known PVRTCDecompress call sites). FACE_* family = the engine character
registry @0xc0b018 (28 entries, vaddr): FACE_X -> actor-name STRINGS
(FACE_BATMAN=Batman, FACE_HOSTAGE=Hostage, FACE_MERCENARY=Mercenary,
FACE_NONE=NULL, FACE_MC=Batman, ... FACE_THUG4=Thug4). The Lua globals are
registered strings, not numbers. MC_MAX_DISTANCE: string @0xb30948, ZERO pool
words, ZERO code refs = FIFTH independent negative -> never registered by the
engine; 10.0 stays a shim placeholder. CAMERA_SHAKE_BOMB: same. ZONE: 36
script-local boolean defs in game_config.gla. Runtime hook still blocked: no
static registrant xref (table referenced via computed addresses), Thumb glue.

## T4 (5f8f8e2) — per-binding test: wiring CORRECT
5/5 measurable loco bindings in EXACT name-keyed FK gait order: mean foot
range Idle 8.28 < Idle_to_Walk 20.75 < Walk 27.50 < Run_to_Idle 30.06 < Run
58.50 (shuffled-binding null P(exact order of 5 random clips) = 0.0071;
individual ranks 0.10/0.18/0.25/0.25/0.85 all in expected directions).
s39's class-level loco failure (p=0.33) EXPLAINED: the xy_rate feature is
wrong for this rig — root xy_rate ~ 0.000005 on transition clips (in-place
anims; locomotion is code-driven), so the class test measured nothing; it was
NOT a binding error. Walk_to_Run _564 inconclusive (ankle channels absent
from the anim; fk-missing in s36 and the s40 rerun; zr 0.106 = highest of all
transitions, consistent with run-ward motion). Wiring UNCHANGED.

## T5 (61fa04f main / 582a0d0 gh-pages) — memory remeasured, real bug fixed
The s38 "13.1 MB heap peak" was V8-heap-only; the implausibility was a REAL
bug: zipDirLazy's `file.size - 1 << 20` parses as (file.size-1)<<20 which
wraps to 0 for an 895 MB zip -> the ENTIRE zip was materialized (~895 MB
external ArrayBuffer; RSS >1.3 GB in the s38/s39 runs) before any parsing.
FIXED (true last-1MiB tail). Post-fix, end-to-end (zip -> actors.gla -> anims
-> skin -> READY, headless Chromium, real zip): JS heap peak 10.0 MB
(performance.memory) / 12.6 MB (CDP); renderer RSS peak 379 MB, ~341 MB near
READY (includes ~100-150 MB SwiftShader software-GL overhead; no GPU here).
Held at READY before release: actors.gla 103.2 MB + actors_tex 30.7 MB +
commons.gla 4.2 MB; the page now nulls these + the 11.5 MB street prefix
after decode. Steady state: GLB 175 KB + street RGBA 16.7 MB + scene. Street
SHA parity still exact; 0 page errors.

## T6 (4da1fc7) — analytic wall-slide follower: honest negative on policy
Analytic wall slide (project mv on the blocking edge at the BLOCKED trial
position; corner-aware, tangent sweeps, NO tunneling), continuous-collision
0.2 m sub-steps with ground re-snap, per-edge step-height A* cost (1 +
2*max(0,dz)), 64 routes (34 hist + 30 seeded, >= 40 required). RESULT:
ok 10/40 same-region vs s38's 13/40. Failure classes: stuck_wall 24,
timeout 3, no_ground 2, step_too_high 1. vs s38: step_too_high 5->1 (step
cost + slide-at-riser WORKS), fell->no_ground 6->2 (sub-stepping prevents
falls), stuck_wall 14->24 — s38's escape hatch crept THROUGH walls
(unverified 0.25 m moves), inflating ok; with tunneling removed the true
collision-data blocking surface is exposed (42,248 slide events; route 61
slid 137 times over 133 m then stuck in a concave pocket). CONCLUSION:
follower policy is NOT the binding constraint; the collision data layer
(missing walkable flags / step geometry) is — s38's conclusion reinforced
with a stricter instrument. Nulls: shuffled dest 14 same/20 cross vs real
hist 10/24 (consistent with s38). A per-route 40k-iteration cap was added
after a micro-slide stall burn was observed (route 27 ground loop).

## T7 (3af4b64, BRANCH s40-user-zip-slice — NOT deployed)
Option (a) first slice: playable/index.html loads Batman from the USER's zip
through the pipeline (zipDirLazy -> guards -> actors.gla -> skin/anims ->
in-memory GLB via the engine-verified assembly; BGR-fixed RGB888 texture).
Gate adapted: file input + #freeze hook preserved; headless gate PASS (skinned
mesh, 3 clips, STATE_TABLE, frozen pose, 0 errors, GLB 175 KB in 845 ms).
Nothing removed anywhere; live site untouched.
EFFORT: option (a) full migration = the street city decoder is the whole cost
(browser-side city bdae/gla decode + material/UV system, est. 3+ sessions);
the Batman slice itself took ~1 hour. What breaks under (a): first-load
latency (+zip pick; the playable becomes unusable without the user's file),
the release screenshot gate must feed the zip (adapted, works), CDN cache
warmth lost. What breaks under (b) (drop street viewer): models/manifest.json
consumers (the city viewer page), ~117 MB of served content removed, site
goes pure-code ~0.8 MB; the playable is unaffected (it never used the street
models).

## T8 — delivery (this session)
No token supplied -> NO PUSH. Local heads: main 61fa04f... wait, T8 commit
extends main; see the final commit list in the delivery message. Verified
incremental bundles (git bundle verify PASS):
- main_s40_inc.bundle (bd7c709..main, 6+1 commits, 85,083 B, SHA256
  fc6349388450b6589156d4b68e3c5b05e94560e24d921b784886e2b5f3cb8ea2)
- ghpages_s40_inc.bundle (a1bf3b1..gh-pages, 2 commits, 7,410 B, SHA256
  d6e8c0e987b35977d796f846b6e1e95c775c165bb51964a49a26187e20c34899)
- slice_s40_branch.bundle (a1bf3b1..s40-user-zip-slice, 3 commits, 12,638 B,
  SHA256 1dd4dec5da2f0c2b938a2eae8a96b8efbc4943ace19a1cf607bbd9e9cf413dc5)
Final ls-remote: main bd7c709, gh-pages a1bf3b1 (v21.1 LIVE),
gh-pages-staged 39298a4, essentials-s36 7c8defc — all unchanged.
CAPABILITY ESTIMATE (unchanged in shape, updated internals): IN = walkable
world (navmesh + collision patches, single region), character renderer +
animation (skeleton parity 6/6, FK-verified, table-driven state resolution),
Lua shim (fengari, 100/100 parity on 100 scripts), browser asset pipeline
(ETC1 bit-exact decoder, GLB assembly, lazy zip streaming). NOT IN = glide,
grapple, combat, AI, mission flow, audio, UI, cloth cape, cross-region
navigation, city-scale rendering from user files (the T7 slice is the first
step of that last one).

## Push addendum (post-T8, 2026-10-20) — token supplied, REJECTED, no push
A classic PAT (ghp_…, same dDfK prefix as the s39 credential) was supplied
in-session. Two validation pitfalls are worth recording: (1) unauthenticated
reads of a PUBLIC repo never trigger the HTTP 401 challenge, so a successful
`git ls-remote` proves NOTHING about a token — the credential helper is never
consulted; (2) the real test is a push or an authenticated API call. The push
was rejected ("Invalid username or token"); `api.github.com /user` and
`/rate_limit` with the same token both return 401 = the token is DEAD
(revoked/expired), not merely scope-limited. NO PUSH PERFORMED; remote heads
unchanged: main bd7c709, gh-pages a1bf3b1 (v21.1 LIVE), gh-pages-staged
39298a4, essentials-s36 7c8defc. Hygiene: the token existed only in the shell
environment and an ephemeral inline credential helper; never written to any
file, never entered .git/config; env cleared immediately after the attempt.
The s39 credential-store cleanup was re-checked this session: no
credential.helper in any visible git scope (system/global/local), no
.git-credentials file in any accessible location — nothing to delete.
Fallback per task book STANDS: local commits + verified incremental bundles.
main_s40_inc.bundle was REGENERATED after this commit (bd7c709..main, now
covers part 9); its SHA256 is recorded alongside the unchanged gh-pages and
slice hashes in download/bundles_s40/BUNDLES_s40_SHA256.txt. NEXT PUSH (when
a live token with Contents:read+write on TDKR-Game exists, fine-grained
preferred): `git push origin gh-pages main s40-user-zip-slice` — three
fast-forwards, locally verified against exactly these remote heads.

## Push 2 addendum (post-part-9, 2026-10-20) — second token VALID, PUSH EXECUTING
A second in-session token (classic PAT, ghp_GeFq…) was validated the RIGHT way
this time: authenticated /user -> 200; X-OAuth-Scopes includes `repo` (the
token is far broader than needed — recommend a fine-grained, Contents-only
token next round and revoking this one after use, since it transited chat);
/repos/nawaf-al-hussain/TDKR-Game permissions.push = true. Cache-consistency
pre-check on the gh-pages delta (a1bf3b1..582a0d0 = +etc1_tdkr.js,
pipeline.html +127/-11, tdkr_pipeline.js zipDirLazy fix): the site uses NO
?v= cache-buster convention on playable pages (plain <script src> tags;
GitHub Pages max-age=600 bounds staleness to 10 min) and models/manifest.json
stays at version 21 (city model set unchanged) — no bump required. THIS
COMMIT IS INCLUDED IN THE PUSH EXECUTED IMMEDIATELY AFTER IT: gh-pages
a1bf3b1..582a0d0, s40-user-zip-slice (NEW branch, tip 3af4b64), main
bd7c709..(this commit). Post-push ls-remote verification recorded in the
session worklog. Token handled ephemerally (env var + inline credential
helper only; nothing persisted to any file or .git/config; env cleared after
the push).
