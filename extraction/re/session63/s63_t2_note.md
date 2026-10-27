# SESSION 63 — T2: posed merc skinning nulls restated (full table with n)

## Table (page raw-WebGL1 raster vs numpy reference; 64x64 grid IoU)
15 real rows (5 clips x fracs 0.25/0.5/0.75), full data in s63_t2_table.json:
- IoU 0.7880..0.9389, mean 0.9001 (reproduced; reproduction check vs the stored row OK)
- n per row: nVerts = 1294 (all rows), page lit 9,862..16,844 px, numpy lit 720..1,166 px
- meanVertDist = 0.0000 on every row (the s62 restMaxDev-0 fix holds)
- clips: _014_idle_enemy_combat (Idle), _166_enemy_walk (Walk), _171_enemy_run (Run),
  _223_enemy_hurtl (Hurt), _250_enemy_death1 (Death)
- Batman row (s60 T3, static bind-pose render = DIFFERENT, rest-frame pipeline):
  IoU 0.9516, nVerts 1294, nulls batman-mesh-cross 0.6922 / x-flipped 0.6772.

## Nulls (all built the same way as the real statistic)
- rolled-pose (90-deg about Z through pelvis): 0.0000..0.5478 (n=15) - ALL below the real
  minimum -> DISCRIMINATES the pose channel.
- batman-mesh cross (page merc vs numpy skinned with Batman's rest offsets): 0.0127..0.6004
  (n=15) - DISCRIMINATES the mesh channel.
- NEW wrong-clip matrix (numpy skin of clip B, B's own boneMats, vs page grid of clip A),
  frac 0.5, 20 ordered pairs: 0.3528..0.6838. Every moving-clip-as-page row drops below the
  real band (death1-as-page <= 0.4327, hurt-as-page <= 0.5176); the closest pairs are
  Idle<->Walk / Idle<->Run (0.57..0.68, similar upright poses) - discriminative but with a
  narrower margin, exactly as expected for pose-similar clips.

## Which comparisons discriminate and which do not
- DISCRIMINATE: real vs rolled (gap >= 0.24), real vs wrong-clip for moving clips (gap >= 0.32
  for Death/Hurt pages), real vs batman-cross (gap >= 0.19).
- DO NOT (weak): rest-frame comparisons between rigs sharing the BIPED rest offsets - the s60
  Batman rest row's cross-nulls (0.69/0.68) sit far closer to the real 0.9516 than any posed
  null does to 0.9001; rest silhouettes are dominated by the shared rest offsets, so a
  rest-frame rig cross-check is NOT evidence of correct skinning. The posed-frame nulls are
  the discriminating ones.
- Wrong-clip pairs between pose-similar clips (Idle<->Walk 0.61-0.68) overlap nothing in the
  real band but only by ~0.11 - report as discriminative-with-margin, not absolute.

## Artifacts
s63_t2_table.py -> s63_t2_table.json (rows + all three null sets + wrong-clip matrix).
No page re-run needed: everything derives from the s62 capture (s62_t2_capture2.json) with
the s62 pipeline reproduced (reproduction check OK).
