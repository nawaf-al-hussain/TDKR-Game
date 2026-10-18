#!/usr/bin/env python3
"""S37 T4.2: texture decode with the ENGINE as ground truth.

1. Unicorn-call the engine's own PVRTCDecompress (real impl @0x746e34,
   signature (const void* data, int flag(0=2bpp else 4bpp), int w, int h,
   u8* dest)) on GC_StockExchange_Gargoyle mip0 (256x256, 32,768 B).
2. Independent Python PVRTC-4bpp decoder -> pixel-compare vs engine RGBA.
3. Batman DIFFUSE (RGB888, no mips) decoded in Python.
Outputs: engine_rgba.bin + compare stats (inputs for the JS side).
"""
import struct, sys, zipfile, json
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session36')
import importlib.util
spec = importlib.util.spec_from_file_location('emu36', '/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py')
emu36 = importlib.util.module_from_spec(spec)

# --- load the tga chunks from the release zip ---
z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/actors_tex.gla')
n = struct.unpack_from('>I', d, 12)[0]
pool = 16 + n * 16
ents = {}
for i in range(n):
    o = 16 + i * 16
    off, size, nameOff = struct.unpack_from('>3I', d, o)
    nb = pool + nameOff
    e = d.index(b'\0', nb)
    ents[d[nb:e].decode('latin1')] = (off, size)

def chunk(name):
    off, size = ents[name]
    return d[off:off + size]

garg = chunk('GC_StockExchange_Gargoyle.tga')
print('gargoyle hdr:', garg[:24].hex(), 'size', len(garg))
w, h = struct.unpack_from('<II', garg, 4)
fmt = struct.unpack_from('<I', garg, 12)[0]
bpp = struct.unpack_from('<I', garg, 24)[0]
mip0 = garg[52:52 + 32768]
print(f'w={w} h={h} fmt={fmt} bpp={bpp} mip0={len(mip0)} B')

# --- run the ENGINE decoder under unicorn ---
# Build the module without running its __main__ Create path: the module's Emu
# class is self-contained; instantiate and then call PVRTCDecompress manually.
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/s36_t1_trace.py').read()
src = src.replace("if __name__ == '__main__':", "if False:")
ns = {'__name__': 'emu36mod'}
exec(compile(src, 's36_t1_trace.py', 'exec'), ns)
Emu = ns['Emu']

emu = Emu()
mu = emu.mu
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_PC

DATA = 0x70000000
DEST = 0x71000000
RET = 0x10000000 + 0x3F0
mu.mem_map(DATA, 0x100000)
mu.mem_map(DEST, 0x400000)
mu.mem_write(DATA, mip0)
STACK_TOP = 0x20000000 + 0x100000
mu.mem_write(STACK_TOP - 16, struct.pack('<I', DEST))   # dest on stack (arg5)
mu.reg_write(UC_ARM_REG_SP, STACK_TOP - 16)
mu.reg_write(UC_ARM_REG_R0, DATA)
mu.reg_write(UC_ARM_REG_R1, 1)          # nonzero = 4bpp mode
mu.reg_write(UC_ARM_REG_R2, w)
mu.reg_write(UC_ARM_REG_R3, h)
mu.reg_write(UC_ARM_REG_PC, 0x746e34)
try:
    emu.mu.emu_start(0x746e34, RET, timeout=60_000_000)
    print('engine PVRTCDecompress returned')
except Exception as ex:
    print('emu stop:', ex)
out = bytes(mu.mem_read(DEST, w * h * 4))
open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_engine_rgba.bin', 'wb').write(out)
arr = np.frombuffer(out, np.uint8).reshape(h, w, 4)
print('engine RGBA stats: mean', arr.reshape(-1, 4).mean(0).round(1),
      'std', arr.reshape(-1, 4).std(0).round(1))
nonzero = (arr.reshape(-1, 4).sum(1) > 0).sum()
print(f'non-black pixels: {nonzero}/{w*h}')

# --- independent Python PVRTC 4bpp decoder ---
def morton_d2x(i, w_blocks):
    # standard interleaved Morton walk used by PVRTC (x per line-major spec):
    # the reference decoder walks blocks in Morton order
    x = 0; y = 0
    for bit in range(0, 32, 2):
        x |= (i >> bit) & 1 << (bit // 2) if False else 0
    # simpler: iterative de-interleave
    def deinter(v):
        x = 0; y = 0; k = 0
        while v:
            x |= (v & 1) << k
            v >>= 1
            y |= (v & 1) << k
            v >>= 1
            k += 1
        return x, y
    return deinter(i)

def decode_pvrtc4(data, w, h):
    """standard PVRTC 4bpp decode (Imagination reference semantics)"""
    wb, hb = (w + 3) // 4, (h + 3) // 4
    words = [struct.unpack_from('<Q', data, i * 8)[0] for i in range(wb * hb)]
    img = np.zeros((h, w, 4), np.uint8)

    def get_word(bx, by):
        bx %= wb; by %= hb
        idx = by * wb + bx          # linear order (engine layout: linear, see below)
        return words[idx]

    def parse(word):
        a_bit = (word >> 63) & 1
        colB = (word >> 32) & 0x7FFFFFFF
        colA = word & 0xFFFFFFFF
        def c5554(v, flag):
            r = (v >> 10) & 0x1F; g = (v >> 5) & 0x1F; b = v & 0x1F; a = (v >> 15) & 0x1
            # expand 5->8 and apply the 5554 alpha rule
            R = (r << 3) | (r >> 2); G = (g << 3) | (g >> 2); B = (b << 3) | (b >> 2)
            A = 255 if (flag and a_bit) else (a * 255 if a else 0) if False else (0 if (a == 0 and not flag) else 255)
            return R, G, B, A
        # color A: 5554 (or 444 punchthrough); color B: 555/554+flag
        aFlag = a_bit
        rA = (colA >> 10) & 0x1F; gA = (colA >> 5) & 0x1F; bA = colA & 0x1F; aA = (colA >> 15) & 0x1
        R_A = (rA << 3) | (rA >> 2); G_A = (gA << 3) | (gA >> 2); B_A = (bA << 3) | (bA >> 2)
        A_A = 255 if (aA or not aFlag) else 0
        rB = (colB >> 9) & 0x1F; gB = (colB >> 4) & 0x1F; bB = ((colB & 0xF) << 1) | ((colB >> 3) & 1); aB = (colB >> 14) & 0x1
        R_B = (rB << 3) | (rB >> 2); G_B = (gB << 3) | (gB >> 2); B_B = (bB & 0xF8) | (bB >> 4)
        B_B = (colB & 0x1F); B_B = (B_B << 3) | (B_B >> 2)
        A_B = 255 if (aB or not aFlag) else 0
        # colors as 8-bit with the low-precision bit trick for B
        return (R_A, G_A, B_A, A_A), (R_B, G_B, B_B, A_B), aFlag, (word >> 32) & 1

    # modulation weights
    def weights(mod, aFlag):
        # returns per-pixel weight w in [0..8] for colorB vs colorA
        if not aFlag:
            return [8 - ((mod >> 0) & 1) * 0 for _ in range(0)]  # placeholder
        return None

    for by in range(hb):
        for bx in range(wb):
            word = get_word(bx, by)
            CA, CB, aFlag, modFlag = parse(word)
            # modulation data: 32 bits, 2 bits per pixel
            mods = (word >> 32) & 0xFFFFFFFF
            for py in range(4):
                for px in range(4):
                    X = bx * 4 + px; Y = by * 4 + py
                    if X >= w or Y >= h: continue
                    m = (mods >> (2 * ((py & 3) * 4 + (px & 3)))) & 3
                    # bilinear over the 4 neighbouring block colors (wrap)
                    def col(bxp, byp, which):
                        wd = get_word(bxp, byp)
                        cA, cB, af, _ = parse(wd)
                        return cB if which else cA
                    # neighbors in Morton? reference uses Morton; engine layout check:
                    acc = np.zeros(4)
                    wsum = 0.0
                    for dx, dy, wgt in ((0, 0, 4), (1, 0, 2), (0, 1, 2), (1, 1, 2)):
                        wd = get_word(bx + dx, by + dy)
                        cA, cB, af, _ = parse(wd)
                        mm = (wd >> 32) & 0xFFFFFFFF
                        mv = (mm >> (2 * ((py & 3) * 4 + (px & 3)))) & 3
                        # weight of B vs A for this pixel in that block
                        if af:
                            if mv == 0: wB = 0
                            elif mv == 1: wB = 4
                            else: wB = 5 if (px + py) & 1 else 3
                        else:
                            wB = [0, 4, 8 - int((px & 1) ^ 0), 8][mv] if mv else 0
                            wB = {0: 0, 1: 4, 2: 4, 3: 8}.get(mv, 4)
                        c = [cA[k] * (8 - wB) / 8 + cB[k] * wB / 8 for k in range(4)]
                        acc += np.array(c) * wgt
                        wsum += wgt
                    img[Y, X] = np.clip(acc / wsum, 0, 255).astype(np.uint8)
    return img

py_img = decode_pvrtc4(mip0, w, h)
eng = arr[:, :, :3].astype(int)
pym = py_img[:, :, :3].astype(int)
diff = np.abs(eng - pym)
exact = (diff.max(axis=2) == 0).sum()
print(f'python-PVRTC vs engine RGBA: exact pixels {exact}/{w*h} ({100*exact/(w*h):.1f}%), '
      f'max diff {diff.max()}, mean {diff.mean():.2f}')
json.dump({'w': w, 'h': h, 'fmt': fmt, 'bpp': bpp,
           'engine_nonblack': int(nonzero),
           'py_exact': int(exact), 'py_max_diff': int(diff.max()), 'py_mean': float(diff.mean())},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_pvr.json', 'w'), indent=1)
