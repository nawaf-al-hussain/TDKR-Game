#!/usr/bin/env python3
"""s47 T1 step H: drive CResFile::CResFile(name, IReadFile, bool) @0x7c785c
directly under the tracer with the whole bdae zip as the IReadFile, then
inspect what got built. This bypasses the CResFileManager registry whose
singleton the emulator cannot initialize."""
import sys, io, zipfile, struct, json

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session25')
import lvc_tracer
from lvc_tracer import Tracer, MAGIC
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_LR
from unicorn import UC_HOOK_CODE

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
ZIP = open(P, 'rb').read()
LE = zipfile.ZipFile(io.BytesIO(ZIP)).read('little_endian_not_quantized.bdae')
FILE_SIZE = len(ZIP)

FILE_BASE = 0x60000000
FILE_VT = MAGIC + 0xC80
FILE_OBJ = MAGIC + 0xC00
READ_MAGIC = MAGIC + 0xD00
SEEK_MAGIC = MAGIC + 0xD20
TELL_MAGIC = MAGIC + 0xD40
GETSIZE_MAGIC = MAGIC + 0xD60
CANSEEK_MAGIC = MAGIC + 0xDA0
CANREAD_MAGIC = MAGIC + 0xD80
NAME_PTR = MAGIC + 0xF00
CRESFILE_CTOR = 0x7c785c

tr = Tracer(verbose=False)
tr.str_area_base = tr.str_area
mu = tr.mu
mu.mem_map(FILE_BASE, (FILE_SIZE + 0xFFF) & ~0xFFF)
mu.mem_write(FILE_BASE, ZIP)
mu.mem_write(FILE_VT + 0xC, struct.pack('<I', READ_MAGIC))
mu.mem_write(FILE_VT + 0x18, struct.pack('<I', SEEK_MAGIC))
mu.mem_write(FILE_VT + 0x4, struct.pack('<I', CANREAD_MAGIC))
mu.mem_write(FILE_VT + 0x8, struct.pack('<I', CANSEEK_MAGIC))
mu.mem_write(FILE_VT + 0x20, struct.pack('<I', GETSIZE_MAGIC))
mu.mem_write(FILE_OBJ, struct.pack('<I', FILE_VT))
mu.mem_write(NAME_PTR, b'GothamCity_materials.bdae\x00')

file_pos = 0
file_ops = []

def svc(mu, address, size, ud):
    global file_pos
    if address == READ_MAGIC:
        buf = mu.reg_read(UC_ARM_REG_R1)
        n = mu.reg_read(UC_ARM_REG_R2)
        avail = min(n, FILE_SIZE - file_pos) if 0 <= file_pos < FILE_SIZE else 0
        chunk = ZIP[file_pos:file_pos + avail] if avail > 0 else b''
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

for a in (READ_MAGIC, SEEK_MAGIC, TELL_MAGIC, GETSIZE_MAGIC, CANSEEK_MAGIC, CANREAD_MAGIC):
    mu.hook_add(UC_HOOK_CODE, svc, begin=a, end=a)

# lock stubs
for a in (0xccda8, 0xccd70, 0xccd8c, 0xccfbc, 0xcd058, 0x124610, 0x124624):
    mu.mem_write(a, struct.pack('<2I', 0xe3a00000, 0xe12fff1e))
# map page 0 as zero page (some code paths deref null-globals pre-init)
try:
    mu.mem_map(0, 0x1000)
except Exception:
    pass

comp = tr.new_component()
file_pos = 0
err = tr.run(CRESFILE_CTOR, [comp, NAME_PTR, FILE_OBJ, 0], count=200_000_000)
print('CResFile ctor err:', err, '| benign:', tr.benign_fault)
print('file ops:', len(file_ops), 'heap_ptr:', hex(tr.heap_ptr))
if file_ops:
    print('first:', file_ops[:10])
    print('last:', file_ops[-6:])
print('comp words:', [hex(x) for x in struct.unpack('<16I', bytes(mu.mem_read(comp, 64)))])
