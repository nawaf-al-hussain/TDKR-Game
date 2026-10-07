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
| District props | 78 buildings/props/interiors | ~14k |
| Low-detail LOD | ultra-far fallbacks | ~18k |

348,136 verts · 202,857 tris total, streaming as 34 GLB files (~13.4 MB) with 35
external JPEG textures (~5 MB). Textures are the game's baked night lightmaps.

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
