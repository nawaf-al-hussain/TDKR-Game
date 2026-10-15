#!/usr/bin/env python3
"""T2 session 26: run the REAL CColladaDatabase parse over batman.bdae with
a zeroed CResFileManager (cache bypass) and a complete fake IReadFile.
Hooks: file read/seek (layout), getStream/configureStream (attribute ids),
skin techniques."""
import struct, sys, collections

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, MAGIC
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_PC, UC_ARM_REG_LR)

FILE_BASE = 0x60000000
FILE_SIZE = 450892
FILE_OBJ = MAGIC + 0xC00
FILE_VT = MAGIC + 0xC80
T = {'read': MAGIC + 0xD00, 'seek': MAGIC + 0xD20, 'tell': MAGIC + 0xD40,
     'size': MAGIC + 0xD60, 'canseek': MAGIC + 0xD80, 'canread': MAGIC + 0xDA0,
     'name': MAGIC + 0xDC0, 'drop': MAGIC + 0xDE0}
MGR = 0x56000000
GOT_SLOT = 0xC589AC

HOOKS = {
    0x86D02C: 'getStream_const', 0x86D09C: 'getStream',
    0x8B7FBC: 'configureStream',
    0x7CBBFC: 'HwSkin.init', 0x7CBC40: 'HwSkin.skin',
    0x7CC234: 'SwSkin.init', 0x7CC600: 'SwSkin.skin',
    0x777DA4: 'createSkin', 0x77835C: 'createModularSkin',
}


class H:
    def __init__(self):
        self.tr = Tracer()
        self.tr.str_area_base = self.tr.str_area
        self.mu = self.tr.mu
        self.pos = 0
        self.ops = []
        self.calls = []
        self.names = {}
        mu = self.mu
        mu.mem_map(FILE_BASE, (FILE_SIZE + 0xFFF) & ~0xFFF)
        mu.mem_write(FILE_BASE, open(
            '/home/z/my-project/work/actors/batman.bdae', 'rb').read())
        mu.mem_map(MGR, 0x20000)
        mu.mem_write(MGR, b'\x00' * 0x20000)
        mu.mem_write(GOT_SLOT, struct.pack('<I', MGR))
        # manager+0x20 -> sub-object; sub+0x28 -> filename->db cache map
        mu.mem_write(MGR + 0x20, struct.pack('<I', MGR + 0x10000))
        mu.mem_write(MGR + 0x10028, struct.pack('<I', MGR + 0x11000))
        # fake IReadFile vtable: slots every 4 B; common glitch IReadFile:
        # +0x04 canRead, +0x08 canSeek, +0x0C read, +0x10 ?, +0x18 seek,
        # +0x1C tell?, +0x20 size, +0x28 getFileName
        for k, a in T.items():
            pass
        mu.mem_write(FILE_VT + 0x04, struct.pack('<I', T['canread']))
        mu.mem_write(FILE_VT + 0x08, struct.pack('<I', T['canseek']))
        mu.mem_write(FILE_VT + 0x0C, struct.pack('<I', T['read']))
        mu.mem_write(FILE_VT + 0x18, struct.pack('<I', T['seek']))
        mu.mem_write(FILE_VT + 0x1C, struct.pack('<I', T['tell']))
        mu.mem_write(FILE_VT + 0x20, struct.pack('<I', T['size']))
        mu.mem_write(FILE_VT + 0x28, struct.pack('<I', T['name']))
        mu.mem_write(FILE_OBJ, struct.pack('<I', FILE_VT))
        for a in T.values():
            mu.hook_add(UC_HOOK_CODE, self._svc, begin=a, end=a)
        for a in HOOKS:
            mu.hook_add(UC_HOOK_CODE, self._hook, begin=a, end=a)

    def _svc(self, mu, address, size, ud):
        r0 = mu.reg_read(UC_ARM_REG_R0)
        r1 = mu.reg_read(UC_ARM_REG_R1)
        r2 = mu.reg_read(UC_ARM_REG_R2)
        if address == T['read']:
            n = r2
            chunk = bytes(mu.mem_read(FILE_BASE + self.pos,
                                      min(n, FILE_SIZE - self.pos)))
            mu.mem_write(r1, chunk)
            self.ops.append(('read', self.pos, n))
            self.pos += n
            mu.reg_write(UC_ARM_REG_R0, n)
        elif address == T['seek']:
            off = struct.unpack('<i', struct.pack('<I', r1))[0]
            rel = r2
            self.ops.append(('seek', off, rel))
            self.pos = self.pos + off if rel else off
        elif address == T['tell']:
            mu.reg_write(UC_ARM_REG_R0, self.pos)
        elif address == T['size']:
            mu.reg_write(UC_ARM_REG_R0, FILE_SIZE)
        elif address in (T['canseek'], T['canread']):
            mu.reg_write(UC_ARM_REG_R0, 1)
        elif address == T['name']:
            s = 'batman.bdae'
            b = s.encode() + b'\x00'
            a = MAGIC + 0xE00
            mu.mem_write(a, b)
            mu.reg_write(UC_ARM_REG_R0, a)
        mu.reg_write(UC_ARM_REG_PC, mu.reg_read(UC_ARM_REG_LR))

    def _hook(self, mu, address, size, ud):
        if address in HOOKS:
            regs = [mu.reg_read(x) for x in (UC_ARM_REG_R0, UC_ARM_REG_R1,
                                             UC_ARM_REG_R2, UC_ARM_REG_R3)]
            self.calls.append((HOOKS[address], [hex(x) for x in regs]))

    def run(self, flag=0):
        comp = self.tr.new_component()
        self.pos = 0
        err = self.tr.run(0x7BA83C, [comp, FILE_OBJ, flag, 0])
        return err, comp


if __name__ == '__main__':
    h = H()
    err, comp = h.run(0)
    print('ctor err:', err, '| benign:', h.tr.benign_fault)
    print('file ops:', len(h.ops))
    print('first ops:', h.ops[:10])
    print('last ops:', h.ops[-6:])
    print('hooked calls:', len(h.calls))
    for c in h.calls[:24]:
        print('  ', c[0], c[1])
    print('logs tail:', h.tr.logs[-6:])
