# Gotham City — BDAE Geometry Viewer

Live at: **https://nawaf-al-hussain.github.io/TDKR-Game/**

Real-time browser view of Gotham City, reverse-engineered from the mobile game
*The Dark Knight Rises* (Gameloft, 2012). Every triangle here comes from the
game's own `.bdae` mesh files (BRES / compiled COLLADA), parsed by the toolkit in
the [`main` branch → `extraction/`](https://github.com/nawaf-al-hussain/TDKR-Game/tree/main/extraction).

## What you're looking at

| Layer | Content | Triangles |
|---|---|---|
| Skyline | islands, roads, bridges, monorail — the game's own LongDist night-lightmap bake | ~120k |
| Footprints | island footprint detail layer | ~51k |
| District props | ~70 buildings/props/interiors | ~14k |
| Low-detail LOD | near-LOD island copies, per-mesh FP/roads bakes | ~16k |

346,960 verts · 202,137 tris total, streaming as 25 GLB files (~13.3 MB) with 80
external JPEG textures. Textures are the game's baked night lightmaps.

### How textures are bound (v2)

Each `.bdae` mesh carries its own material name in its footer; each file's
string pool lists the `.tga` textures its materials reference. The exporter
resolves textures **per mesh**:

1. uv-verified overrides (island/road/bridge bakes)
2. footer material name ↔ pool candidate match
3. unique diffuse candidate in the file's pool
4. per-mesh UV-fit scoring among pool candidates
5. island bake-atlas fallback for footprint/LongDist chunks, else dark

The 87 ZIP_SPLIT textures (zip-wrapped `rgb.pvr` + `alpha.pvr`) — including the
`GC_LongDist_Island*_FP1/2/3` footprint atlases — are decoded by
[`tex_split_convert.py`](https://github.com/nawaf-al-hussain/TDKR-Game/blob/main/extraction/scripts/tex_split_convert.py).

## Pipeline

```
OBB → .gla containers → *.bdae chunks → parse_meshes() → geometry-only GLBs + JPEG atlases
```

- Format spec: [`extraction/REPORT.md`](https://github.com/nawaf-al-hussain/TDKR-Game/blob/main/extraction/REPORT.md) §3
- Exporter: [`extraction/scripts/export_city.py`](https://github.com/nawaf-al-hussain/TDKR-Game/blob/main/extraction/scripts/export_city.py)
- Viewer: static `index.html` + `app.js` (Three.js r170 via CDN, no build step)

## Notice

Research/education only. Game content © Gameloft · Warner Bros. · DC.
Not affiliated with or endorsed by any of them.
