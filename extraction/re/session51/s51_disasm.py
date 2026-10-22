#!/usr/bin/env python3
"""s51 T1: disassemble engine sampler-state functions from libKRHP.so (static)."""
import sys, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
data = open(SO, 'rb').read()

# program headers -> map vaddr to file offset
e_phoff = struct.unpack_from('<I', data, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', data, 0x2a)[0]
e_phnum = struct.unpack_from('<H', data, 0x2c)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz, p_memsz = struct.unpack_from('<6I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, fsz in segs:
        if va <= v < va + fsz:
            return off + (v - va)
    raise ValueError('vaddr not mapped: 0x%x' % v)

def disas(vaddr, size):
    off = v2o(vaddr)
    code = data[off:off + size]
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = False
    out = []
    for ins in md.disasm(code, vaddr):
        out.append('0x%08x  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
    return '\n'.join(out)

def findsym(substr):
    import re
    txt = subprocess.run(['readelf', '-sW', SO], capture_output=True, text=True).stdout
    res = []
    for line in txt.splitlines():
        if substr in line:
            parts = line.split()
            # num value size type bind vis ndx name
            res.append((parts[1], int(parts[1], 16), int(parts[2]), parts[7] if len(parts) > 7 else line))
    return res

if __name__ == '__main__':
    import subprocess
    funcs = {
        'applyTextureSampler': (0x78c320, 128),
        'CCustomColladaFactory::getSamplerState': (0x43d504, 40),
        'CCustomTexturePolicy::useOnlyOneMipmap': (0x444c84, 312),
        'CCustomTexturePolicy::getMipmapCountToSkip': (0x444a54, 560),
        'CCustomTexturePolicy::getMipmapCountForSubstitute': (0x444ea0, 96),
        'ITexturePolicy::getMipmapNumberForSubstitute': (0x459b9c, 8),
    }
    name = sys.argv[1] if len(sys.argv) > 1 else None
    for n, (va, sz) in funcs.items():
        if name and name not in n:
            continue
        print('=== %s @0x%x (%d B) ===' % (n, va, sz))
        try:
            print(disas(va, sz))
        except Exception as e:
            print('ERR', e)
        print()
