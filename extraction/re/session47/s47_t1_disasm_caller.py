#!/usr/bin/env python3
"""s47 T1 step C: enclosing function of 0x7768c4 (sole caller of
setMaterialParameter<CMaterial,SSetParam>) and its own callers; disassembly
of the region to see where SSetParam entries + values originate."""
import struct
import numpy as np
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
f = open(SO, 'rb').read()

e_shoff = struct.unpack_from('<I', f, 0x20)[0]
e_shentsize = struct.unpack_from('<H', f, 0x2E)[0]
e_shnum = struct.unpack_from('<H', f, 0x30)[0]
e_shstrndx = struct.unpack_from('<H', f, 0x32)[0]
secs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from('<10I', f, off)
    secs.append(dict(name=name, typ=typ, addr=addr, offset=offset, size=size, link=link, entsize=entsize))
shstr = secs[e_shstrndx]
def cstr(base, n):
    end = f.index(b'\0', base + n)
    return f[base + n:end].decode('utf-8', 'replace')
for s in secs:
    s['nm'] = cstr(shstr['offset'], s['name'])
sec_by = {s['nm']: s for s in secs}
symtab = sec_by['.symtab']
strtab = secs[symtab['link']]
FUNC = []
for i in range(symtab['size'] // 16):
    o = symtab['offset'] + i * 16
    nm, val, sz, info, oth = struct.unpack_from('<IIIBB', f, o)
    if info & 0x0F != 2:  # FUNC
        continue
    name = cstr(strtab['offset'], nm)
    if name:
        FUNC.append((val, sz, name))
FUNC.sort()

def enclosing(addr):
    lo, hi = 0, len(FUNC) - 1
    best = None
    for val, sz, name in FUNC:
        if val <= addr < val + max(sz, 4):
            return (val, sz, name)
    return None

def demangle_short(m):
    return m

for probe in (0x7768c4, 0x49aba8, 0x46d3ac):
    e = enclosing(probe)
    print(f'{probe:#x} inside: {e}')

# who calls the enclosing function of 0x7768c4?
e = enclosing(0x7768c4)
fe, fsz, fname = e
text = sec_by['.text']
t_off = text['offset']
words = np.frombuffer(f[t_off:t_off + text['size']], '<u4', text['size'] // 4)
callers = []
for k in range(len(words)):
    w = int(words[k])
    if (w & 0x0F000000) == 0x0B000000 and (w & 0xF0000000) != 0xF0000000:
        imm = w & 0x00FFFFFF
        if imm & 0x800000:
            imm -= 0x1000000
        pc = text['addr'] + k * 4 + 8
        if pc + imm * 4 == fe:
            callers.append(pc)
print(f'callers of {fname[:90]} ({fe:#x}): {len(callers)}')
for c in callers[:15]:
    print(f'   {c:#x} inside {enclosing(c)}')

# disassemble the enclosing function of 0x7768c4 (mode per symbol LSB)
MODE = CS_MODE_THUMB if (fe & 1) else CS_MODE_ARM
md = Cs(CS_ARCH_ARM, MODE)
md.detail = False
foff = None
for s in secs:
    if s['nm'] == '.text' and s['addr'] <= fe < s['addr'] + s['size']:
        foff = s['offset'] + (fe - s['addr'])
print(f'--- disasm {fname[:80]} @ {fe:#x} (size {fsz:#x}) mode={"THUMB" if fe & 1 else "ARM"} ---')
code = f[foff:foff + fsz]
n_print = 0
for ins in md.disasm(code, fe):
    line = f'{ins.address:#09x}: {ins.mnemonic:8s} {ins.op_str}'
    # annotate bl targets
    if ins.mnemonic in ('bl', 'blx'):
        try:
            tgt = int(ins.op_str.replace('#', ''), 16) if ins.op_str.startswith('#') else int(ins.op_str, 16)
        except Exception:
            tgt = None
        if tgt:
            hit = [n for v, sz, n in FUNC if v == tgt]
            if hit:
                line += f'   ; {hit[0][:100]}'
    print(line)
    n_print += 1
    if n_print > 400:
        print('...truncated')
        break
