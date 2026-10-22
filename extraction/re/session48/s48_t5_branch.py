import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
print('BuiltinBox class id:', 1923007858, hex(1923007858))
print('other:', 938977454, hex(938977454), 'cyl:', 1955669699, hex(1955669699))
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
code = data[0x368ac0:0x368ac0+11308]
hits = []
insns = list(md.disasm(code, 0x368ac0))
for i, ins in enumerate(insns):
    if '0x72a5c572' in ins.op_str.lower() or '0x72a6' in ins.op_str.lower():
        hits.append(i)
        print('HIT:', '%08x %s %s' % (ins.address, ins.mnemonic, ins.op_str))
for h in hits:
    for ins in insns[h:h+14]:
        print('   ', '%08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
