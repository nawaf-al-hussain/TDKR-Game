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

## Findings — session 2 (Ghidra phase, day 2)

2. **Weather/illumination preset struct decoded** (weathermanager__41eccc.c = ApplyIlluminationSettings,
   weathermanager__41d250.c = SetIllumination(idx,f,f), weathermanager__41d4b4.c = UpdateIllumination(t)):
   - `CWeatherManager` holds preset TABLE at +0xc..+0x10 (array), current preset ptr @+0x58.
   - Preset entry layout (offsets read by Apply/SetIllumination):
     +0x08 int id; +0x0c..+0x20 five color slots (each consumed as PAIR with target entry for lerp);
     +0x40,+0x44 floats (uv scale u,v) and +0x48,+0x4c floats -> bound as vec4 (u,v,1/w,1/h) => texture ATLAS transform;
     +0x50 char* texture name -> `CTextureManager::getTexture(name)` CLAMP-wrapped, bound to global param id *(u16*)(mgr+0x48);
     +0x54 float -> global param id *(u16*)(mgr+0x4e);
     +0x58 float/int -> mgr+0x74 (intensity) -> param id *(u16*)(mgr+0x4c).
   - `SetIllumination(idx,...)`: finds preset by id==idx, builds LERPED color quads (cur.rgb, tgt.rgb, a) at mgr+0x78..+0xe4 (transition support), then commits target preset to +0x58 and copies +0x5c fogStart, +0x60 fogEnd, +0x64 fogColor(SColor), +0x68..+0x70 3rd color, +0x74 intensity.
   - `ApplyIlluminationSettings` pushes to glitch global params: fogColor -> param id *(u16*)(app+0x172) [SAME id as Lua SetFogColor], fog vec3(start*scale, 1/(end-start)) -> id+2 [matches Lua SetFogDistance].
   - => **fog/illumination VALUES are pure data**: `CTemplateLevelProperties::Load` @0x2023bc defines the stream layout; values live in per-level template streams (GothamCity.lvc.bin "DICT" container).
3. **ColorGrading LUT mechanism fully decoded** (buildcolorgradingtexture__458e18.c, effects/CCFS.glsl.bin):
   - LUTs are TWO pre-existing 2D textures in an array (postprocess +8), selected at +0x38; NEAREST filtering.
   - Player-health blend: `(20 - GetHealth())*K + 1.0` lerps between tex@+0x50 (normal) and tex@+0x54 (hurt); HURT alpha clamps blend; constants DAT_004590c0/c4.
   - CCFS.glsl math: 3D LUT (32^3) stored as 2D atlas 1024x32: `u = (r/32)*0.9375 + (1/64)*(1/32) + floor(b*31.9996)/32; v = g;` CCFS2 = 16-step variant (sampler ColorGradingSampler2).
   - => porting = find the two atlas textures in data (names bound in effects/PostEffect.bdae.bin + PostProcessManager texture array built from level stream).
4. **Level config container**: `game_config/GothamCity.lvc.bin` (7.4MB) starts with magic `DICT` (same as gol.bin). Parser = `CMemoryStream::GetDictionary/SetDictionary` (string interning + object streams). `.index.bin` = small offset table.
5. **Toolchain note**: Ghidra 12 headless runs Java scripts only (no PyGhidra in bare headless); pre=LeanAnalysis.java (disables Decompiler Parameter ID etc. for disk/RAM), post=ExportTargets.java. Env rebuild: setup_ghidra.sh (~1.07GB: Ghidra trimmed -FunctionID -BSim -GhidraServer -Extensions, + JDK 25).
6. **Runtime bakes**: `IrradianceBaker::BakeNode` walks scene children, bakes meshes whose node FourCC is 'dead'/'sead'/'MeaD' via `BakeMesh`(intrusive_ptr<IMesh>) -> footprints/GI are baked from meshes at runtime (Autodesk Beast components feed light data). `CTemplateBakeGroup::Load(CMemoryStream*)` + `CComponentBeastBakeGroup::Load` parse bake setups from level streams.
7. **Engine**: glitch (Irrlicht fork). Lua 5.1 embedded (747 bound functions, full list in lua_api.txt). Level flow: Lua `RequireLoadLevel(name,idx)` -> `Application::RequireLoadLevel`.
8. **Data formats identified**: `gol.bin` = "DICT"+"GO" persistent global-object state (CLevel::LoadGlobalObjects/SaveGlobalObjects); scene graph = CZonesManager zones -> CGameObject w/ component streams (each component Load(CMemoryStream*)); BEAST light components per object (Area/Directional/Omni/Skylight/Spot/Window).
9. Decompiles banked in decompiled/ (+ key/ via /dev/shm workaround when quota hit 0).
