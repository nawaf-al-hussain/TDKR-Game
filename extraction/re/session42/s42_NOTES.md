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
