# RE session 10 — authoritative material chains + street-tier structural binding

## 1. Zone materials DB CRACKED (source.dae setparam chain)

Session 9's note "source.dae gives materials+effects but no per-instance
texture values" was WRONG. The COLLADA `instance_effect` carries per-instance
`<setparam>` overrides with the REAL bindings:

    <material id="tiles_...">
      <instance_effect url="#LightMapDC-fx_...">
        <setparam ref="texture23"><surface><init_from>image13</init_from></surface></setparam>
        <setparam ref="LightMap"><sampler2D><source>texture23</source></sampler2D></setparam>
        <setparam ref="texture24"><surface><init_from>image17</init_from></surface></setparam>
        <setparam ref="DiffuseMap"><sampler2D><source>texture24</source></sampler2D></setparam>
        <setparam ref="LightMapAtlas"><float4>1 1 0 0</float4></setparam>

Chain: sampler symbol -> textureN -> surface -> imageN -> <image><init_from>FILE.tga.
Parsed island1: 305/307 materials resolved; island2: 195/196.
(script: scripts/parse_zone_collada2.py -> work/zone/zone_materials_full.json)

Effect census island1: LightMapDC 227, NormalSpecOverbright 38, AlphaMasking 17,
StandardDiffuseDC 5, SimpleAdditive 8, LightmapVCBlendDC 4, ...
LightMap distribution: BakeGroup_Island1_A0 x109, B0 x91, Landmarks0 x54,
Roads0 x25, LightMapSampler x5.
=> THE WHOLE CITY RUNS: Color = DiffuseMap(albedo) * LightMap(island bake page) * 2.

## 2. Engine-parity viewer (v11)

export_city.py v11 + app.js: material contract '<dif>|<lm>|<mode>' with
TEXCOORD_1 = Coord1*so1 (bake-group record), viewer multiplies
tex(map,vUv) * tex(lmap,vUv1) * uMult. bake_coord1() replaces
choose_bake_channel(): the record binds, the score only CHOOSES the Coord1
source (stored +12 stream vs planar projection), floor lowered 0.6 -> 0.3.

## 3. fp LongDiffuseMaps are RUNTIME BAKES

gt diffuses for GC_Footprint_*_LongDist files = 'GC_Footprint_XX_LongDist',
'..._LongDistCompleteMap' — NONE ship in the tex archives (Beast bakes
generated at load). So fp buildings without an offline page render the island
bake tile alone (x2); the ~6 with offline pages (AWT, GA_TH, IC...) get
albedo*lightmap*2.

## 4. Street tier v5 — structural cross-section binding (smears killed)

Session 9's v4 edge-score binding produced rainbow smears (deployed state
verified headless). Root cause: ground pieces bound to band-atlas pages whose
v-bands do not contain the piece's v-range (cross-band stretch).

Fix: road atlases are cross-section stacks (sidewalk/asphalt/sidewalk groups
separated by dark curb rows). Groups detected from row luminance; a flat
segment binds the page whose ONE group contains its v-range (hard filter);
score only disambiguates among containing candidates.
Island2: 125 road + 248 albedo-tile + 647 dark (was ~all smear-prone).
Island1 similar. Full-page UV segments (vspan>0.985) -> dark.

## 5. What remains open

- batch_info.bin record layout (307B island1 / 196B island2, bit-packed):
  no fixed (bit_off,width<=16) field stays < material count across all 197
  records — the material reference needs the interleaved-allocator parse
  (CInterleavedDataAllocator ctor @0x4621e8 / vertex_data_allocator init
  @0x92f13c). CColladaDatabase ctor @0x7ba798 loads materials.bdae inside
  CDoubleBufferedDynamicBatchMesh ctor @0x45c750.
- bih_data.bin: [u32 5317] + variable leaf payloads; (off,sz) pairs observed
  (0xa62c,0x132) step 0x10b — role unresolved.
- 265 flat wide-u segments match NO cross-section group — their pages unknown.
- CLevelStreaming_DB::Load @0x3f6dfc = zone loader (opens all 7 files, feeds
  the ctors). getBatchMaterial reads SBatch+8/+0xc (material ptrs).
