# RE Session 11 — "grass/roads on buildings" root-caused and killed

## User complaint
"EVERY FUCKING BUILDING IS WRONGLY TEXTURED. I CAN SEE GRASS/ROAD TEXTURES ON BUILDINGS."

## Root causes (all verified, not guessed)

### 1. UV-fit page selection bound buildings to the ROADS page
v7-v11 "fp-page-fit" scored the 8 island pages by EDGE-DENSITY sampled at the
mesh's uv0 ("does this page have detail where my UVs point") — it never asked
whether the CONTENT matches. Road atlases are edge-rich everywhere, so
GC_Footprint_GA/VA_LongDist scored >= 0.9 on GC_LongDist_Island2_Roads and
literally wore roads. CB/CC/CD/CG got full-page top-down atlases (same
disease, different symptom: whole-city smear on walls).

### 2. Bake pages used as albedo substitutes
Both exporters had "lm && !tex -> render lm as diffuse" paths (mode 2x).
BakeGroup facade atlases and LongDist complete maps ended up as BUILDING
albedo with wrong sampling coords.

### 3. Wrong mode: 2x instead of x1
bdae TRUTH (GC_Footprint_CB/GA/VA_LongDist.bdae):
    DiffuseMap = GC_LongDist.tga, technique = #StandardDiffuseDC-fx
    -> Color = Diffuse x 1, NO LightMap slot.
The fp ladder hardcoded fp_mode="2x" -> overbright smear.

### 4. The whole LongDist/fp layer is authored in LOCAL coordinates
parse_meshes bbox: every GC_Footprint_*_LongDist unit spans ~+-100 units
around origin; the per-page ASSEMBLY bdaes too; GC_island1_LongDist too.
World placement lives in the lvc/BRES node graph (not yet decoded — the
530-record bake-group frames do NOT carry it; GothamCity.lvc string table
does not reference the footprint mesh names at all). Deployed until now as
zero-transform nodes = a pile of city blocks at the origin.

## Fixes shipped (v12)

### Authoritative footprint -> bake-page map (zero heuristics)
The assembly bdaes MERGE exactly the footprints baked into each page:
    GC_LongDist_Island1_FP1.bdae -> {LA,AA,AB,AC,AWT,CC,CD,GA,GC,GD,LC,VC,ZD}
    GC_LongDist_Island1_FP2.bdae -> {CA,AG,CF,DB,DC,DD,LB,VD,ZA,ZB,ZC}
    GC_LongDist_Island1_FP3.bdae -> {CB,CE,CH,CN,DA,GF,IA,IB,IC,LE,LF,VA,VB}
    GC_LongDist_Island1_Roads.bdae -> {DSE,VPOW}
    GC_LongDist_Island2_FP1/FP2/FP3/Roads -> {DF,ZF} / {LPOL,ZE,AJ,CM,GB,ID,IE,LG} / {CJ,CL,DG,DMUS} / {VRS}
Spot-verified against the v8 native records: GA/VPOW/GF all consistent.
export_city.py: load_fp_page_map() + footprint_page(); any unshippable fp
diffuse (GC_LongDiff OR per-footprint aliases like
'GC_Footprint_AA_LongDist'/'GC_Footprint_DA_LongdistDiffuseMap') binds its
assembly page at mode 'd'. Result: 50 fp meshes authoritative, 36 shipped
albedos, 12 honest dark. Fallback for unlisted ids (CFCG): structural
coverage-density x page-luminance Pearson match (replaces edge-density fit).

### Bake pages never used as albedo (both ladders)
lm-only -> dark. bake-fit threshold paths removed.

### Water planes
GC_water / GC_Water_Island2 (whole-map rects) were bound to the riverbed
sand tile = giant tan sheet under blue fog (the "green blanket").
Now bind the shipped water texture.

### Viewer boot policy (game-faithful)
Street tier (world-placed, real road/grass/prop materials) boots first and
is the default city; hero/fp/district/low are research toggles until the
node-graph transforms are decoded. District props default-off (unplaced
local props floated over the city).

## Next (ordered)
1. BRES node-graph transform decode (l_gothamcity.gla scene graph / bdae
   node sections) -> place hero+fp LongDist units at world coords; then
   re-enable skyline+fp by default.
2. Street batch material index (batch_info.bin bitstream,
   CInterleavedDataAllocator) -> real albedo for the ~600 dark near-tier
   building segments (this is what makes close-ups rich).
3. Ground fidelity split (roads/grass single-planar-unit complaint) after 2.
