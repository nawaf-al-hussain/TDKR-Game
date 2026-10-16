#!/usr/bin/env python3
"""S29: vtable -> RTTI name, correct segment mapping; then disassemble clsid_fns."""
import json, struct
from elftools.elf.elffile import ELFFile

SO = '/tmp/my-project/work/re29/libKRHP.so'
f = open(SO, 'rb'); elf = ELFFile(f)
segs = [(s['p_vaddr'], s['p_memsz'], s['p_offset'], s['p_filesz']) for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']

def v2o(v):
    for va, msz, off, fsz in segs:
        if va <= v < va + msz: return off + (v - va)
    return None
def rd(v, n):
    o = v2o(v)
    if o is None: return None
    f.seek(o); return f.read(n)
def u32(v):
    b = rd(v, 4); return struct.unpack('<I', b)[0] if b else None
def cstr(v, m=160):
    b = rd(v, m)
    if b is None: return None
    z = b.find(b'\0')
    return b[:z if z >= 0 else m].decode('latin1')

vt = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session24/vtable_classes.json'))
out = {}
for clsid, info in vt.items():
    vtoff = int(info['vtable_file'], 16)          # FILE offset (session 24 name)
    vaddr = vtoff if vtoff < 0xbbe1ec else vtoff + 0x1000  # second LOAD delta +0x1000
    ti = u32(vaddr - 4)
    name = None
    if ti and 0x1000 < ti < 0xc12838:
        nptr = u32(ti + 4)
        if nptr and 0xac2490 <= nptr < 0xbbf930:  # name should live in .rodata
            s = cstr(nptr)
            if s and any(c.isalpha() for c in s[:4]): name = s
    out[clsid] = {'name': name, 'ti': hex(ti) if ti else None, 'vaddr': hex(vaddr),
                  'clsid_fn': info.get('clsid_fn'), 'load': info.get('load'), 'vslots': info.get('vslots')}
json.dump(out, open('/tmp/my-project/work/re29/vtable_names.json', 'w'), indent=1)
named = {k: v for k, v in out.items() if v['name']}
print('named vtables:', len(named), '/', len(out))
# demangle-ish: strip leading digits
for k, v in sorted(named.items(), key=lambda kv: kv[1]['name']):
    n = v['name']
    i = 0
    while i < len(n) and n[i].isdigit(): i += 1
    v['cls'] = n[i:]
    print(f"  id {k:>12s}  {v['cls']:<40s} clsid_fn {v['clsid_fn']}  load {v['load']}")
json.dump({k: v.get('cls') for k, v in named.items()}, open('/tmp/my-project/work/re29/clsid_names.json', 'w'), indent=1)
