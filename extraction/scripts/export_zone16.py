#!/usr/bin/env python3
"""Zone-tier exporter v16 — ENGINE-TRUE BINDINGS via descriptor +40.

Session 16 proved (runtime_mats16.py / agreement_test16.py / render probes):
  - descriptor +40 indexes the COMPILED material record array of
    <island>_materials.bdae (selfidx==position 307/307 and 196/196;
    order == source.dae library_materials).
  - the v5 structural band-atlas binding was self-fulfilling and WRONG
    (smoking gun: a street-lamp row bound to a road-crossings page).
  - street verts carry ONE UV; Coord1 is unbound -> GL default (0,0);
    the runtime Coord1_scaleoffset comes from batch_info (collada value is
    zeros), so pageUV = so.zw = d.xy (batch_info rec offset 145) — a
    CONSTANT per material on the LightMap page (1/16-grid quantized,
    3.7x over null; sampled texels plausible bake tints).
    => Color = Diffuse(uv0) x LightMapPage(d.xy) x 2  (LightMapDC-f exact).

Binding rule (per segment):
  m = +40 -> row = runtime_mats[m]; tex/lm stems, technique.
  SimpleAdditive            -> '<tex>|add'
  LightMap bound (any tech) -> '<tex>|<lm>|2x' + TEXCOORD_1 const (dx,1-dy)
                               (viewer: makeCityMaterialLM = engine exact)
  LightmapVCBlend (no dif)  -> '|<lm>|2x'   (bake-alone viewer path)
  otherwise                 -> '<tex>|d'
  unbound diffuse+LM / unknown material -> __dark

Writes street GLBs + used textures into SITE models/, replaces the street
tier in manifest.json, bumps version to 16.
"""
import json
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_zone import (parse_island, strip_to_tris, uv_of, jpg_from_png,  # noqa
                         find_png, ISLANDS)
from export_zone import GlbBuilder  # noqa

ZONE = "/home/z/my-project/work/zone"
SITE = "/home/z/my-project/work/ghpages_site"
MODELS = os.path.join(SITE, "models")
TEXD = os.path.join(MODELS, "tex")
RE = "/home/z/my-project/repo/extraction/re"


def stem(s):
    if not s or s == "UNBOUND":
        return None
    return s.replace(".tga", "")


def batch_groups(island):
    """material m -> (a, d) vec3s from batch_info offsets 109 / 145.
    Session 16: pageUV = w3_uv * a.xy + d.xy (100.00% inside on both
    islands; slot a = Coord1 scale, d = Coord1 offset)."""
    d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    out = []
    for m in range(M):
        rec = d[4 + stride * m: 4 + stride * (m + 1)]
        a = struct.unpack_from("<3f", rec, 109)
        dd = struct.unpack_from("<3f", rec, 145)
        out.append((a, dd))
    return out


def m40_and_w3(island):
    """Per segment (parse_island filter order): (+40, w3 packed Coord1)."""
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if not stride:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        w3 = None
        if stride == 24:
            w = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, 6)
            w3 = w[:, 3].copy()
        out.append((m40, w3))
    return out


class GlbBuilder16(GlbBuilder):
    """Adds per-primitive constant TEXCOORD_1 (LM page UV) + v11 names."""

    def material_for16(self, tex, lm, mode):
        key = (tex, lm, mode)
        if key in self._mat_by:
            return self._mat_by[key]
        if tex is None and lm is None:
            mat = dict(name="__dark", doubleSided=True,
                       pbrMetallicRoughness=dict(
                           baseColorFactor=[0.055, 0.07, 0.10, 1.0],
                           metallicFactor=0.0, roughnessFactor=1.0))
        elif tex is None:
            mat = dict(name=f'|{lm}|{mode}', doubleSided=True,
                       pbrMetallicRoughness=dict(
                           baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                           metallicFactor=0.0, roughnessFactor=1.0))
        elif lm:
            mat = dict(name=f'{tex}|{lm}|{mode}', doubleSided=True,
                       pbrMetallicRoughness=dict(
                           baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                           metallicFactor=0.0, roughnessFactor=1.0))
        else:
            mat = dict(name=f'{tex}|{mode}', doubleSided=True,
                       pbrMetallicRoughness=dict(
                           baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                           metallicFactor=0.0, roughnessFactor=1.0))
        self.materials.append(mat)
        mid = len(self.materials) - 1
        self._mat_by[key] = mid
        return mid

    def add_segment_mesh16(self, name, segs_binds):
        """segs_binds: (seg, tex, lm, mode, uv1|None array Nx2 game-space)."""
        by_mat = {}
        order = []
        for seg, tex, lm, mode, uv1 in segs_binds:
            tris = strip_to_tris(seg["idx"])
            if not tris:
                continue
            key = (tex, lm, mode)
            if key not in by_mat:
                by_mat[key] = dict(pos=[], uv=[], uv1=[], idx=[])
                order.append(key)
            b = by_mat[key]
            pos = seg["pos"]
            xyz = np.column_stack([pos[:, 0], pos[:, 2], -pos[:, 1]]).astype(np.float32)
            u, v = uv_of(seg)
            uv = np.column_stack([u, 1.0 - v]).astype(np.float32)
            nv = len(pos)
            if uv1 is not None:
                g = np.column_stack([uv1[:, 0], 1.0 - uv1[:, 1]]).astype(np.float32)
            else:
                g = np.zeros((nv, 2), np.float32)
            nv_existing = sum(len(p) for p in b["pos"])
            idx = np.asarray(tris, np.uint32).reshape(-1) + nv_existing
            b["pos"].append(xyz)
            b["uv"].append(uv)
            b["uv1"].append(g)
            b["idx"].append(idx)
        prims = []
        for key in order:
            tex, lm, mode = key
            b = by_mat[key]
            xyz = np.ascontiguousarray(np.concatenate(b["pos"]))
            uv = np.ascontiguousarray(np.concatenate(b["uv"]))
            uv1 = np.ascontiguousarray(np.concatenate(b["uv1"]))
            idx = np.ascontiguousarray(np.concatenate(b["idx"]))
            sp, lp = self._add(xyz.tobytes())
            su, lu = self._add(uv.tobytes())
            s1, l1 = self._add(uv1.tobytes())
            si, li = self._add(idx.tobytes())
            base = len(self.views)
            self.views += [dict(buffer=0, byteOffset=sp, byteLength=lp),
                           dict(buffer=0, byteOffset=su, byteLength=lu),
                           dict(buffer=0, byteOffset=s1, byteLength=l1),
                           dict(buffer=0, byteOffset=si, byteLength=li)]
            mn, mx = xyz.min(0), xyz.max(0)
            a = self.accessors
            a.append(dict(bufferView=base, componentType=5126, count=len(xyz),
                          type="VEC3", min=[float(x) for x in mn],
                          max=[float(x) for x in mx]))
            a.append(dict(bufferView=base + 1, componentType=5126,
                          count=len(uv), type="VEC2"))
            a.append(dict(bufferView=base + 2, componentType=5126,
                          count=len(uv1), type="VEC2"))
            a.append(dict(bufferView=base + 3, componentType=5125,
                          count=len(idx), type="SCALAR"))
            prims.append(dict(attributes=dict(POSITION=len(a) - 4,
                                              TEXCOORD_0=len(a) - 3,
                                              TEXCOORD_1=len(a) - 2),
                              indices=len(a) - 1,
                              material=self.material_for16(tex, lm, mode),
                              mode=4))
        if not prims:
            return False
        mi = len(self.meshes)
        self.meshes.append(dict(name=name, primitives=prims))
        self.nodes.append(dict(mesh=mi, name=name))
        return True


def bind16(m, rows, groups, w3):
    """-> (tex, lm, mode, uv1_array|None). uv1 = w3*a.xy + d.xy (game
    space) for LightMap-bound materials (the engine's pageUV)."""
    if m >= len(rows):
        return (None, None, "dark", None)
    row = rows[m]
    tex = stem(row.get("DiffuseMap"))
    lm = stem(row.get("LightMap"))
    tech = (row.get("technique") or "").lower()
    if "#simpleadditive" in tech and tex:
        return (tex, None, "add", None)
    if tex is None:
        if lm:
            return (None, lm, "2x", None)   # bake-alone viewer path
        return (None, None, "dark", None)
    if lm and w3 is not None:
        a, dd = groups[m] if m < len(groups) else ((0, 0, 0), (0, 0, 0))
        cu = (w3 & 0xFFFF).astype(np.float32) / 65535.0
        cv = (w3 >> 16).astype(np.float32) / 65535.0
        pu = cu * a[0] + dd[0]
        pv = cv * a[1] + dd[1]
        uv1 = np.stack([pu, pv], 1)
        return (tex, lm, "2x", uv1)
    if lm:
        return (tex, lm, "2x", None)
    if "lightmapvcblend" in tech:
        return (None, None, "dark", None)
    return (tex, None, "d", None)


def main():
    os.makedirs(MODELS, exist_ok=True)
    os.makedirs(TEXD, exist_ok=True)
    manifest_path = os.path.join(MODELS, "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) \
        else dict(tiers={}, glbs=[], total_verts=0, total_tris=0, version=15)

    used_tex = set()
    st_glbs = []
    for islname, isl in ISLANDS.items():
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        groups = batch_groups(islname)
        segs = parse_island(islname)
        m40w3 = m40_and_w3(islname)
        assert len(segs) == len(m40w3)

        binds = []
        stats = dict(dark=0, lm=0, d=0, add=0, bakealone=0, missing=0)
        for s, (m, w3) in zip(segs, m40w3):
            tex, lm, mode, uv1 = bind16(m, rows, groups, w3)
            if mode == "dark":
                stats["dark"] += 1
            elif tex is None:
                stats["bakealone"] += 1
            elif mode == "add":
                stats["add"] += 1
            elif lm:
                stats["lm"] += 1
            else:
                stats["d"] += 1
            if (tex or lm) and not find_png(tex or lm):
                stats["missing"] += 1
                tex = lm = None
                mode = "dark"
                uv1 = None
            binds.append((s, tex, lm, mode, uv1))
            if tex:
                used_tex.add(tex)
            if lm:
                used_tex.add(lm)
        print(f"{islname}: {len(segs)} segments, bindings {stats}")

        # spatial chunks (same grid as v5: 4x3 buckets)
        xs = np.array([s["pos"][:, 0].mean() for s in segs])
        ys = np.array([s["pos"][:, 1].mean() for s in segs])
        gx = ((xs - xs.min()) / max(np.ptp(xs), 1) * 4).clip(0, 3).astype(int)
        gy = ((ys - ys.min()) / max(np.ptp(ys), 1) * 3).clip(0, 2).astype(int)
        buckets = {}
        for i in range(len(segs)):
            buckets.setdefault((int(gx[i]), int(gy[i])), []).append(i)
        chunks = [v for k, v in sorted(buckets.items())]
        for ci, chunk in enumerate(chunks):
            gb = GlbBuilder16()
            nv = nt = 0
            for i in chunk:
                s, tex, lm, mode, lmuv = binds[i]
                tris = strip_to_tris(s["idx"])
                if not gb.add_segment_mesh16(f"seg_{i}", [(s, tex, lm, mode, lmuv)]):
                    continue
                nv += len(s["pos"])
                nt += len(tris)
            if not nt:
                continue
            name = f'street_{"island1" if isl["isl"]=="1" else "island2"}_{ci:02d}.glb'
            size = gb.write(os.path.join(MODELS, name))
            st_glbs.append(dict(file="models/" + name, bytes=size, verts=nv,
                                tris=nt, tier="street",
                                files=[dict(name=name[:-4], verts=nv, tris=nt,
                                            meshes=len(chunk))]))
            print(f"  + {name:<32} {size/1024:>7.0f} KB {nt:>8,} tris")

    for t in sorted(used_tex):
        src = find_png(t)
        if not src:
            print("  !! missing:", t)
            continue
        n = t + ".jpg"
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048, 88)
        print(f"  tex {n:<44} {sz/1024:>6.0f} KB")

    manifest["glbs"] = [g for g in manifest["glbs"]
                        if g.get("tier") != "street"] + st_glbs
    manifest["tiers"]["street"] = [g["file"] for g in st_glbs]
    manifest["version"] = 16
    manifest["total_verts"] = sum(g["verts"] for g in manifest["glbs"])
    manifest["total_tris"] = sum(g["tris"] for g in manifest["glbs"])
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"manifest v16: {len(st_glbs)} street GLBs, "
          f"totals {manifest['total_verts']:,}v {manifest['total_tris']:,}t")


if __name__ == "__main__":
    main()
