#!/usr/bin/env python3
"""Add --grad mode to s50_t1_pyref.py: diffuse replaced by the same UV gradient."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_pyref.py'
s = open(p).read()
import ast
if '--grad' not in s:
    old = "ap.add_argument('--bbox', default=None, help='x0,z0,x1,z1 camera override')"
    new = old + "\nap.add_argument('--grad', action='store_true', help='diffuse = UV gradient (r=tx*2, g=ty*2)')"
    assert old in s, 'arg anchor'
    s = s.replace(old, new, 1)
    old2 = "        tx = np.clip((uu * T).astype(np.int64) % T, 0, T - 1)\n        ty = np.clip((vv * TH_).astype(np.int64) % TH_, 0, TH_ - 1)\n        col = tex['rgb'][ty, tx].astype(np.float32)"
    new2 = ("        tx = np.clip((uu * T).astype(np.int64) % T, 0, T - 1)\n"
            "        ty = np.clip((vv * TH_).astype(np.int64) % TH_, 0, TH_ - 1)\n"
            "        if args.grad:\n"
            "            col = np.stack([np.clip(tx * 2, 0, 255), np.clip(ty * 2, 0, 255),\n"
            "                            np.zeros_like(tx)], axis=-1).astype(np.float32)\n"
            "        else:\n"
            "            col = tex['rgb'][ty, tx].astype(np.float32)")
    assert old2 in s, 'sample anchor'
    s = s.replace(old2, new2, 1)
    open(p, 'w').write(s)
    print('pyref --grad added')
else:
    print('already present')
ast.parse(open(p).read())
print('syntax OK')
