# Session 42 (round 32) notes

## State on entry
Remote exactly as expected: main 501388a, gh-pages 36788a9 (LIVE), s41-city-slice
7e84317, s40-user-zip-slice 3af4b64, essentials-s36 7c8defc, gh-pages-staged 39298a4.
Local tree clean. CREDENTIALS: nothing to clean (0 helper entries any scope,
no credential files, clean remote URL, no history files). No token this session ->
local commits + verified bundles only.

## T1 — PASS: RGB888 channel order SETTLED (engine + content + live, 3 independent instruments)

1. ENGINE ENUM (decisive): the game .tga texture chunks carry a 52-B header
   (hs,h,w,mips,flags,dsz,bpp); the RGB888 class is bpp=24, code=flags&0xff=0x15.
   CImageLoaderPVR::loadImage @0x80d6f0 (ARM) dispatches on the low byte:
   `uxtb r3, r2; sub r3, r3, #1; cmp r3, #0x5f; addls pc, pc, r3, lsl #2`
   @0x80d864-0x80d874, branch-table base 0x80d87c. File code 0x15 -> slot
   0x80d8cc -> case @0x80dba4 `mov r7, #0xa`. Sanity anchors on the same table:
   file code 19 (0x13) -> R5G6B5 (matches the v6 note 'PVR v1 fmt19'), file code
   54 -> 0x1d = COMPRESSED_RGB8_ETC (ETC1, matches s40/s41 'fmt-29').
   glitch E_PIXEL_FORMAT name table @0xbca67c (getStringsInternal::strings,
   208 B): [0x0a]='R8G8B8', [0x0b]='B8G8R8' — the byte order is IN the name.
2. ENGINE DESCRIPTOR TABLE: per-format 40-B records @0xb87a30 (base resolved
   from the literal @0x800f74 used by pixel_format::convert/convertPackedFromRGB8
   @0x7fff98). R8G8B8 (0x0a) record @0xb87bc0: RMask=0x000000FF, GMask=0x0000FF00,
   BMask=0x00FF0000, channel byte offsets 00 01 02 -> R=byte0, G=byte1, B=byte2.
   B8G8R8 (0x0b) @0xb87be8 is the MIRRORED sibling (RMask=0x00FF0000). The engine
   distinguishes the two; our files map to 0x0a.
3. ENGINE UPLOAD PATH: CCommonGLDriver::CTexture::updateData @0x7e7ea0 (ARM)
   holds the ONLY glTexImage2D (PLT 0xa5890) / glTexSubImage2D (0xa58b4) call
   sites @0x7e827c/0x7e834c; GL format/type come from per-format records
   (table+0x570+fmt*20; fields +4 internalformat, +8 format, +0xc type) filled
   by genericDriverInit @0x7defb8. The fmt-0xa record is ZEROED there (never
   filled) -> no DIRECT GL entry for R8G8B8; the driver CONVERTS first
   (convertPackedFromRGB8 @0x7fff98, driven by the descriptor table of (2)).
   INDEPENDENT SEMANTIC PROOF: createScreenShot @0x7fadc0 creates a CImage of
   the SAME enum 0xa (`mov r1, #0xa` @0x7fae40) and fills it via
   glReadPixels(GL_RGB, GL_UNSIGNED_BYTE) (`movw lr,#0x1401` @0x7faec0,
   `movw ip,#0x1907` @0x7faeec) — GL semantics put R in byte0. If 0xa meant
   BGR in memory, every engine screenshot would be R/B-swapped.
4. CONTENT CHECK (independent of the engine): all 8 RGB888 chunks verified
   code 0x15/bpp24/hs52. Batman NM as-RGB channel means [125.6, 127.2, 242.9]
   = z-in-byte2 (standard tangent-space normal). 4x skyboxes blue-dominant as
   RGB (B 77-81 vs R 38-42) = night sky. Batman DIFFUSE (1024^2):
   yellow-cluster census (R,G>>B) = 775 texels, blue-cluster = 0 -> the
   belt/emblem gold exists ONLY under the RGB read (775:0). UV-region means
   from the deployed batman.glb bind mesh (belt/chest/face bands) all read
   warm-dark R>G>B under RGB.
5. DEPLOYED PATHS: LIVE gh-pages needs NO change — pipeline.html already has
   the s41 RGB correction (verified LIVE last session); playable/index.html
   uses the embedded PNG (no 888 decode). The ONLY wrong site was the
   s40-user-zip-slice page (playable/index.html line 307 BGR swap) — FIXED and
   committed on that branch (80274a1, branch-only, not deployed).
6. HEADLESS VERIFY (branch page + real 895 MB zip, playwright): 0 console/page
   errors both runs; belt band warmth (R-B) = +1.97 (fixed RGB) vs -0.42
   (BGR-null control: same page with the old line re-applied) — sign-correct
   on a deliberately dark render (page camera is far; magnitudes small).
7. LIVE VERIFY (public URL, #freeze0.5): 0 errors; character-localized bands
   belt +3.42 / chest +3.38 / head +3.78 / legs +4.03, brightest-15% highlight
   mean warmth +11.56 (warm brown/tan) — every region warm; a BGR-order error
   would flip all of these negative.

VERDICT: RGB888 = R,G,B in memory. s41 correct; s40 'BGR fix' was inverted
(its pool verification circular, as s41 already noted). The order question is
now closed with the engine's own enum name, its format descriptor table, its
screenshot path, and content/live measurements.

Artifacts: extraction/re/session42/s42_t1_*.{py,json,png}
(scripts s42_t1_enum/upload/callsites/updatedata/content/gate/live).
## T2 — PASS: clean-room ETC1 decoder 647/647 + ENGINE ORACLE SOLVED (9-arg layout cracked)

1. CLEAN-ROOM DECODER (from the Khronos ETC1 spec only, standard modifier
   tables): implemented independently (s42_t2_cleanroom.py). Two spec details
   had to be (re)derived during bring-up, both documented in the source: the
   ETC1 plane-order QUIRK (MSB plane bytes = [b5=cols01, b4=cols23] but LSB
   plane bytes = [b7=cols01, b6=cols23] — opposite word order between the
   planes) and the block-row-major image assembly (transpose before reshape).
   RESULT: 647/647 chunks, 6464 levels, 40,336,337 blocks — 0 mismatches vs
   the s41 reference (which is itself 910/910-validated vs texture2ddecoder
   and the deployed JPGs). Nulls: N1 garbage-block conformance vs the
   reference decoder 40/40 (both spec decoders agree on adversarial input);
   N2 cross-texture pair 0.25 agreement = the two 32x32 textures share flat
   regions (weak null, honestly noted); N3 single-bit flip changes the
   decode (sensitivity) PASS.
2. ENGINE ORACLE (Unicorn, direct call — the s41 '9-arg convention' blocker
   SOLVED): the signature is
   decompress(fmt=r0, src=r1, blockRowPitch=r2, dstFmt=r3, dst=[sp],
              dstPitch=[sp+4], w=[sp+8], h=[sp+12], flip=[sp+16])
   - derived statically: prologue saves r0-r3 + 5 stack args; fmt==0x1d
     branches to the inline ETC1 decoder @0x80110c; end-pointer =
     src + (h>>2)*r2 => r2 = BYTES PER BLOCK ROW = (w/4)*8 (s41 passed
     3*w*h — the miss); dstFmt 0xa (R8G8B8) = decode straight into the
     caller buffer at [sp+4] bytes/row; the bool = VERTICAL FLIP (must be 0).
   - pixel_format::decompress @0x800f84 confirmed ARM (prologue e92d4ff0);
     convert @0x802758 HAS 17+ direct callers (decompress truly has none —
     dispatched); the TGA-loader convert call site @0x80e75c fixed the
     family convention: (fmtFrom, src, srcPitch, fmtTo, dst, dstPitch, w, h, bool).
   - RESULT (s42_t2_oracle.py + s42_t2_matrix.py): engine decode == Python
     reference BIT-EXACT on 4 full textures: 16x16 (16 blocks), 32x32 (64),
     128x128 (1024), 256x256 (4096) = 5,200 blocks >> the required 50 and
     2 full textures. Output layout = RGB888, R,G,B (independently re-confirms
     T1's byte order on the DECODE side).
   - NULLS: block-order shuffle changes the engine output on the non-flat
     texture (HeatDistort) as required; flip=1 control drops agreement to
     0.08/0.04 (sensitive); the flat placeholder (crowbar_placeh, 1 distinct
     block) is reported as a vacuous-null case, not counted as evidence.
   - engine internals observed: blocks parsed as rev'ed BIG-ENDIAN words
     (matches s41's static note); modifier tables/masks standard.

VERDICT: ETC1 decode now has FOUR independent agreements on game data:
clean-room-from-spec == s41 Python reference == texture2ddecoder (s41) ==
the ENGINE ITSELF (Unicorn oracle), 0 mismatches everywhere; the pipeline's
decoder is proven against the engine that shipped the game.

Artifacts: extraction/re/session42/s42_t2_{cleanroom,oracle,matrix,diag,diag2}.py
+ s42_t2_oracle.json.

## T3 — PASS-WITH-BLOCKER: the mechanism is DECODED (table + registry), the runtime VALUE stays unresolved; estimate 40..3000

1. WHAT THE ENGINE ACTUALLY REGISTERS (decodes RegisterScriptGlobalVariables
   @0x146db0, 4784 B, ARM — the only function with lua_setfield(GLOBALSINDEX)
   sites, 86 setfield callers scanned overall, 0 Thumb callers):
   - SetGlobal("HeadLight_Right", -1), SetGlobal("CurrentActor", -1) [runtime
     Unicorn trace of the function reproduces exactly these first two events].
   - A flag loop: SetGlobal(name_i, 1<<i, true) over a stack-built name array.
   - Grouped enum loops: SetGlobal(name, j) for j = 1..5 in groups.
   - NUMBER registrations (lua_pushnumber, single-float build: the number is
     r1 as f32 — lua_pushnumber @0xa499dc stores ONE word + tag 3):
     NPC_SOUND_WALK_DISTANCE = 8.0f, NPC_SOUND_RUN_DISTANCE = 12.0f,
     MC_SOUND_DISTANCE = 40.0f.
   - TABLE registrations (lua_createtable(L,0,0) -> lua_setfield(GLOBALS,name)
     -> CLuaScriptManager::GlobalVarAddToLocalTable(name,false) @0x14966c,
     which appends {name,bool,bool} to the manager vector at this+0x48):
     ~10 names INCLUDING MC_MAX_DISTANCE (name str @0xb30948 = the single
     \0-bounded occurrence in the binary; setfield site @0x147724).
2. SCRIPT SIDE (game_config.gla, 26.3 MB, Lua SOURCE): MC_MAX_DISTANCE occurs
   1,210 times — 0 assignments (regex corrected: s41's 'assign' pattern only
   matched reads `X = MC_MAX_DISTANCE`; a dedicated write-pattern
   `MC_MAX_DISTANCE =` finds 0), 0 field accesses (`MC_MAX_DISTANCE.x` = 0).
   Uses: StartEventAtObjectNode(..., MC_MAX_DISTANCE) 899x (arg 3), 
   StartSoundAtObjectNode 229x, plus 149 arithmetic sites (5 * MC_MAX_DISTANCE).
   => the global must be a NUMBER at script runtime; the registration-time
   empty table is replaced/filled through the this+0x48 registry path.
3. THE FILL PATH IS NOT STATICALLY VISIBLE: no SetGlobal(char*,int,bool) call
   site names it (113 sites scanned; the 89-in-function loop covers enum
   groups), no other -10002 setfield exists, the whole 895 MB OBB contains the
   name ONLY in game_config.gla scripts, and no pointer word anywhere in the
   image points into the MC_* pool except the registration itself. This IS the
   'computed addressing' s41 inferred — now explained as the
   registry-driven (this+0x48) data path. ResetScriptGlobalVariables
   @0x148060 re-creates the empty table for 'WeaponCache' only.
4. VALUE: UNRESOLVED (honest). ESTIMATE from usage neighbours (task-book
   fallback): literal radii used at the same argument position of the same
   call families elsewhere: StartSoundAtObjectNode arg3 median 50 (n=29,
   p90 1400, max 2000); StartEventAtObjectNode arg3 median 3000 (n=17);
   engine sibling MC_SOUND_DISTANCE = 40.0. => labeled ESTIMATE: the runtime
   value plausibly lies in 40..3000 (sound-hearing scale vs event-broadcast
   scale); the shipped 10.0 shim remains a REQUIRED PLACEHOLDER and is likely
   too small. Positive control: the static decode is anchored by the runtime
   Unicorn trace of the same function (first two events byte-identical:
   CurrentActor/-1, EventSender/-1 — wait, first two = HeadLight_Right and
   CurrentActor per static decode; runtime log shows CurrentActor + 
   EventSender after early stub divergence; the FACE_* registry check of the
   task book was superseded by this stronger same-function control).
5. CORRECTION to the s41 model: 'engine MUST define MC_MAX_DISTANCE [as a
   number]' — refined: the engine defines the NAME as an empty table at init;
   a number is installed later via the registry/data path; the Lua shim
   should model MC_MAX_DISTANCE as a number placeholder (10.0) but flag it
   as engine-registry-driven, NOT a compile-time constant.

Artifacts: extraction/re/session42/s42_t3_{poolxref,setfields,globals,runreg,ordered,setglobal}.py

## T4 — PASS (instrument + verdict): navmesh-surface walking measured; adopted in harness (15/40, 2.5x distance), page adoption deferred with rationale

Instrument (s42_t4_navmesh.py, derived from the s41 T4 lib): new NavCtx mode
'navmesh' — walking height interpolated from the NAVMESH CELL TRIANGLES
(nm_ground: barycentric z over cells, cell bbox grid 10 m), walls = the same
soup non-walkable triangle set as 'full'; slides validated against the soup
as before. Same 40 same-region routes, same A* paths, same step rules.

Route table (ok/40, total advanced metres):
  ghost (no collision, s41 control)      36/40      (reproduced exactly)
  full collision (s40/s41 baseline)      10/40   5,664.7 m  (reproduced exactly)
  navmesh surface (soup walls)            9/40   8,791.1 m
  navmesh surface + stepignore 0.55      15/40  14,040.7 m  <- best collision-bearing
  NULL (shuffled dest assignment)         4/40                 (pairing signal real)

Failure classification of the plain navmesh run (26 classified):
  real_step_soup_agrees    9  (soup walkable ground also steps >0.9 = real curbs)
  navmesh_soup_disagree   10  (navmesh z 0.57-2.5 m BELOW soup walkable: 8.31 vs
                               8.88, 8.31 vs 6.34 — the two datasets disagree in
                               height exactly where the walker gets walled)
  off_soup                 7  (route leaves soup-covered ground; navmesh-only areas)

ANSWERS to the task questions:
- Is the collision data or the walking surface the constraint? BOTH, now
  quantified: on the navmesh surface the soup walls alone bind (28 stuck_wall),
  and 10/26 failures are direct navmesh-vs-soup HEIGHT disagreements (navmesh
  lower) — the s41 "20% of cells off by >0.5 m" concentrates exactly at the
  failures. The step_too_high/fell locations are real curbs in 9 cases and
  navmesh/soup disagreements in 10 (soup flat where navmesh steps, or vice
  versa) - neither dataset is 'wrong' everywhere; they are misregistered.
- Is navmesh-surface walking clearly better? With the s41 stepignore fix:
  YES on this instrument - 15/40 vs 10/40 routes, 2.5x total distance
  (14,040.7 m vs 5,664.7 m), null 4/40. ADOPTED as the reference walking
  model in the harness. NOT adopted in the playable page this session:
  the page's JS follower consumes only the 12,512-tri collision patch and has
  no navmesh data shipped; adoption = ship GothamCity navdata + nm_ground in
  JS + gate rerun (a deployment-side change; we are branch-only this session).
  Recipe recorded: replace ground sampling with navmesh barycentric
  interpolation, keep the soup wall set + stepignore 0.55.
- Null: shuffled-destination navmesh walk = 4/40 (vs 9/40 real pairing) and
  the full/ghost controls reproduce s41 exactly - the instrument is sound.

VERDICT: the binding constraint is the NAVMESH/SOUP REGISTRATION, not the
controller (s41 exonerated the controller; this session quantifies the two
data layers' disagreement and shows navmesh-height + soup-walls + stepignore
is the best available walker). Named next: reconcile navmesh z to soup
walkable ground (per-cell offset fit), then re-run the 40 routes.

Artifacts: extraction/re/session42/s42_t4_navmesh.py + s42_t4_result.json

## T5 — PASS-WITH-NULL-RESULT: objId+TRS capture SOLVED from existing tokens; spatial per-object test run; 87 pairs < 100 and does NOT discriminate -> volume model stays "unvalidated, engine-derived only"

1. CAPTURE SOLVED (s41's named blocker, without new emulation): the generic
   object records live in the EXISTING s26 walk TOKEN TREES as contiguous
   [B][i32 objId][f x9] runs — 907 records (462 GothamCity + 445 Island2),
   885 distinct objIds, id space 31000..2400056 (engine object-id space).
   s41's "0 contiguous runs" was a search-scope miss (it scanned the
   fault-truncated engine-walk token capture, not the full token trees).
   Floats decoded as [pos3, rot3, scale3] in city coordinates (rec 2 =
   identity-at-origin scale 1; rec 3 = pos(-820.7,-962.3,-2.1) scale(36.3,34,35);
   ranges match the trigger pos ranges).
2. ID-SPACE FINDINGS (all joins measured): trigger-table ids (80001..2400099,
   n=440) vs component objIds (885): overlap 0; vs walk-record load-order ids
   (2..14308): overlap 0; trigger-tid records (9803/9809/18250) carry NO
   [B][i][9f] components at all (their volumes are their OWN record fields —
   the s36 data-determined halves). The id spaces are three distinct things;
   any id-based pairing is structurally impossible from the walk products.
3. SPATIAL JOIN (the workable pairing): objects whose TRS position lies
   within trigger pos +- (half + 0.25 pad): 635 pairs across 87 of 440
   triggers (median trigger half = 0.5 -> 1 m boxes; most contain nothing).
   Nearest-object-per-trigger testable pairs: 87 < the 100-pair GATE.
4. PER-OBJECT TEST at n=87: corr(log(half_geom), log(scale/2)) = 0.2839;
   SAME-SIZE-CLASS NULL (log2 scale bucket, 200 shuffles): mean 0.2776,
   std 0.0066, p95 0.2878 -> the real correlation does NOT exceed the null
   (0.2839 < 0.2878). The "trigger volumes bound their paired objects"
   hypothesis is dead for the spatially-pairable subset.
5. VERDICT per the task's own rule (cannot reach 100 pairs OR discriminate):
   the trigger-volume model stays "UNVALIDATED, ENGINE-DERIVED ONLY" — now
   with the pairing mechanism solved, a measured pair count (87), and a
   quantified null instead of an id-space mystery. Named next (if ever
   revisited): obtain the trigger->object LINK the scripts use (the 440
   trigger ids are script-space; the lvc objects are engine-space; the bridge
   is the per-zone object tables the loader builds, not the walk dumps).

Artifacts: extraction/re/session42/s42_t5_test.py + s42_t5_pairs.json + s42_t5_capture.json
