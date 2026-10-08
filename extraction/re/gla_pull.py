#!/usr/bin/env python3
"""Pull chunks out of a .gla container by name (session 6 restore helper)."""
import struct, sys, os

def entries(path):
    d = open(path, 'rb').read(16)
    _, idx_size, table_bytes, n = struct.unpack('>IIII', d)
    f = open(path, 'rb')
    f.seek(16)
    tbl = f.read(n * 16)
    pool_start = 16 + n * 16
    f.seek(pool_start)
    pool = f.read(idx_size - pool_start)
    out = {}
    for i in range(n):
        off, sz, name_off, _ = struct.unpack('>IIII', tbl[i*16:(i+1)*16])
        end = pool.find(b'\x00', name_off)
        out[pool[name_off:end].decode('latin1', 'replace')] = (off, sz)
    return f, out

def pull(gla, wanted, outdir):
    f, ents = entries(gla)
    os.makedirs(outdir, exist_ok=True)
    got = 0
    for name, (off, sz) in sorted(ents.items()):
        if wanted and not any(w.lower() in name.lower() for w in wanted):
            continue
        f.seek(off)
        data = f.read(sz)
        open(os.path.join(outdir, name), 'wb').write(data)
        got += 1
    print(f'{gla}: pulled {got}/{len(ents)} chunks -> {outdir}')

if __name__ == '__main__':
    gla = sys.argv[1]
    wanted = sys.argv[3:] if len(sys.argv) > 3 else []
    pull(gla, wanted, sys.argv[2])
