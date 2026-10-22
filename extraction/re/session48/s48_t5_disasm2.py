import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
code = data[0x368ac1:0x368ac1+0x200]
n = 0
for ins in md.disasm(code, 0x368ac0):
    print('%08x  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
    n += 1
    if n > 90: break
