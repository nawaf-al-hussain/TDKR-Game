#!/usr/bin/env python3
"""Session 26 T1: run the REAL CLevel::LoadNextObject over the real lvc
with a real GOM template map (populated via Reload on real gol.bin).
The engine does ALL framing; Python only replicates the outer loop."""
import struct, json, sys, collections

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
from lvc_tracer import Tracer, STREAM, READERS
from unicorn.arm_const import UC_ARM_REG_R0
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_LR

DATA = '/home/z/my-project/work/data'
GOL = f'{DATA}/gol.bin'

RELOAD = 0x366104
LN_OBJ = 0x489ECC
GOT_STREAM_SLOT = 0xC08054     # *(slot) = &stream_ptr_holder

GOM = 0x54000000
LEVEL = 0x54100000
ZONE = 0x54200000
GOLSTREAM = 0x54300000
GOLBUF = 0x54400000
GOLDICTV = 0x54800000          # gol dict vector (1 MB)
GOLDICTS = 0x54900000          # gol dict string objects (1 MB)
STREAMPTR = 0x54a00000         # holds STREAM (the global variable)

syms = json.load(open('/home/z/my-project/work/so_syms.json'))['by_name']


def build(tr):
    mu = tr.mu
    for base, size in ((GOM, 0x100000), (LEVEL, 0x1000), (ZONE, 0x1000),
                       (GOLSTREAM, 0x1000), (GOLBUF, 0x200000),
                       (GOLDICTV, 0x100000), (GOLDICTS, 0x100000),
                       (STREAMPTR, 0x1000)):
        try:
            mu.mem_map(base, size)
        except Exception:
            print(f'map exists? {base:#x}+{size:#x} — retrying aligned')
            mu.mem_map(base, (size + 0xFFF) & ~0xFFF)
        mu.mem_write(base, b'\x00' * size)
    mu.mem_write(LEVEL + 0xa94, struct.pack('<I', GOM))
    mu.mem_write(LEVEL + 0x114, struct.pack('<I', ZONE))
    mu.mem_write(LEVEL + 0xec, struct.pack('<I', tr.PARENT))
    # the global: *(GOT slot) = &holder; holder = STREAM
    mu.mem_write(STREAMPTR, struct.pack('<I', STREAM))
    mu.mem_write(GOT_STREAM_SLOT, struct.pack('<I', STREAMPTR))
    # gol stream buffer
    g = open(GOL, 'rb').read()
    mu.mem_write(GOLBUF, g)
    mu.mem_write(GOLSTREAM + 0x0, struct.pack('<I', GOLBUF))
    mu.mem_write(GOLSTREAM + 0x8, struct.pack('<I', len(g)))
    mu.mem_write(GOLSTREAM + 0xc, struct.pack('<I', 0))
    mu.mem_write(GOLSTREAM + 0x34, b'\x01')
    return g


def load_gol_dict(tr, gol):
    """Build a real engine-ABI string dict for the gol stream."""
    mu = tr.mu
    assert gol[:4] == b'DICT'
    table_off = struct.unpack_from('>I', gol, 4)[0]
    pos = table_off
    nstr = struct.unpack_from('>i', gol, pos)[0]
    pos += 4
    strings = []
    for i in range(nstr):
        ln = struct.unpack_from('>i', gol, pos)[0]
        pos += 4
        strings.append(gol[pos:pos + ln].decode('utf-8', 'replace'))
        pos += ln
    # string char data in the tracer's str area (continues after lvc dict)
    a = tr.str_area
    ptrs = []
    for s in strings:
        b = s.encode('utf-8') + b'\x00'
        mu.mem_write(a + 4, b)
        mu.mem_write(a, struct.pack('<i', 0x7FFFFFFF))
        obj = GOLDICTS + 0x100 + 32 * len(ptrs)
        mu.mem_write(obj, struct.pack('<III', a + 4, len(s), len(s)))
        ptrs.append(obj)
        a += 4 + len(b) + 8
    tr.str_area = a
    vec = GOLDICTV + 0x100
    for i, p in enumerate(ptrs):
        mu.mem_write(vec + 4 * i, struct.pack('<I', p))
    mu.mem_write(GOLSTREAM + 0x1C, struct.pack('<I', vec))
    mu.mem_write(GOLSTREAM + 0x20, struct.pack('<I', vec + 4 * len(ptrs)))
    print(f'gol dict: {nstr} strings')
    return strings


MAP_OPR = 0x3C6084        # map<int,vector<TObjectData>>::operator[]
VEC_ASSIGN = 0x3A6F88     # vector<TObjectData>::operator=(const vector&).constprop
SCRATCH = 0x54B00000      # scratch page (keys, temp vectors, entry arrays)

# stub sites: engine bookkeeping that needs a live Lua VM / global managers
# and otherwise faults MID-RECORD (truncating component reads).
ACCEL_ENABLE = 0xC5CB8      # glf::AndroidEnableAccelerometer - global mgr
RESFMGR_GET = 0x7DC0A8      # CResFileManager::get - threading/cache wall
LUA_LOADFROMBUFFER = 0x14813C
LUA_GETFUNCREF = 0x14931C
LUA_S_NEWLSTR = 0xA61510
GLITCH_STROP = 0x206C64
FAKESTR = 0x54C00000      # fake Lua TString / COW string block


def install_stubs(tr):
    mu = tr.mu
    mu.mem_map(FAKESTR, 0x1000)
    mu.mem_write(FAKESTR, b'\x00' * 0x1000)
    # COW string block at FAKESTR+0x100: {refcount huge} + {p,len,cap}
    mu.mem_write(FAKESTR + 0xFC, struct.pack('<i', 0x7FFFFFFF))
    mu.mem_write(FAKESTR + 0x100,
                 struct.pack('<III', FAKESTR + 0x104, 0, 0))
    mu.mem_write(FAKESTR + 0x104, b'\x00' * 16)

    def _ret0(mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_R0, 0)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _fakestr(mu, address, size, ud):
        mu.reg_write(UC_ARM_REG_R0, FAKESTR + 0x100)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _strop(mu, address, size, ud):
        # glitch string operator=: copy {p,len,cap}, no refcount math
        r0 = mu.reg_read(UC_ARM_REG_R0)
        r1 = mu.reg_read(UC_ARM_REG_R1)
        try:
            p, ln, cap = struct.unpack('<III', bytes(mu.mem_read(r1, 12)))
        except Exception:
            p, ln, cap = 0, 0, 0
        try:
            mu.mem_write(r0, struct.pack('<III', p, ln, cap))
        except Exception:
            pass
        mu.reg_write(UC_ARM_REG_R0, r0)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    for addr, fn in ((LUA_LOADFROMBUFFER, _ret0),
                     (LUA_GETFUNCREF, _ret0),
                     (LUA_S_NEWLSTR, _fakestr),
                     (ACCEL_ENABLE, _ret0),
                     (RESFMGR_GET, _ret0)):
        mu.hook_add(UC_HOOK_CODE, fn, begin=addr, end=addr)


def populate_gom(tr):
    """Insert all 653 gol templates into the GOM map natively.
    TObjectData = {u8 flag, pad3, void* gct, u32 ctid} (12 B)."""
    mu = tr.mu
    tr.keep_heap = True
    mu.mem_map(SCRATCH, 0x100000)
    gol = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/'
                         're/session24/gol_templates.json'))
    tmpl = gol['templates']
    mu.mem_write(SCRATCH + 0x0, b'\x00' * 0x100000)
    heap = SCRATCH + 0x1000
    n_ins = 0
    for ks, comps in tmpl.items():
        key = int(ks, 16) & 0xFFFFFFFF
        n = len(comps)
        arr = heap
        heap += 12 * n + 16
        for i, (flag, ctid) in enumerate(comps):
            ent = arr + 12 * i
            mu.mem_write(ent, struct.pack('<B3xII', 1 if flag else 0,
                                          0, ctid & 0xFFFFFFFF))
        # temp vector {begin, end, cap} at SCRATCH+0x40
        mu.mem_write(SCRATCH + 0x40, struct.pack('<III', arr, arr + 12 * n,
                                                 arr + 12 * n))
        # map operator[](GOM, &key)
        mu.mem_write(SCRATCH + 0x0, struct.pack('<I', key))
        err = tr.run(MAP_OPR, [GOM, SCRATCH + 0x0])
        if err:
            raise RuntimeError(f'map operator[] failed: {err}')
        vec = tr.mu.reg_read(UC_ARM_REG_R0)
        # vector::operator=(vec*, temp)
        err = tr.run(VEC_ASSIGN, [vec, SCRATCH + 0x40])
        if err:
            raise RuntimeError(f'vector assign failed: {err}')
        n_ins += 1
        if heap > SCRATCH + 0xF0000:
            raise RuntimeError('scratch overflow')
    tr.keep_heap = False
    tr.heap_floor = tr.heap_ptr   # preserve map nodes during the walk
    print(f'GOM populated: {n_ins} templates, heap floor '
          f'{tr.heap_floor:#x}')


def main():
    island = sys.argv[1] if len(sys.argv) > 1 else 'GothamCity'
    maxrec = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    out = sys.argv[3] if len(sys.argv) > 3 else None
    d = open(f'{DATA}/{island}.lvc', 'rb').read()
    table_off = struct.unpack_from('>I', d, 4)[0]
    pos = table_off
    nstr = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings = []
    for i in range(nstr):
        ln = struct.unpack_from('>i', d, pos)[0]
        pos += 4
        strings.append(d[pos:pos + ln].decode('utf-8', 'replace'))
        pos += ln
    tr = Tracer()
    tr.load_lvc(d, strings)
    gol = build(tr)
    load_gol_dict(tr, gol)

    # 1) populate GOM map (native insertions, banked template list)
    populate_gom(tr)

    # 2) walk records with the REAL LoadNextObject
    # banked walk boundaries for live comparison
    try:
        walk = json.load(open(f'/tmp/my-project/work/walk_records_{island}.json'))
        walk_by_off = {r['off']: int(r['end'], 16) for r in walk if r['ok']}
    except Exception:
        walk_by_off = {}
    tr.set_cursor(17)
    tr.mu.mem_write(STREAM + 0x8, struct.pack('<I', table_off))
    n = 0
    cur = 17
    log = []
    t0 = __import__('time').time()
    n_match = n_div = n_new = 0
    divsamp = []
    while cur < table_off and n < maxrec:
        n += 1
        tid_before = struct.unpack_from('>i', d, cur)[0]
        tr.benign_fault = None
        err = tr.run(LN_OBJ, [LEVEL])
        end = tr.get_cursor()
        log.append(dict(n=n, off=cur, tid=tid_before, end=end,
                        err=err, benign=tr.benign_fault,
                        nev=len(tr.trace.events)))
        key = hex(cur)
        if key in walk_by_off:
            if walk_by_off[key] == end:
                n_match += 1
            else:
                n_div += 1
                if len(divsamp) < 40:
                    divsamp.append((n, key, hex(tid_before & 0xffffffff),
                                    hex(walk_by_off[key]), hex(end)))
        else:
            n_new += 1
        if n % 500 == 0:
            dt = __import__('time').time() - t0
            print(f'... {n} recs @{cur:#x} rate={n/dt:.0f}/s '
                  f'match={n_match} diverge={n_div} new={n_new} '
                  f'benign_so_far={sum(1 for e in log if e["benign"])}',
                  flush=True)
        cur = end
    dt = __import__('time').time() - t0
    print(f'== {n} records in {dt:.0f}s ({n/dt:.0f}/s); '
          f'match={n_match} diverge={n_div} new={n_new}')
    for s in divsamp[:20]:
        print('   DIV:', s)
    if out:
        json.dump(log, open(out, 'w'))
        print('wrote', out)


if __name__ == '__main__':
    main()
