#!/usr/bin/env python3
"""S41 T6: Python reference for the city-slice — parse GothamCity.zip from the
zone gla (lod_table.bin + lod_data.bin), per-segment vertex/index counts,
stride-24 position checksums, +40 material descriptor. JS must match."""
import hashlib, io, json, struct, sys, zipfile
import numpy as np

GLA = '/tmp/l_gothamcity.gla'
OUT = '/home/z/my-project/scripts/s41_t6_pyref.json'


def gla_member(g, want):
    _, idx_size, table_bytes, n = struct.unpack('>IIII', g[:16])
    tbl_all = g[16:16 + n * 16]
    pool = g[16 + n * 16: idx_size]
    for i in range(n):
        off, sz, no, _ = struct.unpack('>IIII', tbl_all[i*16:(i+1)*16])
        name = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
        if name == want:
            return g[off:off+sz]
    return None


def main():
    g = open(GLA, 'rb').read()
    zb = gla_member(g, 'GothamCity.zip')
    assert zb, 'GothamCity.zip member not found'
    Z = zipfile.ZipFile(io.BytesIO(zb))
    names = Z.namelist()
    lt = Z.read('lod_table.bin')
    ld = Z.read('lod_data.bin')
    si = Z.read('stream_info.bin') if 'stream_info.bin' in names else b''
    bi = Z.read('batch_info.bin') if 'batch_info.bin' in names else b''
    res = {'zone_zip_members': names, 'lod_table_bytes': len(lt), 'lod_data_bytes': len(ld),
           'stream_info_bytes': len(si), 'batch_info_bytes': len(bi)}
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    segs = []
    ok4 = 0
    for (off, sz) in pairs:
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off + 68)
        if four != 4:
            segs.append({'off': off, 'skip': f'four={four}'})
            continue
        ok4 += 1
        vstart = data_off + 4
        istart = vstart + vb
        idx = np.frombuffer(ld[istart:istart + ib], '<u2').astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], '<f4').reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            segs.append({'off': off, 'skip': 'no-stride'})
            continue
        pos = np.frombuffer(ld[vstart:vstart + vb], '<f4').reshape(-1, stride // 4)[:, :3]
        segs.append({
            'off': off, 'm40': struct.unpack_from('<I', ld, off + 40)[0],
            'm36': struct.unpack_from('<I', ld, off + 36)[0],
            'nv': int(vb // stride), 'ni': int(len(real)), 'nidx_raw': int(len(idx)),
            'stride': stride, 'vb': vb, 'ib': ib,
            'pos_sha': hashlib.sha256(pos.tobytes()).hexdigest(),
            'idx_sha': hashlib.sha256(real.astype('<u4').tobytes()).hexdigest(),
        })
    res['n_segments'] = n
    res['n_stride_ok'] = ok4
    res['segments'] = segs
    json.dump(res, open(OUT, 'w'))
    print('segments:', n, 'stride-ok:', ok4)
    print('sample seg0:', json.dumps(segs[0])[:220])
    print('saved', OUT)


if __name__ == '__main__':
    main()
