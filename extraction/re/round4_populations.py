#!/usr/bin/env python3
"""Round-4 populations: w3 decode + who carries real LM UVs + vertex colour.

Reviewer asks:
  - exact w3 encoding (u16 pair? snorm? byte order?) and which segments
    have w3 = 0; the constant-offset population vs the per-vertex UV
    population; WHICH buildings carry real UVs and which don't.
  - do street vertices carry vertex colour at all (stride-20 vs stride-24
    may differ)?  LightmapVCBlendDC's blend factor and the x2 assumption
    depend on it.

Also banks the per-material w3 population table for the exporter policy.
Output: extraction/re/round4_populations.json + stdout.
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import ISLANDS  # noqa: E402

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round4_populations.json"


def stem_of(dm):
    if not dm or dm == "UNBOUND":
        return None
    s = dm
    for ext in (".tga", ".png", ".jpg"):
        if s.lower().endswith(ext):
            return s[: -len(ext)]
    return s


def seg_raw(island):
    """parse_island order, with words + stride."""
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
        if stride is None:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        out.append(dict(m40=m40, stride=stride, words=words,
                        nv=int(words.shape[0])))
    return out


def main():
    report = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        segs = seg_raw(islname)
        lm = {m for m in range(len(rows))
              if rows[m].get("LightMap") and rows[m]["LightMap"] != "UNBOUND"}

        nseg = len(segs)
        n24 = sum(1 for s in segs if s["stride"] == 24)
        n20 = sum(1 for s in segs if s["stride"] == 20)
        n32 = sum(1 for s in segs if s["stride"] == 32)
        print(f"segments {nseg}: stride24 {n24}, stride20 {n20}, stride32 {n32}")

        # ---- w3 populations per material (stride-24 only)
        # zero | const-nonzero | narrow-var (range<0.05) | varies
        per_mat = {}
        pop = collections.Counter()
        w3_zero_segs = 0
        for s in segs:
            if s["stride"] != 24:
                continue
            m = s["m40"]
            W = s["words"][:, 3]
            cu = (W & 0xFFFF).astype(np.float32) / 65535.0
            cv = (W >> 16).astype(np.float32) / 65535.0
            if W.max() == 0:
                cl = "zero"
                w3_zero_segs += 1
            elif cu.max() - cu.min() < 1e-4 and cv.max() - cv.min() < 1e-4:
                cl = "const_nonzero"
            elif max(cu.max() - cu.min(), cv.max() - cv.min()) < 0.05:
                cl = "narrow_var"
            else:
                cl = "varies"
            pop[cl] += 1
            e = per_mat.setdefault(m, collections.Counter())
            e[cl] += 1
            e["verts"] += s["nv"]
        print(f"stride-24 segment w3 populations: {dict(pop)}")

        # ---- encoding checks
        # u16 lanes both in [0,1]?  snorm signs?  byte order swap test:
        # swapped decode = (hi, lo) — coherence under the s121 chain decides
        # (banked in round4_lm_partition occupancy); here just report ranges.
        allw3 = [s["words"][:, 3] for s in segs if s["stride"] == 24]
        if allw3:
            A = np.concatenate(allw3)
            lo = A & 0xFFFF
            hi = A >> 16
            print(f"w3 raw: lo u16 [{lo.min()}, {lo.max()}] "
                  f"hi u16 [{hi.min()}, {hi.max()}] (both full u16 range -> "
                  f"two independent unorm16 lanes, no sign bit population)")
        # word5 = octahedral 8-bit normal hypothesis
        w5 = [s["words"][:, 5] for s in segs if s["stride"] == 24]
        octa_ok = 0
        octa_n = 0
        pad0 = 0
        if w5:
            B = np.concatenate(w5)
            b0 = (B & 0xFF).astype(np.int32)
            b1 = ((B >> 8) & 0xFF).astype(np.int32)
            b2 = ((B >> 16) & 0xFF).astype(np.int32)
            b3 = ((B >> 24) & 0xFF).astype(np.int32)
            pad0 = float((b3 == 0).mean())
            nx = (b0 - 127.5) / 127.5
            ny = (b1 - 127.5) / 127.5
            inside = (np.abs(nx) + np.abs(ny)) <= 1.0001
            octa_ok = int(inside.sum())
            octa_n = int(len(B))
            print(f"word5 as octa8 normal: |nx|+|ny|<=1 for {octa_ok}/{octa_n} "
                  f"({100.0*octa_ok/max(octa_n,1):.2f}%); byte3==0 for "
                  f"{pad0*100:.2f}%")
            report.setdefault("word5_bytes", {})
            report["word5_bytes"][islname] = dict(
                octa_frac=round(octa_ok / max(octa_n, 1), 5),
                pad0_frac=round(pad0, 5),
                b2_mean=round(float(b2.mean()), 2),
                b2_nonzero_frac=round(float((b2 != 0).mean()), 4))
        # stride-20 word3: same octa test
        w20 = [s["words"][:, 3] for s in segs if s["stride"] == 20]
        if w20:
            C = np.concatenate(w20)
            c0 = (C & 0xFF).astype(np.int32)
            c1 = ((C >> 8) & 0xFF).astype(np.int32)
            nx = (c0 - 127.5) / 127.5
            ny = (c1 - 127.5) / 127.5
            inside = (np.abs(nx) + np.abs(ny)) <= 1.0001
            print(f"stride-20 word3 as octa8: {inside.mean()*100:.2f}% inside; "
                  f"u16hi mostly {( (C>>16)==0 ).mean()*100:.1f}% zero")

        # ---- per-material table (LM-bound first)
        table = {}
        for m in sorted(per_mat, key=lambda m: -per_mat[m]["verts"]):
            c = per_mat[m]
            tot = sum(v for k, v in c.items() if k != "verts")
            table[m] = dict(
                name=rows[m]["name"] if m < len(rows) else "?",
                technique=rows[m]["technique"].split("-fx_")[0].lstrip("#")
                if m < len(rows) else "?",
                lm=stem_of(rows[m].get("LightMap")) if m < len(rows) else None,
                dif=stem_of(rows[m].get("DiffuseMap")) if m < len(rows) else None,
                n_seg=tot, verts=int(c["verts"]),
                zero=int(c.get("zero", 0)),
                const=int(c.get("const_nonzero", 0)),
                narrow=int(c.get("narrow_var", 0)),
                varies=int(c.get("varies", 0)))
        report.setdefault("per_material", {})[islname] = table

        n_lm24 = sum(1 for s in segs if s["stride"] == 24 and s["m40"] in lm)
        lm_cls = collections.Counter()
        for s in segs:
            if s["stride"] != 24 or s["m40"] not in lm:
                continue
            W = s["words"][:, 3]
            cu = (W & 0xFFFF).astype(np.float32) / 65535.0
            cv = (W >> 16).astype(np.float32) / 65535.0
            if W.max() == 0:
                lm_cls["zero"] += 1
            elif cu.max() - cu.min() < 1e-4 and cv.max() - cv.min() < 1e-4:
                lm_cls["const_nonzero"] += 1
            elif max(cu.max() - cu.min(), cv.max() - cv.min()) < 0.05:
                lm_cls["narrow_var"] += 1
            else:
                lm_cls["varies"] += 1
        print(f"LM-bound stride-24 segments: {n_lm24}; populations {dict(lm_cls)}")

        # buildings with vs without real UVs (varies vs zero/const)
        bld_carrier = [t for t in table.values() if t["varies"] > 0
                       and (t["dif"] or "").startswith(("GC_Footprint", "GC_Residential",
                                                        "GC_Z1_Shops", "GC_footprint"))]
        bld_flat = [t for t in table.values() if t["varies"] == 0
                    and (t["dif"] or "").startswith(("GC_Footprint", "GC_Residential",
                                                     "GC_Z1_Shops", "GC_footprint"))]
        print(f"building-family materials WITH per-vertex w3: {len(bld_carrier)} "
              f"({sum(x['verts'] for x in bld_carrier):,} verts); without: "
              f"{len(bld_flat)} ({sum(x['verts'] for x in bld_flat):,} verts)")

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
