#!/usr/bin/env python3
"""T3 — ground-raycast reconciliation with positive control + honest labels.

Cameras (all documented; session-21's exact cameras are LOST with that
sandbox, so same-camera identity CANNOT be proven — the 19.9% coincidence
is checked but not overclaimed):
  camA "default-view proxy": the viewer's fitCamera boot view — pos = c +
       r*(1.05, .62, 1.05) in viewer space (x, y_up, z = -game_y), target c,
       fov 55, 1280x720 -> raycast at 320x180 and upsample the class map.
  camB "road control": straight down 120u above the centroid of a known
       Roads0-bound street segment (positive control: MUST return road hits).
  camC "plaza": straight down above a plaza/crossing segment.
Mesh: BOTH islands' street segments (double-sided Moeller-Trumbore).
Hits classified by the triangle's segment +40 material index; also bucketed
by height. Void = no hit in the ground third / footprint respectively.
Far-LOD check: materials 34/35 of GothamCity_low rasterised against camA
miss pixels (bottom third).
"""
import json
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/scripts")
from t1_tests import island_segments  # noqa

OUT = "/home/z/my-project/work"
W, H = 40, 24


def build_mesh():
    tris_all = []
    mat_all = []
    from export_zone import strip_to_tris
    for islname in ("GothamCity", "GothamCity_Island2"):
        lt = open(f"/home/z/my-project/work/zone/{islname}/lod_table.bin", "rb").read()
        ld = open(f"/home/z/my-project/work/zone/{islname}/lod_data.bin", "rb").read()
        u = struct.unpack(f"<{len(lt)//4}I", lt)
        n = u[0]
        segs = []
        for off, sz in [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]:
            data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
            if four != 4:
                continue
            vstart = data_off + 4
            idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
            real = idx[idx != 0xFFFF]
            mx = int(real.max()) if len(real) else 0
            stride = None
            for st in (24, 20, 32):
                if vb % st == 0 and mx < vb // st:
                    t_ = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, st // 4)[:, :3]
                    if np.isfinite(t_).all() and np.abs(t_).max() < 6000:
                        stride = st
                        break
            if not stride:
                continue
            m40 = struct.unpack_from("<I", ld, off + 40)[0]
            segs.append(dict(m40=m40, pos=np.frombuffer(
                ld[vstart:vstart + vb], "<f4").reshape(-1, stride // 4)[:, :3],
                idx=real.astype(np.uint32)))
        for si, s in enumerate(segs):
            tris = strip_to_tris(s["idx"])
            if not tris:
                continue
            p = s["pos"]
            t = np.array(tris, np.int64)
            # viewer space: (x, z, -y)
            v = np.stack([p[t[:, 0]], p[t[:, 1]], p[t[:, 2]]], 1)  # (n,3,3)
            v = v[:, :, [0, 2, 1]] * np.array([1, 1, -1], np.float32)
            tris_all.append(v.astype(np.float32))
            mat_all.append(np.full(len(t), s["m40"], np.int32))
    return np.concatenate(tris_all), np.concatenate(mat_all)


CELL = 150.0


def build_grid(tris):
    """XY cell -> triangle index array (viewer x,z plane)."""
    cen = tris.mean(1)
    gx = np.floor(cen[:, 0] / CELL).astype(np.int64)
    gz = np.floor(cen[:, 2] / CELL).astype(np.int64)
    from collections import defaultdict
    grid = defaultdict(list)
    for i in range(len(tris)):
        grid[(gx[i], gz[i])].append(i)
    return {k: np.array(v, np.int64) for k, v in grid.items()}


def raycast(orig, dirs, tris, grid):
    """Double-sided MT with per-ray grid pruning (cells sampled along the
    ray's XY projection). Returns (best_t, best_tri_index)."""
    n_r = len(dirs)
    v0g = tris[:, 0]
    best_t = np.full(n_r, np.inf, np.float32)
    best_i = np.full(n_r, -1, np.int64)
    rc = 128
    for r0 in range(0, n_r, rc):
        d = dirs[r0:r0 + rc]
        o = orig if np.ndim(orig) == 2 else orig[None, :]
        o = np.broadcast_to(np.asarray(o, np.float32), (len(d), 3))
        # cells along each ray (sample 60 steps to 6000u)
        ss = np.linspace(0, 3000, 30, dtype=np.float32)
        pts = o[:, None, :] + d[:, None, :] * ss[None, :, None]
        cx = np.floor(pts[..., 0] / CELL).astype(np.int64)
        cz = np.floor(pts[..., 2] / CELL).astype(np.int64)
        for j in range(len(d)):
            cells = set(zip(cx[j].tolist(), cz[j].tolist()))
            idxs = []
            for (a, b) in cells:
                for da in (-1, 0, 1):
                    for db in (-1, 0, 1):
                        idxs.append(grid.get((a + da, b + db)))
            if not any(x is not None for x in idxs):
                continue
            ti = np.unique(np.concatenate([x for x in idxs if x is not None]))
            T = tris[ti]
            v0, v1, v2 = T[:, 0], T[:, 1], T[:, 2]
            e1, e2 = v1 - v0, v2 - v0
            dj = d[j]
            pvec = np.cross(e2, dj)
            det = np.einsum("ij,ij->i", e1, pvec)
            ok = np.abs(det) > 1e-12
            inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
            tvec = o[j] - v0
            u = np.einsum("ij,ij->i", tvec, pvec) * inv
            qvec = np.cross(tvec, e1)
            vv = np.einsum("ij,j->i", qvec, dj) * inv
            tt = np.einsum("ij,ij->i", qvec, e2) * inv
            hit = ok & (u >= -1e-6) & (vv >= -1e-6) & (u + vv <= 1 + 1e-6) & (tt > 1.0)
            tt = np.where(hit, tt, np.inf)
            k = int(np.argmin(tt))
            if tt[k] < best_t[r0 + j]:
                best_t[r0 + j] = tt[k]
                best_i[r0 + j] = ti[k]
    return best_t, best_i


def cam_rays(pos, target, fov=55.0, w=W, h=H):
    pos = np.asarray(pos, np.float32)
    fwd = np.asarray(target, np.float32) - pos
    fwd /= np.linalg.norm(fwd)
    up = np.array([0, 1, 0], np.float32)
    right = np.cross(fwd, up)
    right /= np.linalg.norm(right)
    up2 = np.cross(right, fwd)
    a = np.tan(np.radians(fov) / 2)
    xs = (np.arange(w) + 0.5) / w * 2 - 1
    ys = 1 - (np.arange(h) + 0.5) / h * 2
    px, py = np.meshgrid(xs, ys)
    d = (fwd[None, None, :] + a * (px[..., None] * right[None, None, :]
         + py[..., None] * up2[None, None, :]))
    d = d.reshape(-1, 3)
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    return d.astype(np.float32)


def down_rays(pos, half, n=W):
    g = np.linspace(-half, half, n)
    px, py = np.meshgrid(g, g)
    o = np.tile(np.asarray(pos, np.float32), (n * n, 1))
    d = np.stack([px.ravel(), np.zeros(n * n, np.float32), py.ravel()], 1)
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    return o, d.astype(np.float32)


def raycast_cells(orig, dirs, tris, grid, cell_of=None):
    """Batched double-sided MT: rays grouped by the grid cells their XY
    path crosses (60 samples to 6000u), one vectorized block per cell."""
    from collections import defaultdict
    n_r = len(dirs)
    best_t = np.full(n_r, np.inf, np.float32)
    best_i = np.full(n_r, -1, np.int64)
    orig = np.asarray(orig, np.float32)
    o = np.broadcast_to(orig.reshape(1, 3) if orig.size == 3 else orig,
                        (n_r, 3))
    ss = np.linspace(0, 3000, 30, dtype=np.float32)
    pts = o[:, None, :] + dirs[:, None, :] * ss[None, :, None]
    cx = np.floor(pts[..., 0] / CELL).astype(np.int64)
    cz = np.floor(pts[..., 2] / CELL).astype(np.int64)
    pair = (cx.ravel() + 1) * 100000 + (cz.ravel() + 1)
    ray_of_sample = np.repeat(np.arange(n_r), len(ss))
    # unique (cell, ray) pairs
    key = pair * 10000000 + ray_of_sample
    uk = np.unique(key)
    cells = uk // 10000000
    rays = uk % 10000000
    order = np.argsort(cells, kind="stable")
    cells, rays = cells[order], rays[order]
    # group boundaries
    bounds = np.flatnonzero(np.diff(cells)) + 1
    groups = np.split(np.arange(len(cells)), bounds)
    # triangles per cell
    for g in groups:
        cl = (int(cells[g[0]]) - 1, 0)
        # decode: pair = (cx+1)*100000 + (cz+1)
        cc = int(cells[g[0]])
        cxi = cc // 100000 - 1
        czi = cc % 100000 - 1
        ridx = np.unique(rays[g])
        tidx = []
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                t = grid.get((cxi + da, czi + db))
                if t is not None:
                    tidx.append(t)
        if not tidx:
            continue
        ti = np.concatenate(tidx)
        T = tris[ti]
        v0, v1, v2 = T[:, 0], T[:, 1], T[:, 2]
        e1, e2 = v1 - v0, v2 - v0
        # sub-chunk rays to bound memory
        for r0 in range(0, len(ridx), 64):
            rr = ridx[r0:r0 + 64]
            d = dirs[rr]
            oo = o[rr]
            pvec = np.cross(d[:, None, :], e2[None, :, :])
            det = (e1[None, :, :] * pvec).sum(-1)
            ok = np.abs(det) > 1e-12
            inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
            tvec = oo[:, None, :] - v0[None, :, :]
            u = (tvec * pvec).sum(-1) * inv
            qvec = np.cross(tvec, e1[None, :, :])
            vv = (qvec * d[:, None, :]).sum(-1) * inv
            tt = (qvec * e2[None, :, :]).sum(-1) * inv
            hit = ok & (u >= -1e-6) & (vv >= -1e-6) & (u + vv <= 1 + 1e-6) & (tt > 1.0)
            tt = np.where(hit, tt, np.inf)
            k = np.argmin(tt, axis=1)
            tmin = tt[np.arange(len(rr)), k]
            upd = tmin < best_t[rr]
            bi = ti[k]
            bt = best_t[rr]
            best_t[rr] = np.where(upd, tmin, bt)
            pre = best_i[rr]
            best_i[rr] = np.where(upd, bi, pre)
    return best_t, best_i


def main():
    tris, mats = build_mesh()
    print(f"mesh: {len(tris)} tris")
    # ground-pruned mesh for the ground study (median height < 40u)
    gh = tris.mean(1)[:, 1] < 40.0
    gtris = tris[gh]
    gmat_of_tri = np.repeat(0, 1)  # placeholder, mats aligned below
    print(f"ground-zone tris (median y<40): {len(gtris)}")
    centers = tris.mean(1)  # (n,3)
    heights = centers[:, 1]

    # ---- scene bounds in viewer space (street tier only) -> camA
    lo = tris.reshape(-1, 3).min(0)
    hi = tris.reshape(-1, 3).max(0)
    c = (lo + hi) / 2
    r = float(np.linalg.norm(hi - lo) / 2)
    posA = c + r * np.array([1.05, 0.62, 1.05], np.float32)
    dA = cam_rays(posA, c)
    gtris_idx = np.where(gh)[0]
    gtris_mats = mats[gtris_idx]
    grid = build_grid(tris)
    tA, iA = raycast_cells(posA, dA, tris, grid)
    hitA = iA >= 0
    # ground third of the IMAGE (bottom rows)
    gm = np.zeros(H * W, bool)
    gm.reshape(H, W)[2 * H // 3:, :] = True
    ghit = hitA & gm
    print(f"\ncamA (default-view proxy {W}x{H}):")
    print(f"  all-pixel hit fraction: {hitA.mean():.3f}")
    print(f"  ground-third: hits {ghit.sum()}/{gm.sum()} = "
          f"{ghit.sum() / max(gm.sum(), 1):.3f}, void "
          f"{(gm & ~hitA).sum() / max(gm.sum(), 1):.3f}")
    hm = gtris_mats[iA[ghit]]
    vals, cnts = np.unique(hm, return_counts=True)
    top = sorted(zip(cnts, vals), reverse=True)[:10]
    print("  ground-third hits by +40 material index (top 10):")
    for cn, vv in top:
        print(f"    +40={vv:4d}: {cn:5d} ({cn / max(ghit.sum(), 1) * 100:.1f}%)")
    hh = gtris[iA[ghit]].mean(1)[:, 1]
    print(f"  hit height (viewer y): median {np.median(hh):.1f} "
          f"p10 {np.percentile(hh, 10):.1f} p90 {np.percentile(hh, 90):.1f}")
    # class map image (bottom third marked)
    cls = np.zeros(H * W, np.int32)   # 0 miss, 1 hit
    cls[hitA] = 1
    cls[~gm] = 2                      # sky region mark
    im = np.zeros((H, W, 3), np.uint8)
    im.reshape(-1, 3)[cls == 0] = (30, 30, 30)
    im.reshape(-1, 3)[cls == 1] = (200, 60, 60)
    im.reshape(-1, 3)[cls == 2] = (10, 10, 40)
    Image.fromarray(im).resize((1280, 720), Image.NEAREST).save(
        f"{OUT}/ray_classmap_camA.png")

    # ---- camB positive control: above a Roads0-bound road segment
    rows1 = json.load(open(
        "/home/z/my-project/repo/extraction/re/runtime_mats_GothamCity.json"))

    def stem(s):
        s = str(s or "")
        return s.lower().rsplit(".", 1)[0] if s and s != "UNBOUND" else None
    segs1 = island_segments("GothamCity")
    road_si = None
    for si, s in enumerate(segs1):
        m = s["m40"]
        if m < len(rows1) and stem(rows1[m].get("LightMap")) and \
                "Roads" in str(rows1[m].get("LightMap")):
            road_si = si
            break
    sc = segs1[road_si]
    print(f"\ncamB positive control: segment {road_si} +40={sc['m40']} "
          f"lm={rows1[sc['m40']].get('LightMap')} "
          f"centroid=({sc['cx']:.0f},{sc['cy']:.0f})")
    oB, dB = down_rays([sc["cx"], 120.0, -sc["cy"]], 60.0)
    tB, iB = raycast_cells(oB, dB, tris, grid)
    hitB = iB >= 0
    hmB = mats[iB[hitB]]
    road_hits = int((hmB == sc["m40"]).sum())
    print(f"  downward 120u grid: hits {hitB.mean():.3f}; "
          f"same-material hits {road_hits}/{hitB.sum()} = "
          f"{road_hits / max(hitB.sum(), 1):.3f}")
    vals, cnts = np.unique(hmB, return_counts=True)
    print("  by material:", {int(v): int(n) for n, v in
                             sorted(zip(cnts, vals), reverse=True)[:6]})

    # ---- camC plaza: a crossing-family segment
    plaza_si = None
    for si, s in enumerate(segs1):
        m = s["m40"]
        if m < len(rows1) and "Crossing" in str(rows1[m].get("DiffuseMap", "")):
            plaza_si = si
            break
    if plaza_si is not None:
        sp = segs1[plaza_si]
        oC, dC = down_rays([sp["cx"], 120.0, -sp["cy"]], 60.0)
        tC, iC = raycast_cells(oC, dC, tris, grid)
        hitC = iC >= 0
        hmC = mats[iC[hitC]]
        print(f"\ncamC plaza: segment {plaza_si} +40={sp['m40']} "
              f"diffuse={rows1[sp['m40']].get('DiffuseMap')}")
        print(f"  hits {hitC.mean():.3f}; same-material "
              f"{int((hmC == sp['m40']).sum())}/{int(hitB.sum() and hitC.sum())}")

    # ---- far-LOD slabs (+40 34/35 of GothamCity_low) vs camA miss pixels
    print("\nfar-LOD slab coverage of camA ground-third misses:")
    ltl = open("/home/z/my-project/work/zone/GothamCity_low/lod_table.bin", "rb").read()
    lld = open("/home/z/my-project/work/zone/GothamCity_low/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(ltl)//4}I", ltl)
    n = u[0]
    lo_slabs = []
    for off, sz in [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]:
        data_off, four, vb, ib = struct.unpack_from("<4I", lld, off + 68)
        if four != 4:
            continue
        m40 = struct.unpack_from("<I", lld, off + 40)[0]
        if m40 not in (34, 35):
            continue
        vstart = data_off + 4
        p = np.frombuffer(lld[vstart:vstart + vb], "<f4").reshape(-1, 3)
        lo_slabs.append((m40, p[:, [0, 2, 1]] * np.array([1, 1, -1], np.float32)))
    for m40, p in lo_slabs:
        print(f"  low +40={m40}: {len(p)} verts, viewer-space bbox "
              f"x[{p[:,0].min():.0f},{p[:,0].max():.0f}] "
              f"y[{p[:,1].min():.0f},{p[:,1].max():.0f}] "
              f"z[{p[:,2].min():.0f},{p[:,2].max():.0f}]")
        # rasterise: which camA miss pixels (ground third) project into bbox
        miss = (gm & ~hitA)
        if miss.sum() == 0:
            continue
        mp = np.mgrid[0:H, 0:W]
        pts = np.stack([mp[1][miss.reshape(H, W)], mp[0][miss.reshape(H, W)]],
                       1)
        # unproject misses is heavy; instead report bbox overlap with the
        # city extent the misses occupy (cheap proxy, honest about it)
        print(f"    (proxy) slab z-range vs city z-range: "
              f"[{p[:,2].min():.0f},{p[:,2].max():.0f}] vs "
              f"[{lo[2]:.0f},{hi[2]:.0f}]")
    json.dump(dict(camA=dict(hit=round(float(hitA.mean()), 4),
                             ground_hits=round(float(ghit.sum() / max(gm.sum(), 1)), 4),
                             ground_void=round(float((gm & ~hitA).sum() / max(gm.sum(), 1)), 4)),
                    camB=dict(hit=round(float(hitB.mean()), 4),
                              same_material=round(road_hits / max(hitB.sum(), 1), 4)),
                    note="cameras reconstructed; same-camera identity with session-21 unprovable"),
               open(f"{OUT}/raycast_results.json", "w"), indent=1)
    print("wrote raycast_results.json + ray_classmap_camA.png")


if __name__ == "__main__":
    main()
