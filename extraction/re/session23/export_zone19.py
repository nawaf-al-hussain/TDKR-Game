#!/usr/bin/env python3
"""Zone-tier exporter v19 (STAGED A/B) — v17 defaults + engine-chain UVs.

v17 default channels are preserved byte-for-byte in TEXCOORD_0/1:
  uv0 = w4 dequant (v17 diffuse)          [export_zone16 uv_of]
  uv1 = frac(w3_deq * s121 + s145)        [v17 lightmap chain]

Added (engine chain, PROVEN by Unicorn emulation session 22):
  TEXCOORD_2 = uv0e = (w3_u16 * s109.xy + s121.xy) mod 1   [diffuse]
  TEXCOORD_3 = uv1e = (w4_u16 * s133.xy + s145.xy) mod 1   [lightmap]
where the pair index and source word come from the record's OWN descriptor
list (attrId -> descriptor index -> pair slot j == descriptor j; source word
= byteOff/4).  When the record has NO TexCoord1 descriptor (classes (4,1),
(3,1), (3,0)) the engine has no Coord1 stream: GL disabled-attribute default
(0,0) is shipped for TEXCOORD_3.

three r160 GLTFLoader maps TEXCOORD_2 -> 'uv2', TEXCOORD_3 -> 'uv3'; the
viewer swaps uv<-uv2 / uv1<-uv3 + RepeatWrapping when ?chain=engine.
Default render (no query param) is pixel-identical to v18-staged.
"""
import json
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re/session22")
from export_zone import jpg_from_png, find_png, strip_to_tris, ISLANDS  # noqa
import export_zone as _ez
_ez.PNG = "/home/z/my-project/work/TDKR_assets/textures_png"  # work copy (download/ was pruned)
from export_zone16 import (GlbBuilder16, bind16, stem, m40_and_w3,  # noqa
                           batch_groups)
import batch_parser  # noqa


def find_png2(name):
    """v17 find_png + '.tga.png' name style (work-copy naming)."""
    for a in ("l_gothamcity_tex", "commons_tex"):
        for ext in (".png", ".tga.png"):
            p = os.path.join(_ez.PNG, a, name + ext)
            if os.path.exists(p):
                return p
    return None

ZONE = "/home/z/my-project/work/zone"
SITE = os.environ.get("SITE19", "/home/z/my-project/work/staged_wt")
MODELS = os.path.join(SITE, "models")
TEXD = os.path.join(MODELS, "tex")
RE = "/home/z/my-project/repo/extraction/re"


def island_words(island):
    """(m40, words, pos, idx) per segment — full vertex words for engine uvs.
    Same filter order as export_zone.parse_island."""
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
        for s in (24, 20, 32):   # v17 parity — stride-28 ((5,2)) streams are
            if vb % s == 0 and mx < vb // s:   # DROPPED by v17 too; see gap note
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if not stride:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        pos = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, stride // 4)[:, :3]
        out.append(dict(m40=m40, words=words, pos=pos,
                        uvw=words[:, 4].copy(), idx=real.astype(np.uint32)))
    return out


def attr_word_pair(rec, attr, words):
    """-> ((scale, offset), word_array|None) for attrId via the record's own
    descriptor list. Pair slot j == descriptor j; source word = byteOff/4."""
    for i, dd in enumerate(rec["descs"]):
        if dd["attr"] == attr:
            wi = dd["byteOff"] // 4
            if wi >= words.shape[1]:
                return rec["pairs"][i], None
            return rec["pairs"][i], words[:, wi]
    return None, None


def engine_uvs(rec, words):
    """-> (uv0e, uv1e) float32 [nv,2], wrapped; uv1e zeros when no Coord1."""
    u16 = lambda w: (w & 0xFFFF).astype(np.float64)
    v16 = lambda w: (w >> 16).astype(np.float64)
    pair0, w0 = attr_word_pair(rec, 1, words)
    if pair0 is None or w0 is None:
        # engine has no TexCoord0 stream either: dequant identity of word3
        w0 = words[:, 3] if words.shape[1] > 3 else None
        if w0 is None:
            z = np.zeros((len(words), 2), np.float32)
            return z, z.copy()
        uv0 = np.stack([u16(w0) / 65535.0, v16(w0) / 65535.0], 1)
        return uv0.astype(np.float32), np.zeros((len(words), 2), np.float32)
    sc, of = pair0
    uv0 = np.stack([np.mod(u16(w0) * sc[0] + of[0], 1.0),
                    np.mod(v16(w0) * sc[1] + of[1], 1.0)], 1)
    pair1, w1 = attr_word_pair(rec, 2, words)
    if pair1 is None or w1 is None:
        return uv0.astype(np.float32), np.zeros((len(words), 2), np.float32)
    sc1, of1 = pair1
    uv1 = np.stack([np.mod(u16(w1) * sc1[0] + of1[0], 1.0),
                    np.mod(v16(w1) * sc1[1] + of1[1], 1.0)], 1)
    return uv0.astype(np.float32), uv1.astype(np.float32)


class GlbBuilder19(GlbBuilder16):
    """v16 builder + TEXCOORD_2/3 (engine chain) buffer views."""

    def add_segment_mesh19(self, name, segs_binds):
        """segs_binds: (seg, tex, lm, mode, uv1|None, uv0e, uv1e)."""
        by_mat = {}
        order = []
        for seg, tex, lm, mode, uv1, uv0e, uv1e in segs_binds:
            tris = strip_to_tris(seg["idx"])
            if not tris:
                continue
            key = (tex, lm, mode)
            if key not in by_mat:
                by_mat[key] = dict(pos=[], uv=[], uv1=[], uv2=[], uv3=[],
                                   idx=[])
                order.append(key)
            b = by_mat[key]
            pos = seg["pos"]
            xyz = np.column_stack([pos[:, 0], pos[:, 2], -pos[:, 1]]).astype(np.float32)
            from export_zone import uv_of
            u, v = uv_of(seg)
            uv = np.column_stack([u, 1.0 - v]).astype(np.float32)
            nv = len(pos)
            if uv1 is not None:
                g = np.column_stack([uv1[:, 0], 1.0 - uv1[:, 1]]).astype(np.float32)
            else:
                g = np.zeros((nv, 2), np.float32)
            u2 = np.column_stack([uv0e[:, 0], 1.0 - uv0e[:, 1]]).astype(np.float32)
            u3 = np.column_stack([uv1e[:, 0], 1.0 - uv1e[:, 1]]).astype(np.float32)
            nv_existing = sum(len(p) for p in b["pos"])
            idx = np.asarray(tris, np.uint32).reshape(-1) + nv_existing
            b["pos"].append(xyz)
            b["uv"].append(uv)
            b["uv1"].append(g)
            b["uv2"].append(u2)
            b["uv3"].append(u3)
            b["idx"].append(idx)
        prims = []
        for key in order:
            tex, lm, mode = key
            b = by_mat[key]
            xyz = np.ascontiguousarray(np.concatenate(b["pos"]))
            uv = np.ascontiguousarray(np.concatenate(b["uv"]))
            uv1 = np.ascontiguousarray(np.concatenate(b["uv1"]))
            uv2 = np.ascontiguousarray(np.concatenate(b["uv2"]))
            uv3 = np.ascontiguousarray(np.concatenate(b["uv3"]))
            idx = np.ascontiguousarray(np.concatenate(b["idx"]))
            sp, lp = self._add(xyz.tobytes())
            su, lu = self._add(uv.tobytes())
            s1, l1 = self._add(uv1.tobytes())
            s2, l2 = self._add(uv2.tobytes())
            s3, l3 = self._add(uv3.tobytes())
            si, li = self._add(idx.tobytes())
            base = len(self.views)
            self.views += [dict(buffer=0, byteOffset=sp, byteLength=lp),
                           dict(buffer=0, byteOffset=su, byteLength=lu),
                           dict(buffer=0, byteOffset=s1, byteLength=l1),
                           dict(buffer=0, byteOffset=s2, byteLength=l2),
                           dict(buffer=0, byteOffset=s3, byteLength=l3),
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
            a.append(dict(bufferView=base + 3, componentType=5126,
                          count=len(uv2), type="VEC2"))
            a.append(dict(bufferView=base + 4, componentType=5126,
                          count=len(uv3), type="VEC2"))
            a.append(dict(bufferView=base + 5, componentType=5125,
                          count=len(idx), type="SCALAR"))
            prims.append(dict(attributes=dict(POSITION=len(a) - 6,
                                              TEXCOORD_0=len(a) - 5,
                                              TEXCOORD_1=len(a) - 4,
                                              TEXCOORD_2=len(a) - 3,
                                              TEXCOORD_3=len(a) - 2),
                              indices=len(a) - 1,
                              material=self.material_for16(tex, lm, mode),
                              mode=4))
        if not prims:
            return False
        mi = len(self.meshes)
        self.meshes.append(dict(name=name, primitives=prims))
        self.nodes.append(dict(mesh=mi, name=name))
        return True


def main():
    os.makedirs(MODELS, exist_ok=True)
    os.makedirs(TEXD, exist_ok=True)
    manifest_path = os.path.join(MODELS, "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) \
        else dict(tiers={}, glbs=[], total_verts=0, total_tris=0, version=18)

    used_tex = set()
    st_glbs = []
    for islname, isl in ISLANDS.items():
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        recs = batch_parser.parse_island(islname)
        groups = batch_groups(islname)
        segs = island_words(islname)
        m40w3 = m40_and_w3(islname)
        assert len(segs) == len(m40w3), (len(segs), len(m40w3))

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
            if (tex or lm) and not find_png2(tex or lm):
                stats["missing"] += 1
                tex = lm = None
                mode = "dark"
                uv1 = None
            rec = recs[m] if m < len(recs) else None
            if rec is not None:
                uv0e, uv1e = engine_uvs(rec, s["words"])
            else:
                z = np.zeros((len(s["pos"]), 2), np.float32)
                uv0e = uv1e = z
            binds.append((s, tex, lm, mode, uv1, uv0e, uv1e))
            if tex:
                used_tex.add(tex)
            if lm:
                used_tex.add(lm)
        print(f"{islname}: {len(segs)} segments, bindings {stats}")

        xs = np.array([s["pos"][:, 0].mean() for s in segs])
        ys = np.array([s["pos"][:, 1].mean() for s in segs])
        gx = ((xs - xs.min()) / max(np.ptp(xs), 1) * 4).clip(0, 3).astype(int)
        gy = ((ys - ys.min()) / max(np.ptp(ys), 1) * 3).clip(0, 2).astype(int)
        buckets = {}
        for i in range(len(segs)):
            buckets.setdefault((int(gx[i]), int(gy[i])), []).append(i)
        chunks = [v for k, v in sorted(buckets.items())]
        for ci, chunk in enumerate(chunks):
            gb = GlbBuilder19()
            nv = nt = 0
            for i in chunk:
                s, tex, lm, mode, lmuv, uv0e, uv1e = binds[i]
                tris = strip_to_tris(s["idx"])
                if not gb.add_segment_mesh19(f"seg_{i}",
                                             [(s, tex, lm, mode, lmuv,
                                               uv0e, uv1e)]):
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
        src = find_png2(t)
        if not src:
            print("  !! missing:", t)
            continue
        n = t + ".jpg"
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048, 88)
        print(f"  tex {n:<44} {sz/1024:>6.0f} KB")

    old_street = {g["file"]: g["bytes"] for g in manifest["glbs"]
                  if g.get("tier") == "street"}
    manifest["glbs"] = [g for g in manifest["glbs"]
                        if g.get("tier") != "street"] + st_glbs
    manifest["tiers"]["street"] = [g["file"] for g in st_glbs]
    manifest["version"] = 19
    manifest["total_verts"] = sum(g["verts"] for g in manifest["glbs"])
    manifest["total_tris"] = sum(g["tris"] for g in manifest["glbs"])
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1)
    new_bytes = sum(g["bytes"] for g in st_glbs)
    old_bytes = sum(old_street.values())
    print(f"manifest v19: {len(st_glbs)} street GLBs, "
          f"street bytes {old_bytes/1e6:.1f}MB -> {new_bytes/1e6:.1f}MB "
          f"(+{new_bytes-old_bytes:.1e})")


if __name__ == "__main__":
    main()
