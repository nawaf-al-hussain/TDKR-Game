from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
insns = list(md.disasm(data[0x368ac0:0x368ac0+11308], 0x368ac0))
idxs = [i for i, ins in enumerate(insns) if ins.mnemonic == 'movt' and '0x729e' in ins.op_str]
print('movt 0x729e hits:', len(idxs))
for i in idxs:
    for ins in insns[max(0,i-1):i+14]:
        print('   %08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
    print('---')
