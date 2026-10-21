#!/usr/bin/env python3
"""s45 T1a step 7: definitive per-record structure map via rec70, fully annotated."""
import numpy as np, io, zipfile

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)
f32 = np.frombuffer(bres, '<f4', len(bres) // 4)
BASE, REC = 0x23308, 260

def cstr(off):
    if not (0 < off < len(bres)):
        return None
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > 120:
        return None
    try:
        t = bres[off:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

def dump(a, b, indent='  '):
    for off in range(a, b, 4):
        v = int(u32[off // 4])
        s = cstr(v)
        note = f" -> {s!r}" if s else ''
        fv = float(f32[off // 4])
        if not s and 1e-4 < abs(fv) < 1e6:
            note += f'  f={fv:.5g}'
        if not s and 0 < v < 4096:
            note += f'  i={v}'
        print(f'{indent}{off:#07x}: {v:#010x}{note}')

i = 70
a = BASE + i * REC
w = [int(x) for x in u32[a // 4:a // 4 + 65]]
print(f'=== record {i} @ {a:#x}, all 65 u32 slots ===')
for s in range(65):
    v = w[s]
    s_ = cstr(v)
    extra = f' -> {s_!r}' if s_ else ''
    print(f'  slot {s:2d} (byte {s*4:3d}): {v:#011x}{extra}')

print('\n=== pointer targets (slots with values in file range, nonzero, not name-pool) ===')
for s in range(12, 63):
    v = w[s]
    if 0x1000 < v < len(bres) - 64 and v % 4 == 0 and s not in (63, 64):
        # is it a name-pool string (already shown)? skip if cstr matched above
        if cstr(v):
            continue
        print(f'\n-- slot {s} target {v:#x}: --')
        dump(v, v + 96)
