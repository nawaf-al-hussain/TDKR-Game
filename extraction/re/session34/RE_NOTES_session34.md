# Session 34 (round 24) notes

## State
- Remote unchanged: main 8842b35, gh-pages f22b098 (v17 live), gh-pages-staged 9a9fb3b.
- Local main after this session: c33a2d7 (2d7025e T1, 02f58b2 T2, c33a2d7 T3+T4).
- Bundle: download/bundles_s34/main_s34_inc.bundle (4,361,139 B,
  SHA256 0116ed11a16d502951328081f8036961ae23b13fd0b5508871962659d029e3cb,
  requires 8842b35, verified).
- EIGHT rounds (17-24) now exist only in sandbox bundles. Push requested.

## T1 animation
- .bdae anims = 656 back-to-back [table][data] segments, 28-B chain records
  @0xcd00 stride 0x1c [tickEnd][0][0][ptr][dist][0][tickEnd]; ptr+dist==next.ptr.
- Exact file placement rule: data_k = seg_data_base + cumsum(len) — zero pads;
  idle 157/157 + run 156/156 validated (ticks ascending, quats unit, vec3 finite).
- Engine sampler: keyCount = entry.len>>2; quaternion::getMatrix = XYZW (w slot 3);
  blender 16-B keys, conjugate pattern on slots 0-2 => no 4-shift (engine-resolved).
- _008_run decoded (seg6: table 0xb2818, data 0xb2cfc..0xc2790).
- Battery: smoothness 15.9x vs shuffled null; root 166.30 deg = YAW difference
  (rest -90Z vs idle +76.4Z) not a convention error; fingers 109/91/43 curled-bind.
- batman_s34_anims.glb: TRS nodes, 2 animations, three.js GLTFLoader+AnimationMixer
  == numpy FK: worst 0.0004 cm (non-circular PASS).
- OPEN: clip->segment-subrange mapping (clip-list timeline vs packed pool timeline).

## T2 rig/cape
- Clavicle parent = Bip01_Neck (dt 0.000 cm, dq 0.011 deg; null p05 6.76 cm;
  positive control 29 joints max 0.001 cm). r22 "4 arm-root records off" = parent
  map bug (palette 11/17 = clavicles, not 10/16 = upper arms).
- Full rig from raw records: dp<=0.0202 cm, dr<=0.06 deg; skin mean 0.0199 cm.
- Cape: Load() = 27 ReadFloat + 1 ReadInt (cloth params only); vertex blocks
  1449/394/194 x 80 B ALL zero-filled; indices/binds/weights present.
  VERDICT: cape geometry = runtime cloth, absent from file.

## T3 navmesh/triggers
- .nm: [0x78][0x68][BE f32 soup] = 30,822 cells (x,y,z) Z-up; cell records
  (7 short + char, 16 B) field map OPEN.
- Ground validation: |dz| median 0.206 m vs shuffled null 18.7 m (80.1% < 0.5 m).
- Routes 0/34 (16 timeout, 15 fell, 2 stuck, 1 no_path) with derived adjacency;
  not better than grid A* 1/30; causes named.
- IsObjectInside: OBB-local via 4 stored vectors + owner scale; extents runtime.
- Spatial firing demo: trigger 1900053 fired by capsule entering decoded volume.
- FPS: no real-GPU evidence.

## T4 Lua
- 541 scripts (354 OnReach, 45 OnSpawn, 37 OnScriptEvent, 34 OnEnter, 33 Always,
  25 WhileIn, 9 Init, 2 OnExit, 2 WhileOut); ZERO 5.1-only constructs.
- 463/541 (85.6%) complete with handler invocation + semantic stubs.
- API ranking: Wait 127, ActorSetState 113, SetActorSpeedWalk 56, GetTime 52,
  KillActor 46, print 46, ActorLookTo 40, Enable 30, ShowMessage 26, Disable 23.

## Estimate
- In: walkable world (271,589 tris), character renderer + 2 animations, Lua shim
  (541-script-validated), triggers (positional fire).
- Not in: glide/grapple/combat/AI/mission flow/audio/UI, cape cloth, exact
  activation volumes, clip->subrange mapping, navmesh portal records.
- First playable milestone the evidence supports: walk-as-Batman on the collision
  ground of GothamCity with idle/run animations and positional Lua triggers
  firing (mission-chain scripts executing with stubbed engine APIs).
