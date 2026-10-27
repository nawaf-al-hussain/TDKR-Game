# SESSION 63 — T4: carriers recomputed with the engine-true nested specs (57/57 OK) + lvc second-signal scan

## Carrier walk (denominator: the 57 Health/Awareness carrier templates; the task's "50" =
## the s58-era carrier set; the census grew to 57 as more carriers were identified)
- **57/57 walk OK, ZERO fails** (s62: 51/57 with 6 StateSet fails).
- vs s62: agree 47, disagree 4, new-now-OK 6.
- NEW (were the 6 StateSet residual fails): Helicopter 300.0 (awareness family 30/50),
  Helicopter_Bane 300.0, Military_Heli 300.0, BatPod 150.0 (tail:4 template - health read,
  payload_end false as documented), TheBatDrive 150.0, Test_Object 60.0.
- 4 DISAGREEMENTS = s62 CORRECTIONS: Monorail_Back / Monorail_Car / Monorail_Front /
  Subway_Car: s62 said health 0.0 -> s63 says **300.0** with payload_end TRUE and the
  VEHICLE awareness family [5,15,2,8,1,3,0.5,1.5,...]. The s62 0.0s were misaligned reads
  caused by the forced-flat StateSet spec walking count>0 payloads short; the nested spec
  places Health correctly. The s58/s60 calibrated values are re-derived EXACTLY everywhere
  they existed (merc 120 + (11,17) family; Tumbler/Police_Car/Bane_SUV 300).
- Health distribution now: 300x25 (was 18), 150x8, 1400x5, 120x5, 60x4, 1x4, 50x2,
  100/90/140x1 (bosses 1400, civilians 60 - the s56 family clustering holds).

## Second signal for vehicle health 300.0: CLOSED-NEGATIVE at the instance level
- Raw-byte scan for the Health component id 0x0ddcd6c4 across ALL .lvc files
  (BatCave, GothamCity, GothamCity_Island2, Military, Test.lvc, ...): **ZERO occurrences**.
  Combined with the s13 engine evidence (CLevel::LoadNextObject reads exactly
  CComponentBase::Load + CComponentMesh::Load per instance record - no Health reader in
  the instance path), lvc instances CANNOT carry a Health override.
- Verdict: vehicle health 300.0 remains **PARTIAL single-signal** (the one signal is now
  engine-NAMED and walks cleanly for 25/25 vehicle carriers).

## Artifacts
s63_t4_carriers.py -> s63_t4_carriers.json (all 57 carriers with payload_end flags, the
s62 comparison, the distribution, the lvc scan).
