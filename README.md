# The Dark Knight Rises — Private Research Archive

**Game:** The Dark Knight Rises (Gameloft, 2012) — delisted mobile title
**Purpose:** Private analysis of game mechanics, data formats, and engine structure
**Status:** PRIVATE repository — do not distribute, re-host, or share contents

## Provenance & Attestation

- Source: apkaward.com listing for TDKR v1.1.6b ("Fix support for Android 15" build), downloaded 2026-10-07
- Repository owner asserts permission from the rights holders to retain and study this copy for research purposes
- All copyrights remain the property of Gameloft Entertainment / Warner Bros. / DC Comics
- No license is granted by this repository to any party for use, modification, or redistribution

## Contents

| File | Size | SHA-256 |
|------|------|---------|
| `TDKR_v1.1.6b.apk` | 7,800,817 B | `1214db998440682641f69309dfffe1589c85ccafda211eb2c1b730fe51a7e072` |
| `TDKR_v1.1.6b_APK_OBB.zip` (Release asset) | 895,253,801 B | `0510e54c128de0f52bebc6db41ea3e3a9556f666d5ca5bb09eb39880c213aa6f` |

The zip is too large for git (GitHub hard limit: 100 MB/file) and is attached as a
**Release asset** under tag `v1.1.6b`. Fetch it via the Releases tab or:

```bash
gh release download v1.1.6b --repo nawaf-al-hussain/TDKR-Game
```

## Technical Profile

| Property | Value |
|----------|-------|
| App label | The Dark Knight Rises |
| APK package | `com.gameloft.android.GAND.GloftKRLT` (GAND distribution channel) |
| Data folder in zip | `com.gameloft.android.AMAZ.GloftKRAS` (AMAZON channel build) |
| Native engine | `lib/armeabi-v7a/libKRHP.so` (16.5 MB, armeabi-v7a / 32-bit) |
| classes.dex | 326,260 B — patched 2025-10 (Android 15 compatibility shim) |
| Data payload | 164 files, ~1.9 GB uncompressed |

> **Channel mismatch note:** the APK (GAND/KRLT) and the data zip (AMAZ/KRAS) come from
> different Gameloft distribution channels. To pair them, rename the data folder to
> match the installed package, e.g.:
> `Android/obb/com.gameloft.android.GAND.GloftKRLT/` (or `Android/data/...` depending
> on how the patched loader resolves paths). Internally the engine also references
> `gloftkrhm` cache names — Gameloft used per-channel game codes for this title.

## Data Layout (inside the zip)

All game assets live under `com.gameloft.android.AMAZ.GloftKRAS/files/`:

- `data/*.gla` — Gameloft archive containers (levels, actors, effects, UI/SWF):
  - `l_gothamcity.gla` (208 MB), `l_batcave.gla`, `l_thepit.gla`, `l_stockexchange.gla`,
    `l_military.gla`, `l_policestation.gla`, `l_stadion.gla`, `l_underground.gla` — level packs
  - `actors.gla` (103 MB), `vehicles.gla`, `gameswf_*.gla` (per-resolution UI layers)
  - `sounds.gla` (437 MB) + `sounds.xml` (sound bank manifest)
  - `game_config.gla`, `strings.gla` (localization), `Controls.bin`, `oconf.bar`
- `data/options/` — per-GPU/per-device quality profiles (`GPUs.xml`, `GPU_*.xml`, `custom/*.xml`)
- `textures/*_tex.gla` — texture banks paired with each level pack
- `datakrhm_gloftkrhm.cache` — Gameloft Live cache artifact
- `welcome/welcome.html` — Gameloft Live web overlay

## Research Starting Points

1. **Asset extraction (DONE)** — see [`extraction/`](extraction/): full `.gla` container
   format cracked, 7,731 chunks + 1,186 textures + 3,110 sounds extracted, formats
   documented in [`extraction/REPORT.md`](extraction/REPORT.md)
2. **Save/progress system** — `Controls.bin`, `oconf.bar`, and the `.cache` files
3. **Level structure** — `*.bdae` scene/mesh chunks inside the level packs (next RE milestone)
4. **Difficulty & economy tuning** — inside `game_config.gla` and per-level packs
5. **Audio events** — `sounds.xml` maps triggers to the `sounds.gla` bank
6. **GPU scalability** — `options/` XMLs reveal the internal quality-tier system
