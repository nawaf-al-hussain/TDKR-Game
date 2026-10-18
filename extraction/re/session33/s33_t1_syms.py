#!/usr/bin/env python3
"""S33 T1: parse ELF symtab of libKRHP.so; find glitch animation symbols."""
import struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()

def sections(d):
    e_shoff = struct.unpack_from('<I', d, 0x20)[0]
    e_shentsize = struct.unpack_from('<H', d, 0x2e)[0]
    e_shnum = struct.unpack_from('<H', d, 0x30)[0]
    e_shstrndx = struct.unpack_from('<H', d, 0x32)[0]
    secs = []
    for i in range(e_shnum):
        o = e_shoff + i * e_shentsize
        name, typ, flags, addr, off, size, link, info, align, entsize = struct.unpack_from('<10I', d, o)
        secs.append(dict(name_off=name, typ=typ, addr=addr, off=off, size=size, link=link, entsize=entsize))
    stro = secs[e_shstrndx]['off']
    for s in secs:
        e = d.find(b'\0', stro + s['name_off'])
        s['name'] = d[stro + s['name_off']:e].decode('latin1')
    return secs

secs = sections(d)
for s in secs:
    if s['typ'] in (2, 11):  # SYMTAB, DYNSYM
        print(f"section {s['name']} off 0x{s['off']:x} size 0x{s['size']:x} entsize {s['entsize']} link {s['link']}")
        stro = secs[s['link']]['off']
        n = s['size'] // 16
        syms = []
        for i in range(n):
            o = s['off'] + i * 16
            nameoff, value, size, info, other, shndx = struct.unpack_from('<IIIBBH', d, o)
            if not nameoff: continue
            e = d.find(b'\0', stro + nameoff)
            nm = d[stro + nameoff:e].decode('latin1')
            if value: syms.append((value, size, nm))
        print(f'  {len(syms)} named symbols')
        import pickle
        pickle.dump(syms, open(f'/tmp/my-project/scripts/s33_syms_{s["name"]}.pkl', 'wb'))

# now search
import pickle
for fn in ('/tmp/my-project/scripts/s33_syms_.symtab.pkl', '/tmp/my-project/scripts/s33_syms_.dynsym.pkl'):
    try:
        syms = pickle.load(open(fn, 'rb'))
    except Exception:
        continue
    print(f'\n== {fn}: {len(syms)} syms')
    hits = [s for s in syms if 'Animation' in s[2] and ('glitch' in s[2])]
    print(f'animation+glitch symbols: {len(hits)}')
    for v, sz, nm in sorted(set(hits))[:60]:
        print(f'  0x{v:08x} sz={sz:5d} {nm[:110]}')
