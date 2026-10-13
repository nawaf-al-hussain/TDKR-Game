#!/usr/bin/env python3
"""Engine-faithful batch_info.bin parser (pure Python) + cross-validation
against the Unicorn harness run (harness_lhs.json).

Layout (derived from loadHeadersAndSkipData @0x8e1d34 disassembly and
verified by emulation of all 503 records):
  [u16 self][30 attr bytes][u8][u32le N]
  [N x 12B desc: u32 byteOff; u16 attrId; u16 f2; u16 f3; u16 stride]
  [(K+1) x 24B pair (vec3f scale, vec3f offset)]   K = popcount(mask & 0xFFFE)
  [u32 X][seek X*desc0.stride][24B tail {t0,kind,count,t3,t4,t5}]
Pair slot j <-> descriptor j (parallel to CVertexStreams streams array).
Attrs with id >= 16 (Normal/Color0) get no pair.
"""
import json
import struct

ZONE = "/home/z/my-project/work/zone"


def parse_record(rec):
    selfidx = struct.unpack_from("<H", rec, 0)[0]
    n = struct.unpack_from("<I", rec, 33)[0]
    descs = []
    mask = 0
    for k in range(n):
        f0, f1, f2, f3, f4 = struct.unpack_from("<IHHHH", rec, 37 + 12 * k)
        descs.append(dict(byteOff=f0, attr=f1, f2=f2, f3=f3, stride=f4))
        mask |= 1 << (f1 & 0x1F)
    K = bin(mask & 0xFFFE).count("1")
    pstart = 37 + 12 * n
    pairs = []
    for j in range(K + 1):
        sc = struct.unpack_from("<3f", rec, pstart + 24 * j)
        of = struct.unpack_from("<3f", rec, pstart + 24 * j + 12)
        pairs.append((sc, of))
    xoff = pstart + 24 * (K + 1)
    X = struct.unpack_from("<I", rec, xoff)[0]
    tail_at = xoff + 4 + X * (descs[0]["stride"] if descs else 24)
    tail = struct.unpack_from("<6I", rec, tail_at)
    return dict(selfidx=selfidx, n=n, descs=descs, mask=mask, K=K,
                pairs=pairs, X=X, tail=tail, tail_at=tail_at,
                attrbytes=rec[2:32])


def parse_island(islname):
    d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    return [parse_record(d[4 + stride * m: 4 + stride * (m + 1)])
            for m in range(M)]


def main():
    hj = json.load(open("/home/z/my-project/work/harness_lhs.json"))
    report = {}
    for isl, per in hj.items():
        mine = parse_island(isl)
        assert len(mine) == len(per), (isl, len(mine), len(per))
        mism = 0
        K_mismatch = []
        for m, (rec, eng) in enumerate(zip(mine, per)):
            slots = eng["pairs"] or []
            if rec["K"] + 1 != len(slots):
                K_mismatch.append(m)
                mism += 1
                continue
            for j, slot in enumerate(slots):
                sc, of = rec["pairs"][j]
                got = [round(v, 9) for v in (sc + of)]
                if any(abs(a - b) > 1e-6 for a, b in zip(got, slot)):
                    mism += 1
                    break
        # extra: X and tail sanity
        bad_tail = [m for m, rec in enumerate(mine)
                    if rec["tail_at"] + 24 > 197]
        report[isl] = dict(records=len(mine), pair_mismatches=mism,
                           K_slot_mismatch_records=K_mismatch[:10],
                           tail_overflow=bad_tail[:10])
        print(f"{isl}: {len(mine)} records, pair mismatches vs engine: {mism}"
              f", K+1-slot mismatches: {len(K_mismatch)}"
              f", tail-overflow records: {len(bad_tail)}")
    json.dump(report, open("/home/z/my-project/work/parser_validation.json", "w"),
              indent=1)

    # class census (T2 part 1) — per island
    print("\n-- (N, K) class census --")
    for isl in ("GothamCity", "GothamCity_Island2"):
        mine = parse_island(isl)
        from collections import Counter
        cls = Counter((rec["n"], rec["K"]) for rec in mine)
        order = Counter(tuple(dd["attr"] for dd in rec["descs"])
                        for rec in mine)
        print(f"{isl}: classes (N,K): {dict(sorted(cls.items()))}")
        print(f"  descriptor attr orders: "
              f"{dict(sorted(order.items(), key=lambda kv: -kv[1])[:6])}")
        # TexCoord1 descriptor index distribution
        t1 = Counter(next((i for i, dd in enumerate(rec["descs"])
                           if dd["attr"] == 2), -1) for rec in mine)
        t1w = Counter(next((dd["byteOff"] for dd in rec["descs"]
                            if dd["attr"] == 2), None) for rec in mine)
        t0w = Counter(next((dd["byteOff"] for dd in rec["descs"]
                            if dd["attr"] == 1), None) for rec in mine)
        print(f"  TexCoord1 desc index dist: {dict(sorted(t1.items(), key=str))}")
        print(f"  TexCoord1 byteOff dist: {dict(sorted(t1w.items(), key=str))}")
        print(f"  TexCoord0 byteOff dist: {dict(sorted(t0w.items(), key=str))}")


if __name__ == "__main__":
    main()
