# SESSION 61 — T2: vehicle health second signal — search closed, verdict PARTIAL (single signal)

## What this session added
- Signal 1 provenance UPGRADED: the Health component id 0x0ddcd6c4 is now ENGINE-NAMED via
  the GCT case body (vtable -> CComponentHealth::Load 0x2d7bf0, spec [f,c,i,i] = 13 B,
  hand-checked in the s61 reader extraction). The 300.0 for 19 vehicle carriers is read by
  the engine's own named Health reader on the hybrid-walked payload (s58/s60 calibrated).
- New search executed (the remaining candidate signal): BYTE-LEVEL census of 300.0 across
  all 14 vehicle-family carrier payloads (Bane_SUV, Coupe, Hatch, Tumbler, Police_Car,
  Destroyable_SUV, monorail/subway family, helicopter family):
  **300.0 occurs exactly ONCE per payload - at the Health position (137, or 149 for the
  Bane_SUV position class).** No second independent store.
- Helicopter family shows extra 300.0 byte-hits at 2783/3048 (Military_Heli 2796/3061) -
  these sit deep inside large float-array components (Trail-class payloads), at
  family-specific offsets with no component-semantic attach point = coincidence, NOT a
  vehicle-health field. Monorail/Subway share identical payloads (1167 B) with one hit at 907.
- Avenues already closed by s58/s60 remain closed: Lua (SetActorHealth x26 all
  actor-generic, zero vehicle refs; GiveDamage 146 sites, none target vehicles);
  upgrade map (key 0x1f = glide helper only); Awareness vector (radii, not health).

## Verdict (unchanged, now stronger)
- Vehicle Health = 300.0: **single-signal** (engine Health reader, aligned, 19/19 carriers).
  Mechanism corroborated (generic per-actor Health on vehicles, no vehicle-specific path
  anywhere in Lua/engine naming); the VALUE has no independent second signal in the data.
- PARTIAL by rule 5 (the acceptance criterion "a real second signal" is not met).
- Residual idea for a future session: trace GetActorMaxHealth's C++ export (s60 open item)
  or capture a runtime health value via an instrumented build; both need tooling beyond
  static analysis.

## Artifact
- census inline in the session worklog; payloads re-derivable from s61_t1_parse.json
