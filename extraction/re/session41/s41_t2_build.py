#!/usr/bin/env python3
"""S41 T2: build the full-chunk reference pack + Python reference decode.

Walks the 7 OBB tex archives (910 chunks), slices RAW payloads into a pack
file for JS, decodes every chunk/level with the Python reference (ETC1 via
s41_refdec_lib; RGB565 = u16 LE R5G6B5 bit-replicated [EXACT vs deployed
LUT PNG]; RGB888 = memory R,G,B [NM z-channel + skybox blue + City_BKG];
RGBA8888 = memory R,G,B,A [FX template edge + alpha=byte3]) and records
per-level SHA256. ZIP_SPLIT entries: parse the embedded stored zip
('SPLIT' marker + rgb.pvr + alpha.pvr) and decode both members' chains.
"""
import hashlib, json, struct, sys, zipfile
import numpy as np
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import decode_blocks, read_archive

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
ARCHS = ['actors_tex.gla', 'commons_tex.gla', 'l_batcave_tex.gla',
         'l_gothamcity_tex.gla', 'l_menu_tex.gla', 'l_military_tex.gla',
         'l_policestation_tex.gla']
PACK = '/home/z/my-project/scripts/s41_t2_chunks.pack'
MAN = '/home/z/my-project/scripts/s41_t2_chunks.manifest.json'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def chain_layout(w, h, avail):
    out = []
    pos = 0
    while True:
        s = ((w + 3) // 4) * ((h + 3) // 4) * 8
        if pos + s > avail: break
        out.append((w, h, s))
        pos += s
        if w == 1 and h == 1: break
        w = max(1, w // 2); h = max(1, h // 2)
    return out, pos


def decode_565(buf, w, h):
    v = np.frombuffer(buf, '<u2').reshape(h, w)
    r5 = ((v >> 11) & 31).astype(np.uint8); g6 = ((v >> 5) & 63).astype(np.uint8); b5 = (v & 31).astype(np.uint8)
    r = (r5 << 3) | (r5 >> 2); g = (g6 << 2) | (g6 >> 4); b = (b5 << 3) | (b5 >> 2)
    out = np.empty((h, w, 4), np.uint8)
    out[:, :, 0] = r; out[:, :, 1] = g; out[:, :, 2] = b; out[:, :, 3] = 255
    return out.tobytes()


def decode_888(buf, w, h):
    a = np.frombuffer(buf, np.uint8, w * h * 3).reshape(h, w, 3)
    out = np.empty((h, w, 4), np.uint8)
    out[:, :, :3] = a  # memory order R,G,B (calibrated s41)
    out[:, :, 3] = 255
    return out.tobytes()


def etc1_chain_rgba_levels(buf52, wid, hgt, dsz):
    """Decode an ETC1 mip chain from a PVR blob (52-byte header). Returns
    [(w,h,rgba_bytes)] and raises if the chain does not exactly consume dsz."""
    lv, consumed = chain_layout(wid, hgt, dsz)
    if consumed != dsz:
        raise ValueError(f'chain {consumed} != dsz {dsz}')
    out = []
    p = 52
    for (w, h, s) in lv:
        out.append((w, h, decode_blocks(buf52[p:p+s], w, h).tobytes()))
        p += s
    return out


def main():
    packblobs = []   # (jsrec, raw_blob)
    man = []         # reference manifest
    counts = {}
    exceptions = []

    for arch in ARCHS:
        d, ents = read_archive(Z, arch)
        for (name, off, size) in ents:
            full = d[off:off + size]
            key = f'{arch}:{name}'
            if full[:2] == b'PK':
                # embedded stored zip: SPLIT marker + rgb.pvr + alpha.pvr
                pos = 0
                members = {}
                while pos + 30 <= len(full) and full[pos:pos+4] == b'PK\x03\x04':
                    _v, _f, _m, _t, _dt, _c, comp, _u, nlen, xlen = struct.unpack_from('<HHHHHIIIHH', full, pos + 4)
                    nm = full[pos+30:pos+30+nlen].decode('latin1')
                    members[nm] = full[pos+30+nlen+xlen: pos+30+nlen+xlen+comp]
                    pos += 30 + nlen + xlen + comp
                if not ('SPLIT' in members and 'rgb.pvr' in members and 'alpha.pvr' in members):
                    exceptions.append({'name': key, 'issue': f'split members {list(members)}'})
                    continue
                rec = {'name': key, 'kind': 'ZIP_SPLIT', 'members': {}}
                jsrec = {'name': key, 'kind': 'ZIP_SPLIT', 'levels': []}
                blob = b''
                chunk_all = b''
                for member in ('rgb.pvr', 'alpha.pvr'):
                    mb = members[member]
                    hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', mb[:52], 0)
                    if hs != 52 or (flags & 0xff) != 0x36:
                        exceptions.append({'name': key, 'issue': f'{member} hs={hs} flags={flags:#x}'})
                        continue
                    try:
                        levels = etc1_chain_rgba_levels(mb, wid, hgt, dsz)
                    except ValueError as e:
                        exceptions.append({'name': key, 'issue': f'{member}: {e}'})
                        continue
                    msha = sha(b''.join(x[2] for x in levels))
                    rec['members'][member] = {'w': wid, 'h': hgt, 'mips': mips,
                                              'levels': [{'w': w, 'h': h, 'sha': sha(rb)} for (w, h, rb) in levels],
                                              'sha': msha}
                    chunk_all += b''.join(x[2] for x in levels)
                    p = 52
                    for (w, h, s) in chain_layout(wid, hgt, dsz)[0]:
                        raw = mb[p:p+s]; p += s
                        jsrec['levels'].append({'w': w, 'h': h})
                        blob += struct.pack('<III', w, h, len(raw)) + raw
                rec['sha'] = sha(chunk_all)
                man.append(rec)
                packblobs.append((jsrec, blob))
                counts['ZIP_SPLIT'] = counts.get('ZIP_SPLIT', 0) + 1
                continue

            hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', full[:52], 0)
            code = flags & 0xff
            kind = None
            if bpp == 4 and hs == 52 and code == 0x36: kind = 'ETC1'
            elif bpp == 16 and hs == 52 and code == 0x13: kind = 'RGB565'
            elif bpp == 24 and hs == 52 and code == 0x15: kind = 'RGB888'
            elif bpp == 32 and hs == 52 and code == 0x12: kind = 'RGBA8888'
            if kind is None:
                exceptions.append({'name': key, 'issue': f'unclassified bpp={bpp} code={code:#x} hs={hs}'})
                continue
            # slice raw levels
            if kind == 'ETC1':
                try:
                    lv, consumed = chain_layout(wid, hgt, dsz)
                    if consumed != dsz: raise ValueError(f'chain {consumed} != dsz {dsz}')
                    raws = []
                    p = 52
                    for (w, h, s) in lv:
                        raws.append((w, h, full[p:p+s])); p += s
                except ValueError as e:
                    exceptions.append({'name': key, 'issue': str(e)})
                    continue
            else:
                nbytes = wid * hgt * (2 if kind == 'RGB565' else 3 if kind == 'RGB888' else 4)
                if dsz != nbytes or size - 52 < nbytes:
                    exceptions.append({'name': key, 'issue': f'{kind} dsz {dsz} != {nbytes}'})
                    continue
                raws = [(wid, hgt, full[52:52+nbytes])]
            # reference decode
            levels = []
            chunk_all = b''
            for (w, h, raw) in raws:
                if kind == 'ETC1':
                    rgba = decode_blocks(raw, w, h).tobytes()
                elif kind == 'RGB565':
                    rgba = decode_565(raw, w, h)
                elif kind == 'RGB888':
                    rgba = decode_888(raw, w, h)
                else:
                    rgba = bytes(raw)  # already RGBA in memory order
                levels.append({'w': w, 'h': h, 'sha': sha(rgba)})
                chunk_all += rgba
            man.append({'name': key, 'kind': kind, 'mips': mips,
                        'levels': levels, 'sha': sha(chunk_all)})
            jsrec = {'name': key, 'kind': kind, 'levels': [{'w': w, 'h': h} for (w, h, _) in raws]}
            blob = b''.join(struct.pack('<III', w, h, len(raw)) + raw for (w, h, raw) in raws)
            packblobs.append((jsrec, blob))
            counts[kind] = counts.get(kind, 0) + 1

    with open(PACK, 'wb') as pk:
        pk.write(struct.pack('<I', len(packblobs)))
        for (jsrec, blob) in packblobs:
            nm = jsrec['name'].encode('latin1')
            pk.write(struct.pack('<H', len(nm)) + nm)
            pk.write(struct.pack('<I', len(blob)))
            pk.write(blob)

    json.dump({'chunks': man, 'counts': counts, 'exceptions': exceptions},
              open(MAN, 'w'), indent=0)
    print('chunks:', counts, 'total', sum(counts.values()))
    print('exceptions:', len(exceptions))
    for e in exceptions[:10]: print('EXC:', e)
    print('reference global sha:', sha(json.dumps([c['sha'] for c in man]).encode())[:24])
    import os
    print('pack size:', os.path.getsize(PACK))


if __name__ == '__main__':
    main()
