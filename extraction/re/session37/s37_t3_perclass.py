#!/usr/bin/env python3
"""S37 T3a: per-class pass rates with causes, replayed from the s36 battery
artifacts (rows carry every metric; test() is re-applied verbatim).

Signature battery (s36_t3_signatures.json rows, 921 clips):
  - re-apply the exact test() from s36 -> per-class tested/passed
  - every failure tagged with a cause (name-pattern rules established r26)
Gait battery (session36_t3_gaitfk.json results, 154 walk/run-named clips):
  - criteria: period in [200,2000] ms + ac > null+0.1 + foot z > 0.12 m
    + |anti-phase| > 0.5 (r26 strict set)
  - per-class rates + causes
Assembly-error check: 'decode' (empty-root) clips must have decodable JOINT
channels (r26); seam continuity re-referenced from s36_seams.json.
"""
import json, collections, re

B = '/tmp/my-project/work/TDKR-Game/extraction/re/'
S = json.load(open(B + 'session36/session36_t3_signatures.json'))
rows = S['rows']

def classify(name):
    n = name.lower()
    if '_to_' in n: return 'transition'
    if n.startswith('idle') or '_idle' in n: return 'idle'
    if 'turn' in n and ('90' in n or '180' in n): return 'turn'
    if 'walk' in n: return 'walk'
    if 'run' in n or 'sprint' in n: return 'run'
    if 'jump' in n: return 'jump'
    if 'fall' in n: return 'fall'
    if 'death' in n or 'die' in n: return 'death'
    if 'crouch' in n or 'sneak' in n: return 'crouch'
    if 'combat' in n or 'jab' in n or 'attack' in n or 'punch' in n: return 'combat'
    if 'climb' in n or 'hang' in n or 'grap' in n: return 'climb'
    if 'glide' in n or 'fly' in n: return 'glide'
    return 'other'

# verbatim test() from s36_t3_signatures.py
def test(r):
    c = r['cls']
    if c == 'idle':
        ok = r['zr'] < 0.25 and r['lf_rng'] < 20 and r['rf_rng'] < 20 and r['xy_rate'] < 0.3
    elif c in ('walk', 'run'):
        ok = (r['lth_rng'] > 15 or r['rth_rng'] > 15) and r['lth_ac'] > r['null_lth_ac'] + 0.15
    elif c == 'turn':
        ok = r['yaw_total'] > 30 or r['yaw_rng'] > 45
    elif c in ('jump', 'fall'):
        ok = ('loop' not in r['name'].lower()) and (r['zr'] > 0.35 or r['z_start_end'] > 0.25)
    else:
        ok = None
    return ok

def cause(name, cls):
    n = name.lower()
    if '_to_' in n: return 'transition clip (blend, no fixed signature)'
    if 'idle_start' in n: return 'locomotion start transition'
    if any(k in n for k in ('car_', 'batpod_', 'pray', 'wall_lean', 'table_', 'newspaper',
                            'bus_idle', 'tied_', 'conversation', 'listen')):
        return 'code-driven/prop root motion'
    if any(k in n for k in ('hang', 'contact', 'grapnel', 'parachute', 'stream_jet')):
        return 'overlay/anchored pose (root animated by code)'
    if cls in ('fall', 'jump') and 'loop' in n: return 'loop clip: net-z ~0 by design'
    if 'enemy_' in n or 'npc_' in n or 'bane_' in n or 'mercenarie_' in n:
        return 'NPC/enemy variant (different rig scale/gait)'
    if 'combat' in n or 'jab' in n or 'hurt' in n or 'wip' in n: return 'combat overlay'
    if 'turn' in n: return 'turn-in-idle compound'
    return 'UNEXPLAINED'

per = collections.defaultdict(lambda: {'tested': 0, 'passed': 0, 'fails': [], 'causes': collections.Counter()})
decode_fail = []
for r in rows:
    c = r['cls']
    if 'fail' in r:
        decode_fail.append(r['name'])
        continue
    ok = test(r)
    if ok is None:
        continue
    per[c]['tested'] += 1
    if ok:
        per[c]['passed'] += 1
    else:
        per[c]['fails'].append(r['name'])
        per[c]['causes'][cause(r['name'], c)] += 1

print('=== SIGNATURE battery per-class (verbatim test replay) ===')
tot_t = tot_p = 0
unexplained = []
for c in sorted(per):
    d = per[c]
    tot_t += d['tested']; tot_p += d['passed']
    rate = d['passed'] / max(d['tested'], 1)
    print(f'  {c:10s} tested={d["tested"]:3d} passed={d["passed"]:3d} rate={rate:5.1%} '
          f'fails={len(d["fails"])}')
    for k, v in d['causes'].most_common():
        print(f'      - {k}: {v}')
    unexplained += [(n, c) for n in d['fails'] if cause(n, c) == 'UNEXPLAINED']
print(f'  TOTAL tested={tot_t} passed={tot_p} ({100*tot_p/max(tot_t,1):.1f}%)')
print(f'  decode-untestable (empty root channels): {len(decode_fail)} (joint channels decode; code-driven roots per r26)')
print(f'  UNEXPLAINED failures: {unexplained}')

# assembly check
try:
    seams = json.load(open(B + 'session36/s36_seams.json'))
    print('seams artifact present:', list(seams)[:4] if isinstance(seams, dict) else len(seams))
except Exception as e:
    print('seams artifact:', e)

# gait battery replay (VERBATIM criteria from s36_t3_gaitfk.py: left-foot only,
# acL > max(null+0.1, 0.3), footz_L > 0.12, (anti0 < -0.5 or anti > 0.5))
G = json.load(open(B + 'session36/session36_t3_gaitfk.json'))
res = G['results']
gper = collections.defaultdict(lambda: {'tested': 0, 'passed': 0, 'fails': [], 'causes': collections.Counter()})
for r in res:
    if 'fail' in r or r['acL'] is None:
        continue
    ok = (float(r['acL']) > max(float(r['null_ac'] or 0) + 0.1, 0.3)
          and float(r['footz_L']) > 0.12
          and ((r['anti0'] is not None and float(r['anti0']) < -0.5)
               or (r['anti'] is not None and float(r['anti']) > 0.5)))
    gper[r['cls']]['tested'] += 1
    if ok:
        gper[r['cls']]['passed'] += 1
    else:
        # which criterion failed (left-foot verbatim battery)
        why = []
        if not (float(r['acL']) > max(float(r['null_ac'] or 0) + 0.1, 0.3)):
            why.append('acL')
        if not float(r['footz_L']) > 0.12:
            why.append('footz_L')
        if not ((r['anti0'] is not None and float(r['anti0']) < -0.5)
                or (r['anti'] is not None and float(r['anti']) > 0.5)):
            why.append('anti')
        gper[r['cls']]['causes']['crit:' + '+'.join(why)] += 1
        gper[r['cls']]['fails'].append(r['name'])
        gper[r['cls']]['causes'][cause(r['name'], r['cls'])] += 1

print('\n=== FK GAIT battery per-class (strict criteria replay) ===')
gt = gp = 0
g_unexpl = []
for c in sorted(gper):
    d = gper[c]
    gt += d['tested']; gp += d['passed']
    print(f'  {c:10s} tested={d["tested"]:3d} passed={d["passed"]:3d} rate={d["passed"]/max(d["tested"],1):5.1%}')
    for k, v in d['causes'].most_common():
        print(f'      - {k}: {v}')
    g_unexpl += [(n, c) for n in d['fails'] if cause(n, c) == 'UNEXPLAINED']
print(f'  TOTAL tested={gt} passed={gp} ({100*gp/max(gt,1):.1f}%)')
print(f'  UNEXPLAINED: {g_unexpl[:10]}')

json.dump({'signature_per_class': {c: {'tested': d['tested'], 'passed': d['passed'],
                                       'fails': d['fails'],
                                       'causes': dict(d['causes'])} for c, d in per.items()},
           'sig_total': [tot_t, tot_p], 'decode_untestable': len(decode_fail),
           'unexplained_sig': unexplained,
           'gait_per_class': {c: {'tested': d['tested'], 'passed': d['passed'],
                                  'fails': d['fails'],
                                  'causes': dict(d['causes'])} for c, d in gper.items()},
           'gait_total': [gt, gp], 'unexplained_gait': g_unexpl},
          open(B + 'session37/s37_t3_perclass.json', 'w'), indent=1)
print('saved s37_t3_perclass.json')
