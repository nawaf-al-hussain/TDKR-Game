#!/usr/bin/env python3
"""Round-4 review evidence — the street-tier flip quantified.

Reviewer (log-only) demands BEFORE the +40 flip is accepted:
  1. Texel-validity test  : fraction of diffuse-texture samples landing on
     non-empty texels, scored for THREE bindings over the SAME segment UVs:
       +40 (engine), v5 exporter (old), shuffled +40 (null, K perms).
     Decision rule: +40 must beat both on prop/atlas materials; if v5 ~
     shuffle, the old heuristic was self-fulfilling.
  2. UV-footprint test    : atlas materials — segment UV footprint should
     sit inside ONE atlas cell; report pass fraction +40 vs shuffle.
  3. Class UV-rect tightness (added after round-4 diag): segments sharing a
     +40 material must crowd into ONE atlas cell -> per-class
     union(rect)/max(rect) tightness, +40 vs v5 classes vs shuffled classes.
     Unbiased by page density (unlike raw texel-validity, whose dark-pad
     confound is also reported).
  4. (a,d) null test      : apply ANOTHER material's batch_info (a,d) pair
     to each segment's w3 -> in-page rate must drop clearly vs the correct
     pair, else the 100.0000% in-page number proves nothing. PLUS the
     tile-rect overlap test: correct (a,d) should tile the page without
     collisions; shuffled pairs collide.

Also banks per-segment validity arrays for re-audit.
Outputs: extraction/re/round4_evidence.json + stdout tables.
"""
import collections
import json
import random
import struct
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import (parse_island, bind_segment, cross_sections,  # noqa
                         ISLANDS, uv_of, find_png, strip_to_tris)

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round4_evidence.json"

K_NULL = 24          # shuffle permutations (null distribution)
K_AD = 48            # wrong (a,d) pairs sampled per island for the LM null
MAX_SAMPLES = 40000  # per segment per binding pass
DOWNSCALE = 1024     # texture working resolution for validity sampling

ROAD_FAMILY = {"GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
               "GothamCity_Road_Island_2", "GothamCity_Road_v2_Island_2",
               "GothamCity_Road_v1_Island_2", "GothamCity_Road_Crossings_Island_1",
               "GothamCity_Road_Crossings_Island_2", "gothamcity_roads_details"}
FLAT_FAMILY = {"GC_Park_grass", "GC_Park_dirt", "GothamCity_sand_tile",
               "GothamCity_asphalt_tile", "GC_SXC_grass", "GC_SXC_ground_tile",
               "GC_SXC_hedge", "GC_T_Concrete_01", "GC_T_Concrete_02",
               "GC_Diner_Floor", "GC_Park_statue"}


def stem_of(dm):
    """Case-insensitive extension strip (the .TGA bug fix, banked here)."""
    if not dm or dm == "UNBOUND":
        return None
    s = dm
    for ext in (".tga", ".png", ".jpg"):
        if s.lower().endswith(ext):
            s = s[: -len(ext)]
            break
    return s


def fam40(stem):
    """Fine-grained engine family of a material's diffuse stem."""
    if stem is None:
        return "unbound"
    if stem in ROAD_FAMILY:
        return "road_band"
    if stem in FLAT_FAMILY:
        return "flat"
    if stem.startswith("GC_Z1_Props_Street"):
        return "props_street"
    if stem.startswith("GC_Z1_Props_Rooftop"):
        return "props_rooftop"
    if stem == "trunk":
        return "trees"
    if stem.startswith("FX_Coronas"):
        return "coronas"
    if stem.startswith("HC_Prop_Billboard"):
        return "billboards"
    if "Residential_Props" in stem:
        return "props_mono_rail"
    if stem.startswith("GC_Footprint") or stem.startswith("GC_footprint"):
        return "building_footprint"
    if stem.startswith("GC_Residential_BD") or stem.startswith("GC_Z1_Shops"):
        return "building_residential"
    if (stem.startswith("GC_Cath") or stem.startswith("GC_SXC")
            or stem.startswith("GC_Walls") or stem.startswith("GC_CBCE")
            or stem.startswith("GC_DMUS") or stem.startswith("GC_Glass")
            or stem.startswith("GC_Statues") or stem.startswith("GC_VPOW")
            or stem.startswith("GC_VRS") or stem.startswith("GC_Park_atlas")
            or stem.startswith("GC_footprint") or "bridge" in stem.lower()
            or stem.startswith("GC_Truck") or stem.startswith("GC_Industrial")):
        return "building_landmark_misc"
    return "other"


COARSE = {"road_band": "road", "flat": "sidewalk_flat",
          "props_street": "props", "props_rooftop": "props", "trees": "props",
          "coronas": "props", "billboards": "props", "props_mono_rail": "props",
          "building_footprint": "buildings", "building_residential": "buildings",
          "building_landmark_misc": "buildings", "other": "other",
          "unbound": "unbound"}

# ---------------------------------------------------------------- textures
_tex_cache = {}


class TexData:
    """RGBA uint8 array + emptiness mask + (atlas) component labels."""

    def __init__(self, stem):
        png = find_png(stem)
        if png is None:
            self.ok = False
            return
        im = Image.open(png).convert("RGBA")
        if max(im.size) > DOWNSCALE:
            im = im.resize((DOWNSCALE, DOWNSCALE), Image.BILINEAR)
        arr = np.asarray(im, np.uint8)
        self.w, self.h = im.size
        self.rgb = arr[..., :3].astype(np.int16)
        self.alpha = arr[..., 3]
        # background = modal colour quantised to /16 (atlas padding)
        q = (self.rgb // 16).astype(np.int32)
        key = q[..., 0] * 4096 + q[..., 1] * 64 + q[..., 2]
        vals, counts = np.unique(key, return_counts=True)
        bgk = vals[np.argmax(counts)]
        bg = np.array([(bgk // 4096) * 16 + 8,
                       ((bgk // 64) % 64) * 16 + 8,
                       (bgk % 64) * 16 + 8], np.int16)
        self.bg = bg
        dist = np.abs(self.rgb - bg).max(axis=2)
        self.empty = ((self.alpha < 64)
                      | (self.rgb.max(axis=2) <= 10)
                      | (dist <= 10))
        self.empty_frac = float(self.empty.mean())
        # atlas cell labelling on the content mask
        content = ~self.empty
        st = np.ones((3, 3), bool)     # merge cell sub-parts
        cm = ndimage.binary_closing(content, structure=st)
        lab, n = ndimage.label(cm)
        self.lab = lab
        self.n_cells = n
        self.coverage = float(content.mean())
        sizes = ndimage.sum(content, lab, index=range(1, n + 1)) if n else []
        self.big_cells = int(np.sum(np.asarray(sizes) > 200)) if n else 0
        self.ok = True

    def sample(self, u, v):
        """rgb at normalised (u,v), game space (v bottom-origin)."""
        tj = np.clip((u * (self.w - 1)).astype(np.int32), 0, self.w - 1)
        ti = np.clip(((1.0 - v) * (self.h - 1)).astype(np.int32), 0, self.h - 1)
        return self.rgb[ti, tj], self.alpha[ti, tj]

    def cell_of(self, u, v):
        tj = np.clip((u * (self.w - 1)).astype(np.int32), 0, self.w - 1)
        ti = np.clip(((1.0 - v) * (self.h - 1)).astype(np.int32), 0, self.h - 1)
        return self.lab[ti, tj]


def get_tex(stem):
    if stem not in _tex_cache:
        if len(_tex_cache) > 80:
            _tex_cache.pop(next(iter(_tex_cache)))
        _tex_cache[stem] = TexData(stem)
    return _tex_cache[stem]


# ---------------------------------------------------------------- sampling
def seg_samples(seg, rng):
    """Barycentric sample points (u, v) + per-sample triangle id."""
    tris = np.asarray(strip_to_tris(seg["idx"]), np.int64).reshape(-1, 3)
    good = (tris[:, 0] != tris[:, 1]) & (tris[:, 1] != tris[:, 2]) \
        & (tris[:, 0] != tris[:, 2])
    tris = tris[good]
    if not len(tris):
        return None, None
    if len(tris) > MAX_SAMPLES // 4:
        nprng = np.random.default_rng(1604)
        keep = nprng.choice(len(tris), MAX_SAMPLES // 4, replace=False)
        tris = tris[keep]
    u, v = uv_of(seg)
    u = u.astype(np.float32)
    v = v.astype(np.float32)
    # 4 samples per triangle: centroid + 3 edge midpoints
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    W = [np.full(len(tris), 1 / 3, np.float32), np.full(len(tris), 1 / 3, np.float32),
         np.full(len(tris), 1 / 3, np.float32)]
    su = W[0] * u[a] + W[1] * u[b] + W[2] * u[c]
    sv = W[0] * v[a] + W[1] * v[b] + W[2] * v[c]
    for i0, i1 in ((0, 1), (1, 2), (2, 0)):
        w0 = np.full(len(tris), 0.5, np.float32)
        w1 = np.full(len(tris), 0.5, np.float32)
        su = np.concatenate([su, w0 * u[tris[:, i0]] + w1 * u[tris[:, i1]]])
        sv = np.concatenate([sv, w0 * v[tris[:, i0]] + w1 * v[tris[:, i1]]])
    tid = np.repeat(np.arange(len(tris)), 4)
    return su, sv


def validity(tex, su, sv):
    if tex is None or not tex.ok:
        return 0.0
    tj = np.clip((su * (tex.w - 1)).astype(np.int32), 0, tex.w - 1)
    ti = np.clip(((1.0 - sv) * (tex.h - 1)).astype(np.int32), 0, tex.h - 1)
    e = tex.empty[ti, tj]
    return float(1.0 - e.mean())


def rect_tightness(rects):
    """union(rects).area / max(rects).area in UV space. 1.0 = all rects
    identical (one atlas cell); ~0 = scattered across the page."""
    if len(rects) < 2:
        return 1.0
    u0 = min(r[0] for r in rects); u1 = max(r[1] for r in rects)
    v0 = min(r[2] for r in rects); v1 = max(r[3] for r in rects)
    mx = max((r[1] - r[0]) * (r[3] - r[2]) for r in rects)
    if mx <= 1e-12:
        return 0.0
    return max(0.0, min(1.0, (u1 - u0) * (v1 - v0) / mx))


def footprint(tex, su, sv):
    """(vertex-dominant fraction, bbox-grid containment) for atlas cells."""
    if tex is None or not tex.ok or tex.n_cells == 0:
        return 0.0, 0.0
    cells = tex.cell_of(su, sv)
    pos = cells[cells > 0]
    if len(pos) == 0:
        return 0.0, 0.0
    vals, cnts = np.unique(pos, return_counts=True)
    dom = cnts.max() / len(cells)
    # bbox grid containment on the dominant cell
    u0, u1 = su.min(), su.max()
    v0, v1 = sv.min(), sv.max()
    gu, gv = np.meshgrid(np.linspace(u0, u1, 9), np.linspace(v0, v1, 9))
    gcell = tex.cell_of(gu.ravel(), gv.ravel())
    gdom = float((gcell == vals[np.argmax(cnts)]).mean())
    return float(dom), gdom


ATLAS_FAMS = {"props_street", "props_rooftop", "trees", "billboards",
              "props_mono_rail", "building_footprint", "building_residential",
              "building_landmark_misc", "other"}


def m40_list(island):
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
        ok = False
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    ok = True
                    break
        if ok:
            out.append(struct.unpack_from("<I", ld, off + 40)[0])
    return out


def main():
    rng = random.Random(1604)
    report = {}
    for islname, isl in ISLANDS.items():
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        segs = parse_island(islname)
        m40s = m40_list(islname)
        assert len(segs) == len(m40s)

        XSECS = {k: cross_sections(k) for k in (
            "GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
            "GothamCity_Road_Island_2", "gothamcity_roads_details",
            "GothamCity_Road_Crossings_Island_1",
            "GothamCity_Road_Crossings_Island_2")}
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}

        v5_tex = [bind_segment(s, isl, xs)[0] for s in segs]
        p40_stem = [stem_of(rows[m].get("DiffuseMap")) for m in m40s]
        fams = [fam40(st) for st in p40_stem]

        su_list, sv_list = [], []
        uv_rects = []
        for s in segs:
            su, sv = seg_samples(s, rng)
            su_list.append(su)
            sv_list.append(sv)
            if su is not None and len(su):
                uv_rects.append((float(su.min()), float(su.max()),
                                 float(sv.min()), float(sv.max())))
            else:
                uv_rects.append(None)
        print(f"segments={len(segs)}, sampled={sum(1 for x in su_list if x is not None)}")

        # ---------- binding validity vectors
        n = len(segs)
        val_p40 = np.zeros(n)
        val_v5 = np.zeros(n)
        fp_dom = np.zeros(n)
        fp_bbox = np.zeros(n)
        for i in range(n):
            if su_list[i] is None:
                continue
            t = get_tex(p40_stem[i]) if p40_stem[i] else None
            val_p40[i] = validity(t, su_list[i], sv_list[i])
            if t is not None and t.ok:
                fp_dom[i], fp_bbox[i] = footprint(t, su_list[i], sv_list[i])
            if v5_tex[i]:
                val_v5[i] = validity(get_tex(v5_tex[i]), su_list[i], sv_list[i])

        # ---------- shuffle null
        null_val = np.zeros((K_NULL, n))
        null_fp = np.zeros((K_NULL, n))
        idx_all = list(range(n))
        for k in range(K_NULL):
            perm = idx_all[:]
            rng.shuffle(perm)
            for i in range(n):
                if su_list[i] is None:
                    continue
                st = p40_stem[perm[i]]
                t = get_tex(st) if st else None
                null_val[k, i] = validity(t, su_list[i], sv_list[i])
                if t is not None and t.ok:
                    null_fp[k, i], _ = footprint(t, su_list[i], sv_list[i])
        nv_mean = null_val.mean(0)
        nf_mean = null_fp.mean(0)

        # ---------- tables
        def by_family(vals):
            agg = collections.defaultdict(list)
            for i in range(n):
                if su_list[i] is None:
                    continue
                agg[fams[i]].append(vals[i])
            return {f: dict(nseg=len(a), mean=round(float(np.mean(a)), 4))
                    for f, a in sorted(agg.items())}

        popA = [i for i in range(n) if v5_tex[i] and p40_stem[i] and su_list[i] is not None]
        res = dict(
            n_segments=n,
            n_sampled=int(sum(1 for x in su_list if x is not None)),
            plus40=dict(overall=round(float(val_p40[[i for i in range(n)
                                                        if su_list[i] is not None]].mean()), 4),
                        by_family=by_family(val_p40)),
            v5=dict(overall=round(float(val_v5[[i for i in range(n)
                                                if su_list[i] is not None]].mean()), 4),
                    by_family=by_family(val_v5)),
            null=dict(overall=round(float(nv_mean[[i for i in range(n)
                                                   if su_list[i] is not None]].mean()), 4),
                      sd_overall=round(float(nv_mean.std()), 4),
                      by_family_mean={f: round(float(np.mean([nv_mean[i] for i in range(n)
                                                              if fams[i] == f and su_list[i] is not None])), 4)
                                      for f in set(fams)}),
            popA_v5bound=dict(n=len(popA),
                              plus40=round(float(val_p40[popA].mean()), 4),
                              v5=round(float(val_v5[popA].mean()), 4),
                              null=round(float(nv_mean[popA].mean()), 4),
                              null_sd=round(float(null_val[:, popA].mean(1).std()), 4),
                              plus40_wins=int((val_p40[popA] > val_v5[popA]).sum()),
                              v5_wins=int((val_v5[popA] > val_p40[popA]).sum()),
                              tie=len(popA) - int((val_p40[popA] > val_v5[popA]).sum())
                                  - int((val_v5[popA] > val_p40[popA]).sum())),
            footprint=dict(
                atlas_pages=sorted({p40_stem[i] for i in range(n)
                                    if su_list[i] is not None and p40_stem[i]
                                    and fams[i] in ATLAS_FAMS
                                    and get_tex(p40_stem[i]).ok
                                    and get_tex(p40_stem[i]).n_cells >= 2
                                    and get_tex(p40_stem[i]).coverage < 0.85}),
                plus40_dom95=round(float(np.mean([fp_dom[i] >= 0.95 for i in range(n)
                                                  if su_list[i] is not None and p40_stem[i]
                                                  and fams[i] in ATLAS_FAMS
                                                  and get_tex(p40_stem[i]).ok
                                                  and get_tex(p40_stem[i]).n_cells >= 2
                                                  and get_tex(p40_stem[i]).coverage < 0.85])), 4),
                plus40_bbox95=round(float(np.mean([fp_bbox[i] >= 0.95 for i in range(n)
                                                   if su_list[i] is not None and p40_stem[i]
                                                   and fams[i] in ATLAS_FAMS
                                                   and get_tex(p40_stem[i]).ok
                                                   and get_tex(p40_stem[i]).n_cells >= 2
                                                   and get_tex(p40_stem[i]).coverage < 0.85])), 4),
                null_dom95=round(float(np.mean([nf_mean[i] >= 0.95 for i in range(n)
                                                if su_list[i] is not None and p40_stem[i]
                                                and fams[i] in ATLAS_FAMS
                                                and get_tex(p40_stem[i]).ok
                                                and get_tex(p40_stem[i]).n_cells >= 2
                                                and get_tex(p40_stem[i]).coverage < 0.85])), 4),
                null_bbox95=round(float(np.mean([nf_mean[i] >= 0.95 for i in range(n)
                                                 if su_list[i] is not None and p40_stem[i]
                                                 and fams[i] in ATLAS_FAMS
                                                 and get_tex(p40_stem[i]).ok
                                                 and get_tex(p40_stem[i]).n_cells >= 2
                                                 and get_tex(p40_stem[i]).coverage < 0.85])), 4)),
        )

        # ---------- class UV-rect tightness (density-unbiased discriminator)
        def class_tightness(assign_stem, min_n=3):
            by = collections.defaultdict(list)
            for i in range(n):
                if assign_stem[i] and uv_rects[i] and fams[i] in ATLAS_FAMS:
                    by[assign_stem[i]].append(uv_rects[i])
            vals = {}
            for st, rs in by.items():
                if len(rs) >= min_n:
                    vals[st] = dict(nseg=len(rs), tight=round(rect_tightness(rs), 3))
            if not vals:
                return dict(n_classes=0, mean_tight=None,
                            frac_ge07=None, classes={})
            tv = [v["tight"] for v in vals.values()]
            return dict(n_classes=len(vals),
                        mean_tight=round(float(np.mean(tv)), 3),
                        median_tight=round(float(np.median(tv)), 3),
                        frac_ge07=round(float(np.mean([t >= 0.7 for t in tv])), 3),
                        classes=dict(sorted(vals.items(),
                                            key=lambda kv: -kv[1]["tight"])))

        # v5 classes: same assigned texture; +40 classes: same +40 stem;
        # null classes: shuffled +40 assignment (K draws aggregated)
        tight = dict(plus40=class_tightness(p40_stem), v5=class_tightness(v5_tex))
        null_tights = []
        idx_all2 = list(range(n))
        for _ in range(12):
            perm = idx_all2[:]
            rng.shuffle(perm)
            null_stem = [p40_stem[p] for p in perm]
            r = class_tightness(null_stem)
            if r["mean_tight"] is not None:
                null_tights.append(r["mean_tight"])
        tight["null"] = dict(mean=round(float(np.mean(null_tights)), 3),
                             sd=round(float(np.std(null_tights)), 3),
                             k=len(null_tights))
        res["class_tightness"] = tight

        # ---------- (a,d) null test for the LM chain
        d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
        stride_b = struct.unpack_from("<I", d, 0)[0]
        ad = []
        for m in range((len(d) - 4) // stride_b):
            rec = d[4 + stride_b * m: 4 + stride_b * (m + 1)]
            a = struct.unpack_from("<3f", rec, 109)
            dd = struct.unpack_from("<3f", rec, 145)
            ad.append((a, dd))
        lm_mats = [m for m in range(len(rows))
                   if rows[m].get("LightMap") and rows[m]["LightMap"] != "UNBOUND"]
        lm_segs = [(i, m) for i, m in enumerate(m40s) if m in lm_mats]
        # per-material vertex pool (subsample for speed)
        mat_verts = collections.defaultdict(list)
        for i, m in lm_segs:
            w3 = None
            seg = segs[i]
            # recover w3 from raw words via parse order (recompute cheaply)
            mat_verts[m].append(i)
        ad_report = dict(lm_materials=len(lm_mats), lm_segments=len(lm_segs),
                         ad_autopage=None, correct=None, null=None)
        # in-page is authored-trivial check: d + a <= 1 for how many pairs?
        ok_pairs = 0
        for m in lm_mats:
            a, dd = ad[m]
            if a[0] >= -1e-6 and a[1] >= -1e-6 and dd[0] + a[0] <= 1.0001 \
                    and dd[1] + a[1] <= 1.0001 and dd[0] >= -1e-6 and dd[1] >= -1e-6:
                ok_pairs += 1
        ad_report["ad_autopage"] = dict(n=len(lm_mats), d_plus_a_le1=ok_pairs)
        # real per-vertex null over a vertex sample
        lt = open(f"{ZONE}/{islname}/lod_table.bin", "rb").read()
        ld = open(f"{ZONE}/{islname}/lod_data.bin", "rb").read()
        u32 = struct.unpack(f"<{len(lt)//4}I", lt)
        npairs = u32[0]
        prs = [(u32[1 + 2 * k], u32[2 + 2 * k]) for k in range(npairs)]
        w3_of = {}
        si = 0
        for off, sz in prs:
            data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
            if four != 4:
                continue
            vstart = data_off + 4
            ix = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
            rl = ix[ix != 0xFFFF]
            mx = int(rl.max()) if len(rl) else 0
            st_ = None
            for s in (24, 20, 32):
                if vb % s == 0 and mx < vb // s:
                    tt = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                    if np.isfinite(tt).all() and np.abs(tt).max() < 6000:
                        st_ = s
                        break
            if st_ is None:
                continue
            if st_ == 24:
                w = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, 6)
                w3_of[si] = w[:, 3].astype(np.uint32)
            else:
                w3_of[si] = np.zeros(vb // st_, np.uint32)
            si += 1
        assert si == n
        rng2 = random.Random(99)
        correct_in = tot = 0
        null_in = collections.defaultdict(lambda: [0, 0])
        for i, m in lm_segs:
            if i not in w3_of or len(w3_of[i]) == 0:
                continue
            w3 = w3_of[i]
            cu = (w3 & 0xFFFF).astype(np.float32) / 65535.0
            cv = (w3 >> 16).astype(np.float32) / 65535.0
            take = min(len(cu), 4000)
            sel = rng2.sample(range(len(cu)), take)
            cu, cv = cu[sel], cv[sel]
            a, dd = ad[m]
            pu, pv = cu * a[0] + dd[0], cv * a[1] + dd[1]
            correct_in += int(np.sum((pu > -0.02) & (pu < 1.02)
                                     & (pv > -0.02) & (pv < 1.02)))
            tot += take
            for m2 in rng2.sample(lm_mats, min(K_AD, len(lm_mats))):
                a2, d2 = ad[m2]
                pu2, pv2 = cu * a2[0] + d2[0], cv * a2[1] + d2[1]
                ins = int(np.sum((pu2 > -0.02) & (pu2 < 1.02)
                                 & (pv2 > -0.02) & (pv2 < 1.02)))
                null_in[m2][0] += ins
                null_in[m2][1] += take
        rates = [v[0] / max(v[1], 1) for v in null_in.values()]
        ad_report["correct"] = round(correct_in / max(tot, 1), 5)
        ad_report["correct_verts"] = tot
        ad_report["null"] = dict(mean=round(float(np.mean(rates)), 5),
                                 sd=round(float(np.std(rates)), 5),
                                 min=round(float(np.min(rates)), 5),
                                 max=round(float(np.max(rates)), 5),
                                 n_pairs=len(rates))

        # ---- tile-rect overlap test (the honest null for the (a,d) chain):
        # authored rects should tile the page with little mutual overlap;
        # same-size rects placed uniformly at random collide a lot.
        rects = []
        for m in lm_mats:
            a, dd = ad[m]
            if a[0] <= 0 or a[1] <= 0:
                continue
            rects.append((dd[0], dd[1], dd[0] + a[0], dd[1] + a[1]))

        def collide_frac(rs):
            """mean fraction of each rect's area covered by any other rect."""
            if len(rs) < 2:
                return 0.0
            fr = []
            for i, r in enumerate(rs):
                cov = 0.0
                area = max((r[2] - r[0]) * (r[3] - r[1]), 1e-12)
                for j, s in enumerate(rs):
                    if i == j:
                        continue
                    w = min(r[2], s[2]) - max(r[0], s[0])
                    h = min(r[3], s[3]) - max(r[1], s[1])
                    if w > 0 and h > 0:
                        cov += w * h
                fr.append(min(1.0, cov / area))
            return float(np.mean(fr))

        npr = np.random.default_rng(4416)
        null_coll = []
        arr = np.array(rects, np.float32)
        sizes = arr[:, 2:] - arr[:, :2]
        for _ in range(200):
            d0 = npr.uniform(0.0, np.maximum(1.0 - sizes[:, 0], 1e-6))
            d1 = npr.uniform(0.0, np.maximum(1.0 - sizes[:, 1], 1e-6))
            rs = list(zip(d0, d1, d0 + sizes[:, 0], d1 + sizes[:, 1]))
            null_coll.append(collide_frac(rs))
        ad_report["tile_overlap"] = dict(
            n_rects=len(rects),
            authored=round(collide_frac(rects), 4),
            null_mean=round(float(np.mean(null_coll)), 4),
            null_sd=round(float(np.std(null_coll)), 4))
        res["ad_null"] = ad_report
        res["per_segment"] = dict(
            fams=fams,
            val_plus40=[round(float(x), 4) for x in val_p40],
            val_v5=[round(float(x), 4) for x in val_v5],
            val_null_mean=[round(float(x), 4) for x in nv_mean],
            fp_dom=[round(float(x), 3) for x in fp_dom],
            fp_bbox=[round(float(x), 3) for x in fp_bbox],
        )
        report[islname] = res

        # ---------- stdout
        print(f"\n-- texel-validity (fraction of samples on non-empty texels)")
        print(f"  {'family':24s} {'n':>5s} {'+40':>7s} {'v5':>7s} {'null':>7s}")
        fams_order = sorted({f for f in fams})
        for f in fams_order:
            ii = [i for i in range(n) if fams[i] == f and su_list[i] is not None]
            if not ii:
                continue
            print(f"  {f:24s} {len(ii):5d} "
                  f"{val_p40[ii].mean():7.3f} {val_v5[ii].mean():7.3f} "
                  f"{nv_mean[ii].mean():7.3f}")
        ii = [i for i in range(n) if su_list[i] is not None]
        print(f"  {'ALL':24s} {len(ii):5d} "
              f"{val_p40[ii].mean():7.3f} {val_v5[ii].mean():7.3f} "
              f"{nv_mean[ii].mean():7.3f}")
        pa = res["popA_v5bound"]
        print(f"\n-- popA (v5 bound, +40 diffuse available): n={pa['n']}  "
              f"+40 {pa['plus40']:.3f}  v5 {pa['v5']:.3f}  null {pa['null']:.3f}"
              f"±{pa['null_sd']:.3f}  wins +40:{pa['plus40_wins']} v5:{pa['v5_wins']} "
              f"tie:{pa['tie']}")
        fp = res["footprint"]
        print(f"\n-- UV-footprint on atlas pages x atlas families "
              f"({len(fp['atlas_pages'])} pages): "
              f"dom95 +40 {fp['plus40_dom95']:.3f} vs null {fp['null_dom95']:.3f} | "
              f"bbox95 +40 {fp['plus40_bbox95']:.3f} vs null {fp['null_bbox95']:.3f}")
        ct = res["class_tightness"]
        print(f"\n-- class UV-rect tightness (union/max, atlas families):")
        print(f"   +40 : {ct['plus40']['n_classes']:3d} classes  "
              f"mean {ct['plus40']['mean_tight']}  median {ct['plus40']['median_tight']}  "
              f"frac>=0.7 {ct['plus40']['frac_ge07']}")
        print(f"   v5  : {ct['v5']['n_classes']:3d} classes  "
              f"mean {ct['v5']['mean_tight']}  median {ct['v5']['median_tight']}  "
              f"frac>=0.7 {ct['v5']['frac_ge07']}")
        print(f"   null: mean {ct['null']['mean']}±{ct['null']['sd']} "
              f"(k={ct['null']['k']})")
        print(f"\n-- (a,d) null: correct in-page {ad_report['correct']*100:.2f}% "
              f"(n={tot}); wrong-pair null {ad_report['null']['mean']*100:.2f}"
              f"%±{ad_report['null']['sd']*100:.2f} "
              f"[{ad_report['null']['min']*100:.1f}..{ad_report['null']['max']*100:.1f}] "
              f"(n_pairs={ad_report['null']['n_pairs']}); "
              f"d+a<=1 for {ok_pairs}/{len(lm_mats)} LM materials")
        to = ad_report["tile_overlap"]
        print(f"-- (a,d) tile-rect overlap ({to['n_rects']} rects): authored "
              f"{to['authored']*100:.1f}% vs null {to['null_mean']*100:.1f}"
              f"%±{to['null_sd']*100:.1f}%")

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
