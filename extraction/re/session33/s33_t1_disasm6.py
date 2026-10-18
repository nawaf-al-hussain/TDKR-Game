import capstone, struct
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * 32
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1: segs.append((p_vaddr, p_offset, p_filesz, p_memsz))
def v2f(v):
    for vaddr, off, filesz, memsz in segs:
        if vaddr <= v < vaddr + filesz: return off + (v - vaddr)
md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
def dis(va, n, label):
    fo = v2f(va)
    print(f'===== {label} @0x{va:x} =====')
    for ins in md.disasm(d[fo:fo+n], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
dis(0x7badfc, 0xa8, 'getAnimation(name, type, type)')
dis(0x7bb574, 0x68, 'getAnimation(name)')
