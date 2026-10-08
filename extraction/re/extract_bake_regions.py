#!/usr/bin/env python3
"""Extract exact per-footprint bake regions from the zone bake-group streams.

Format (reverse-engineered, GothamCity.lvc / GothamCity_Island2.lvc zone
object streams — byte-packed, all fields BIG-ENDIAN):

  ... [BE u32 strIdx 'BakeGroup_<isle>_<G>.tga']      <- bake page (runtime target)
      [f32 u0][f32 v0][f32 u1][f32 v1]                <- EXACT bake region in page
      [BE u32 strIdx 'BakeGroup_<isle>_<G>0.tga']     <- SHIPPED page ('-0' suffix on disk)
      [u32 1024][u32 512][s32 -1]                     <- atlas sizes / empty string
      ... [u32 0x00018785 / 0x0001869f]               <- component hash
      [u8 1][u32 objectId][f32 pos*3][f32 rot*3][f32 scale*3]
      [u32 strIdx '<gc_footprint_xx>.bdae'][4 x u8]   <- mesh component (CreateObject
                                                       hash 0x152b87: ReadString + 4 bools)
      [u32 strIdx '<...>_collision.bdae'][4 x u8]

Whole-page bakes carry (2, 2, ...) density floats instead of a unit rect.

Association: first non-collision, non-placeholder, non-batman bdae string in
the window [pageRef-40, atlasLowRef+160] — that is the record's mesh.

Output: extraction/re/bake_regions.json
"""
import struct, json, re, sys

NOISE = re.compile(r'collision|placeholder|batman|reflection|staticmesh', re.I)

def load(lvcname):
    d = open(f'/home/z/my-project/download/TDKR_assets/raw/game_config/{lvcname}.lvc', 'rb').read()
    tbl_off = struct.unpack_from('>I', d, 4)[0]
    p = tbl_off; cnt = struct.unpack_from('>I', d, p)[0]; p += 4
    strings = []
    for _ in range(cnt):
        ln = struct.unpack_from('>I', d, p)[0]; p += 4
        strings.append(d[p:p + ln].decode('utf-8', 'replace')); p += ln
    return d, tbl_off, cnt, strings

def beidx(d, o, cnt):
    if o < 0 or o + 4 > len(d): return None
    v = struct.unpack_from('>I', d, o)[0]
    return v if 0 <= v < cnt else None

def extract(lvcname):
    d, tbl_off, cnt, strings = load(lvcname)
    bakes = [i for i, s in enumerate(strings) if s.startswith('BakeGroup')]
    low_re = re.compile(r'ATLAS_low0?\.tga$')
    rows = []
    for bi in bakes:
        s = strings[bi]
        pat = struct.pack('>I', bi)
        o = 9
        while True:
            o = d.find(pat, o, tbl_off)
            if o < 0: break
            rect = [struct.unpack_from('>f', d, o + 4 + k * 4)[0] for k in range(4)]
            nxt = beidx(d, o + 20, cnt)
            is_low = bool(low_re.search(s))
            # find mesh bdae: the record's mesh component string sits at a
            # fixed offset: page+84 = atlasLow(+20) + 1024(+24) + 512(+28) +
            # (-1)(+32) + hash(+36) + 01(+40) + id(+41) + 12 floats(+45..92)
            # + bool(+93) -> mesh str @+94?? (gf measured +84; field count
            # varies) -> scan [+82,+94] exact first, then [+60,+110] with
            # gc_/-prefix preference over library hc_ props.
            mesh = None
            cands = []
            for dq in range(60, 111):
                v = beidx(d, o + dq, cnt)
                if v is not None:
                    cand = strings[v]
                    if cand.endswith('.bdae') and not NOISE.search(cand):
                        cands.append((dq, cand))
            for pref in (84, 85, 83, 86, 82):
                for dq, cand in cands:
                    if dq == pref:
                        mesh = cand
                        break
                if mesh: break
            if mesh is None:
                for dq, cand in cands:
                    if cand.startswith(('gc_', 'island', 'water', 'bridge')):
                        mesh = cand
                        break
            if mesh is None and cands:
                mesh = cands[0][1]
            rows.append(dict(off=o, page=s, is_low_page=is_low, rect=rect,
                             nxt=strings[nxt] if nxt else None, mesh=mesh))
            o += 1
    # group: a "record" = (page,atlas_low) pair; keep pairs whose mesh resolved
    def valid_rect(f):
        return (all(-0.002 <= v <= 1.002 for v in f) and f[2] > f[0] and f[3] > f[1]
                and (f[2] - f[0]) > 0.002 and (f[3] - f[1]) > 0.002)
    out = []
    for r in rows:
        if r['is_low_page']:
            continue
        nxt = r['nxt'] if (r['nxt'] and 'ATLAS_low' in r['nxt']) else None
        if r['mesh'] is None:
            continue
        rect = r['rect']
        if valid_rect(rect):
            out.append(dict(lvc=lvcname, page=r['page'], page_shipped=nxt,
                            rect=rect, density=None,
                            mesh=r['mesh'].replace('.bdae', ''), off=r['off']))
        elif rect[0] == rect[1] and rect[0] > 1.05 and rect[0] < 64:
            out.append(dict(lvc=lvcname, page=r['page'], page_shipped=nxt,
                            rect=None, density=rect[0],
                            mesh=r['mesh'].replace('.bdae', ''), off=r['off']))
    return out

def main():
    allrows = []
    for lv in ('GothamCity', 'GothamCity_Island2'):
        rows = extract(lv)
        print(f"=== {lv}: {len(rows)} bake-group records with resolved mesh")
        for r in rows[:4000]:
            base = r['mesh']
            if 'footprint' in base or 'longdist' in base or 'bigbridge' in base:
                rr = r['rect']
                dens = r['density']
                print(f"  {r['page']:<36} rect={rr if rr else 'DENSITY ' + str(dens)}  mesh={base}")
        allrows += rows
    json.dump(allrows, open('/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions.json', 'w'), indent=1)
    print(f"saved extraction/re/bake_regions.json ({len(allrows)} records)")

if __name__ == '__main__':
    main()
