#!/usr/bin/env python3
"""T1/T2 — falsifiable tests of EF2raw (uv = w4_raw * s133 + s145) against
the shipped chain frac(w3_deq * s121 + s145) and permuted-slot nulls.

Engine-faithful per-class parse (validated vs Unicorn harness, 503/503):
pair slot j <-> descriptor j; TexCoord1 (attr 2) pair = (scale, offset).

Tests (per island, per chain):
  A containment : fraction of Coord1-bearing materials whose visited UV
                  rect lies inside [0,1]^2, vs permuted-pair null (K=100).
  B partition   : per bake page, total rect area (x page area) and mean
                  pairwise overlap, vs permuted-origins null (K=100).
  C spread      : for segment pairs >= 200u apart, fraction with
                  non-overlapping UV footprints, vs permuted-origins null.
Also: multi-wrap counts, T2 class census for segments, fixed-offset damage.
"""
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
ISLANDS = ("GothamCity", "GothamCity_Island2")
DEQ = 1.0 / 65535.0
rng = np.random.default_rng(20221013)


# ---------------------------------------------------------------- segments
def island_segments(islname):
    """Per segment: m40 (+40 material), w3, w4 raw u32 words, centroid xy,
    position extent. Mirrors export_zone.parse_island stride detection."""
    lt = open(f"{ZONE}/{islname}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{islname}/lod_data.bin", "rb").read()
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
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        w3 = words[:, 3].copy()          # attr1 TexCoord0 (byteOff 12)
        w4 = words[:, 4].copy() if stride >= 20 else None  # attr2 TexCoord1 (16)
        pos = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, stride // 4)[:, :3]
        out.append(dict(m40=m40, w3=w3, w4=w4, stride=stride,
                        cx=float(pos[:, 0].mean()), cy=float(pos[:, 1].mean()),
                        ext=float(max(np.ptp(pos[:, 0]), np.ptp(pos[:, 1])))))
    return out


def stem(s):
    if not s or s == "UNBOUND":
        return None
    s = str(s)
    low = s.lower()
    for ext in (".tga", ".png", ".jpg"):
        if low.endswith(ext):
            return s[:-len(ext)]
    return s


def uvs_of(w_raw, scale, offset, wrap):
    """raw u32 word -> (u, v) under uv = raw_deq_or_raw * scale + offset."""
    u16 = (w_raw & 0xFFFF).astype(np.float64)
    v16 = (w_raw >> 16).astype(np.float64)
    if scale is None:                      # identity: plain dequant
        pu, pv = u16 * DEQ, v16 * DEQ
    else:
        pu = u16 * scale[0] + offset[0]
        pv = v16 * scale[1] + offset[1]
    if wrap:
        pu = np.mod(pu, 1.0)
        pv = np.mod(pv, 1.0)
    return pu, pv


def rect_inside(pu, pv, eps=1e-6):
    return (pu.min() >= -eps) and (pu.max() <= 1 + eps) and \
           (pv.min() >= -eps) and (pv.max() <= 1 + eps)


def wraps_count(pu, pv):
    """Multi-wrap = per-axis span (unwrapped) exceeding 1.0."""
    su = pu.max() - pu.min()
    sv = pv.max() - pv.min()
    return int(su > 1.0 or sv > 1.0)


def main():
    result = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        recs = __import__("batch_parser").parse_island(islname)
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        segs = island_segments(islname)
        print(f"segments: {len(segs)}")

        # ---- T2: class census over SEGMENTS (via material class)
        segcls = {}
        for s in segs:
            m = s["m40"]
            if m < len(recs):
                rec = recs[m]
                cls = (rec["n"], rec["K"])
            else:
                cls = ("oob",)
            segcls[cls] = segcls.get(cls, 0) + 1
        print(f"segment (N,K) census: {dict(sorted(segcls.items(), key=str))}")
        # T2 damage: segments whose material lacks TexCoord1 (K<2 attr2) but
        # would still get uv1 from the fixed-offset exporter if lm-bound
        dmg = 0
        lm_bound = 0
        for s_ in segs:
            m = s_["m40"]
            if m >= len(recs):
                continue
            rec = recs[m]
            has_t1 = any(dd["attr"] == 2 for dd in rec["descs"])
            lm = stem(rows[m].get("LightMap")) if m < len(rows) else None
            if lm:
                lm_bound += 1
                if not has_t1:
                    dmg += 1
        print(f"lm-bound segments: {lm_bound}; of those WITHOUT TexCoord1 "
              f"(exporter uv1 = garbage fixed-offset bytes): {dmg} "
              f"({dmg / max(lm_bound, 1) * 100:.1f}%)")
        result.setdefault(islname, {})["t2_damage"] = dict(
            lm_bound=lm_bound, garbage_uv1=dmg)

        # ---- group segments by material
        bymat = {}
        for si, s in enumerate(segs):
            bymat.setdefault(s["m40"], []).append(si)

        # ---- Coord1-bearing materials: attr2 present + LightMap bound
        t1mats = []
        for m, rec in enumerate(recs):
            t1i = next((i for i, dd in enumerate(rec["descs"])
                        if dd["attr"] == 2), None)
            lm = stem(rows[m].get("LightMap")) if m < len(rows) else None
            if t1i is not None and lm and m in bymat:
                t1mats.append((m, t1i, lm, rec))
        print(f"TexCoord1-bearing materials with LightMap + segments: "
              f"{len(t1mats)}")

        # ---- chains
        def chain_uv(rec, t1i, w4, mode):
            sc, of = rec["pairs"][t1i]
            if mode == "EF2raw":
                return uvs_of(w4, (sc[0], sc[1]), (of[0], of[1]), wrap=False)
            if mode == "EF2wrap":
                return uvs_of(w4, (sc[0], sc[1]), (of[0], of[1]), wrap=True)
            if mode == "shipped":
                # fixed bytes: s121 = pairs[1].offset, s145 = pairs[2].offset
                s121 = rec["pairs"][1][1] if len(rec["pairs"]) > 1 else (0, 0, 0)
                s145 = rec["pairs"][2][1] if len(rec["pairs"]) > 2 else (0, 0, 0)
                return uvs_of(w4, None, None, wrap=False)  # placeholder
            raise ValueError(mode)

        def shipped_uv(rec, w3):
            s121 = rec["pairs"][1][1] if len(rec["pairs"]) > 1 else (0, 0, 0)
            s145 = rec["pairs"][2][1] if len(rec["pairs"]) > 2 else (0, 0, 0)
            return uvs_of(w3, (s121[0], s121[1]), (s145[0], s145[1]), wrap=True)

        # material-level uv cache per chain
        data = {}
        for m, t1i, lm, rec in t1mats:
            ws = [segs[si]["w4"] for si in bymat[m]]
            w3s = [segs[si]["w3"] for si in bymat[m]]
            w4 = np.concatenate(ws)
            w3 = np.concatenate(w3s)
            sc, of = rec["pairs"][t1i]
            ef_u, ef_v = uvs_of(w4, (sc[0], sc[1]), (of[0], of[1]), wrap=False)
            s121 = rec["pairs"][1][1] if len(rec["pairs"]) > 1 else (0, 0, 0)
            s145 = rec["pairs"][2][1] if len(rec["pairs"]) > 2 else (0, 0, 0)
            sh_u, sh_v = uvs_of(w3, (s121[0], s121[1]), (s145[0], s145[1]),
                                wrap=False)
            id_u, id_v = uvs_of(w4, None, None, wrap=False)
            data[m] = dict(lm=lm, ef=(ef_u, ef_v), sh=(sh_u, sh_v),
                           id=(id_u, id_v), rec=rec, t1i=t1i,
                           segs=list(bymat[m]),
                           cents=np.array([[segs[si]["cx"], segs[si]["cy"]]
                                           for si in bymat[m]]))
        ms = list(data)

        # ================= A. containment
        def containment(chains):
            out = {}
            for cname in chains:
                ins = tot = 0
                for m in ms:
                    pu, pv = data[m][cname]
                    tot += 1
                    ins += rect_inside(pu, pv)
                out[cname] = (ins, tot, ins / max(tot, 1))
            return out

        cont_obs = containment(["ef", "sh", "id"])
        # null: permute (scale,offset) pairs across materials
        pairpool = [(data[m]["rec"]["pairs"][data[m]["t1i"]]) for m in ms]
        NS = 100
        null_in = dict(ef=[], id=[])
        for pi in range(NS):
            perm = rng.permutation(len(ms))
            for cname, use_w in (("ef", "w4"), ("id", "w4")):
                ins = 0
                for j, m in enumerate(ms):
                    sc, of = pairpool[perm[j]]
                    pu, pv = uvs_of(np.concatenate([segs[si]["w4"] for si in bymat[m]]),
                                    (sc[0], sc[1]), (of[0], of[1]), wrap=False)
                    ins += rect_inside(pu, pv)
                null_in[cname].append(ins / max(len(ms), 1))
        print("\n-- A. containment (fraction of materials inside [0,1]^2)")
        arow = {}
        for cname, label in (("ef", "EF2raw"), ("sh", "shipped"),
                             ("id", "identity")):
            ins, tot, frac = cont_obs[cname]
            line = f"   {label:9s}: {ins}/{tot} = {frac:.3f}"
            if cname in null_in and np.std(null_in[cname]) > 0:
                mu_, sd_ = float(np.mean(null_in[cname])), float(np.std(null_in[cname]))
                z = (frac - mu_) / sd_ if sd_ > 0 else None
                line += f"   null {mu_:.3f}+/-{sd_:.3f} z={z if z is None else round(z, 2)}"
            elif cname in null_in:
                line += f"   null {float(np.mean(null_in[cname])):.3f}+/-0.0 z=not computable"
            print(line)
            arow[label] = dict(ins=ins, tot=tot, frac=frac,
                               null=(float(np.mean(null_in[cname])),
                                     float(np.std(null_in[cname])))
                               if cname in null_in else None)
        result.setdefault(islname, {})["containment"] = arow

        # multi-wrap census
        for cname, label in (("ef", "EF2raw"), ("sh", "shipped"),
                             ("id", "identity")):
            wc = sum(wraps_count(*data[m][cname]) for m in ms)
            print(f"   {label:9s} multi-wrap materials: {wc}/{len(ms)}")

        # ================= B. partition (per bake page)
        pages = {}
        for m in ms:
            pages.setdefault(data[m]["lm"], []).append(m)
        print(f"\n-- B. partition over {len(pages)} bake pages")

        def page_metrics(rects):
            """rects: list of (u0, v0, u1, v1). Returns (total_area,
            mean pairwise overlap/min-area)."""
            ta = sum(max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1])
                     for r in rects)
            ovs = []
            for i in range(len(rects)):
                for j in range(i + 1, len(rects)):
                    a, b = rects[i], rects[j]
                    iw = min(a[2], b[2]) - max(a[0], b[0])
                    ih = min(a[3], b[3]) - max(a[1], b[1])
                    if iw > 0 and ih > 0:
                        amin = min((a[2] - a[0]) * (a[3] - a[1]),
                                   (b[2] - b[0]) * (b[3] - b[1]))
                        if amin > 0:
                            ovs.append(iw * ih / amin)
            return ta, (float(np.mean(ovs)) if ovs else 0.0), len(ovs)

        def chain_rects(cname):
            out = {}
            for pg, pms in pages.items():
                rs = []
                for m in pms:
                    pu, pv = data[m][cname]
                    rs.append((pu.min(), pv.min(), pu.max(), pv.max()))
                out[pg] = rs
            return out

        for cname, label in (("ef", "EF2raw"), ("sh", "shipped"),
                             ("id", "identity")):
            rects = chain_rects(cname)
            tas, ovs = [], []
            for pg, rs in rects.items():
                if len(rs) >= 2:
                    ta, ov, npair = page_metrics(rs)
                    tas.append(ta)
                    ovs.append(ov)
            print(f"   {label:9s}: pages(n>=2 mats)={len(tas)} "
                  f"total-area median={np.median(tas):.2f}x "
                  f"mean-overlap median={np.median(ovs):.3f}" if tas else
                  f"   {label:9s}: no multi-material pages")
            result.setdefault(islname, {}).setdefault(
                "partition", {})[label] = dict(
                pages=len(tas),
                total_area_median=float(np.median(tas)) if tas else None,
                overlap_median=float(np.median(ovs)) if ovs else None)
        # null for EF2raw partition: permuted origins (keep sizes)
        NS2 = 50
        null_ta, null_ov = [], []
        rect_sizes = {}
        for pg, pms in pages.items():
            rect_sizes[pg] = [((data[m]['ef'][0].max() - data[m]['ef'][0].min()),
                               (data[m]['ef'][1].max() - data[m]['ef'][1].min()))
                              for m in pms]
        for pi in range(NS2):
            tas, ovs = [], []
            for pg, pms in pages.items():
                if len(pms) < 2:
                    continue
                w_, h_ = zip(*rect_sizes[pg])
                origins_u = rng.permutation(
                    np.array([data[m]['ef'][0].min() for m in pms]))
                origins_v = rng.permutation(
                    np.array([data[m]['ef'][1].min() for m in pms]))
                rs = [(origins_u[i], origins_v[i],
                       origins_u[i] + w_[i], origins_v[i] + h_[i])
                      for i in range(len(pms))]
                ta, ov, _ = page_metrics(rs)
                tas.append(ta)
                ovs.append(ov)
            null_ta.append(np.median(tas))
            null_ov.append(np.median(ovs))
        z_ta = z_ov = None
        if np.std(null_ta) > 0:
            z_ta = (result[islname]["partition"]["EF2raw"]["total_area_median"]
                    - np.mean(null_ta)) / np.std(null_ta)
        if np.std(null_ov) > 0:
            z_ov = (result[islname]["partition"]["EF2raw"]["overlap_median"]
                    - np.mean(null_ov)) / np.std(null_ov)
        print(f"   EF2raw nulls: total-area {np.mean(null_ta):.2f}"
              f"+/-{np.std(null_ta):.2f} (z={'nc' if z_ta is None else round(z_ta, 2)}), "
              f"overlap {np.mean(null_ov):.3f}+/-{np.std(null_ov):.3f} "
              f"(z={'nc' if z_ov is None else round(z_ov, 2)})")
        result[islname]["partition_null"] = dict(
            ta=(float(np.mean(null_ta)), float(np.std(null_ta)), z_ta),
            ov=(float(np.mean(null_ov)), float(np.std(null_ov)), z_ov))

        # ================= C. per-segment spread
        print("\n-- C. per-segment spread (pairs >= 200u apart)")
        def spread(cname, minsep=200.0):
            nonov = tot = 0
            for m in ms:
                C = data[m]["cents"]
                pu, pv = data[m][cname]
                ns = len(C)
                if ns < 2:
                    continue
                # per-segment uv rects
                rs = []
                ofs = 0
                for si in data[m]["segs"]:
                    nv = len(segs[si]["w4"])
                    r = (pu[ofs:ofs + nv].min(), pv[ofs:ofs + nv].min(),
                         pu[ofs:ofs + nv].max(), pv[ofs:ofs + nv].max())
                    rs.append(r)
                    ofs += nv
                for i in range(ns):
                    for j in range(i + 1, ns):
                        d = float(np.hypot(*(C[i] - C[j])))
                        if d < minsep:
                            continue
                        tot += 1
                        a, b = rs[i], rs[j]
                        if (a[2] < b[0]) or (b[2] < a[0]) or \
                           (a[3] < b[1]) or (b[3] < a[1]):
                            nonov += 1
            return nonov, tot

        for cname, label in (("ef", "EF2raw"), ("sh", "shipped")):
            nonov, tot = spread(cname)
            frac = nonov / max(tot, 1)
            line = (f"   {label:9s}: {nonov}/{tot} = {frac:.3f} "
                    f"non-overlapping footprints")
            null_fracs = []
            if cname == "ef":
                for _ in range(30):
                    n2 = 0
                    for m in ms:
                        C = data[m]["cents"]
                        pu, pv = data[m][cname]
                        ns = len(C)
                        if ns < 2:
                            continue
                        rs = []
                        ofs = 0
                        for si in data[m]["segs"]:
                            nv = len(segs[si]["w4"])
                            w_ = pu[ofs:ofs+nv].max() - pu[ofs:ofs+nv].min()
                            h_ = pv[ofs:ofs+nv].max() - pv[ofs:ofs+nv].min()
                            o_ = rng.uniform(0, 1 - max(w_, 1e-9))
                            p_ = rng.uniform(0, 1 - max(h_, 1e-9))
                            rs.append((o_, p_, o_ + w_, p_ + h_))
                            ofs += nv
                        for i in range(ns):
                            for j in range(i + 1, ns):
                                d = float(np.hypot(*(C[i] - C[j])))
                                if d < 200.0:
                                    continue
                                a, b = rs[i], rs[j]
                                if (a[2] < b[0]) or (b[2] < a[0]) or \
                                   (a[3] < b[1]) or (b[3] < a[1]):
                                    n2 += 1
                    tt = spread("ef")[1]
                    null_fracs.append(n2 / max(tt, 1))
                mu_, sd_ = float(np.mean(null_fracs)), float(np.std(null_fracs))
                z = (frac - mu_) / sd_ if sd_ > 0 else None
                line += (f"   null {mu_:.3f}+/-{sd_:.3f} "
                         f"z={'nc' if z is None else round(z, 2)}")
                result.setdefault(islname, {}).setdefault(
                    "spread", {})["EF2raw_null"] = (mu_, sd_, z)
            print(line)
            result.setdefault(islname, {}).setdefault(
                "spread", {})[label] = dict(nonov=nonov, tot=tot, frac=frac)

        # ---- diffuse coherence: per-segment v-span under engine diffuse
        # (w3 x s109 + s121) vs shipped diffuse (w4 dequant)
        print("\n-- D. diffuse v-span coherence (road-family band atlas)")
        for label, use_engine in (("engine w3*s109+s121", True),
                                  ("shipped w4 dequant", False)):
            spans = []
            for m, t1i, lm, rec in t1mats:
                t0i = next((i for i, dd in enumerate(rec["descs"])
                            if dd["attr"] == 1), None)
                if t0i is None:
                    continue
                sc, of = rec["pairs"][t0i]
                for si in bymat[m]:
                    w3 = segs[si]["w3"]
                    w4 = segs[si]["w4"]
                    if use_engine:
                        u16 = (w3 & 0xFFFF).astype(np.float64)
                        v16 = (w3 >> 16).astype(np.float64)
                        pv = v16 * sc[1] + of[1]
                        pv = np.mod(pv, 1.0)
                    else:
                        pv = ((w4 >> 16).astype(np.float64)) * DEQ
                    spans.append(float(np.ptp(pv)))
            spans = np.array(spans)
            print(f"   {label:22s}: median v-span {np.median(spans):.3f} "
                  f"p10 {np.percentile(spans, 10):.3f} "
                  f"p90 {np.percentile(spans, 90):.3f}")

    class NpEnc(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (np.integer,)):
                return int(o)
            if isinstance(o, (np.floating,)):
                return float(o)
            return super().default(o)
    json.dump(result, open("/home/z/my-project/work/t1_results.json", "w"),
              indent=1, cls=NpEnc)
    print("\nwrote /home/z/my-project/work/t1_results.json")


if __name__ == "__main__":
    main()
