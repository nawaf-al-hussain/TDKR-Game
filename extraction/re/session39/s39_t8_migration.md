# S39 T8 — asset distribution migration plan (report only; nothing removed)

## Current live site (v21, gh-pages 39298a4) — 182 files, ~120 MB
| component | size | origin | depends |
|---|---|---|---|
| models/ street GLBs (12) + 51 viewer textures + city_low + district_00 + fp_island2 | 117.3 MB | CONVERTED GAMELOFT | index.html street viewer (landing page) |
| playable/batman.glb | 1.33 MB | CONVERTED GAMELOFT (rig+mesh+normals+5 anims+diffuse PNG) | playable/index.html, playable/pipeline.html test path |
| playable/patch.json | 1.06 MB | CONVERTED GAMELOFT DATA (12,512-tri collision patch + 13 engine-derived trigger volumes + spawn) | playable/index.html (collision+triggers), pipeline page fallback |
| playable/index.html + fengari-web.js + pipeline.html + tdkr_pipeline.js | ~0.7 MB | PURE CODE (ours) | everything playable |
| shell (app.js, manifest, css) | ~0.1 MB | PURE CODE | site shell/cache |

## User-supplied-only target (everything decoded at runtime from the user zip)
Already demonstrated end-to-end by the lazy pipeline (pipeline.html live: the
895 MB user zip -> batman.bdae/anims/diffuse decoded in-browser, 20.5 s lazy).

## Migration plan (dependency order, effort, breakage)
1. playable/ first (LOW effort, ~1 session): index.html currently loads
   batman.glb + patch.json directly. Swap to runtime decode via tdkr_pipeline
   (zipDirLazy/zipReadLazy + the s36 in-memory GLB assembler) with a File input
   + a cached IndexedDB copy after first decode. Breaks: nothing structural;
   first-load time +~20 s; the release screenshot gate needs a harness change
   (gate must supply the zip file instead of loading the GLB URL).
2. pipeline.html: already user-files-only (v21) — this is the reference flow.
3. street viewer models/ (HIGH effort, 3+ sessions): city GLBs came from the
   zone decoder (export_zone*.py) which has NO browser runtime yet (city
   decode not built). Options: (a) build the browser city pipeline (large);
   (b) drop the street viewer from a user-supplied-only site (landing page
   becomes playable-only). DECISION REQUIRED from the user.
4. shell: unchanged (pure code).

## Totals
- After step 1: published game-derived bytes = 117.3 MB (street) only.
- After step 3b: published game-derived bytes = 0; site = ~0.8 MB pure code.
