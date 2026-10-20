#!/usr/bin/env python3
"""S40 T1a: PVR header format-code histogram over ALL textures in the OBB
+ engine loader (CImageLoaderPVR) disassembly to map the code -> pixel type.
"""
import struct, zipfile, json, sys, collections

ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
TEX_ARCHIVES = ['actors_tex.gla', 'commons_tex.gla', 'l_batcave_tex.gla',
                'l_gothamcity_tex.gla', 'l_menu_tex.gla', 'l_military_tex.gla',
                'l_policestation_tex.gla']

def read_archive(z, name):
    d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/' + name)
    n = struct.unpack_from('>I', d, 12)[0]
    pool = 16 + n * 16
    ents = []
    for i in range(n):
        o = 16 + i * 16
        off, size, nameOff = struct.unpack_from('>3I', d, o)
        nb = pool + nameOff
        e = d.index(b'\0', nb)
        ents.append((d[nb:e].decode('latin1'), off, size))
    return d, ents

def main():
    z = zipfile.ZipFile(ZIP)
    field_mipcount = collections.Counter()   # u32 LE at +12
    field_flags    = collections.Counter()   # u32 LE at +16
    field_bpp      = collections.Counter()   # u32 LE at +24
    field_bpp_fmt  = collections.Counter()   # (bpp, flags&0xff)
    field_bpp_fmt16= collections.Counter()   # (bpp, flags&0xffff)
    badhdr = 0
    total = 0
    per_arch = {}
    gargoyle_hdr = None
    names_by_fmt = collections.defaultdict(list)
    for arch in TEX_ARCHIVES:
        d, ents = read_archive(z, arch)
        cnt = collections.Counter()
        for (name, off, size) in ents:
            total += 1
            hdr = d[off:off+52]
            if len(hdr) < 52:
                badhdr += 1; continue
            hs, hgt, wid, mips, flags, dsz, bpp, mr, mg, mb, ma, magic, nsurf = \
                struct.unpack_from('<13I', hdr, 0)
            if magic == 0x21525650:  # 'PVR!' LE
                cnt['pvr2_le'] += 1
            else:
                cnt['magic_%08x' % magic] += 1
            if hs == 52:
                cnt['hs52'] += 1
            else:
                cnt['hs_%d' % hs] += 1
            field_mipcount[mips] += 1
            field_flags[flags] += 1
            field_bpp[bpp] += 1
            field_bpp_fmt[(bpp, flags & 0xff)] += 1
            field_bpp_fmt16[(bpp, flags & 0xffff)] += 1
            if len(names_by_fmt[(bpp, flags & 0xff)]) < 6:
                names_by_fmt[(bpp, flags & 0xff)].append(arch + ':' + name)
            if name == 'GC_StockExchange_Gargoyle.tga':
                gargoyle_hdr = hdr
        per_arch[arch] = dict(cnt)
        print(f'{arch}: {len(ents)} chunks', dict(cnt))

    print('\nTOTAL chunks:', total, 'badhdr:', badhdr)
    print('\n+12 (mipCount) top:', field_mipcount.most_common(8))
    print('\n+24 bpp top:', field_bpp.most_common(8))
    print('\n(bpp, flags&0xff) top:')
    for k, v in field_bpp_fmt.most_common(20):
        print('  bpp=%d fmt=0x%02x: %d  e.g. %s' % (k[0], k[1], v, names_by_fmt[k][:3]))
    print('\n(bpp, flags&0xffff) top:')
    for k, v in field_bpp_fmt16.most_common(20):
        print('  bpp=%d fmt=0x%04x: %d' % (k[0], k[1], v))
    print('\nflags(+16) top:', field_flags.most_common(10))

    if gargoyle_hdr:
        print('\nGargoyle header (LE u32):')
        labels = ['headerSize','height','width','mipCount(+12)','flags(+16)','dataSize(+20)',
                  'bpp(+24)','maskR','maskG','maskB','maskA','magic','numSurfs']
        vals = struct.unpack('<13I', gargoyle_hdr)
        for lab, v in zip(labels, vals):
            print(f'  {lab:16s} = {v} (0x{v:08x})')
        print('  raw hex:', gargoyle_hdr.hex())
        json.dump({'gargoyle_hex': gargoyle_hdr.hex()}, open('/tmp/my-project/scripts/s40_t1a_gargoyle_hdr.json','w'))

    # full json dump for the report
    out = {
        'total': total, 'per_archive': per_arch,
        'bpp_fmt': {'0x%02x bpp=%d' % (k[1], k[0]): v for k, v in field_bpp_fmt.most_common()},
        'flags_top': {hex(k): v for k, v in field_flags.most_common(12)},
        'mipcount_top': {str(k): v for k, v in field_mipcount.most_common(8)},
    }
    json.dump(out, open('/tmp/my-project/scripts/s40_t1a_histogram.json', 'w'), indent=1)
    print('\nsaved s40_t1a_histogram.json')

if __name__ == '__main__':
    main()
