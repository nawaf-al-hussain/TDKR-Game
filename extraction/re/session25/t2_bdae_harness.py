#!/usr/bin/env python3
"""T2 engine-driven: run the REAL glitch::collada::CColladaDatabase loader
over batman.bdae under Unicorn, tracing:
  - IReadFile read/seek (the file-layout map)
  - CVertexStreams::getStream(E_VERTEX_ATTRIBUTE, ...)  -> attribute ids used
  - CAppendMeshBuffer::configureStream(h, i, E_VAVT, u16) -> stream setup
  - CHardwareMatrixSkinTechnique::init / CSoftwareSkinTechnique::init
    (which skinning path the engine picks)
"""
import struct
import sys

sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, MAGIC
import struct as _st
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_PC, UC_ARM_REG_LR)

FILE_BASE = 0x60000000          # batman.bdae image
FILE_SIZE = 450892
FILE_OBJ = MAGIC + 0xC00        # fake IReadFile object
FILE_VT = MAGIC + 0xC80
READ_MAGIC = MAGIC + 0xD00      # trampolines
SEEK_MAGIC = MAGIC + 0xD20
TELL_MAGIC = MAGIC + 0xD40
GETSIZE_MAGIC = MAGIC + 0xD60
CANSEEK_MAGIC = MAGIC + 0xD80
CANREAD_MAGIC = MAGIC + 0xDA0

HOOKS = {
    0x86D02C: 'getStream_const(attr=r1)',
    0x86D09C: 'getStream(attr=r1)',
    0x8B7FBC: 'configureStream(r1..r4)',
    0x7CBBFC: 'HwMatrixSkin.init',
    0x7CBC40: 'HwMatrixSkin.skin',
    0x7CC234: 'SwSkin.init',
    0x7CC600: 'SwSkin.skin',
    0x777DA4: 'CColladaFactory.createSkin',
    0x77835C: 'CColladaFactory.createModularSkin',
}


class BdaeHarness:
    def __init__(self, verbose=False):
        self.tr = Tracer(verbose=verbose)
        self.tr.str_area_base = self.tr.str_area   # no lvc dict needed
        self.mu = self.tr.mu
        self.verbose = verbose
        self.file_pos = 0
        self.file_trace = []
        self.attr_log = []
        self.calls = []
        self._setup_file()
        self._setup_hooks()

    def _setup_file(self):
        mu = self.mu
        mu.mem_map(FILE_BASE, (FILE_SIZE + 0xFFF) & ~0xFFF)
        mu.mem_write(FILE_BASE, open(
            '/home/z/my-project/work/data/batman.bdae', 'rb').read())
        mu.mem_write(FILE_VT + 0xC, struct.pack('<I', READ_MAGIC))
        mu.mem_write(FILE_VT + 0x18, struct.pack('<I', SEEK_MAGIC))
        mu.mem_write(FILE_VT + 0x4, struct.pack('<I', CANREAD_MAGIC))
        mu.mem_write(FILE_VT + 0x8, struct.pack('<I', CANSEEK_MAGIC))
        mu.mem_write(FILE_VT + 0x20, struct.pack('<I', GETSIZE_MAGIC))
        mu.mem_write(FILE_OBJ, struct.pack('<I', FILE_VT))

    def _svc(self, mu, address, size, ud):
        if address == READ_MAGIC:
            buf = mu.reg_read(UC_ARM_REG_R1)
            n = mu.reg_read(UC_ARM_REG_R2)
            chunk = bytes(mu.mem_read(FILE_BASE + self.file_pos,
                                      min(n, FILE_SIZE - self.file_pos)))
            mu.mem_write(buf, chunk)
            self.file_trace.append(('read', self.file_pos, n))
            self.file_pos += n
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == SEEK_MAGIC:
            off = struct.unpack('<i', struct.pack(
                '<I', mu.reg_read(UC_ARM_REG_R1)))[0]
            rel = mu.reg_read(UC_ARM_REG_R2)
            self.file_trace.append(('seek', off, rel))
            self.file_pos = self.file_pos + off if rel else off
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == TELL_MAGIC:
            mu.reg_write(UC_ARM_REG_R0, self.file_pos)
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address == GETSIZE_MAGIC:
            mu.reg_write(UC_ARM_REG_R0, FILE_SIZE)
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))
        elif address in (CANSEEK_MAGIC, CANREAD_MAGIC):
            mu.reg_write(UC_ARM_REG_R0, 1)
            mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _hook(self, mu, address, size, ud):
        if address in HOOKS:
            self.calls.append((HOOKS[address],
                               [mu.reg_read(r) for r in
                                (UC_ARM_REG_R0, UC_ARM_REG_R1,
                                 UC_ARM_REG_R2, UC_ARM_REG_R3)]))
        elif address == READ_MAGIC:
            self._svc(mu, address, size, ud)
        elif address in (SEEK_MAGIC, TELL_MAGIC, GETSIZE_MAGIC,
                         CANSEEK_MAGIC, CANREAD_MAGIC):
            self._svc(mu, address, size, ud)

    def _setup_hooks(self):
        mu = self.mu
        for a in (READ_MAGIC, SEEK_MAGIC, TELL_MAGIC, GETSIZE_MAGIC,
                  CANSEEK_MAGIC, CANREAD_MAGIC):
            mu.hook_add(UC_HOOK_CODE, self._hook, begin=a, end=a)
        for a in HOOKS:
            mu.hook_add(UC_HOOK_CODE, self._hook, begin=a, end=a)

    def run(self, flag=0):
        mu = self.mu
        comp = self.tr.new_component()   # database this (4 KB scratch)
        self.file_pos = 0
        err = self.tr.run(0x7BA83C, [comp, FILE_OBJ, flag, 0])
        return err, comp


if __name__ == '__main__':
    h = BdaeHarness()
    err, comp = h.run(flag=0)
    print('ctor err:', err, '| benign:', h.tr.benign_fault)
    print('file ops:', len(h.file_trace))
    print('first ops:', h.file_trace[:12])
    print('last ops:', h.file_trace[-6:])
    print('hooked calls:')
    for c in h.calls[:30]:
        print('  ', c[0], [hex(x) for x in c[1]])
    print('str violations:', h.tr.str_violation)
    print('svc logs tail:', h.tr.logs[-8:])
