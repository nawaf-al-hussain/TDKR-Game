#!/usr/bin/env python3
"""s47 T1 step D: xrefs to constructImage(by-name 0x7bd4f0 / by-index
0x7bd428 / by-SImage 0x7bd5fc), and enclosing functions of each caller —
find the engine systems that resolve images at runtime."""
import struct
import numpy as np

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
FUNC = []
for i in range(symtab['size'] // 16):
    o = symtab['offset'] + i * 16
    nm, val, sz, info, oth = struct.unpack_from('<IIIBB', f, o)
    if info & 0x0F != 2:
        continue
    name = cstr(strtab['offset'], nm)
    if name:
        FUNC.append((val, sz, name))
FUNC.sort()

def enclosing(addr):
    for val, sz, name in FUNC:
        if val <= addr < val + max(sz, 4):
            return name
    return '?'

text = sec_by['.text']
t_off = text['offset']
words = np.frombuffer(f[t_off:t_off + text['size']], '<u4', text['size'] // 4)

def xrefs(target):
    out = []
    for k in range(len(words)):
        w = int(words[k])
        if (w & 0x0F000000) == 0x0B000000 and (w & 0xF0000000) != 0xF0000000:
            imm = w & 0x00FFFFFF
            if imm & 0x800000:
                imm -= 0x1000000
            pc = text['addr'] + k * 4 + 8
            if pc + imm * 4 == target:
                out.append(pc)
    return out

NAMES = {
    0x7bd428: 'constructImage(driver,int)',
    0x7bd4f0: 'constructImage(driver,const char*)',
    0x7bd5fc: 'constructImage(driver,SImage*)',
    0x7bd0ec: 'constructMaterial(driver,u16,...)',
    0x7bd1bc: 'constructMaterial(driver,SMaterial*,...)',
    0x7891d0: 'setMaterialParameter<CMaterial,SSetParam>',
    0x78c44c: 'setMaterialParameter<CMaterialRenderer,SNewParam>',
    0x43d52c: 'CCustomColladaFactory::createImage',
    0x776828: 'collada::createMaterial(free fn)',
}
for tgt, nm in NAMES.items():
    sites = xrefs(tgt)
    print(f'{nm} @{tgt:#x}: {len(sites)} xrefs')
    seen = set()
    for s in sites:
        en = enclosing(s)
        if en in seen:
            continue
        seen.add(en)
        print(f'   {s:#x} in {en[:110]}')
