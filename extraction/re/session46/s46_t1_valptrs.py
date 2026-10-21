#!/usr/bin/env python3
"""s46 T1: walk all 307 effect-instance nodes' setparam lists in the compiled
bdae; chase valptr1/valptr2 targets one dereference deep; hunt image-table
linkage (image triples @0x22a9c, 176 entries {name_ptr, dup, tga_ptr})."""
import io, zipfile, json, struct
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
N_BYTES = len(bres)
u32 = np.frombuffer(bres, '<u4', N_BYTES // 4)

def cstr(off, maxn=96):
    if not (0 < off < N_BYTES):
        return None
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > maxn:
        return None
    s = bres[off:e]
    try:
        t = s.decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

def in_file(v):
    return 0x1000 < v < N_BYTES

BASE, REC, N = 0x23308, 260, 307

# image table (s43/s45): 176 x 12 B triples {image_name_ptr, dup, tga_ptr} @0x22a9c
IMG_BASE, IMG_N = 0x22a9c, 176
images = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    images.append((int(w[0]), int(w[1]), int(w[2])))
img_name_set = {w[0] for w in images}
img_tga_set = {w[2] for w in images}

def which_image(v):
    """return image ordinal if v is an image name ptr or tga ptr"""
    for i, (nm, dup, tga) in enumerate(images):
        if v == nm:
            return ('name', i)
        if v == tga:
            return ('tga', i)
    return None

# ---- pass 0: full dump of nodes 70 and 73 to validate schema offsets ----
def dump_node(i):
    a = BASE + i * REC
    print(f'--- node {i} @ {a:#x} ---')
    for w in range(REC // 4):
        off = a + w * 4
        v = int(u32[off // 4])
        note = ''
        s = cstr(v)
        if s:
            note += f' -> {s!r}'
        elif in_file(v):
            note += ' (in-file)'
        print(f'  w{w:02d} @{off:#07x}: {v:#010x}{note}')

# ---- pass 1: auto-detect {ptr,cnt} list pairs whose entries are 24B params
#      with resolvable names ----
def detect_lists(i):
    a = BASE + i * REC
    ws = [int(u32[(a + k * 4) // 4]) for k in range(REC // 4)]
    found = []
    for j in range(REC // 4 - 1):
        ptr, cnt = ws[j], ws[j + 1]
        if in_file(ptr) and 1 <= cnt <= 16 and in_file(ptr + cnt * 24):
            ok = 0
            for e in range(cnt):
                ea = ptr + e * 24
                nm = cstr(int(u32[ea // 4]))
                if nm:
                    ok += 1
            if ok == cnt:
                found.append((j * 4, ptr, cnt))
    return found

if __name__ == '__main__':
    # ---- mass walk: setparam lists for all 307 nodes ----
    out = []
    v1_stats, v2_stats = {}, {}
    img_links = 0
    for i in range(N):
        a = BASE + i * REC
        ws = [int(u32[(a + k * 4) // 4]) for k in range(REC // 4)]
        sptr, scnt = ws[15], ws[16]
        node = {'i': i, 'effect': cstr(ws[63]), 'params': []}
        if not (in_file(sptr) and 0 <= scnt <= 16 and in_file(sptr + scnt * 24)):
            node['bad_setparam'] = [sptr, scnt]
            out.append(node)
            continue
        for e in range(scnt):
            ea = sptr + e * 24
            w = [int(u32[(ea + k * 4) // 4]) for k in range(6)]
            name = cstr(w[0])
            ent = {'name': name, 'type': w[1], 'a': w[2], 'b': w[3],
                   'v1': w[4], 'v2': w[5]}
            for key in ('v1', 'v2'):
                v = w[4] if key == 'v1' else w[5]
                stats = v1_stats if key == 'v1' else v2_stats
                stats[v] = stats.get(v, 0) + 1
                if in_file(v):
                    tgt = [int(u32[(v + k * 4) // 4]) for k in range(6)]
                    ent[key + '_words'] = tgt
                    strs = [s for s in (cstr(t) for t in tgt) if s]
                    if strs:
                        ent[key + '_strs'] = strs
                    # deref each target word once more for strings
                    d2 = []
                    for t in tgt:
                        if in_file(t):
                            s2 = cstr(t)
                            if s2:
                                d2.append(s2)
                            t2 = int(u32[t // 4])
                            if in_file(t2):
                                s3 = cstr(t2)
                                if s3:
                                    d2.append('1lvl:' + s3)
                    if d2:
                        ent[key + '_deref'] = d2
                    # image table linkage
                    links = []
                    for t in tgt:
                        r = which_image(t)
                        if r:
                            links.append(f'{r[0]}{r[1]}')
                    # also treat v itself as image link
                    r = which_image(v)
                    if r:
                        links.append(f'direct-{r[0]}{r[1]}')
                    if links:
                        ent['img_links'] = links
                        img_links += 1
            node['params'].append(ent)
        out.append(node)

    json.dump(out, open('/home/z/my-project/scripts/s46_t1_setparam_walk.json', 'w'), indent=1)

    print('nodes walked:', N, ' bad:', sum(1 for n in out if 'bad_setparam' in n))
    print('image-link hits:', img_links)
    print('top v1 values:', sorted(v1_stats.items(), key=lambda kv: -kv[1])[:8])
    print('top v2 values:', sorted(v2_stats.items(), key=lambda kv: -kv[1])[:8])
    print()
    for i in (73, 70, 2, 156, 145):
        n = out[i]
        print(f"node {i} effect={n['effect']!r}")
        for p in n['params']:
            print('   ', json.dumps(p)[:400])
    print()
    # type census
    from collections import Counter
    tc = Counter(p['type'] for n in out for p in n['params'])
    nc = Counter(p['name'] for n in out for p in n['params'])
    print('type census:', dict(tc))
    print('name census:', dict(list(nc.items())[:12]))
