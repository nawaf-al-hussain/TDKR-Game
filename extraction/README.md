# TDKR Asset Extraction Toolkit

Reverse-engineering toolkit for the Gameloft `.gla` resource containers found in
*The Dark Knight Rises* (mobile, 2012) OBB data pack. **Private research use only** —
all extracted game content remains © Gameloft / Warner Bros. / DC. Do not redistribute assets.

**Start with [`REPORT.md`](REPORT.md)** — full format documentation, texture/skybox
inventory, and findings.

## What is versioned here vs. local-only

| Location | Contents | Size |
|---|---|---|
| `extraction/` (this folder, in git) | scripts, report, manifests, contact sheets, skybox previews | ~15 MB |
| `download/TDKR_assets/raw/` (local only) | all 7,731 extracted chunks | 1.8 GB |
| `download/TDKR_assets/textures_png/` (local only) | 1,186 decoded PNG textures | 478 MB |
| `download/TDKR_assets/audio_ogg/` (local only) | 3,110 OGG-transcoded sounds | 136 MB |

The full asset trees stay local (too large for git); everything needed to regenerate
them from the OBB release zip is versioned in `scripts/`.

## Layout

```
extraction/
├── REPORT.md                  # reverse-engineering report (formats, inventory, recipe)
├── scripts/
│   ├── gla_scan.py            # forensic scanner: header/TOC/magic probe of .gla files
│   ├── gla_extract.py         # .gla container parser → raw/<archive>/* + chunk manifest
│   ├── codec_test.py          # codec ID harness (proved ETC1 vs PVRTC/BC1/ATC)
│   ├── tex_convert.py         # PVR2/ETC1/RGB565/RGB888/BGR888 → PNG (+ textures manifest)
│   ├── make_sheets.py         # thumbnail contact sheets per archive
│   └── convert_audio.sh       # MS-ADPCM WAV → OGG Vorbis (parallel ffmpeg)
├── manifests/
│   ├── gla_chunks_manifest.csv    # 7,731 chunks: archive, name, offset, size, magic, sha256[:16]
│   └── textures_manifest.csv      # 1,186 textures: archive, name, w×h, bpp, codec
└── previews/
    ├── contact_sheets/*.jpg   # one thumbnail sheet per texture archive (14 sheets)
    └── skyboxes/*.png         # full-res skybox / envmap / vertical-fog samples (16)
```

## Reproduction pipeline

```bash
# 0. unzip the release asset (TDKR_v1.1.6b_APK_OBB.zip) →
#    com.gameloft.android.AMAZ.GloftKRAS/files/{data,textures}/*.gla
# 1. parse containers (edit BASE/OUT paths at top of scripts first)
python3 scripts/gla_extract.py
# 2. decode textures  (pip install texture2ddecoder pillow)
python3 scripts/tex_convert.py
# 3. transcode audio  (requires ffmpeg)
./scripts/convert_audio.sh
# 4. optional visual QA
python3 scripts/make_sheets.py
```

Requirements: Python 3.10+, `texture2ddecoder`, `pillow`, `ffmpeg`.

## Key findings (see REPORT.md for detail)

- `.gla` = big-endian index container: 16-byte TOC + alphabetical NUL name pool + contiguous chunks; 27/27 archives parse with perfect contiguity.
- Textures = 52-byte PVR v2 header wrapping **ETC1** (4bpp, 971), RGB565 (205), BGR888 (8, incl. 3 Gotham skyboxes), RGBA8888 (2).
- Skyboxes are single-surface dome/panorama maps (no cubemaps); 33 skybox/env/fog assets inventoried.
- Level chunks are `*.bdae` (Gameloft scene/mesh/animation format — parsing is the next RE milestone).
- Audio is MS-ADPCM WAV (ffmpeg-decodable) + 3 proprietary `Vxvs` streams.
