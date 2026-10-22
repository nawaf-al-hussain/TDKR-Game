#!/usr/bin/env python3
"""s49 T1d: CPostProcessEffect_ColorCorrection ctor + InitTexture — which FS/LUT path."""
import subprocess, re
import capstone
d = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
out = subprocess.run(['readelf','-sW','/tmp/my-project/work/re29/libKRHP.so'],
                     capture_output=True, text=True).stdout
syms = {}
for ln in out.splitlines():
    m = re.match(r'\s*\d+:\s+([0-9a-f]+)\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(\S+)', ln)
    if m: syms[m.group(3)] = (int(m.group(1),16), int(m.group(2)))
md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
for name in ['_ZN34CPostProcessEffect_ColorCorrectionC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager',
             '_ZN19CPostProcessManager21ReinitColorCorrectionEv',
             '_ZN34CPostProcessEffect_ColorCorrection11InitTextureEPKc']:
    if name not in syms:
        cands = [k for k in syms if 'ColorCorrection' in k]
        print('missing; cands:', cands); continue
    v, sz = syms[name]
    print('='*20, name, hex(v), sz)
    n = 0
    for ins in md.disasm(d[v:v+sz], v):
        print(f'{ins.address:#x}  {ins.mnemonic}\t{ins.op_str}')
        n += 1
        if n > 150: break
