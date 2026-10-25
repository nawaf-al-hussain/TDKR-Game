# s59 T2 — merc rig IN-PAGE: generalized bdae reader (header-derived), Batman digests EQUAL, merc skeleton validated, enemy clips FK on merc rest locals, ?enemy=1 gate PASS with wrong-clip control

## BRES container (self-describing; all three files same format)
header: 'BRES' @0, ver 0xfffe, n1=0x3c, filesize @0x0c (== actual size all 3), n_relocs @0x10;
offsets @0x18: [0x3c (=reloc table start), pool0, pool1, off3, off4, 0,0,0, big_section];
reloc table 0x3c..pool0 (n_relocs u32 file offsets; targets all < off4; the data section
> off4 is relocation-free). pool0 = strings (mesh/skin names 'Bane_mercenary_LOD00-mesh',
'...-mesh-skin' x20 meshes + Bip names); pool1 = secondary pool.

## Generalized walker (readBdae2 in tdkr_pipeline.js; python twin s59_t2_walk3.py)
1. nodes: validated 0x50 records scanned at 4-B granularity in [pool1, off4) (name/name/alias
   pointers into pool0, |q|~1, |t|<1e4, 0.01<|s|<100, u32(+0x34)==1, u32(+0x38)<=32).
2. vertex stride: first run of >=4 equal u32 in [off4, +0x200) -> stride (batman 80, merc 52).
3. INVB: 64-B col-major mats, row3 (m3,m7,m11,m15)=(0,0,0,1); first run >=10, BACKWARD-extended
   (a false anchor chains through the true block otherwise) -> batman 0x30e30/31, merc 0x74080/31.
4. palette: nBones 8-B entries containing 'Bone' at +0 or +2, after INVB end (batman 0x3167c,
   merc 0x748d8; names Bone7,Bone1,Bone2,...).
5. skin records: try (stride,#weights) in {(20,4),(16,3),(24,5),(12,2),(28,6)}; first run >=200
   after palette -> NV + record geometry (batman 20-B/4-infl NV=1449 @0x31774; merc **16-B/
   3-influence** NV=**1294** @0x749d0 maxJoint 30 -> 31 bones == INVB == palette).
6. verts: descriptor bbox (6 floats at stridesAt-0x18) + ALL-NV-records-in-bbox scan
   (batman 0x4b5c == s22 constant; merc 0x53c4). uv = u16 at stride-8/stride-4 (/4096).
7. indices: first >=32 run of u16 < NV after the vertex block (batman 0x210ba/5431 == s22;
   merc 0x15b16/6007).

## VALIDATION
- **BATMAN DIGESTS EQUAL: readBdae2(batman.bdae) == readBdae(batman.bdae)** (node harness
  s59_t2_check_bdae2.js): verts sha bf4cd6849d3834ed, idx sha 968b43d5b220f980 (5431),
  skinJ sha d1d89fa17550f19b, 31 joints, invB[0][0..3] identical — the generalized reader
  reproduces the s22 layout EXACTLY with zero per-file constants.
- Merc layout cross-checked python vs JS: NV 1294, stride 52, INVB 0x74080 x31, palette
  0x748d8 x31, SKINREC 0x749d0 (16 B, 3 infl), VERTS 0x53c4, IDX 0x15b16/6007 — identical.
- s58's '1449-vertex shared topology / 31 joints from SKIN_OFFS' confirmed as the batman
  layout misread onto merc bytes (merc = 1294 verts).

## Merc skeleton independent validation (s59_t2_skelval.json; |bind origin - skin-weighted
   centroid| in world units; permuted-mapping null, same construction, 5 trials)
- batman (known-good): median 0.0888, p90 0.146, max 0.189; null medians 0.49-0.76 (6-8x).
- **merc: median 0.0750, p90 0.181, max 0.240; null medians 0.64-0.90 (~9x)** — joint mapping
  (skinrec index -> palette/invB order) CORRECT. 31/31 bones have vertices.
- low: median 0.115, null 0.59-0.70 (23 bones).

## Bone-name overlap with clip channels (shared batman_anims.bdae bank, 78-entry CH table)
72 ty=5 channels; base names: **37/72 present in the merc skeleton; ALL 35 missing are the
Batman cape CBone family (Bip01_CBone00..46)** — every locomotion channel (Bip01, Pelvis,
Spine/1, Neck, Head, arms, legs, fingers) exists. Merc rest locals: pelvis->thigh 0.106,
thigh->calf 0.4098, calf->foot 0.45 (identical to batman's biped proportions; rest QUATS differ).

## Enemy-clip FK on the MERC skeleton (s59_t2_fk_merc.json; pelvis = Bip01 ty1 translation,
    clip ty5 quats where present else rest; rolled control = +25 deg x-roll on all locals)
- _166_enemy_walk: loop foot L/R 0.346/0.065, pelvis z 0.869-0.947 (mean 0.908), foot z spans
  0.45-1.39; _171_enemy_run: loops 0.461/0.264, pelvis 0.868-0.956; _014_idle_enemy_combat:
  loops 0.575/0.469, pelvis 0.834-0.878.
- s58 (batman rest locals): walk loops 0.310/0.269 pelvis 0.911; run 0.252/0.908 pelvis 0.913;
  idle-combat 0.432/0.251 pelvis 0.739 — SAME ranges (the pelvis translation is clip-carried
  and rig-independent; leg rest offsets identical; only rest quats differ, overridden by clip
  channels) => the enemy clips are rig-compatible with the merc skeleton; no contradiction
  with the s58 numbers.
- Static calibration _001_idle_stand: loops 0.0000/0.0001 (merc) — battery floor OK.
- Rolled-25 control on merc walk: foot_L_zmin 0.4545 -> 0.3811, loop_R 0.065 -> 0.123,
  foot band shifts — step profile BREAKS (wrong-case discriminator).

## In-page ?enemy=1 (integration_lazy.html + tdkr_pipeline.js, branch s56-t1-glide)
- readBdae2 added + exported; loadMerc now uses it (layout from the file's own headers).
- buildGLB: clip list now caller-suppliable (4th arg); ibm count generalized to invB.length;
  merc call embeds ENEMY_CLIPS. finalizeGate defers `done` in enemy mode until mercTick
  reports; mercTick hoisted into the walk-phase branch (playback continues past idle);
  CPU-skin probe (150 verts via applyBoneTransform) records per-phase mean vertex
  displacement; wrong-clip negative control (walk displacement labeled as the idle slot)
  with updateMatrixWorld refresh.
- GATE (s59_t2_gate.json): default PASS 0 errs soup 00ce7970e45adc85 (= LIVE) 137893 tris;
  **?enemy=1 PASS 0 errs: enemy.ok {verts 1294, joints 31, clips x3}; enemyPlay {wraps 2,
  phasesSeen 3, dispIdle 1.330, dispWalk 1.753, dispRun 1.926 (monotone with gait speed),
  dispCtlWrongClip 1.769 (|ctl-idle| = 0.438 >> intra-clip noise)}; soup + routes 10/10
  unchanged.** dmg = 5 (GiveDamage provenance string kept).
