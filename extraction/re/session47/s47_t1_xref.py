#!/usr/bin/env python3
"""s47 T1 step B: xrefs to setMaterialParameter / constructImage + the
collada-scene material-binding caller; CCustomColladaFactory vtable;
raw byte dump of node 73/302 setparam value blocks.
"""
import json, struct, sys, zipfile, io
import numpy as np

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
f = open(SO, 'rb').read()

# --- ELF sections ---
e_shoff = struct.unpack_from('<I', f, 0x20)[0]
e_shentsize = struct.unpack_from('<H', f, 0x2E)[0]
e_shnum = struct.unpack_from('<H', f, 0x30)[0]
e_shstrndx = struct.unpack_from('<H', f, 0x32)[0]
secs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from('<10I', f, off)
    secs.append(dict(name=name, typ=typ, flags=flags, addr=addr, offset=offset, size=size, link=link, entsize=entsize))
shstr = secs[e_shstrndx]
def cstr(base, n):
    end = f.index(b'\0', base + n)
    return f[base + n:end].decode('utf-8', 'replace')
for s in secs:
    s['nm'] = cstr(shstr['offset'], s['name'])
sec_by = {s['nm']: s for s in secs}

symtab = sec_by['.symtab']
strtab = secs[symtab['link']]
syms = {}
for i in range(symtab['size'] // 16):
    o = symtab['offset'] + i * 16
    nm, val, sz, info, oth = struct.unpack_from('<IIIBB', f, o)
    name = cstr(strtab['offset'], nm)
    if not name:
        continue
    syms.setdefault(val, []).append(name)

def find(name_sub, addr_only=False):
    out = []
    for a, names in syms.items():
        for n in names:
            if name_sub in n:
                out.append((hex(a), n))
    return sorted(out)

print('--- symbols: setMaterialParameter / constructImage / setParameter ---')
for a, n in find('setMaterialParameter')[:8]:
    print(' ', a, n)
for a, n in find('constructImage')[:8]:
    print(' ', a, n)
for a, n in find('CCustomColladaFactory')[:24]:
    print(' ', a, n)

print('--- vtable symbols ---')
for a, n in find('_ZTV')[:0] or []:
    pass
vt_syms = [(a, n) for a, names in syms.items() for n in names if n.startswith('_ZTV') and 'ColladaFactory' in n]
print(' ColladaFactory vtables:', [(hex(a), n) for a, n in vt_syms])

# --- .data.rel.ro / .data section for vtable content ---
def addr2off(addr):
    for s in secs:
        if s['typ'] != 8 and s['addr'] <= addr < s['addr'] + s['size'] and s['nm'] not in ('.symtab', '.strtab', '.shstrtab'):
            return s['offset'] + (addr - s['addr'])
    return None

for a, n in vt_syms:
    off = addr2off(a)
    if off is None:
        continue
    print(f'--- vtable {n} @ {a:#x} (file {off:#x}) ---')
    for k in range(40):
        v = struct.unpack_from('<I', f, off + k * 4)[0]
        names = syms.get(v)
        print(f'  slot {k:2d}: {v:#010x} {names[:1] if names else ""}')

# --- xrefs: scan .text for bl to targets ---
text = sec_by['.text']
TARGETS = {}
for a, names in syms.items():
    for n in names:
        if n in ('_ZN7glitch6collada16CColladaDatabase19setMaterialParameterEPNS_5video11IVideoDriverEPNS_6scene14ISceneNodeEPNS_10CMaterialsERKNS_9SSetParamE',):
            TARGETS[a] = n
# fallback: exact addresses from s46
TARGETS.setdefault(0x7891d0, 'setMaterialParameter@0x7891d0')
TARGETS.setdefault(0x7bd5fc, 'constructImage@0x7bd5fc')
TARGETS.setdefault(0x7bd0ec, 'constructMaterial@0x7bd0ec')
TARGETS.setdefault(0x7bd1bc, 'constructMaterial@0x7bd1bc')

# bl encoding: F000F800-ish; scan
bl_sites = {}
tvals = set(TARGETS)
base, size = text['addr'], text['size']
t_off = text['offset']
words = np.frombuffer(f[t_off:t_off + size], '<u4', size // 4)
for k in range(len(words)):
    w = int(words[k])
    if (w & 0x0F000000) == 0x0B000000 and (w & 0xF0000000) != 0xF0000000:
        imm = w & 0x00FFFFFF
        if imm & 0x800000:
            imm -= 0x1000000
        pc = base + k * 4 + 8
        tgt = pc + imm * 4
        if tgt in tvals:
            bl_sites.setdefault(tgt, []).append(pc)
for tgt, sites in sorted(bl_sites.items()):
    print(f'xrefs to {TARGETS[tgt]} ({tgt:#x}): {len(sites)}')
    for s in sites[:20]:
        print(f'   from {s:#x}')
