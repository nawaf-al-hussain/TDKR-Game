# TDKR Asset Extraction Report — The Dark Knight Rises (Gameloft, 2012)

**Private research extraction** — data obtained from the archived Amazon (AMAZ.GloftKRAS) build.
All extracted content remains © Gameloft / Warner Bros. / DC. For private study & mechanics
analysis only — **do not redistribute** any of the assets in this folder.

## 1. Container format (.gla) — reverse-engineered

All `.gla` archives (both `files/data/*.gla` and `files/textures/*_tex.gla`) share one
big-endian index format:

```
u32[0]  build/tag (varies per archive, unused)
u32[1]  indexSize  = byte offset where chunk DATA starts (= end of header+table+name pool)
u32[2]  tableBytes = (numEntries + 1) * 16
u32[3]  numEntries
[numEntries × 16B entries] : u32 offset | u32 size | u32 nameOffset (into pool) | u32 pad
[name pool] : NUL-terminated ASCII names, alphabetically sorted
[chunk data] : chunks are contiguous; entry offset is absolute from file start
```

Verified: 100% of the 27 archives parse with perfect chunk contiguity → 7,731 chunks.

## 2. Texture format (files/textures/*_tex.gla)

Each texture chunk is a **PVR v2 header (52 bytes, little-endian) wrapping an ETC1 payload**
(not PVRTC — confirmed visually; PVRTC decode = structured noise, ETC1 = perfect image):

```
u32 headerSize=52, height, width, mipCount, flags, dataSize, bpp,
u32 maskR/G/B/A (always 0 here), u32 magic 'PVR!' (0x21525650), u32 numSurfs=1
```

| bpp | count | meaning |
|-----|-------|---------|
| 4   | 971   | **ETC1** (base mip first: `ceil(w/4)*ceil(h/4)*8` bytes), flags 0x136 (0x100=mips) |
| 16  | 205   | RGB565 (masks zeroed; flags 0x13) |
| 24  | 8     | RGB888, memory order BGR (flags 0x15) — includes 3 Gotham skyboxes |
| 32  | 2     | RGBA8888 (flags 0x12) |

- Skyboxes are **single-surface dome/panorama maps** (no cubemaps, numSurfs always 1).
- Several textures have octagonal dome unwraps (e.g. `GothamCity_Skybox_Night`).
- 87 chunks are **ZIP archives** (`PK\x03\x04`) named `*.tga` containing a 4-byte `SPLIT`
  marker + one stored ~2.8 MB raw block — stream continuations for huge long-distance
  city LOD textures (`GC_LongDist_*`, `*_FP3`, `*_DIFF`).

**Decoded output**: `textures_png/<archive>/<name>.png` (1,186 PNGs, 0 failures).
Full inventory: `_textures_manifest.csv`.

### Skybox / environment inventory (33 files)
- Gotham storm skyboxes: `GC_Skybox`, `GC_Skybox_02`, `GC_Skybox_02_Industrial`,
  `GC_Skybox_City` (night panorama with lit buildings) — 24bpp originals in commons_tex,
  ETC1 variants in l_batcave_tex
- Night dome: `GothamCity_Skybox_Night` (starfield + clouds, octagonal unwrap)
- Per-level: `SE_Skybox` (stock exchange), `ST_skybox` (stadium), `MC_Skybox` (military),
  `ThePit_Skybox`, `TP_Sky`, `TP_SkyBox`, `underground_skybox`, `GC_Policestation_Skybox`,
  `MM_Pit_sky`
- Vertical fog / city footprint maps: `GC_VerticalFOG{,_IND,_Island2}`, `police_vertical_fog`,
  `underground_vertical_fog`, `BC_Fog`, `MC_Fog`, `TP_Fog`, `ST_fog`, `fog_street_level`
- Reflection envmaps: `new_envmap`, `old_envmap`, `testEnvMap`, `testEnvMap_IND`
- Contact sheet: `contact_sheets/_SKYBOXES_and_ENV.jpg`

## 3. Level / scene data (files/data/*.gla)

Chunks are named `*.bdae` — Gameloft proprietary binary asset format:
- `GC_Bigbridge*.bdae` (+ `_collision`, `_LongDist` LOD variants)
- `GC_Anim_Crane_BoxDrop_{Anim,Collision,Mesh}.bdae` — animation/mesh/collision triplets
- `FX_BLightning_A.bdae` — effects
- `Footprint_*_Reflections.bdae`, building/prop meshes per district
- Extracted raw under `raw/<archive>/` — geometry parsing is the next RE step (formats TBD).

Largest: `l_gothamcity.gla` = 208 MB, 1,071 chunks (the whole Gotham island set).

## 4. Audio (files/data/sounds.gla + sounds.xml)

- 3,110 chunks = **RIFF/WAVE, MS ADPCM** (fmt tag 2, 32 kHz, mono, 4-bit, 1024-byte blocks,
  custom `voxu` chunk of 64 B). Decodable by ffmpeg directly.
- 2 chunks + standalone `data/BATMAN_TDKR.vxa` = **Vxa stream** (`Vxvs` magic v0.0.2,
  "Segmt" chunks) — proprietary, needs separate RE.
- Transcoded to OGG Vorbis q3: `audio_ogg/` (3,110 files).
- `sounds.xml` maps sound events → wav names ( Useful for hooking gameplay events to audio).

## 5. Other data

- `game_config.gla` (26 MB, 51 chunks) — difficulty/economy/upgrade tables (binary, TBD)
- `strings.gla` — localization tables
- `gameswf_*.gla` — ScaleForm/Gameloft SWF UI per device tier (Flash UI + embedded images)
- `options/GPUs.xml` + `options/custom/*.xml` — per-GPU/per-device quality tiers
- Fonts: AccidentalPresidency, Pfennig, RodinNTLGPro, NanumGothic, WenQuanYi, debugfont

## 6. Tooling (scripts kept for reproducibility)

- `scripts/gla_extract.py` — .gla container parser (7,731 chunks)
- `scripts/tex_convert.py` — PVR2/ETC1/RGB565/RGB888 → PNG (probe + bulk)
- `scripts/codec_test.py` — codec identification harness (ETC1 vs PVRTC vs BC1 vs ATC)
- `scripts/make_sheets.py` — contact sheets
- `scripts/convert_audio.sh` — MS ADPCM WAV → OGG

## 7. Reproduction recipe (for any remaining chunk)

```python
# decode any *_tex chunk
buf = open(chunk, 'rb').read()
hs,h,w,mips,flags,dsz,bpp,*_ = struct.unpack('<13I', buf[:52])  # LE
data = buf[52:]
base = ((w+3)//4) * ((h+3)//4) * 8            # 4bpp base mip
png = texture2ddecoder.decode_etc1(data[:base], w, h)  # BGRA buffer
Image.frombytes('RGBA', (w,h), png, 'raw', 'BGRA').save('out.png')
```
