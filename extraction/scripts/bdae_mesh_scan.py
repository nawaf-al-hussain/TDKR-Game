#!/usr/bin/env python3
"""BDAE mesh scanner — locates vertex streams in the geometry section, decodes
positions + octahedral s16 normals, finds index buffers, renders verification plots.

Working model (from GC_Prop_Tree_07_S_Collision + Batarang):
  geometry section base G = header h[10].
  geo header u32s at G: [A, B, 0x5C, 0x4C, 0xA8, 0x40, 0x34, 0x28, 0x1C, 0x10,
                         1, COUNT, 3, 0x4C, 3, 0x50, 3, 0x54, 3, 0x58, 3, 0x5C,
                         0x7C, 0, 1, REGION]
  vertex stream ends at G+B (B verified on tree & batarang), contains COUNT entries
  of S bytes: [pos f32 x3][packed dwords...] (S auto-detected: 12..48).
  packed dword pair = 2 x s16 octahedral normal (0x7FFFFFFF -> (0.5,0.5) -> +Z).
  after stream: metadata (counts, 'Solid' for collision, u16 index list).
"""
import struct, sys, os
import numpy as np

BASE = '/home/z/my-project/download/TDKR_assets/raw'

def oct_decode(u1, u2):
    """octahedral s16 pair -> unit normal"""
    def s16(v):
        return v - 65536 if v >= 32768 else v
    u, v = s16(u1) / 32767.0, s16(u2) / 32767.0
    nx, ny = u, v
    nz = 1.0 - abs(nx) - abs(ny)
    if nz < 0:
        x, y = nx, ny
        nx = (1 - abs(y)) * (1 if x >= 0 else -1)
        ny = (1 - abs(x)) * (1 if y >= 0 else -1)
        nz = -nz  # keep sign
    n = np.array([nx, ny, nz])
    m = np.linalg.norm(n)
    return n / m if m > 0 else n

def plausible(x):
    return abs(x) < 1e4 and (x == 0.0 or 1e-7 < abs(x) < 1e7)

def find_streams(d, geo_base, tag):
    """Auto-detect vertex streams: walk back from candidate ends."""
    results = []
    return results

def analyze(path, out_png=None):
    d = open(path, 'rb').read()
    h = struct.unpack_from('<14I', d, 0)
    G = h[10]
    f = struct.unpack_from('<26I', d, G)
    print(f'== {os.path.basename(path)} size={len(d):#x} geo@{G:#x}')
    print(f'   geo fields: {[hex(x) for x in f[:8]]} ... count={f[11]:#x} region={f[25]:#x}')
    B = f[1]; COUNT = f[11]; REGION = f[25]
    end = G + B
    print(f'   stream end = {end:#x}, count={COUNT}')
    # brute force stride + start: try strides, walk back from end
    best = None
    for S in range(12, 52, 4):
        start = end - COUNT * S
        if start <= G + 0x40:
            continue
        # score: fraction of entries whose 3 f32s are position-plausible
        ok = 0
        for i in range(min(COUNT, 400)):
            x, y, z = struct.unpack_from('<3f', d, start + i * S)
            if plausible(x) and plausible(y) and plausible(z):
                ok += 1
        score = ok / min(COUNT, 400)
        if not best or score > best[0]:
            best = (score, S, start)
    score, S, start = best
    print(f'   best stride={S} start={start:#x} plausibility={score:.3f}')
    if score < 0.5:
        print('   !! low plausibility, aborting this file')
        return
    # extract positions + packed
    pos = np.zeros((COUNT, 3), np.float32)
    pk = np.zeros((COUNT, 2), np.int64)
    for i in range(COUNT):
        off = start + i * S
        pos[i] = struct.unpack_from('<3f', d, off)
        pk[i, 0], pk[i, 1] = struct.unpack_from('<2I', d, off + 12)
    mn, mx = pos.min(0), pos.max(0)
    print(f'   pos bounds: min={mn.round(4)} max={mx.round(4)}')
    # AABB cross-check: 6 floats shortly before stream (AABB at start-0x70..start)
    for back in range(0x10, 0xC0, 4):
        v = struct.unpack_from('<6f', d, start - back)
        if all(plausible(x) for x in v):
            amin, amax = np.array(v[:3], np.float32), np.array(v[3:], np.float32)
            if np.all(amin <= mx + 1e-3) and np.all(amin >= mn - 5e-2) and \
               np.all(amax >= mn - 1e-3) and np.all(amax <= mx + 5e-2):
                print(f'   AABB @ {start-back:#x}: min={amin.round(4)} max={amax.round(4)} MATCH')
                break
    # normals sample
    norms = [oct_decode(*pk[i]) for i in range(0, min(COUNT, 8))]
    print('   oct-normals sample:', np.round(norms, 2).tolist())
    # index buffer hunt after stream: u16 runs with values < COUNT
    idx_off = None
    for off in range(end, min(end + 0x400, len(d) - 1), 2):
        seq = struct.unpack_from(f'<{min(24, (len(d)-off)//2)}H', d, off)
        if len(seq) >= 12 and all(v < COUNT for v in seq[:12]) and sum(seq[:12]) > 0:
            idx_off = off
            break
    if idx_off:
        seq = struct.unpack_from(f'<{min(72,(len(d)-idx_off)//2)}H', d, idx_off)
        print(f'   u16 index candidates @ {idx_off:#x}: {list(seq[:24])}')
    # plot
    if out_png:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.font_manager as fm
        for fp in ('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf',
                   '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
            try: fm.fontManager.addfont(fp)
            except Exception: pass
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
        fig = plt.figure(figsize=(14, 6), constrained_layout=True)
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.scatter(pos[:, 0], pos[:, 2], pos[:, 1], s=6, c=pos[:, 1], cmap='viridis')
        ax1.set_xlabel('X'); ax1.set_ylabel('Z'); ax1.set_zlabel('Y')
        ax1.set_title(f'{os.path.basename(path)} — {COUNT} verts')
        ax2 = fig.add_subplot(122, projection='3d')
        if idx_off:
            idx = list(struct.unpack_from(f'<{min(900,(len(d)-idx_off)//2)}H', d, idx_off))
            tris = np.array(idx[:len(idx)//3*3]).reshape(-1, 3)
            for t in tris[:200]:
                p = pos[t][:, [0, 2, 1]]
                ax2.plot(p[:, 0], p[:, 1], p[:, 2], 'b-', lw=0.5, alpha=0.6)
        ax2.scatter(pos[:, 0], pos[:, 2], pos[:, 1], s=4, c='r')
        ax2.set_title('wireframe (if indices found)')
        fig.savefig(out_png, dpi=110)
        plt.close(fig)
        print(f'   plot -> {out_png}')

if __name__ == '__main__':
    files = sys.argv[1:] or [
        f'{BASE}/actors/Batarang.bdae.bin',
        f'{BASE}/l_gothamcity/GC_Prop_Tree_07_S_Collision.bdae.bin',
    ]
    os.makedirs('/home/z/my-project/download/TDKR_assets/probe/meshes', exist_ok=True)
    for p in files:
        name = os.path.basename(p).replace('.bdae.bin', '')
        analyze(p, f'/home/z/my-project/download/TDKR_assets/probe/meshes/{name}_scan.png')
        print()
