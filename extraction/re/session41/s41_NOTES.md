# Session 41 (round 31) notes

## State on entry
Remote exactly as expected: main 13b7890, gh-pages 582a0d0 (LIVE, s40 content),
s40-user-zip-slice 3af4b64, essentials-s36 7c8defc, gh-pages-staged 39298a4.
Local tree clean. CREDENTIALS: nothing to clean — 0 credential.helper entries
in any git scope, 0 remote URLs containing '@', no shell history files, no
.git-credentials anywhere accessible (the s40 cleanup already removed
/home/z/.git-credentials, mode 600, 75 bytes, + the ~/.gitconfig helper entry).
No token this session -> local commits + verified bundles only.

## T1 (this commit) — PASS: full-page deployment gate + negative controls + LIVE verification
1. NEW GATE (s41_t1_gate.py, playwright/chromium): loads EVERY gh-pages page
   locally (street viewer index.html, playable/index.html, playable/
   pipeline.html with the real zip) and fails on ANY console error, pageerror,
   requestfailed, non-2xx response, or unmet DOM/canvas expectation.
   RESULT: 3/3 pages PASS. Batman IoU vs numpy truth 0.9421 (lying null
   0.0229, shifted 0.002); pipeline street SHA == Python reference
   52fcbf32...; street viewer scene alive (children>0, 583k tris, fg painted).
2. NEGATIVE CONTROLS (new): for each page a copy with an injected
   SyntaxError script served from a symlink-farm overlay; the SAME monitor
   must flag it. 3/3 controls flagged (pageerror: Unexpected token).
   Incident recorded honestly: the first farm build used a DIRECTORY symlink
   for playable/ and the corrupted-page replace step followed it and deleted
   the real worktree playable/index.html (restored via checkout; the farm was
   rewritten to real dirs + file symlinks + a ROOT-alias assert on the parent
   path). Lesson: path-aliasing in overlay farms is a data-deletion hazard.
3. LIVE VERIFICATION via public URLs (s41_t1_live.py): all three pages
   PASS, 111 requests 0 non-2xx, 0 console errors.
   - Batman: IoU 0.9421 / lying 0.0229 / wrong-pose 0.89 / shifted 0.002;
     FK idle+run at 2 times each vs numpy = max 2.0 cm (wrong-time null mean
     30.0 cm = sensitive); albedo-vs-texture 5.0.
   - Pipeline: READY in ~1 s, street SHA exact, preview-canvas colour
     statistics vs Python reference: the preview draws the TOP-LEFT 512x512
     CROP (drawImage full,0,0,512,512 -> 256) — stats vs that reference:
     mean-dist 0.12, std-dist 0.05; NULL (BakeGroup_Island1_A0 same crop):
     mean-dist 19.9 = margin ~20x over the pass threshold.
   - Street viewer: scene children 8, "streaming city 6-7/21", 583-596k tris,
     0 errors while streaming (gate checks error-freedom, not completeness).
4. s40 NOTES CORRECTED (in place, marked [CORRECTED s41 T1]): the engine's
   8 modifier tables ARE the standard ETC1 intensity modifier table (rows 5-7
   = {24,80},{33,106},{47,183}); the "differ from ETC2-spec punchthrough"
   claim and the 74/109/159 numbers were WRONG (s40_t1_refdec.py comment
   fixed too). The JS/Py decoders always used the correct values (647/647
   bit-exact), so no code change — notes only.

Artifacts: extraction/re/session41/s41_t1_*.{py,json,png} + s41_refdec_lib.py.

## T2 (next commit) — PASS: 910/910 chunk parity, 0 exceptions; engine oracle INCONCLUSIVE
1. FORMAT RECON (s41_t2_recon.py): all 910 OBB chunks classified: 647 ETC1 +
   205 RGB565 + 8 RGB888 + 2 RGBA8888 + 48 ZIP_SPLIT. Mip semantics PROVEN:
   dsz(+20) = sum of levels from w x h down to 1 x 1 inclusive (header `mips`
   field = log2(max dim); the chain holds log2+1 levels) — verified exactly
   on all 647 ETC1 chains + 96 split-member chains (0 exceptions).
2. ZIP_SPLIT CRACKED (s41_t2_split.py): each of the 48 entries is an embedded
   STORED zip: 'SPLIT' (4-byte zero marker) + 'rgb.pvr' + 'alpha.pvr' — both
   members are complete standalone ETC1 PVRs with full mip chains (rgb e.g.
   512^2 mips=9, alpha 256^2 mips=8; alpha can be half-res). The combination
   is shader-side (rgb supplies color, alpha.pvr the alpha plane); parity is
   per member.
3. CHANNEL-ORDER CALIBRATION with independent references (s41_t2_calib*.py):
   - RGB565: u16 LE, R5G6B5, BIT-REPLICATION expansion — EXACT (1.0000) vs
     the deployed lossless LUT_000_default.png (512x16). (Arithmetic scaling
     *255//N is wrong: only 0.12 exact.)
   - RGB888: memory order = R,G,B — NOT BGR as the s40 note claimed (the s40
     "pixel-exact vs pool" check was circular: the pool shared the same
     convention). Independent evidence: chara_Batman_NM memory means
     [125.6,127.2,242.9] = z-in-byte2 = standard normal map under RGB;
     GC_Skybox [38.6,62.1,77.2] = blue-dominant sky under RGB; City_BKG corr
     slightly favors RGB. CORRECTION propagated to the live-page question:
     pipeline.html's s40 "BGR fix" actually SWAPS R/B on 888 textures
     (invisible on the grey suit); fix prepared, NOT deployed (no push).
   - RGBA8888: memory order = R,G,B,A (byte3=alpha=255 constant on
     FX_Coronas_Glow; template match vs deployed FX_Coronas.jpg corr(R)=0.906
     > corr(B)=0.896; consistent with the RGB888 finding).
4. FULL PARITY (s41_t2_build.py + s41_t2_parity.js): Python reference decodes
   ALL 910 chunks incl. every mip level and both split members; node JS
   decodes the same raw payloads from a pack INDEPENDENTLY (etc1_tdkr.js for
   ETC1/split, fresh typed-array decoders for 565/888) and compares SHA256
   per level AND per chunk: ETC1 647/647, RGB565 205/205, RGB888 8/8,
   RGBA8888 2/2, ZIP_SPLIT 48/48 — 910/910, 0 mismatches, 11.3 s.
   Reference global sha 38ea26f86c7b5aafbc6a4d25...
5. MIP CHAINS: all levels decoded + size-checked (see 1); sanity contact
   sheet for Assault-rifle_HKG36C_d (10 levels 512^2 -> 1x1, dsz exact)
   saved as s41_t2_mipsanity.png.
6. ENGINE ORACLE (s41_t2_oracle.py) — INCONCLUSIVE within the time-box:
   unicorn+capstone installed; whole-image ARM emulation harness with
   bump-allocator interception reaches the fmt-29 inline decoder (fresh
   static confirmation: BE-word reads + masks 0xf8000000/0xf80000/0xf800,
   sbfx sign-extended deltas = standard ETC1 unpack over b0=R,b1=G,b2=B).
   BLOCKED on the 9-arg convention: 0x800f84 has ZERO direct BL/BLX callers
   and zero pointer references (dispatch is computed), so the true argument
   semantics (loop bounds) could not be reconstructed from the function body
   alone. NAMED NEXT: reconstruct the computed-dispatch call path (ADR/ADD
   stubs around 0x800f40), then re-run the harness.

## T3 (next commit) — PASS-with-blocker: usage analysis DECISIVE; hook still blocked
1. POSITIVE CONTROL (same kind) now run formally: FACE_HOSTAGE string
   @0xb42c6c -> exactly 1 pointer word, the registry entry @0xc0b050 — the
   scanner sees registered names. Registry 0xc0b018.. = a contiguous
   name-pointer array (FACE_NONE, FACE_BATMAN, ..., FACE_HOSTAGE, ...).
2. TAIL-MERGE REFUTED: MC_MAX_DISTANCE occurs EXACTLY ONCE in the loaded
   image, \0-bounded on both sides (@0xb30948; context: REWARD_PROPERTY |
   MC_MAX_DISTANCE | INTERFERENCE_COOLDOWN_TIME). Nothing to merge into.
3. SIXTH NEGATIVE, now exhaustive across ALL address-formation modes:
   0 pool words, 0 Thumb LDR-literal sites, 0 MOVW/MOVT pairs pointing at
   0xb30948. The whole sibling name pool (SFX_*, NPC_*_DISTANCE,
   MC_SOUND_DISTANCE, CAMERA_SHAKE_*, REWARD_*, g* globals) has ZERO pointer
   words for ANY member — consumed via computed addressing / runtime string
   registration; the FACE_* registry is a DIFFERENT mechanism.
4. SCRIPT USAGE (decisive new evidence, 1,210 sites in game_config.gla):
   313 commented, 897 LIVE — 748 call arguments
   (StartEventAtObjectNode("env_...", CurrentActor, MC_MAX_DISTANCE) = the AI
   awareness radius), **149 ARITHMETIC** (e.g. 5 * MC_MAX_DISTANCE) where nil
   would raise "attempt to perform arithmetic on a nil value", 0 comparisons,
   0 definitions in ANY data file of the OBB. => The engine MUST define
   MC_MAX_DISTANCE; the constant is data/code-driven through the
   computed-addressing mechanism invisible to static xref. MC_MAX_DISTANCE is
   the ONLY member of its pool with arithmetic use (CAMERA_SHAKE_BOMB 27
   uses 0 arith; MC_SOUND_DISTANCE 309/0; FACE_* all value-passed).
5. VERDICT: the 10.0 shim placeholder is REQUIRED (scripts error without
   it), and its VALUE remains unproven — the Lua C API hook (lua_setglobal
   during boot) is the only remaining route and stays blocked by the Thumb
   glue / computed dispatch (s39/s40 finding, unchanged). Inconclusive on
   the value; conclusive on "must be defined".
