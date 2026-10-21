#!/usr/bin/env python3
"""S36 T6: run the SAME 10 OnEnter scripts in REAL Lua 5.1 (lupa.lua51) with
identical stubs + call logging; compare vs the fengari logs."""
import json
import lupa.lua51 as l51

D = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
onEnter = [s for s in D['all_scripts'] if '_OnEnter' in (s.get('fn') or '')][:10]
feng = json.load(open('/home/z/my-project/scripts/s36_t6_fengari_logs.json'))

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
        'EnableRain ShowObjectiveMessage SetObjectiveText ObjectiveHide StartMainStoryFromQuestId '
        'fz_sandbox_enable_before_pit PlayCameraAnim r_RandomChoice fz_RandomChoice TurretSetActive '
        'PostProcessingEffectRemove QTE_EnableControl DisableCopAI CameraShake StartSoundAtWaypoint '
        'EnableShowObject StartEventAtObjectNode ObjectiveShow SetCurrentActor ActorWalkTo ActorRunTo').split()

L = l51.LuaRuntime(unpack_returned_tuples=True)
logs = []


def make_logger():
    """returns a fresh lua table factory that records calls"""
    def mk(name):
        def fn(*args):
            out = []
            for a in args:
                try:
                    if isinstance(a, float) and a == int(a) and abs(a) < 2**53:
                        out.append(float(a))
                    elif isinstance(a, (int, float, str, bool)):
                        out.append(a)
                    else:
                        out.append(':' + type(a).__name__)
                except Exception:
                    out.append(':?')
            logs.append([name] + out)
        return fn
    return mk


# semantic stubs are registered via __log wrappers below (identical values)
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
L.globals()['MC_MAX_DISTANCE'] = 40.0

# Wait = coroutine.yield wrapper (5.1)
L.execute('''
__logs = {}
function __log(name, ...)
  local t = {name}
  for i = 1, select('#', ...) do
    local v = select(i, ...)
    if type(v) == 'number' or type(v) == 'string' or type(v) == 'boolean' then
      t[#t+1] = v
    else
      t[#t+1] = ':' .. type(v)
    end
  end
  __logs[#__logs+1] = t
end
''')
for nm in VOID:
    L.globals()[nm] = L.eval(f'function(...) __log("{nm}", ...) end')
for nm, val in (('GetTime', '1000'), ('IsEnabled', 'true'), ('GetDistBetweenObjects', '25.0'),
                ('IsCopAIEnabled', 'false'), ('IsLowEndDevice', 'false'), ('GetGlobalVar', '0'),
                ('IsCameraFacing', 'true'), ('GetCurrentInteractionObjectID', '0'),
                ('ActorIsInStateType', 'true'), ('IsDead', 'false'), ('ActorIsDead', 'false'),
                ('ActorGetState', '1')):
    L.globals()[nm] = L.eval(f'function(...) __log("{nm}", ...) return {val} end')
L.globals()['GetDistFromMC'] = L.eval('function(...) __log("GetDistFromMC", ...) return 12.5 end')
L.globals()['Random'] = L.eval('function(...) __log("Random", ...) return 1.0 end')
L.globals()['ObjectGetPosition'] = L.eval('function(...) __log("ObjectGetPosition", ...) return -470.09, -960.2, -3.91 end')
L.globals()['GetActorFromObject'] = L.eval('function(...) __log("GetActorFromObject", ...) return nil end')
L.globals()['Wait'] = L.eval('function(...) __log("Wait", ...) return coroutine.yield() end')

results = []
for s, feng in zip(onEnter, feng):
    logs.clear()
    L.globals()['__cur_script'] = s['script']
    L.globals()['__cur_fn'] = s['fn']
    L.globals()['__cur_obj'] = s.get('obj_id') or 0
    res = L.execute('''
      __logs = {}
      local f, err = loadstring(__cur_script)
      if not f then return false, 'load: ' .. tostring(err) end
      f()
      local co = coroutine.create(function(...) _G[__cur_fn](...) end)
      local ok, e1 = coroutine.resume(co, __cur_obj, 0)
      local resumes = 0
      while coroutine.status(co) == 'suspended' and resumes < 16 do
        local ok2, e2 = coroutine.resume(co)
        resumes = resumes + 1
        if not ok2 then break end
      end
      return coroutine.status(co), #__logs
    ''')
    lu = L.globals()['__logs']
    calls = []
    n = len(lu)
    for i in range(1, n + 1):
        row = lu[i]
        calls.append([row[j] for j in range(1, len(row) + 1)])
    results.append({'fn': s['fn'], 'calls': calls, 'status': res[0] if isinstance(res, tuple) else res})
    # compare vs fengari
    fcalls = [[c[0]] + [x for x in c[1:]] for c in feng['calls']]
    norm = lambda c: [[x if not isinstance(x, float) or x != int(x) else x for x in row] for row in c]
    same = len(fcalls) == len(calls)
    diffs = []
    if same:
        for a, b in zip(fcalls, calls):
            na = [x if not isinstance(x, float) else float(x) for x in a]
            nb = [x if not isinstance(x, float) else float(x) for x in b]
            if na != nb:
                diffs.append((a, b))
                same = False
    print(f"{s['fn']}: fengari {len(fcalls)} calls vs 5.1 {len(calls)} calls -> {'IDENTICAL' if same else 'DIFF'} [status={results[-1].get('status')} ({calls[:2]})]")
    if not same:
        for a, b in diffs[:4]:
            print('   fengari:', a, '| 5.1:', b)
json.dump(results, open('/home/z/my-project/scripts/s36_t6_lua51_logs.json', 'w'))
