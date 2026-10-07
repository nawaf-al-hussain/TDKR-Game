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

## Findings (Ghidra 12.1.4 headless, pyghidra decompile)

1. **Fog plumbing** (decompiled/):
   - Lua `SetFogColor(r,g,b,a,?)` -> `CWeatherManager::SetFogColor(glitch::video::SColor)` via `CLevel::GetLevel()+0xa98` (key files: setfogcolor__166568)
   - `CWeatherManager::SetFogDistance(start,end)`: writes vec3 `(start*scale, 1/(end-start), ...)` to glitch GLOBAL material param slot `+0x154`, param id from `+0x172+2`; scale factor read from a manager singleton (+0x1c). Matches shipped LightMapDC GLSL uniforms (FogStartEnd/FogColor).
   - `SetFogColor(vec4)`: multiplies channels by global float DAT_0041ebf4 (normalize*255?) -> SColor global param.
   - `CWeatherManager::Load(stream)`: reads {bool enable@+4, byte@+0x28, int presetIndex@+8}; preset ptr@+0x58 = table[+0xc][index]. **Fog VALUES live in per-level template properties** (CTemplateLevelProperties) -> next: decompile `UpdateIllumination(float)` @0x40d4b4 + `CTemplateLevelProperties::Load`.
2. **ColorGrading LUT**: `CPostProcessManager::BuildColorGradingTexture()` (buildcolorgradingtexture__458e18) does NOT synthesize pixels - it BINDS one of several pre-existing textures from an array (+8) indexed by +0x38 (player/state dependent), sets NEAREST filtering, binds as global param (u16 id at +100). => LUT textures exist in DATA (level/effect texture lists). TODO: locate `ColorGrading*` textures in bdae texture tables / effects.
3. **Runtime bakes**: `IrradianceBaker::BakeNode` walks scene children, bakes meshes whose node FourCC is 'dead'/'sead'/'MeaD' via `BakeMesh`(intrusive_ptr<IMesh>) -> footprints/GI are baked from meshes at runtime (Autodesk Beast components feed light data). `CTemplateBakeGroup::Load(CMemoryStream*)` + `CComponentBeastBakeGroup::Load` parse bake setups from level streams.
4. **Engine**: glitch (Irrlicht fork). Lua 5.1 embedded (747 bound functions, full list in lua_api.txt). Level flow: Lua `RequireLoadLevel(name,idx)` -> `Application::RequireLoadLevel`.
5. **Data formats identified**: `gol.bin` = "DICT"+"GO" persistent global-object state (CLevel::LoadGlobalObjects/SaveGlobalObjects); scene graph = CZonesManager zones -> CGameObject w/ component streams (each component Load(CMemoryStream*)); BEAST light components per object (Area/Directional/Omni/Skylight/Spot/Window).
6. Decompiles banked in decompiled/ (+ key/ via /dev/shm workaround when quota hit 0).
