#!/usr/bin/env python3
"""Extract symbol table (all symtab sections) from libKRHP.so -> JSON.
Usage: so_symbols.py [path-to-so] [out-json]
"""
import struct, json, sys

SO = sys.argv[1] if len(sys.argv) > 1 else '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/home/z/my-project/work/so_syms.json'

f = open(SO, 'rb').read()
e_shoff = struct.unpack_from('<I', f, 0x20)[0]
e_shentsize = struct.unpack_from('<H', f, 0x2E)[0]
e_shnum = struct.unpack_from('<H', f, 0x30)[0]
e_shstrndx = struct.unpack_from('<H', f, 0x32)[0]
secs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from('<10I', f, off)
    secs.append(dict(name=name, typ=typ, addr=addr, offset=offset, size=size,
                     link=link, entsize=entsize))
shstr = secs[e_shstrndx]

def cstr(base, n):
    end = f.index(b'\0', base + n)
    return f[base + n:end].decode('utf-8', 'replace')

for s in secs:
    s['nm'] = cstr(shstr['offset'], s['name'])

syms = {}   # addr -> [names]
addr_of = {}  # name -> addr (first wins)
for i, s in enumerate(secs):
    if 'symtab' not in s['nm'] or s['entsize'] == 0:
        continue
    strsec = secs[s['link']]
    n = s['size'] // s['entsize']
    for j in range(n):
        off = s['offset'] + j * s['entsize']
        nm, val, sz, info, other, shndx = struct.unpack_from('<IIIBBH', f, off)
        if not nm or not val:
            continue
        name = cstr(strsec['offset'], nm)
        syms.setdefault(val, []).append(name)
        addr_of.setdefault(name, val)

print(f'sections: {len(secs)}, unique symbol addrs: {len(syms)}, names: {len(addr_of)}')
json.dump({'by_addr': {hex(k): v for k, v in syms.items()},
           'by_name': {k: hex(v) for k, v in addr_of.items()}},
          open(OUT, 'w'))
print('wrote', OUT)

# quick lookups
for pat in ['CMemoryStream', 'ReadString', 'ReadInt', 'ReadFloat', 'ReadByte', 'ReadChar']:
    hits = {k: v for k, v in addr_of.items() if pat in k}
    print(f'--- {pat}: {len(hits)}')
    for k in sorted(hits)[:24]:
        print(f'  0x{hits[k]:06x} {k}')
