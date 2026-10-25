# SESSION 60 — T2: vehicle health, second signal

## Signal 1 (data + engine reader) — vehicle Health = 300.0
- T1's hybrid walk (engine Health reader CComponentHealth::Load = f,c,i,i @0x2d7bf0, GCT-verified)
  closes 33 carriers in two position classes:
  - NPC carriers (Bane, Blake, Crowbar_Enemy...): Health@121, Awareness@138 (x14)
  - VEHICLE carriers (Police_Car, Coupe, Hatch, Bane_SUV...): Health@137, Awareness@154 (x19)
- Vehicle Health value = **300.0** at an engine-consistent alignment (19/19 records close to
  bounds with the engine reader; s56's "2.0" was the pre-collision-fix boundary artifact, s58
  corrected to 300 - this session re-derives 300 with the ENGINE reader, not a fitted spec).
- Boss reference: Bane (NPC class) health = 1400.0 @121; civilians 60; Bazooka_Enemy 90.

## Signal 2 (Lua) — one generic health system; NO vehicle-specific path
- gol.bin string table embeds 1,916 Lua script bodies (AI/combat templates) + the 541 lvc
  trigger scripts (s34): health API census:
  SetActorHealth x26, GetActorHealth x12, GetActorPercentHealth x4, GetActorMaxHealth present.
  ALL call sites are actor-generic (CurrentActor / 0 / EnemyID): e.g.
  `SetActorHealth(CurrentActor, GetActorHealth(CurrentActor) - 60)` (Templ790009),
  `SetActorHealth(CurrentActor, -100)` (fall-death), `SetActorHealth(0, GetActorMaxHealth(0))`.
- **Zero** script references combine vehicle words (Car/SUV/Heli/truck) with Health calls.
- GiveDamage census (game_config.gla, all 146 source-form, re-verified this session):
  5x91, 7x11, 10x9, 500x8, 1000x3+2-commented, 50x6, 25x5, 15x3, 300x2, 20x2, 30x1, 5000x1.
  Context decode (NEW): 500 x8 = Obj602228..235_WhileIn player hazards; 1000 =
  `GiveDamage(r_to_destroy_window_id, 1000)` WINDOW destruction (+2 commented out);
  5000 = scripted player one-hit-kill (Obj600801_OnEnter); 300 = Templ9965_20 (CurrentActor)
  + Obj700123_WhileIn player hazard. **NONE targets a vehicle.**

## Verdict
- The two signals AGREE on the mechanism: a single generic per-actor Health component read
  by the engine loader and manipulated by the generic Lua API; vehicles carry it in the gol
  like every other actor.
- Vehicle Health = 300.0: Signal 1 is direct (engine reader, aligned, 19 records). Signal 2
  corroborates the mechanism but does NOT independently pin the VALUE (the 300-damage literal
  is a coincidence - it targets actors/windows, not vehicles).
- Open: consumer-named roles for Awareness fields 0..12 (radii 11/17 used by the s59/s60 cone
  remain data-derived; only field 13 = VisibilityAngle is engine-named). GetActorMaxHealth's
  C++ export not yet traced (would close the Lua->engine field path end to end).

## Receipts
- extraction/re/session60/s60_t1_walk.json (carrier classes/values)
- this note: value contexts quoted verbatim from the archives
