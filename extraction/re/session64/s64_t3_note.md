# SESSION 64 — T3: vehicle health 300.0 second signal — FINAL LOOK, all angles NEGATIVE (single-signal PARTIAL stands)

## 1. Save-game channel: NEGATIVE (code-exhaustive)
The symtab contains NO CComponent*::Save/SaveSave/LoadSave for ANY component. The only
health serialization in the binary is PlayerComponent::SaveMaxHealth(CMemoryStream*) /
LoadMaxHealth (0x25cde8/0x25ce04 region) - player-only. Vehicle health never enters or
leaves a save game -> the save format cannot be a second data source.

## 2. CVehicle* code: NEGATIVE
Zero CVehicle* symbols touching Health/Damage (nm scan filtered through c++filt).

## 3. Engine writers of health: CLOSED-EXHAUSTIVE (35 xrefs, 7 enclosing functions)
BL-xref scan of the whole text range (0xa5d80..0xac2190) for CGameObject::SetHealth
(0x3604b8), SetMaxHealth (0x360504), GetMaxHealth (0x3604f0): 35 sites resolving to
exactly:
- Lua SetActorHealth(lua_State*) impl (the Lua funnel)
- GameObjectCacheManager::ResetStatus / RemoveAll x2 (cache recycle - re-applies the
  TEMPLATE default = the same single signal re-applied, not a new source)
- CDestroyableComponent::OnEvent
- CElectricTurretComponent::Activate x3
- CSurveillanceCameraComponent::OnBatarangHit x2 (+2 dup nm entries)
- PlayerComponent (RegenerateHealth/RestoreHealth/Save/LoadMaxHealth/HasLowHealth/
  HasHurtEffect/UpdateSounds/UpdateHurtSounds)
- CHUDDisplay::UpdateEnemyHealthBar (read)
NONE is a vehicle path. No CVehicle spawn/update code writes health.

## 4. Upgrades: NEGATIVE
No health/armor upgrade path: ShopManager::BuyUpgrade/ReDoUpgrade + the Lua Upgrade
export drive gadgets/combos (the s58 SUpgrade model; the only Health-adjacent consumer
remains the player). No vehicle-health key consumer exists.

## 5. Lua spawn scripts: NOT STATICALLY ENUMERABLE (bounded, not a new signal)
All 146 GiveDamage + 63 SetActorHealth call sites pass the ACTOR argument as a variable
(s58 census artifacts record the damage literals only; actor ids are runtime values), so
a static vehicle-id x script-id cross-check is impossible without executing level
scripts. The engine-side enumeration (angle 3) covers the funnel these calls go through.

## Verdict
Vehicle health 300.0 (25/25 vehicle carriers walking cleanly under the engine-true
specs) remains **PARTIAL single-signal**: the one signal is engine-NAMED (Health
component id 0x0ddcd6c4 at its payload position), walks byte-exactly, and no second
independent data channel exists in the binary (save: no; vehicle code: no; engine
writers: enumerated, none vehicle; upgrades: no). Per the brief: STOP spending time
here. The remaining theoretical residue (a Lua script writing vehicle health at spawn)
is not statically enumerable and would surface as a script literal, not engine data.
