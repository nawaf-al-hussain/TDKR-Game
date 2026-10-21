#!/usr/bin/env python3
"""s47 T1 step E: disassemble
 - CColladaFactory::createMaterial(db,driver,SMaterial*,root) @0x77713c
 - setMaterialParameter<CMaterial,SSetParam> sampler case @0x7891d0..0x7896xx
 - createMaterialRendererForProfile<GLES2> SNewParam sampler site @0x799e1c region
Goal: establish where the SSetParam/SNewParam VALUE arrays come from and what
the engine does with the {1,next,ff*16B,term} compiled blocks."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
f = open(SO, 'rb').read()
e_shoff = struct.unpack_from('<I', f, 0x20)[0]
e_shentsize = struct.unpack_from('<H', f, 0x2E)[0]
e_shnum = struct.unpack_from('<H', f, 0x30)[0]
e_shstrndx = struct.unpack_from('<H', f, 0x32)[0]
secs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from('<10I', f, off)
    secs.append(dict(name=name, typ=typ, addr=addr, offset=offset, size=size, link=link, entsize=entsize))
shstr = secs[e_shstrndx]
def cstr(base, n):
    end = f.index(b'\0', base + n)
    return f[base + n:end].decode('utf-8', 'replace')
for s in secs:
    s['nm'] = cstr(shstr['offset'], s['name'])
sec_by = {s['nm']: s for s in secs}
symtab = sec_by['.symtab']
strtab = secs[symtab['link']]
FUNC = {}
for i in range(symtab['size'] // 16):
    o = symtab['offset'] + i * 16
    nm, val, sz, info, oth = struct.unpack_from('<IIIBB', f, o)
    name = cstr(strtab['offset'], nm)
    if name:
        FUNC[val] = (sz, name)
text = sec_by['.text']

def disasm(fe, fsz, lo=None, hi=None, label=''):
    MODE = CS_MODE_THUMB if (fe & 1) else CS_MODE_ARM
    md = Cs(CS_ARCH_ARM, MODE)
    foff = text['offset'] + (fe - text['addr'])
    code = f[foff:foff + fsz]
    print(f'=== {label} @ {fe:#x} size {fsz:#x} mode {"T" if fe & 1 else "A"} ===')
    for ins in md.disasm(code, fe):
        if lo is not None and ins.address < lo:
            continue
        if hi is not None and ins.address > hi:
            break
        line = f'{ins.address:#09x}: {ins.mnemonic:8s} {ins.op_str}'
        if ins.mnemonic in ('bl', 'blx'):
            try:
                tgt = int(ins.op_str.lstrip('#'), 16)
                if tgt in FUNC:
                    line += f'  ; {FUNC[tgt][1][:95]}'
            except Exception:
                pass
        print(line)

# 1) CColladaFactory::createMaterial (300 B)
disasm(0x77713c, 300, label='CColladaFactory::createMaterial(SMaterial*)')
print()
# 2) setMaterialParameter sampler case region
disasm(0x7891d0, 0x500, lo=0x789440, hi=0x789660,
       label='setMaterialParameter<CMaterial,SSetParam> sampler case')
