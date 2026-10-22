from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
insns = list(md.disasm(data[0x368ac0:0x368ac0+11308], 0x368ac0))
def find(movw, movt):
    for i in range(len(insns)-1):
        a, b = insns[i], insns[i+1]
        if a.mnemonic == 'movw' and movw in a.op_str and b.mnemonic == 'movt' and movt in b.op_str:
            return i
    return None
for label, w, t in (('BuiltinBox', '0xc572', '0x729e'), ('cyl', '0x26c3', '0x7491')):
    i = find(w, t)
    print('===', label, 'idx', i)
    if i is not None:
        for ins in insns[max(0,i-2):i+12]:
            print('   %08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
