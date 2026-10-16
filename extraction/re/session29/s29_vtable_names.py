#!/usr/bin/env python3
"""S29 T1 step 1: map vtables -> RTTI class names -> clsid_fn; disassemble clsid_fns."""
import json, struct, sys
from elftools.elf.elffile import ELFFile

SO = '/tmp/my-project/work/re29/libKRHP.so'
f = open(SO, 'rb')
elf = ELFFile(f)

# build (vaddr -> file offset) via program headers (this .so is loaded as-is typically)
segs = []
for seg in elf.iter_segments():
    if seg['p_type'] == 'PT_LOAD':
        segs.append((seg['p_vaddr'], seg['p_memsz'], seg['p_offset'], seg['p_filesz']))

def v2o(v):
    for va, msz, off, fsz in segs:
        if va <= v < va + msz:
            return off + (v - va)
    return None

def o2v(o):
    for va, msz, off, fsz in segs:
        if off <= o < off + fsz:
            return va + (o - off)
    return None

def rd(v, n):
    o = v2o(v)
    if o is None: return None
    f.seek(o)
    return f.read(n)

def u32(v):
    b = rd(v, 4)
    return struct.unpack('<I', b)[0] if b else None

def cstr(v, maxlen=128):
    b = rd(v, maxlen)
    if b is None: return None
    z = b.find(b'\0')
    return b[:z if z >= 0 else maxlen].decode('latin1')

print('ELF entry', hex(elf.header.e_entry), 'machine', elf.header.e_machine)

# collect typeinfo names: scan .data.rel.ro / .data for vtables? Simpler: find all "NNNClassName" mangled strings in .rodata
# and build typeinfo candidates: a typeinfo object layout: [vptr_to_typeinfo_class][name_ptr]... 
# Instead: for each vtable in vtable_classes.json, read word at vtable-4 -> typeinfo object; read name at ti+4.
vt = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session24/vtable_classes.json'))
out = {}
for clsid, info in vt.items():
    vtoff = int(info['vtable_file'], 16)
    vaddr = o2v(vtoff)
    if vaddr is None:
        vaddr = vtoff  # maybe it was a vaddr already
    ti = u32(vaddr - 4)
    name = None
    if ti:
        nptr = u32(ti + 4)
        if nptr: name = cstr(nptr)
    out[clsid] = {'name': name, 'ti': hex(ti) if ti else None, 'vaddr': hex(vaddr),
                  'clsid_fn': info.get('clsid_fn'), 'load': info.get('load')}
json.dump(out, open('/tmp/my-project/work/re29/vtable_names.json', 'w'), indent=1)
named = {k: v for k, v in out.items() if v['name']}
print('named vtables:', len(named), '/', len(out))
for k in list(named)[:15]:
    print(k, named[k]['name'], 'clsid_fn', named[k]['clsid_fn'])
