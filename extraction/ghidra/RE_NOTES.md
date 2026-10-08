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

## Findings — session 2, part 2 (lean re-analysis + phase-3 pass; 447 funcs exported)

10. **`CTemplateLevelProperties::Load` @0x2023bc** (templatelevelproperties__2123bc.c) is a thin shell:
    `CComponentLevelInit::Load(this)` -> float +0xa8, string +0xac, float +0xb0, float +0xb4,
    **`CComponentBaseGlobalIllum::Load(this+0xb8)`**, int +0x128.
11. **`CComponentLevelInit::Load` @0x2118f0** (levelinit__2118f0.c) = mission/container config:
    6 strings, bool, string, then N x CContainerMission (stride 0x3c: 4 strings, bool, string,
    int, 2 strings, int, 4 strings, bool), bool, string, bool, 24 floats, bool.
12. **`CComponentBaseGlobalIllum::Load` @0x212000 = THE illumination/fog preset stream** (globalillum__212000.c):
    +0x04 bool enable; +0x08 int; +0x0c,+0x10 float; +0x14..17 RGBA; +0x18,+0x1c float;
    +0x20..23 RGBA; vector{int,int}[count] (zone->GI map); +0x30/+0x31 bool;
    +0x34,+0x38,+0x3c THREE texture-name strings (ColorGrading/LUT candidates!);
    +0x40..+0x4c 4 floats (atlas transform, matches weather preset +0x40..+0x4c);
    +0x50 texture-name string (weather preset +0x50 sky/env tex); +0x54,+0x58 floats;
    +0x5c..5f RGBA; +0x60,+0x64,+0x68 floats (fogStart, fogEnd, ...; preset +0x5c/+0x60);
    +0x6c..6f RGBA.
    => weather preset entries ARE GI-component snapshots; CWeatherManager ctor harvests them.
13. **lvc index format** (key_13CZonesManager16LoadIndexZoneMapEPKc.c): `<level>.index.bin` =
    [u32 LE count][count x 13B {u32 key=lvc offset (RB-tree key), u32 a, u32 b, u8 flag(0=>auto-id)}].
    GothamCity: 23 records. Suffix ".index" appended to base name in code (6-char memcpy).
14. **DICT container**: parsed by `CMemoryStream::GetDictionary` @0x34c130 / SetDictionary @0x34c4f8
    (dictionary__34c130.c/__34c4f8.c) - string interning tables (char + wchar) + bool.
15. **CWeatherManager::Load** @0x41e8dc (weathermanager__41e8dc.c): reads bool enable@+4,
    byte@+0x28, int presetIndex@+8; preset ptr = table[+0xc][idx]. Table itself filled by
    ctor from CTemplateLevelProperties (weathermanager__41ce18.c) - to trace next.
16. Ghidra re-run recipe (proven, ~12 min total): setup_ghidra.sh; analyzeHeadless import
    -preScript LeanAnalysis.java -postScript ExportTargets.java (~10 min); second pass
    `-process lib_libKRHP.so -noanalysis -postScript ExportTargets.java` after adding
    keywords (~1.5 min). 447 functions decompiled, all banked in decompiled/.
17. **Level load chain traced** (pass 3, 590 funcs total):
    - Lua `RequireLoadLevel(name)` -> `Application::RequireLoadLevel` (just records name+mission idx)
    -> `Application::CheckLoadLevel` = SAVEGAME management (EncryptAndSave/DecryptAndLoad
    checkpoints with key sizes 0xb4/0x16/0x1d; saves gol.bin-style state; NOT the lvc path).
    - `Application::LoadLevelInitCheckPoint` (key str via DAT_003f31d8, key 0xb4) -> CLevel::Load;
    `LoadLevelInitGlobalData` (key 0x16) -> CLevel::LoadGlobalObjects etc.
    - **savegame files are ENCRYPTED** via `Application::DecryptAndLoad(path,int,stream)` /
    `EncryptAndSave(path,int,stream)`.
    - lvc (.lvc suffix strings @0xb44cd0/0xb44fb4, `shop.lvc` @0xb365fc, `data/game_config.gla`
    @0xb3f9c8) loading happens deeper (GS_Loading game state / CLevel ctor) - NOT yet found.
18. **DICT parser location**: "DICT" fourcc occurs 4x in .rodata only; code compares via
    movw/movt immediates (e.g. movw Rd,#0x4944 + movt Rd,#0x5443). Next session: scan .text
    for that pair -> owning function = the DICT/lvc reader that feeds CTemplateLevelProperties.
19. Ghidra image-base note: symbol vaddrs (readelf) are offset by +0x10000 vs Ghidra listing
    (e.g. LoadLevelInitCheckPoint 0x3e3108 -> Ghidra 0x3f3108). Map addresses accordingly.

## Findings — session 3 (DICT reader located; lvc parsed; night fog + LUT extracted)

20. **MOVW/MOVT scan came up empty** (scripts/scan_movw_movt.py in extraction/re/):
    15,934 ARM + 2,542 Thumb movw/movt immediates in libKRHP.so, ZERO hit 0x4944/0x5443.
    All 4 "DICT" byte-strings in the .so are libcurl URL-scheme strings. The magic is
    compared as **0x44494354** (FourCC spelled 'D'<<24|'I'<<16|'C'<<8|'T') — the halves
    are 0x4449/0x4354, not 0x4944/0x5443.
21. **The DICT reader = CMemoryStream::BeginRead** (Ghidra 0x3ae97c, banked
    decompiled/). Exact stream format (ALL primitives BIG-ENDIAN — ReadInt @0x349914
    composes b0<<24|b1<<16|b2<<8|b3; ReadFloat likewise BE):
    `[u32 'DICT'=0x44494354][u32 tblOff][u8 flag]`, optional wide table if flag,
    then at tblOff: `[u32 countC][count x {u32 len, bytes}]` char-string table,
    then **read pos = 9** — the object stream starts right after the header.
22. **ReadString** (@0x34a0d4): if stream+0x34 == 0 -> INLINE (u32 len + bytes);
    else interned: +0x35==0 -> charTable[idx] (+0x1c vec), else wcharTable[idx].
    +0x34 is set only by SetDictionary (HandleZoneLoadRequests injects shared
    tables into zone sub-streams). Top-level lvc stream: ctor bool=1 -> interned.
23. **CMemoryStream ctor bool = "uses dictionary"** (LoadLevelProperties passes 1).
24. **CLevel::LoadLevelProperties(path)** @Ghidra 0x499954 (banked): opens the lvc,
    BeginRead, skips ReadShort+ReadShort+ReadInt, reads typeId==**0x2657** ->
    CTemplateLevelProperties::Load. In GothamCity.lvc.bin: header 9B, then
    'NV'(0x4E56), 3, objCount=14917, typeId 0x2657 @0x11, template from 0x15.
25. **CTemplateLevelProperties::Load** (@0x2123bc): CComponentLevelInit::Load
    (6 strings, bool, string, int N, N x {4 str, bool, str, int, 2 str, int,
    4 str, bool}, bool, string, bool, **25 floats** (+0x3c..+0x9c), bool) ->
    float, string, float, float -> **CComponentBaseGlobalIllum::Load** -> int.
    (note 11's "24 floats" was off by one — that desync corrupted earlier parses.)
    GothamCity values: LevelInit strings = Lua bootstrap (#0), botond helpers,
    'gothamcity.lv', 'STR_FPS_LEVEL_GOTHAM', 'l_gothamcity.gla',
    'menu_bg_gotham.swf', bool1=1, 'batman.bdae'; 20 missions; str7=
    '020_gothamcity.xml'; 25 floats [80,79,500,95,125,140,200,150,180,0.2,5,10,
    20,40,60,90,120,160,200,300,2,30,5,25,0.3]; bool4=1; f_a8=25;
    s_ac='gothamcity_minimap.swf'; f_b0=1.07; f_b4=0.4; final int=31004 (0x791C
    = first .index.bin key -> cross-validates the parse).
26. **CComponentBaseGlobalIllum::Load stream order** (the night preset, id=0):
    enable(0), id(0), f0c=0, f10=140, RGBA(64,102,119,160), f18=75, f1c=200,
    RGBA(0,0,0,255), 0 zone-pairs, bool,bool(0,0), 3 EMPTY LUT strings (-1),
    atlas floats(-1210,-220,1520,-1130), fogTex='gc_verticalfog.tga',
    f54=0.65, f58=0.013, RGBA(50,60,60,255), floats(0,0,1), RGBA(230,230,255,255).
27. **Field semantics via CWeatherManager** (SetIllumination @0x41d250 +
    ApplyIlluminationSettings @0x41eccc): preset entries ARE GI components
    (table = TLP->GI list, searched by GI+0x08==id). Copies: GI+0x0c->mgr+0x5c
    fogStart, +0x10->+0x60 fogEnd, +0x14->+0x64 fogColor(SColor), +0x18/+0x1c/
    +0x20->+0x68..0x70, +0x58->+0x74 intensity(+0xd8 lerp slot).
    ApplyIlluminationSettings: getTexture(GI+0x50) CLAMP-wrapped -> param
    *(u16*)(mgr+0x48); vec4(+0x40,+0x44,1/+0x48,1/+0x4c) -> param mgr+0x4a
    (**FogMap** = world-space projection of the fog texture!); +0x74 -> mgr+0x4c;
    +0x54 -> mgr+0x4e; SColor mgr+0x64 -> param app+0x172 (**FogColor**);
    vec3(start*s, 1/((end-start)*s)) -> param app+0x172+2 (**FogStartEnd**);
    scale s = *(float*)(configSingleton+0x1c) — singleton ptr @Ghidra 0xc17f18,
    runtime-initialized (BSS), value not statically recoverable; s=1 assumed.
28. **Shipped fog math** (effects/LightmapVCBlendDC-v/-f.glsl + glsl.config.bin:
    `#define VERTICAL_FOG_COLOR vec4(0.93,0.76,0.47,0.35)`,
    `#define VERTICAL_FOG_HEIGHT 18.0`, `#define FOG_DECAY 0.5`):
    VS: FogFactor=(-viewZ-FogStartEnd.x)*FogStartEnd.y;
        fY = worldZ*VerticalFogHeight + FogFactor*FOG_DECAY;
        FogUV = ((World*Position).xy - FogMap.xy) * FogMap.zw;
    FS: FogMapColor=vec4(tex2D(FogTexture,FogUV).rgb, VerticalFogAlpha);
        fogCol2=mix(FogMapColor, FogColor, clamp(fY,0,1));
        Color=mix(Color, fogCol2, clamp(FogFactor,0,1)*fogCol2.a);
    World is Z-UP (height = World[.z row]).
29. **gc_verticalfog.tga found + decoded**: l_gothamcity_tex/GC_VerticalFOG.tga.bin
    (also _IND, _Island2). Container: 52B wrapper {52,1024,1024,10 mips,fcc=0x136,
    699064,4}, mips ASCENDING (small first), mip0 (1024x1024) LAST,
    **ETC2 RGB** (not PVRTC — smoothness probe 0.50 vs 6+ for everything else).
    Image = top-down atlas of Gotham district glow (street lights) over deep navy
    haze — THE night-haze look. Decoded -> gh-pages models/tex/GC_VerticalFOG.png
    (probe_pvr_formats.py; smoothness-scored brute force).
30. **LUT (ColorGrading)**: GI LUT strings are EMPTY for GothamCity. The grade
    comes from the Lua bootstrap (string #0):
    PostProcessingEffectAdd("ColorCorrection", {extra_texture="000_default.tga",
    time_to_fade_in=0}) — night LUT = 000_default.tga; lightning flashes =
    023_lighting.tga (BLightning()); intro = 022_GothamCity.tga (commented out).
    LUT textures not in l_gothamcity_tex (294 files) — likely inside
    effects/DefaultEffects.bdae or the ZIP_SPLIT set; next session.
31. **Viewer ported (v5, gh-pages 75277eb)**: exact TEXTURE_FOG path, extracted
    values, axis-mapped (game(x,y,z)->view(x,z,-y); FogUV u=(x+1210)/1520,
    v=(z-220)/1130), manifest.json v5 carries the fog block. Live check OK.

## Findings — session 4 (fog scale pinned; LUT decoded + graded; fp brightness fixed)

32. **Toolchain note**: host objdump has no ARM support; capstone per-function
    decoding (dynsym FUNC entries, mode = LSB of st_value) is the reliable
    disassembly route — linear .text disasm dies on literal pools; section
    headers of libKRHP.so are partly FORGED (symbols below stated .text start;
    program headers + 1:1 vaddr/fileoff mapping are authoritative).
33. **config+0x1c singleton identified = DeviceOptions::Singleton**:
    - access idiom (SetFogDistance @0x40ebf8, ApplyIlluminationSettings
      @0x40eccc, BeginRenderReflections): `ldr rX,[pc,#imm]` (offset) +
      `ldr rX,[pc,rX]` -> GOT slot **0xc07f18** (R_ARM_RELATIVE addend
      0xc22ce4) -> `ldr rX,[rX]` = **DeviceOptions::Singleton** (BSS ptr,
      dynsym: `_ZN13DeviceOptions9SingletonE` @0xc22ce4) -> `vldr s15,[rX,#0x1c]`.
    - `DeviceOptions::C2` ctor @0x4a91ac: +0x1c default = **1.0f**
      (`mov r3,#0x3f800000; str r3,[r0,#0x1c]` @0x4a91f0); +0x14/+0x18/+0x20
      also 1.0; +0x10=9 (LOD end); +0x60=5.0; +0x64=9.5; +0x94=43.
    - `DeviceOptions::LoadOptions(std::string&)` @0x4a9768 parses XML
      attributes: strcmp keys -> atof -> fields. Key for +0x1c =
      **"Fog distance factor"** (write @0x4a9bec). Full schema extracted:
      LOD start/end level, LOD distance factor, Coronas LOD factor,
      **Fog distance factor**, Camera Far factor, Update factor,
      DynamicLights/HardwareSkinning/FresnelOnPixel/Undef_* shader bools,
      ParticleDensity, HighQualityParticles, Texture MIN filter, Anisotropy,
      Animation streaming cache size, Streaming Buffer Size, Max texture size,
      Particles Buffers, TextureMemoryPoolSize, Mipmaps to skip, Enhanced 3D
      sounds, Reverb, RmOnLowSFX/RmOnMedSFX, Enable post processing ...
    - profile chain: LoadProfile @0x4ab878 -> LoadOptions(CPU_S/M*.xml,
      MEM_{256,512,768}.xml) + LoadGpuProfile(gpuName) -> GPU_%d.xml;
      per-device custom/*.xml. GPU profile XMLs ship in
      files/data/options/ (OBB). **GPU_5.xml (top tier: iPad3/Adreno 320/
      SGX543MP4 class) = "Fog distance factor" 1.1; all others 1.0**
      (ctor default 1.0). => runtime scale s = 1.1 for the max-quality look:
      fog (0,140) -> (0,154); FogStartEnd=(0, 1/154). Camera Far factor 1.1.
    - DeviceOptions globals: Singleton 0xc22ce4 (GOT 0xc07f18), m_gpuName
      std::string 0xc22ce8 (default "PowerVR SGX 544MP2" @0xb46c8c), three
      0.5f defaults 0xc22cf4.
34. **ColorGrading LUT textures FOUND + DECODED**: commons_tex.gla entries
    `000_default.tga`, `022_GothamCity.tga`, `022_GothamCity_Industrial.tga`,
    `023_lighting.tga`, `024_default.tga` (+ per-device clones
    Galaxy_Nexus_*/GT-I9000_*/...), each exactly 16436 B. Container = **PVR v1
    header** {hdrSize=52, H=16, W=512, mips=0, fmt=19, size=16384, bpp=16,
    masks=0, magic='PVR!'} -> **512x16 RGB565 atlas** (16^3 LUT, half-res).
    fmt=19=RGB565; verticalfog's fmt 0x136=ETC2-family (mip-chained).
    LUT appearance: 32 vertical hue slices x 16 green rows; 023_lighting mean
    (220,229,234) = near-white lightning flash grade; 000_default mean
    (129,136,136) = subtle cool night grade. Decoded ->
    gh-pages models/tex/LUT_000_default.png + LUT_023_lighting.png.
35. **Shipped grading shader = CCFS.glsl** (effects.gla, 669 B, verbatim):
        cells=32; cellsize=1/32; r=color.r*cellsize; v=color.g;
        b=floor(color.b*31.9999)*cellsize;
        u=r*0.9375 + 0.03125*cellsize + b;
        Complete = texture2D(ColorGradingSampler, vec2(u,v));
    CCFS2.glsl = 16-step variant (0.0625 cells, r_scale 0.94, r_off 0.001875).
    The 512x16 atlas works directly with CCFS (u,v normalized; NEAREST
    filtering per CPostProcessManager). Game binds ColorGradingSampler from
    PostProcessManager texture array (+8); Lua bootstrap adds
    PostProcessingEffectAdd("ColorCorrection", {extra_texture="000_default.tga"}).
    Ported to viewer as EffectComposer: RenderPass -> ShaderPass(lutShader)
    with UnsignedByteType RTT (engine's ColorGradingRTT parity), NEAREST.
    (ShaderPass CLONES its shader uniforms — mutate lutPass.uniforms.)
36. **Footprint textures identified as offline COMPLETE bakes**: shipped
    per-footprint textures (GC_Footprint_AWT.tga 2048², GC_Footprint_IC.tga,
    GC_Footprint_LB_Cinema.tga, ...) contain the final night lighting (lit
    windows, glowing WAYNE sign; mean ~0.28 vs island bake pages ~0.11). The
    gt diffuse names 'X_LongDist[CompleteMap|DiffuseMap]' are runtime Beast
    bake targets; the shipped no-suffix textures ARE the bake content.
    => fp tier renders them at 1x ('d'); the old technique-driven 2x made
    them daylight-bright (the v5 "footprint-atlas brightness" bug).
    Footprints whose bake target has no shipped equivalent (diffuse =
    'GC_LongDist') bind by UV-fit >= 0.9 against the 8 GC_LongDist_Island*
    pages at 2x (hero parity; strict page family — BakeGroup_* atlases
    outcompete the true page on edge density and must be excluded).
    Reflections-fx (LightMapSampler) footprints -> honest dark fallback.
    Exporter: export_city.py fp ladder (gt / fp-family / fp-page-fit / dark).
37. **Viewer v6 (gh-pages f4d9b42)**: LUT grade + fog 154 + fp rebinding;
    A/B verified in headless Chrome (grade on = cooler night cast; street
    level shows dark buildings with lit windows, no daylight-bright boxes).
    Note: headless SwiftShader fps readings are meaningless (was 0-2 fps in
    v5 too under full load); check on real hardware.

## Findings — session 5 (zone bake-group streams; ground lightmap truth; lightning + hurt wired)

38. **lvc layout fully mapped**: `.index.bin` = N x 13B LE records
    {u32 zoneId, u32 streamStart, u32 streamEnd|size, u8 flag(0=auto-id)};
    zoneId values also appear inline in a 0x2667 record near the template.
    Each zone = CTemplateZone record (typeId 0x2667, see 27/25) followed by a
    contiguous OBJECT STREAM. Stream = [u32 sizeOrEnd][records]. Records =
    [u32 BE typeId][payload] dispatched by CLevel::LoadNextObject @0x489ecc:
    0x2657 LevelProperties, 0x2653 CTemplateOccluder, 0x2667 CTemplateZone
    {bool,string(luascript),int,bool,int zoneId,9 floats pos/rot/scale,3 bools},
    0x265f CTemplateMetaZone, 0x140869f CTemplateBakeGroup (template form —
    ZERO instances in shipped Gotham data), 0x1011/0x2669/0x2661/0x2662/0x2664
    (waypoint/portal/worldbox variants; 0x2664 = single int), 0x1404050/51,
    0xd0bbb8 CWorldBox. Object/component plumbing:
    CGameObjectManager::CreateObject @0x36774c walks per-class component
    template lists (map<int,vector<TObjectData>>; TObjectData = {u8 flag, ptr,
    u32 hash}); hash 0x152b87 = MESH component (inline: ReadString bdae +
    4 bools), 0x14ca79 = CComponentBase (pos/rot/scale), 0x2ad2a046 = group
    builtin, default -> CComponentFactory::CreateComponent(hash,obj,data)
    @0x223e3c -> virtual Load(stream); unknown -> GenerateComponentTemplate
    @0x368ac0. Component hashes seen special-cased: 0x17ac851f, 0x2ad2a046,
    0x14ca79, 0x152b87.
39. **CComponentBeastBakeGroup stream payload located in zone object streams**
    (the template typeId 0x140869f is never used in shipped data; the
    component data IS — as part of object records). Frame (byte-packed,
    BIG-ENDIAN floats AND strings, verified across GothamCity + Island2):
        [u32 strIdx 'BakeGroup_<isle>_<G>.tga']   bake page (runtime target)
        [f32 u0][f32 v0][f32 u1][f32 v1]          bake region in page (Beast
                                                  top-down projection rect) —
                                                  whole-page bakes carry
                                                  density floats (2,2,...)
        [u32 strIdx 'BakeGroup_<isle>_<G>0.tga']  SHIPPED pre-baked twin
                                                  ('-0' suffix = on disk)
        [u32 1024][u32 512][s32 -1]               atlas sizes, empty string
        [u32 hash 0x00018785 | 0x0001869f]
        [u8 1][u32 objectId][12 x f32 pos/rot/scale + extras]
        [u32 strIdx '<gc_footprint_xx>.bdae'][4 x u8]   mesh component
        [u32 strIdx '<...>_collision.bdae'][4 x u8]     collision component
    Extraction: extraction/re/extract_bake_regions.py -> bake_regions.json
    (530 records, 119 distinct mesh bindings). Authoritative page assignments
    recovered, e.g. gc_footprint_cn/ga/vb/vc -> BakeGroup_Island1_A0,
    gc_footprint_gc -> BakeGroup_Island1_B0, gc_footprint_id/ie ->
    Island2_Landmarks0, bridges/monorail/railway -> Island2_Roads0. Files
    whose ONLY texture is the runtime target 'GC_LongDist' with no
    bake-group record (cb/cc/cd/cg/gf/va/vpow) keep the v6 UV-fit fallback.
    Bake pages measure mean 0.11-0.20 = authored for LightMapDC *2.0.
    NOTE: footprint DISTRICT meshes carry absolute page UVs; the rects are
    the per-object world-projection regions Beast baked into the page.
40. **Ground-plane DIM_TEX fudge removed (root cause + shader truth)**:
    GC_City_Plane (ground) = StandardDiffuseDC: `Color = Diffuse * vColor`
    with NO vertex-color stream (20B stride = pos+nrm+uv) -> vColor = white
    -> native 1.0. LightMapDC path: `Color = Diffuse * (LightMap*2.0)`;
    materials binding the LightMapSampler.tga placeholder bind a FLAT
    32x32 0.4706-gray texture (decoded commons_tex/LightMapSampler.png) ->
    net 0.941. LPLD variant: `Color = Diffuse` at 1x. Water (NormalSpec-
    Overbright/Water-f.glsl) = NRM1*NRM2*vColor (animated dual normal-map).
    The v4-era DIM_TEX {asphalt/sand 0.42, water 0.55} pre-dated the exact
    fog+LUT chain and rendered the ground 2.4x too dark -> removed.
41. **Lightning + health blend wired (all constants extracted)**:
    - BLightning (GothamCity lvc Lua string #0) = THREE one-shot
      ColorCorrection pulses of 023_lighting.tga over the 000_default base:
      (fade_in,run,fade_out)ms = (30,30,30) / (60,30,150) / (30,30,90),
      smart light on/off = 75/45, 135/135, 105/75 ms; auto re-strike
      cadence Random(5000,15000) ms (bootstrap comment).
      CPostProcessEffect_ColorCorrection::Update @0x45ac88 = fade-in -> run
      -> fade-out state machine (0/2/1), removal restores mgr +0x5c/+0x60 =
      -1.0. 023_lighting LUT mean (220,229,234): flash lifts a 0.06 frame to
      0.43 (verified headless).
    - Health blend (BuildColorGradingTexture @0x458e18):
      t = (20-health)*(1/60)+1 [DAT_004590c0=0.0166667]; t=min(t,1-hurtAlpha);
      t=clamp(t,0,1) [DAT_004590c4=0]; render LUT(+0x50) blended toward
      LUT(+0x54) by (1-t). Hurt LUT string absent for GothamCity ->
      getHackTex fallback = '000_default.tga' (string @0xb44028) -> the
      shipped night city hurt grade is a visual no-op; mechanism wired with
      keys [ / ] (uHurt = 1-t).
42. **Viewer v7 (site)**: dual-LUT CCFS pass (base 000_default + flash
    023_lighting + hurt slot), BLightning sequencer (L key manual, Shift+L
    auto toggle, moon light = smartLight stand-in), exact bake-group page
    bindings in fp tier, native-brightness ground/water. Manifest v7.
    Headless check: no page errors; flash/hurt/lutOn/off pixel A/B verified
    via readPixels (screenshots are stale frames under SwiftShader 0fps).

## Findings — session 6 (FP-page origin traced; per-building rect-relative UVs; viewer v8)

43. **Symbol-address correction**: libKRHP_symbols.txt carries +0x10000 shifts
    for many functions vs the banked lib_libKRHP.so ELF symtab (sibling
    GAND/AMAZ build). extraction/re/elf_syms.py + disasm_reader_seq.py read
    the true ELF symtab (readelf -sW) — all session-6 addresses below are
    TRUE addresses. (Ghidra decompile filenames keep the shifted addresses.)
44. **CComponentBeastObjectComponent::Load @0x2e1e8c** reads:
        vec4 so1 -> +0x04..0x10; string -> +0x14; vec4 so2 -> +0x18..0x24
    (stream: [f32 x4][strIdx][f32 x4], BE). CBeastObjectComponent::Load
    @0x2a1ea4 then: getTexture(pageStr) + getTexture('LightMapSampler.tga'),
    copies so1 into Coord1_scaleoffset (+0x1c..0x28), fills ShaderParams with
    getParameterID('LightMapAtlas') etc. — so2 is read but DISCARDED (it
    belongs to the following {str 'ATLAS_low0', u32 W, u32 H, s32 -1}
    low/-0-path component). String pool @0xb3b26c 'LightMap', 0xb3b310
    'LightMapSampler.tga', 0xb3b324 'LightMapAtlas'.
45. **LightMapDC-v.glsl (effects.gla) holds the exact UV chain**:
        vCoord1 = (Coord1*Coord1_scaleoffset.xy + Coord1_scaleoffset.zw)
                  * LightMapAtlas.xy + LightMapAtlas.zw
    => pageUV = uv*so1.xy + so1.zw. so1 = (scaleU, scaleV, offU, offV) with
    scaleU==scaleV ALWAYS (square Beast tiles) — the v1 "u0==v0 anomaly" was
    the scale pair misread as rect coords, and the v1 'rect' was actually the
    DISCARDED so2. Meshes carry NO bake UVs (Coord1 == unit diffuse UV, extra
    stride-24/28 dwords duplicate Coord0) — the tile transform is entirely
    object-level, hence 'rect-relative UV refinement' is required when
    rendering bake pages with unit-UV meshes.
46. **Record typeIds**: CLevel::LoadNextObject @0x499ecc: 0x2666 WayPoint,
    0x265e light, 0x1011 IrradianceVolume, 0xbba MetaZone, 0x2653 Occluder,
    0x2657 LevelProperties, 99999 (0x1869F) = CTemplateBakeGroup::Load
    (@0x48d870: char,int,9f,3bools,(string,float)x2), 82000 refl-batch,
    0xdbbb8 WorldBox, default -> CGameObjectManager::CreateObject @0x35774c
    (component dispatch from the per-class TObjectData template list; stream
    carries ONLY payloads in template order — hashes 0x152b87 mesh
    (ReadString+4 bools), 0x14ca79 CComponentBase, 0x2ad2a046 group builtin).
47. **extract_bake_regions_v2.py -> bake_regions_v2.json**: 89 frames
    (GothamCity 67 + Island2 22), mesh-resolved 86; 54 footprint + 35
    prop/bridge bindings with EXACT (page1, so1). Corrects v7 UV-fit errors:
    gc_footprint_gf -> BakeGroup_Island1_A0 @(0.0002,0.2502) (v7 had
    Island2_FP2!), gc_footprint_vpow -> Island1_Landmarks0 @(0.4995,0.5002)
    (v7 had Island1_FP3). ~20 footprints that rendered dark (no shipped
    per-footprint bake) now carry their true Beast tiles. CB/CC/CD/CG/VA
    have NO bake component anywhere (CC x1059 / CD x394 instances =
    mass-repeated far-only buildings) — their only lighting is the
    GC_LongDist_Island* streaming pages (kept v7 UV-fit page binding).
48. **Textures**: the 8 BakeGroup island pages are 2048^2 ETC1 mip-chained
    (PVRv2 hdr: h,w,mips=11,flags=0x136); GC_LongDist_*_FP* + Roads pages +
    26 more chunks are ZIP_SPLIT = [PK zip: 'SPLIT' marker, rgb.pvr 2048^2
    ETC1, alpha.pvr 1024^2 ETC1] — batch_decode_tex.py now splits+decodes
    (294/294 + 266/266). All 8 page1s + tiles verified non-overlapping
    power-of-two grid per page.
49. **Viewer v8 (manifest v8)**: exporter v8 — fp tier binds bake_regions_v2
    (page1 + so1); per-mesh rect-relative UV refinement applied at export
    (uv' = uv*so.xy+so.zw baked into GLB TEXCOORD_0; verified: VC uv
    u[0.0002..0.2493] v[0.0001..0.1894] == tile(0.2495 @ 0.0002,0.0001)
    x unit-uv-max 0.7587). Reflection variants untouched. 42/55 fp _LongDist
    files bakegroup-bound (was 5), dark 40 -> 7, far-only five keep
    UV-fit pages. Headless: no page errors, all 7 shipped pages fetch 200.
50. **Session 7 — v8 "wrong textures" root-caused (three independent defects)**:
    a) *Wrong UV channel*: the fp _LongDist meshes store the BEAST bake UV
       (Coord1) in the FIRST vertex dword (+12, u16 x2 /65535) — NOT in the
       +16 stream the exporter used. Proof: GC_Footprint_IC_LongDist is a
       16-byte-stride mesh (pos + ONE dword at +12, no normal); its +12
       stream under so1 rasterizes EXACTLY onto the machinery content of its
       assigned BakeGroup_Island1_A0 tile (visual overlay + 2.3x edge-score
       over uniform-fill control), while +16 reads the NEXT VERTEX'S POSITION
       bytes (out-of-vertex-bounds garbage). For 24B meshes (CA): +12 = uv,
       +16 = second uv (Coord0/runtime complete-map), +20 = packed normal
       (byte3 == 0 -> z~=0 up-axis normals for tower walls). v8 therefore
       sampled the bake page with the complete-map layout -> smeared mosaics.
    b) *Projection-bake landmarks*: VPOW-class meshes (st=16, +12 = normal)
       have NO stored bake UV — the runtime derives Coord1 as a TOP-DOWN
       PLANAR PROJECTION of position: uv1 = (pos.x-mn.x)/ext.x,
       (pos.y-mn.y)/ext.y (game Z-up -> x,y = horizontal plane). Confirmed
       visually: VPOW's normalized (x,y) wireframe locks onto the circular
       machinery of its Landmarks0 tile.
    c) *Mesh-binding offset pinned*: CComponentBeastObjectComponent::Load
       @0x2e1e8c disassembly (capstone ARM): 4x ReadF32 (so1), ReadString
       (page1), 4x ReadF32 (so2), tail-call ReadString (page2) — no mesh
       index in this component. The mesh bdae string index lives at frame
       base +84 (0x54) in the FOLLOWING component — derived empirically
       (59/67 + 19/22 frames bind self-consistent infrastructure meshes at
       dq=84: monorail->monorail, railway->railway, bridges->bridges). The
       v1/v2 "first plausible bdae idx in [36,220)" scan was a false-positive
       magnet (hc_prop_billboardwall_01's small string index collided with
       W/H/hash u32s). bake_regions_v3.json = v2 records with mesh read at
       fixed +84 (53 footprint bindings, mostly identical to v2 — v2 got 84
       first for most frames, so v2 bindings were mostly right; the CHANNEL
       bug was the real killer).
51. **Exporter v9**: choose_bake_channel() — candidates {uvm (+12 stream),
    top-down position projection}, edge-scored against the assigned tile;
    higher wins, weak 0.6 floor only rejects degenerate candidates (dense
    mosaic tiles make absolute thresholds meaningless — even correct
    sampling barely beats the tile's mean edge density). Winner transformed
    by so1 into page space and baked into TEXCOORD_0; material = page|2x.
    bdae_extract: uvm stream added, st=16 uv=None (was out-of-bounds
    garbage), GlbBuilder/apply_scaleoffset/uv_fit None-guarded.
52. Engine frame cross-check: so1 == [scaleU, scaleV, offU, offV] (square
    pow2 tiles), so2 = low-page (ATLAS_low0) tile for the trailing low-path
    component; page strings end .tga in the lvc string table (u32-indexed,
    big-endian lvc container).
