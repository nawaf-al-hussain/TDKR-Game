# TDKR Native-Library Reverse Engineering (Ghidra phase)

Binary: `libKRHP.so` — extracted from `TDKR_v1.1.6b.apk` (committed at repo root).
`unzip TDKR_v1.1.6b.apk lib/armeabi-v7a/libKRHP.so`

- ELF 32-bit LSB ARM EABI5, **not stripped, with DWARF debug_info** -> full symbols + types
- 41,515 function symbols (see `libKRHP_symbols.txt`, demangled in `libKRHP_symbols_demangled.txt`)
- Engine: **glitch** — a GPU-tuned Irrlicht fork (namespaces glitch::scene/video/core)
- Embedded **Lua 5.1** VM: gameplay + engine control exposed to scripts
- Ghidra 12.1.4 headless analysis (ARM:LE:32:v7), post-script `ExportTargets.py`

## Targets and what we already know from symbols

| RE goal | Symbol evidence |
|---|---|
| Exact fog constants | `CWeatherManager::SetFogColor(glitch::core::vector4d<float> const&)`, `SetFogDistance(float,float)`, Lua: `SetFogColor(lua_State*)`, `SetFogDistance`, `ResetFog` |
| ColorGrading LUT (not shipped on disk) | `CPostProcessManager::BuildColorGradingTexture()` + strings `ColorGradingRTT`, `ColorGradingSampler` -> LUT is BUILT at runtime into a render target; decompile to port |
| 55 dark meshes = runtime-only bakes | `IrradianceBaker::BakeMesh/BakeNode/BakeBuffer`, `CTemplateBakeGroup::Load(CMemoryStream*)`, `CComponentBeastBakeGroup::Load` (Autodesk Beast integration) |
| Lightmap atlas per zone | `CZone::ChangeLightMap(char const*,char const*)`, `CZonesManager::ChangeLightMap`, Lua `ChangeLightMap` |
| Shader param plumbing | glitch::video::IShaderManager, CGenericBaker, strings: FogColor/FogDensity/FogMode/FogStartEnd (matches shipped GLSL uniforms) |

## Config data found outside the .so (from OBB)

- `game_config/GothamCity.lvc.bin` (7.4 MB) + `.index.bin` — packed float-heavy level config
  (likely light volumes / level view config). Pairs of `0.7` float patterns etc. Needs .so code
  to interpret (LVC loader function to locate via strings "lvc").
- `raw/effects/*.glsl.bin` — full GLSL corpus, already ported (v4 viewer).

## Method

1. Ghidra headless import + analyze (background, ~30-60 min for 16.5 MB ARM w/ DWARF).
2. Post-script `ExportTargets.py` decompiles every function matching target keywords to
   `/home/z/ghidra_out/*.c` + index.
3. Port findings to viewer (fog constants, offline LUT bake, footprint bake reconstruction).

## Status log

- [x] Locate binary (was in repo APK all along; Amazon mirror byte-identical 7,800,817 B)
- [x] Symbol dump committed
- [x] Ghidra headless analysis started
- [ ] Decompiled exports -> findings -> viewer integration
