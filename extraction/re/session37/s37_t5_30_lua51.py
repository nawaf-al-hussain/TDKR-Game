#!/usr/bin/env python3
"""S37 T5: real Lua 5.1 (lupa) side - SAME 30 scripts, SAME stubs, SAME log
format as the fengari side; coroutine-resumed like fengari; then per-script
diff vs the fengari logs."""
import json
import lupa
import lupa.lua51 as l51

D = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
pool = [s for s in D['all_scripts'] if ('_OnEnter' in (s.get('fn') or '') or '_OnReach' in (s.get('fn') or ''))]
sel, seen = [], set()
for want in ('OnEnter', 'OnReach'):
    for s in pool:
        if len(sel) >= 30:
            break
        if want in (s.get('fn') or '') and s['obj_id'] not in seen:
            sel.append(s); seen.add(s['obj_id'])
    if len(sel) >= 30:
        break

VOID = ('Enable Disable ShowObject HideObject ShowMessage HideOccluder ShowOccluder DisableHideObject '
        'StartCinematicObject StartFadeOut StartFadeIn RequireLoadLevel ObjectiveAdd ObjectiveRemove '
        'ShowObjectiveMessage StartSound StopSound SetRotateControlEnable SetMoveControlEnable CameraLookAt '
        'ActorLookTo SetQuestFailed SetQuestEnabled MissionFailedAutoReload StartPipeGame NextMission '
        'StopSideMissionManager EnableHotSpotManager ActorSetState SpawnObject SetStateType ActivateDistrictZone '
        'ObjectiveCompleted SetActorInvincible FreezePlayer UnfreezePlayer SetCameraMode PrintDebug SetTimer '
        'KillTimer ActorPlayAnim SetCollisionEnable AttachObject DetachObject SetPos SetObjectPos PlaySound '
        'CineStart CineStop SetSky SetObjectiveComplete AddScore SetHealth GiveWeapon SetBrightness '
        'ShowMissionBar HideMissionBar SetFadeColor ReturnToHub SetTimerMS KillActor GiveDamage '
        'SetActorSpeedWalk SetActorSpeedRun SetActorSpeedGlide StartMainStoryFromQuestId NPCSetSniper '
        'NPCSetStance TeleportPlayerToZone NPCGoToWaypointWithNavmesh NPCAttackTarget NPCGoToPath '
        'ClearObjectiveMessage NPCStandGroundTarget NPCPatrolArea NPCGoToWaypoint print RemoveGenericObjectFromMap '
        'EnableRain SetObjectiveText ObjectiveHide StartEventAtObjectNode SetCurrentActor ActorWalkTo ActorRunTo '
        'fz_sandbox_enable_before_pit PlayCameraAnim r_RandomChoice fz_RandomChoice TurretSetActive '
        'PostProcessingEffectRemove QTE_EnableControl DisableCopAI CameraShake StartSoundAtWaypoint '
        'ObjectiveShow EnableShowObject SetJumpControlEnable StartEffect PlayEffectOnObject SetQuestDisabled '
        'Traffic_SpawnerEnable ResetAllIgnoredControls SaveGame MissionFailed ActorSetTarget NPCGoTo '
        'ActorTeleportTo CameraFade SetWorldPause fz_sandbox_enable_all_first_island fz_sandbox_disable_all '
        'fz_sandbox_enable_ALL EnableMainStory SetQuestCompleted QTE_GrapplingSetTarget ResetSlowMotion '
        'SetRopeVisible PostProcessingEffectAdd EnableInteractionForObject EnterBatPod EnableControls SetZFar '
        'r_map StopMusic DisableInteractionForObject PlayAnimation StopCurrentSFXAtObject').split()

out = {}
for s in sel:
    L = l51.LuaRuntime(unpack_returned_tuples=True)
    calls = []

    def push(*a, _calls=calls):
        row = []
        for v in a:
            if isinstance(v, bool):
                row.append(v)
            elif isinstance(v, (int, float)):
                row.append(float(v))
            elif isinstance(v, str) or v is None:
                row.append(v)
            else:
                row.append(':' + type(v).__name__)
        _calls.append(row)
    L.globals()['__push'] = push
    L.execute('function __log(name, ...) __push(name, ...) end')

    L.globals()['GetTime'] = lambda *a: 1000.0
    L.globals()['IsEnabled'] = lambda *a: True
    L.globals()['GetDistBetweenObjects'] = lambda *a: 25.0
    L.globals()['IsCopAIEnabled'] = lambda *a: False
    L.globals()['IsLowEndDevice'] = lambda *a: False
    L.globals()['GetGlobalVar'] = lambda *a: 0.0
    L.globals()['IsCameraFacing'] = lambda *a: True
    L.globals()['GetCurrentInteractionObjectID'] = lambda *a: 0.0
    L.globals()['ActorIsInStateType'] = lambda *a: True
    L.globals()['IsDead'] = lambda *a: False
    L.globals()['ActorIsDead'] = lambda *a: False
    L.globals()['ObjectGetPosition'] = lambda *a: (-470.09, -960.2, -3.91)
    L.globals()['GetDistFromMC'] = lambda *a: 12.5
    L.globals()['Random'] = lambda *a: 1.0
    L.globals()['ActorGetState'] = lambda *a: 1.0
    L.globals()['ObjectGetInt'] = lambda *a: 0.0
    L.globals()['GetActorFromObject'] = lambda *a: None
    L.globals()['MC_MAX_DISTANCE'] = 10.0
    L.globals()['Wait'] = L.eval('function(...) coroutine.yield(...) end')
    for nm in VOID:
        L.globals()[nm] = L.eval('function(...) __log("%s", ...) end' % nm)

    outcome, err = 'ok', None
    try:
        L.execute(s['script'])
        body = (
            "local co = coroutine.create(%s)\n"
            "local n = 0\n"
            "while n < 64 do\n"
            "  local ok, e = coroutine.resume(co, nil)\n"
            "  n = n + 1\n"
            "  if not ok then error(tostring(e)) end\n"
            "  if coroutine.status(co) == 'dead' then break end\n"
            "end\n"
            "if coroutine.status(co) ~= 'dead' then error('yield_incomplete') end\n"
        ) % s['fn']
        try:
            L.execute(body)
        except Exception as e2:
            m = str(e2)
            if 'yield_incomplete' in m:
                outcome = 'yield'
            else:
                outcome, err = 'error', m[:120]
    except Exception as e:
        outcome, err = 'error', str(e)[:120]
    out[str(s['obj_id']) + ':' + s['fn']] = {'outcome': outcome, 'err': err, 'calls': list(calls)}

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t5_lua51_30.json', 'w'), indent=1)
print('lua51 logs written for', len(out), 'scripts')

# ---- diff vs fengari ----
feng = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t5_fengari30.json'))

def norm(calls):
    r = []
    for c in calls:
        row = [c[0]]
        for v in c[1:]:
            if isinstance(v, bool) or v is None or isinstance(v, str):
                row.append(v)
            else:
                row.append(float(v))
        r.append(row)
    return r

identical = 0
diffs = []
for k, fv in feng.items():
    a = norm(fv['calls'])
    lv = out.get(k)
    b = norm(lv['calls']) if lv else []
    if a == b:
        identical += 1
    else:
        diffs.append((k, fv['outcome'], lv['outcome'] if lv else 'missing', len(a), len(b)))
print(f'IDENTICAL call logs: {identical}/{len(feng)}')
for k, fo, lo, na, nb in diffs[:10]:
    print(f'  DIFF {k}: outcome fengari={fo} 5.1={lo}; calls {na} vs {nb}')
json.dump({'identical': identical, 'total': len(feng),
           'diffs': diffs[:30]},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t5_diff.json', 'w'), indent=1)
