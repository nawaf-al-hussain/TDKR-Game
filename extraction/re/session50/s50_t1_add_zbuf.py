#!/usr/bin/env python3
"""Add --zbuf (depth-buffer, engine-semantics) reference mode to s50_t1_pyref.py."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_pyref.py'
s = open(p).read()

old = "ap.add_argument('--lmonly', action='store_true')"
new = ("ap.add_argument('--lmonly', action='store_true')\n"
       "ap.add_argument('--zbuf', action='store_true', help='depth-buffer reference (engine semantics)')")
assert old in s, 'arg anchor'
s = s.replace(old, new)

old2 = """zm_cat = np.concatenate([o[0] for o in order])
si_cat = np.concatenate([o[1] for o in order])
ti_cat = np.concatenate([o[2] for o in order])
painter = np.lexsort((ti_cat, si_cat, zm_cat))
si_cat = si_cat[painter]
ti_cat = ti_cat[painter]
print('total triangles:', len(zm_cat), 'painter built at %.1f s' % (time.time() - t_start))"""
new2 = """zm_cat = np.concatenate([o[0] for o in order])
si_cat = np.concatenate([o[1] for o in order])
ti_cat = np.concatenate([o[2] for o in order])
if args.zbuf:
    mat_hm = {}
    mat_cnt = {}
    for s2 in segdata:
        if not s2['draw']:
            continue
        raw2 = np.frombuffer(ld, np.uint8, s2['vb'], s2['off']).reshape(s2['nv'], s2['stride'])
        h2v = raw2[:, 8:12].copy().view('<f4').reshape(-1).astype(np.float64)
        mat_hm[s2['mat']] = mat_hm.get(s2['mat'], 0.0) + float(h2v.sum())
        mat_cnt[s2['mat']] = mat_cnt.get(s2['mat'], 0) + s2['nv']
    for m2 in mat_hm:
        mat_hm[m2] /= max(mat_cnt[m2], 1)
    seg_order = sorted(range(len(meta)), key=lambda i2: (mat_hm[meta[i2]['mat']], meta[i2]['mat']))
    si_cat = np.concatenate([np.full(len(tris_all[i2][3]), i2, np.int32) for i2 in seg_order])
    ti_cat = np.concatenate([np.arange(len(tris_all[i2][3]), dtype=np.int32) for i2 in seg_order])
    print('total triangles:', len(si_cat), 'GL batch order built at %.1f s' % (time.time() - t_start))
else:
    painter = np.lexsort((ti_cat, si_cat, zm_cat))
    si_cat = si_cat[painter]
    ti_cat = ti_cat[painter]
    print('total triangles:', len(zm_cat), 'painter built at %.1f s' % (time.time() - t_start))"""
assert old2 in s, 'sort anchor'
s = s.replace(old2, new2)

old3 = """    region = img[ylo:yhi + 1, xlo:xhi + 1]
    img[ylo:yhi + 1, xlo:xhi + 1] = np.where(mask[..., None], col, region)
    batches += 1"""
new3 = """    region = img[ylo:yhi + 1, xlo:xhi + 1]
    if args.zbuf:
        zregion = zbuf[ylo:yhi + 1, xlo:xhi + 1]
        hf = w0 * pos[i0, 2] + w1 * pos[i1, 2] + w2 * pos[i2, 2]
        clipz = -2.0 / 350.0 * hf + 150.0 / 350.0
        zw = mask & (clipz <= zregion)
        zregion[zw] = clipz[zw]
        img[ylo:yhi + 1, xlo:xhi + 1] = np.where(zw[..., None], col, region)
    else:
        img[ylo:yhi + 1, xlo:xhi + 1] = np.where(mask[..., None], col, region)
    batches += 1"""
assert old3 in s, 'write anchor'
s = s.replace(old3, new3)

old4 = "img = np.zeros((H, W, 3), np.float32)\nt_r0 = time.time()"
new4 = ("img = np.zeros((H, W, 3), np.float32)\n"
        "zbuf = np.full((H, W), 1.0, np.float64) if args.zbuf else None\n"
        "t_r0 = time.time()")
assert old4 in s, 'img anchor'
s = s.replace(old4, new4)

open(p, 'w').write(s)
print('zbuf reference mode added')
