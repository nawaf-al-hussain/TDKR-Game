#!/usr/bin/env python3
"""s49 T1d v3: precise Thumb disasm of CWeatherManager fog path (symbol + size)."""
import subprocess, re, struct
import capstone

d = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()
# symbol table via readelf
out = subprocess.run(['readelf', '-sW', '/tmp/my-project/work/re29/libKRHP.so'],
                     capture_output=True, text=True).stdout
syms = {}
for ln in out.splitlines():
    m = re.match(r'\s*\d+:\s+([0-9a-f]+)\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(\S+)', ln)
    if m and ('WeatherManager' in m.group(3) or 'TemplateLevelProperties' in m.group(3)):
        syms[m.group(3)] = (int(m.group(1), 16), int(m.group(2)))
print('found:', list(syms)[:6], '...')

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
def dis(name, n=None):
    v, sz = syms[name]
    code = d[v: v + sz]
    print('='*25, name, hex(v), 'size', sz)
    for i, ins in enumerate(md.disasm(code, v)):
        print(f'{ins.address:#x}  {ins.mnemonic}\t{ins.op_str}')
        if n and i + 1 >= n: break

for fn in ['_ZN24CTemplateLevelProperties4LoadEP13CMemoryStream',
           '_ZN15CWeatherManagerC2EP24CTemplateLevelProperties',
           '_ZN15CWeatherManager25ApplyIlluminationSettingsEv']:
    pass
for fn in ['_ZN15CWeatherManager11SetFogColorERKN6glitch4core8vector4dIfEE',
           '_ZN15CWeatherManager11SetFogColorERKN6glitch5video6SColorE',
           '_ZN15CWeatherManager14SetFogDistanceEff',
           '_ZN15CWeatherManager5ResetEv',
           '_ZN15CWeatherManagerC2EP24CTemplateLevelProperties']:
    dis(fn)

print('\n' + '='*30 + ' extras')
for fn in ['_ZN24CTemplateLevelProperties4LoadEP13CMemoryStream',
           '_ZN15CWeatherManager25ApplyIlluminationSettingsEv']:
    dis(fn)

for fn in ['_ZN15CWeatherManager4LoadEP13CMemoryStream',
           '_ZN15CWeatherManager4SaveEP13CMemoryStream',
           '_ZN15CWeatherManager4InitEv',
           '_ZN15CWeatherManager22LoadGlobalIlluminationEP13CMemoryStream']:
    dis(fn)
