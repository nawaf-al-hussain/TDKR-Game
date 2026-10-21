#!/usr/bin/env python3
"""s47 T1 step F (DECISIVE): run the REAL CColladaDatabase loader
(@0x7BA83C, the s25 harness entry) over the little_endian_not_quantized
variant of GothamCity_materials.bdae under unicorn; then compare the
in-memory setparam VALUE BLOCKS against the on-disk bytes.

If the loader patches the {1,next,ff*16B,term} placeholder blocks into real
SImage* pointer arrays, extract the per-material image table for all 307
materials and compare with the source.dae authoring table (s45).
If NOT patched, the engine must bind at scene construction (XML path).
"""
import sys, os, io, zipfile, struct, json
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session25')
import lvc_tracer
from lvc_tracer import Tracer, MAGIC
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_PC, UC_ARM_REG_LR)

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
FILE_SIZE = len(LE)

FILE_BASE = 0x60000000
FILE_VT = MAGIC + 0xC80
FILE_OBJ = MAGIC + 0xC00
READ_MAGIC = MAGIC + 0xD00
SEEK_MAGIC = MAGIC + 0xD20
TELL_MAGIC = MAGIC + 0xD40
GETSIZE_MAGIC = MAGIC + 0xD60
CANSEEK_MAGIC = MAGIC + 0xDA0
CANREAD_MAGIC = MAGIC + 0xD80

CCTOR = 0x7BA83C

tr = Tracer(verbose=False)
tr.str_area_base = tr.str_area
mu = tr.mu
mu.mem_map(FILE_BASE, (FILE_SIZE + 0xFFF) & ~0xFFF)
mu.mem_write(FILE_BASE, LE)
mu.mem_write(FILE_VT + 0xC, struct.pack('<I', READ_MAGIC))
mu.mem_write(FILE_VT + 0x18, struct.pack('<I', SEEK_MAGIC))
mu.mem_write(FILE_VT + 0x4, struct.pack('<I', CANREAD_MAGIC))
mu.mem_write(FILE_VT + 0x8, struct.pack('<I', CANSEEK_MAGIC))
mu.mem_write(FILE_VT + 0x20, struct.pack('<I', GETSIZE_MAGIC))
mu.mem_write(FILE_OBJ, struct.pack('<I', FILE_VT))

file_pos = 0
file_ops = []

def svc(mu, address, size, ud):
    global file_pos
    if address == READ_MAGIC:
        buf = mu.reg_read(UC_ARM_REG_R1)
        n = mu.reg_read(UC_ARM_REG_R2)
        avail = min(n, FILE_SIZE - file_pos) if file_pos < FILE_SIZE else 0
        chunk = LE[file_pos:file_pos + avail] if avail > 0 else b''
        if len(chunk) < n:
            chunk = chunk + b'\x00' * (n - len(chunk))
        mu.mem_write(buf, chunk)
        file_ops.append(('read', file_pos, n))
        file_pos += avail
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
    elif address == SEEK_MAGIC:
        off = struct.unpack('<i', struct.pack('<I', mu.reg_read(UC_ARM_REG_R1)))[0]
        rel = mu.reg_read(UC_ARM_REG_R2)
        file_ops.append(('seek', off, rel))
        file_pos = file_pos + off if rel else off
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
    elif address == TELL_MAGIC:
        mu.reg_write(UC_ARM_REG_R0, file_pos)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
    elif address == GETSIZE_MAGIC:
        mu.reg_write(UC_ARM_REG_R0, FILE_SIZE)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
    elif address in (CANSEEK_MAGIC, CANREAD_MAGIC):
        mu.reg_write(UC_ARM_REG_R0, 1)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

from unicorn import UC_HOOK_CODE
for a in (READ_MAGIC, SEEK_MAGIC, TELL_MAGIC, GETSIZE_MAGIC, CANSEEK_MAGIC, CANREAD_MAGIC):
    mu.hook_add(UC_HOOK_CODE, svc, begin=a, end=a)

comp = tr.new_component()
file_pos = 0

# unicorn 2.1.4 env change: the ctor path enters glf::Condition::Wait /
# glf::SpinLock::Lock with a garbage Condition (allocator lock path) and
# faults; a single-threaded emulator needs no locks — stub them.
STUBS = {0xccda8: 'Condition::Wait', 0xccd70: 'Condition::Signal',
         0xccd8c: 'Condition::Broadcast', 0xccfbc: 'SpinLock::Lock',
         0xcd058: 'SpinLock::Unlock', 0x124610: 'vox::Mutex::Lock',
         0x124624: 'vox::Mutex::Unlock'}
for a, nm in STUBS.items():
    mu.mem_write(a, struct.pack('<I', 0xe3a00000) + struct.pack('<I', 0xe12fff1e))  # mov r0,#0 ; bx lr
print('stubs applied:', list(STUBS.values()))

err = tr.run(CCTOR, [comp, FILE_OBJ, 0, 0], count=60_000_000)
print('ctor err:', err, '| benign:', tr.benign_fault, '| str_violation:', tr.str_violation)
print('file ops:', len(file_ops), 'heap_ptr:', hex(tr.heap_ptr))

cnt = int(struct.unpack('<I', mu.mem_read(comp + 0x78, 4))[0])
arr = int(struct.unpack('<I', mu.mem_read(comp + 0x7c, 4))[0])
print('db count @comp+0x78 =', cnt, 'array @comp+0x7c =', hex(arr))
if cnt != 307 or not (0 < arr < 0x7fffffff):
    # try to locate the array by scanning the heap for the 307x36 pattern
    print('fallback scan needed')

def rd(a, n):
    return bytes(mu.mem_read(a, n))

def cstr(a, maxn=96):
    if not (0 < a < 0x7fffffff):
        return None
    try:
        raw = rd(a, maxn)
    except Exception:
        return None
    e = raw.find(b'\0')
    if e <= 0:
        return None
    s = raw[:e]
    try:
        t = s.decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

out = {'err': str(err), 'benign': str(tr.benign_fault), 'count': cnt, 'array': arr,
       'materials': []}

if cnt == 307 and 0 < arr < 0x7fffffff:
    # value-block addrs in FILE for comparison
    u32f = np.frombuffer(LE, '<u4', len(LE) // 4)
    BASE_F, REC_F = 0x23308, 260
    for i in range(cnt):
        e = rd(arr + i * 36, 36)
        w = struct.unpack('<9I', e)
        # w = {name*, effect*, ?, ?, count, params*, ...}
        name = cstr(w[0])
        m = {'i': i, 'name': name, 'w': [hex(x) for x in w], 'params': []}
        pcnt, parr = w[4], w[5]
        if 0 < pcnt <= 16 and 0 < parr < 0x7fffffff:
            for k in range(pcnt):
                pe = rd(parr + k * 24, 24)
                pw = struct.unpack('<6I', pe)
                pname = cstr(pw[0])
                va = pw[5]  # SSetParam+0x14 = value array ptr
                vmem = rd(va, 24) if 0 < va < 0x7fffffff else None
                pr = {'name': pname, 'type': pw[1], 'a': pw[2], 'b': pw[3],
                      'v1': pw[4], 'v2': pw[5]}
                if vmem:
                    pr['mem_words'] = [hex(x) for x in struct.unpack('<6I', vmem)]
                    # file counterpart: v1 = pw[4]
                    v1f = pw[4]
                    if 0 < v1f < len(LE) - 24:
                        pr['file_words'] = [hex(x) for x in struct.unpack(
                            '<6I', LE[v1f:v1f + 24])]
                m['params'].append(pr)
        out['materials'].append(m)

    # summary: are value blocks patched?
    patched = 0
    for m in out['materials']:
        for pr in m['params']:
            if pr.get('mem_words') and pr.get('file_words'):
                if pr['mem_words'] != pr['file_words']:
                    patched += 1
    print('param value blocks differing mem vs file:', patched)
    # show materials 73 and 302 in full
    for probe in (73, 302):
        m = out['materials'][probe]
        print(f"--- material {probe} name={m['name']!r} ---")
        for pr in m['params']:
            print('   ', pr['name'], 'type', pr['type'], 'mem', pr.get('mem_words'),
                  'file', pr.get('file_words'))
    # deref any real pointers: if mem words look like heap pointers != file,
    # try resolving [entry] -> SImage* -> name/tga strings
    resolved = 0
    for m in out['materials']:
        for pr in m['params']:
            if pr['type'] == 13 and pr.get('mem_words'):
                mw = pr['mem_words']
                # entry array at v2 (mem): first word = pointer to SImage* slot?
                va = pr['v2']
                try:
                    ent = struct.unpack('<I', rd(va, 4))[0]
                    simg = struct.unpack('<I', rd(ent, 4))[0]
                    iname = cstr(struct.unpack('<I', rd(simg, 4))[0]) if 0 < simg < 0x7fffffff else None
                    pr['simg'] = hex(simg)
                    pr['image_name'] = iname
                    resolved += 1
                except Exception as ex:
                    pr['deref_err'] = str(ex)
    print('resolved image derefs:', resolved)

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t1_load_dump.json', 'w'), indent=1)
print('saved s47_t1_load_dump.json')
