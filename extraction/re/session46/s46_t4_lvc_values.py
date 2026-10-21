#!/usr/bin/env python3
"""s46 T4: decoded-VALUE digests Python (lvc_pure) vs JS (lvc.js parseLvc)
for lvc members of game_config.gla. Canonical token line: kind|off|value,
floats as raw f64 bits, strings latin1-decoded on both sides."""
import struct, json, hashlib, subprocess, sys
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla'
TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
OUT = '/home/z/my-project/scripts/s46_t4_lvc_values.json'

table = json.load(open(TAB))
gol = json.load(open(GOL))
templates = {int(k, 16): v for k, v in gol['templates'].items()}

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
lvcs = []
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm.endswith('.lvc'):
        lvcs.append((nm, o, s))
lvcs.sort(key=lambda t: -t[2])
print('lvc members:', [(nm, s) for nm, s, in [(a, c) for a, b, c in lvcs[:6]]])
pick = [lvcs[0], lvcs[1], lvcs[2]]  # three largest

def py_digest(data, tmpname):
    tokens = []
    lvc_pure.parse(tmpname, table, templates, tokens, None)
    h = hashlib.sha256()
    nkinds = {}
    for (kind, off, size, val) in tokens:
        nkinds[kind] = nkinds.get(kind, 0) + 1
        if kind == 'i':
            line = f'i|{off}|{val}'
        elif kind == 'f':
            line = 'f|' + str(off) + '|' + struct.pack('>d', val).hex()
        elif kind == 'STR':
            if isinstance(val, str):
                line = 'S|' + str(off) + '|' + val.encode('latin1', 'replace').hex()
            else:
                line = f'S|{off}|#{val}'
        elif kind in ('c', 'B', 's'):
            line = f'{kind}|{off}|{val}'
        else:
            line = f'{kind}|{off}|{size}|-'
        h.update(line.encode())
        h.update(b'\n')
    return {'count': len(tokens), 'sha': h.hexdigest(), 'kinds': nkinds}

pys = {}
js_in = []
for (nm, o, s) in pick:
    data = g[o:o + s]
    tmpname = f'/tmp/my-project/scripts_t4_{nm}.lvc'
    open(tmpname, 'wb').write(data)
    pys[nm] = py_digest(data, tmpname)
    js_in.append(nm)
print('python digests:')
for nm, d in pys.items():
    print(f'  {nm}: n={d["count"]} sha={d["sha"][:16]} kinds={d["kinds"]}')

node_script = '/home/z/my-project/scripts/s46_t4_js_digest.js'
proc = subprocess.run(['node', node_script] + js_in,
                      capture_output=True, text=True, timeout=600)
if proc.returncode != 0:
    print('NODE FAIL:', proc.stderr[-800:])
    sys.exit(1)
jss = json.loads(proc.stdout)
print('js digests:')
for nm, d in jss.items():
    print(f'  {nm}: n={d["count"]} sha={d["sha"][:16]} kinds={d["kinds"]}')

verdict = {}
for nm in pys:
    same = pys[nm]['sha'] == jss.get(nm, {}).get('sha') and pys[nm]['count'] == jss.get(nm, {}).get('count')
    verdict[nm] = {'match': same, 'py': pys[nm], 'js': jss.get(nm)}
ok = all(v['match'] for v in verdict.values())
print('VALUE PARITY:', 'PASS' if ok else 'FAIL')
json.dump({'verdict': 'PASS' if ok else 'FAIL', 'levels': verdict},
          open(OUT, 'w'), indent=1)
