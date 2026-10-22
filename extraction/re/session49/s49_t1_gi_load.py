#!/usr/bin/env python3
"""s49 T1d: CComponentBaseGlobalIllum::Load (940 B) — the GI record fields (fog params)."""
import subprocess, re
import capstone
d = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
out = subprocess.run(['readelf','-sW','/tmp/my-project/work/re29/libKRHP.so'],
                     capture_output=True, text=True).stdout
syms = {}
for ln in out.splitlines():
    m = re.match(r'\s*\d+:\s+([0-9a-f]+)\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(\S+)', ln)
    if m:
        syms[m.group(3)] = (int(m.group(1),16), int(m.group(2)))
md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
v, sz = syms['_ZN25CComponentBaseGlobalIllum4LoadEP13CMemoryStream']
code = d[v:v+sz]
print('===', hex(v), 'size', sz)
n = 0
for ins in md.disasm(code, v):
    print(f'{ins.address:#x}  {ins.mnemonic}\t{ins.op_str}')
    n += 1
    if n > 400: break
