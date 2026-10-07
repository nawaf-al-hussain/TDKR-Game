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
│   ├── convert_audio.sh       # MS-ADPCM WAV → OGG Vorbis (parallel ffmpeg)
│   ├── bdae_probe.py          # BRES header/section dumper + byte-region classifier
│   ├── bdae_mesh_scan.py      # stride/anchor brute-forcer + rendered verification plots
│   ├── bdae_extract.py        # BDAE mesh-block chain parser → GLB exporter (Y-up + textures)
│   ├── bdae_survey.py         # batch survey of all .bdae files (stats → JSON)
│   ├── bdae_uv_verify.py      # UV-sampled texture render (proves UV + lightmap binding)
│   ├── export_showcase.py     # exports the five web-app showcase GLBs
│   └── export_city.py         # full-city LOD-aware Pages export (tiered GLBs + JPEG atlases)
├── manifests/
│   ├── gla_chunks_manifest.csv    # 7,731 chunks: archive, name, offset, size, magic, sha256[:16]
│   ├── textures_manifest.csv      # 1,186 textures: archive, name, w×h, bpp, codec
│   └── bdae_mesh_survey.json      # per-file mesh stats: 853 files, 1.24M verts, 509K tris
└── previews/
    ├── contact_sheets/*.jpg   # one thumbnail sheet per texture archive (14 sheets)
    ├── skyboxes/*.png         # full-res skybox / envmap / vertical-fog samples (16)
    └── meshes/*.png           # island1 top/side views, UV-textured verification renders
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
# 5. BDAE meshes: survey all files, then export showcase GLBs (numpy + pillow)
python3 scripts/bdae_survey.py
python3 scripts/export_showcase.py
# 6. full-city export for the GitHub Pages viewer (stages work/site/)
python3 scripts/export_city.py
```

Requirements: Python 3.10+, `numpy`, `pillow`, `texture2ddecoder`, `ffmpeg`.

## Key findings (see REPORT.md for detail)

- `.gla` = big-endian index container: 16-byte TOC + alphabetical NUL name pool + contiguous chunks; 27/27 archives parse with perfect contiguity.
- Textures = 52-byte PVR v2 header wrapping **ETC1** (4bpp, 971), RGB565 (205), BGR888 (8, incl. 3 Gotham skyboxes), RGBA8888 (2).
- Skyboxes are single-surface dome/panorama maps (no cubemaps); 33 skybox/env/fog assets inventoried.
- `.bdae` = **BRES / Binary DAE** (compiled COLLADA): chained mesh blocks, `[pos 3×f32][normal 11-11-10][uv 2×u16]` vertices, u16 indices, material name in footer — 853 files / 1.24M verts / 509K tris extracted.
- **Full city live on GitHub Pages**: 255 non-collision `l_gothamcity` meshes (348K verts / 203K tris) stream as 34 geometry-only GLBs + 35 external JPEG lightmaps at https://nawaf-al-hussain.github.io/TDKR-Game/ — tiered skyline/footprints/districts/LOD loading via `scripts/export_city.py`.
- Static + collision mesh geometry is fully parsed; still open: scene-graph node transforms, material→DiffuseMap tables, ZIP_SPLIT long-distance texture reassembly, skinned actor vertex formats, Vxvs audio streams.
- Audio is MS-ADPCM WAV (ffmpeg-decodable) + 3 proprietary `Vxvs` streams.
