#!/usr/bin/env python3
"""Round-7 ask 2 — slot 109/133 FIELD REINTERPRETATION for the ~440
LightMapDC records that are NOT the 14 explicit identity records.

Background (round-6): batch_info records (197 B, one per material) carry
vec3 f32 slots at 109/121/133/145.  For LightMapDC, (121,145) is the
validated Coord1 (lightmap) scaleoffset; (109,133) SHOULD be Coord0
(diffuse) by the shader's uniform pairing (Coord0_scaleoffset /
Coord1_scaleoffset, LightMapDC-v.glsl), but s109/s133 are <=1e-4 in
essentially all records except 14 (9 isl-1 tiles_*, 5 isl-2
Material__4986_*) where s109 = 1/65535 (u16 dequant) and s133 ~ 0.
If the engine really multiplied Coord0 by s109 ~ 1e-5, every street
diffuse UV would collapse to a point -- it does not (textured streets
under plain /65535).  So for the other ~440 records the float
scaleoffset reading is UNSUPPORTED.  This script tests the reviewer's
hypothesis: those bytes are not floats but u16/u8 groups, flags or
counts (bit patterns like 0x38b9fe4a "look like fields reinterpreted as
float"), using the per-technique contrast (NSO / StandardDiffuseDC carry
plausible floats at the same offsets).

Method:
  1. BYTE-ROLE CENSUS -- per byte offset 100..160, the cardinality of the
     byte across LightMapDC records (constant bytes = padding/flags;
     smooth bytes = float mantissa; jumpy bytes = small int fields).
     Same census for NSO as the contrast.
  2. INTERPRETATION TABLE -- for slots 109/133 (.x and .y u32s) of
     LightMapDC: cardinality + top bit patterns under f32 / 2xu16 /
     4xu8 / 2xf16; share of records whose u32 repeats; u16 small-int
     fractions.  Contrast: NSO + StandardDiffuseDC same table.
  3. CORRELATES -- do the u16 fields correlate with per-material
     attributes (segment count, |s121| bin, name family)?  Any record
     where u32@109 == u32@133?  Any u16 that equals the material's
     segment count or sampler count?
  4. HEX DUMPS -- full 197-byte records for m97 ( questioned), m90
     (compact anchor), m43 (tiles_* explicit-identity), one NSO record;
     annotated with the four vec3 f32 fields.

Outputs: extraction/re/round7_slot_bytes.json + stdout tables.
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import ISLANDS  # noqa
from round4_street_evidence import stem_of, m40_list  # noqa

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
DEQ = 1.0 / 65535.0


def raw_records(islname):
    d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    return [d[4 + stride * m: 4 + stride * (m + 1)] for m in range(M)]


def u32_at(rec, off):
    return struct.unpack_from("<I", rec, off)[0]


def views(u32):
    b = struct.pack("<I", u32)
    f = struct.unpack("<f", b)[0]
    lo, hi = struct.unpack("<2H", b)
    f16lo, f16hi = struct.unpack("<2e", b)
    return dict(f32=f, u16=(lo, hi), u8=tuple(b),
                f16=(float(f16lo), float(f16hi)),
                hex=b[::-1].hex().upper())


def f16_ok(x):
    return np.isfinite(x)


def interp_table(u32s):
    """Cardinality / repeat structure of a list of u32 values under
    different interpretations."""
    n = len(u32s)
    pats = collections.Counter(u32s)
    top = pats.most_common(4)
    u16lo = [views(v)["u16"][0] for v in u32s]
    u16hi = [views(v)["u16"][1] for v in u32s]
    f16s = [views(v)["f16"] for v in u32s]
    f16_bad = sum(1 for a, b in f16s
                  if not (f16_ok(a) and f16_ok(b)))
    return dict(
        n=n,
        n_distinct_u32=len(pats),
        repeat_share=round(1 - len(pats) / n, 3) if n else 0.0,
        top_u32=[dict(hex=views(v)["hex"], cnt=c,
                      f32=round(views(v)["f32"], 8),
                      u16=views(v)["u16"]) for v, c in top],
        u16lo_small_frac=round(sum(1 for x in u16lo if x < 1024) / n, 3),
        u16hi_small_frac=round(sum(1 for x in u16hi if x < 1024) / n, 3),
        u16lo_top=collections.Counter(u16lo).most_common(3),
        u16hi_top=collections.Counter(u16hi).most_common(3),
        f16_nonfinite_frac=round(f16_bad / n, 3) if n else 0.0,
        f32_med=round(float(np.median([views(v)["f32"] for v in u32s])), 8),
        f32_p90=round(float(np.percentile([abs(views(v)["f32"])
                                           for v in u32s], 90)), 8))


def byte_roles(recs, lo=100, hi=161):
    out = {}
    for off in range(lo, hi):
        col = collections.Counter(r[off] for r in recs)
        out[off] = (len(col), col.most_common(2))
    return out


def main():
    report = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        recs = raw_records(islname)
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        tech = [r.get("technique", "").split("-fx_")[0].lstrip("#")
                for r in rows]
        names = [r.get("name", f"m{m}") for m, r in enumerate(rows)]
        m40s = m40_list(islname)
        segcount = collections.Counter(m40s)
        M = len(recs)
        assert M == len(rows)

        lm = [m for m in range(M) if tech[m] == "LightMapDC"]
        nso = [m for m in range(M) if tech[m] == "NormalSpecOverbright"]
        sdd = [m for m in range(M) if tech[m] == "StandardDiffuseDC"]

        # the 14 explicit-identity records (s109.xy ~ dequant)
        idrecs = [m for m in lm
                  if abs(struct.unpack_from("<f", recs[m], 109)[0] - DEQ)
                  < 3e-7
                  and abs(struct.unpack_from("<f", recs[m], 113)[0] - DEQ)
                  < 3e-7]
        other = [m for m in lm if m not in idrecs]
        print(f"-- LightMapDC {len(lm)} records: {len(idrecs)} explicit "
              f"identity (s109=1/65535), {len(other)} OTHER (the "
              f"unexplained set)")

        # ---- 1. byte roles over LightMapDC + NSO contrast
        for label, subset in (("LightMapDC", lm), ("NormalSpecOverbright",
                                                   nso)):
            br = byte_roles([recs[m] for m in subset])
            const = [off for off, (card, top) in br.items() if card == 1]
            lowcard = [off for off, (card, top) in br.items() if 2 <= card <= 6]
            print(f"-- {label}: constant bytes {len(const)} "
                  f"{const[:14]}{'...' if len(const) > 14 else ''}; "
                  f"low-cardinality (2-6 values) bytes: {lowcard}")

        # ---- 2. interpretation tables
        groups = dict(LightMapDC_other=other, LightMapDC_identity=idrecs,
                      NSO=nso, StandardDiffuseDC=sdd)
        tables = {}
        for gname, ms in groups.items():
            if not ms:
                continue
            tables[gname] = {}
            print(f"\n-- interpretation table [{gname}] (n={len(ms)}):")
            print(f"   {'slot':5s} {'cmp':3s} {'distU32':>8s} {'repShr':>7s} "
                  f"{'u16<1024 lo/hi':>14s} {'f32 median':>12s} "
                  f"{'top u32 (hex, cnt, as f32, as u16)'}")
            for slot in (109, 121, 133, 145):
                for cmp_i, off in ((0, slot), (1, slot + 4)):
                    vals = [u32_at(recs[m], off) for m in ms]
                    t = interp_table(vals)
                    tables[gname][f"s{slot}_{cmp_i}"] = t
                    tu = t["top_u32"][0]
                    print(f"   s{slot:03d} x{cmp_i}  {t['n_distinct_u32']:8d} "
                          f"{t['repeat_share']:7.3f} "
                          f"{t['u16lo_small_frac']:.2f}/{t['u16hi_small_frac']:.2f} "
                          f"{t['f32_med']:12.3e}  "
                          f"{tu['hex']} x{tu['cnt']} f32={tu['f32']:.3e} "
                          f"u16={tu['u16']}")

        # ---- 3. correlates on the unexplained set
        oth = other
        u16lo109 = [views(u32_at(recs[m], 109))["u16"][0] for m in oth]
        u16hi109 = [views(u32_at(recs[m], 109))["u16"][1] for m in oth]
        segs_n = [segcount.get(m, 0) for m in oth]
        corr_lo = float(np.corrcoef(u16lo109, segs_n)[0, 1]) \
            if np.std(u16lo109) > 0 and np.std(segs_n) > 0 else None
        corr_hi = float(np.corrcoef(u16hi109, segs_n)[0, 1]) \
            if np.std(u16hi109) > 0 and np.std(segs_n) > 0 else None
        eq109_133 = sum(1 for m in oth
                        if u32_at(recs[m], 109) == u32_at(recs[m], 133))
        seg_eq = sum(1 for m, lo in zip(oth, u16lo109)
                     if lo == segcount.get(m, 0) and lo > 0)
        # joint (lo,hi) pairing repeats at 109
        pair109 = collections.Counter(zip(u16lo109, u16hi109))
        # byte histogram across the whole vec3 span, LightMapDC only
        print(f"\n-- correlates on the unexplained set (n={len(oth)}):")
        print(f"   corr(u16lo@109, n_segs) = {corr_lo and round(corr_lo, 3)}; "
              f"corr(u16hi@109, n_segs) = {corr_hi and round(corr_hi, 3)}")
        print(f"   records with u32@109 == u32@133: {eq109_133}")
        print(f"   records with u16lo@109 == n_segs (>0): {seg_eq}")
        print(f"   top (lo,hi) u16 pairs @109: {pair109.most_common(6)}")

        # ---- 4. hex dumps
        dumps = {}
        picks = [m for m in (97, 90, 43) if m < M and m in lm]
        if nso:
            picks.append(nso[0])
        for m in picks:
            rec = recs[m]
            f109 = struct.unpack_from("<3f", rec, 109)
            f121 = struct.unpack_from("<3f", rec, 121)
            f133 = struct.unpack_from("<3f", rec, 133)
            f145 = struct.unpack_from("<3f", rec, 145)
            dumps[m] = dict(
                name=names[m], tech=tech[m],
                hex_head=rec[:109].hex(),
                hex_vec3s=rec[109:157].hex(),
                hex_tail=rec[157:].hex(),
                s109=[round(v, 9) for v in f109],
                s121=[round(v, 9) for v in f121],
                s133=[round(v, 9) for v in f133],
                s145=[round(v, 9) for v in f145],
                s109_u16=[views(u32_at(rec, 109 + 4 * i))["u16"]
                          for i in range(3)],
                s133_u16=[views(u32_at(rec, 133 + 4 * i))["u16"]
                          for i in range(3)])
            print(f"\n-- hex dump m{m} [{names[m][:40]}] tech={tech[m]}")
            print(f"   s109 f32={[round(v, 8) for v in f109]} "
                  f"u16={dumps[m]['s109_u16']}")
            print(f"   s121 f32={[round(v, 8) for v in f121]}")
            print(f"   s133 f32={[round(v, 8) for v in f133]} "
                  f"u16={dumps[m]['s133_u16']}")
            print(f"   s145 f32={[round(v, 8) for v in f145]}")

        report[islname] = dict(
            lm_n=len(lm), identity_n=len(idrecs), other_n=len(oth),
            interp=tables, correlates=dict(
                corr_lo_segs=corr_lo and round(corr_lo, 3),
                corr_hi_segs=corr_hi and round(corr_hi, 3),
                eq109_133=eq109_133, seg_eq=seg_eq,
                top_pairs=[[list(k), v] for k, v in pair109.most_common(8)]),
            dumps={str(k): v for k, v in dumps.items()})

    json.dump(report, open(f"{RE}/round7_slot_bytes.json", "w"), indent=1)
    print(f"\nwrote {RE}/round7_slot_bytes.json")


if __name__ == "__main__":
    main()
