from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
for mode, base, name in ((CS_MODE_ARM, 0x368ac0, 'ARM@368ac0'), (CS_MODE_THUMB, 0x368ad0, 'THUMB@368ad0')):
    md = Cs(CS_ARCH_ARM, mode)
    print('===', name)
    n = 0
    for ins in md.disasm(data[base:base+0x140], base):
        print('%08x  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
        n += 1
        if n > 40: break
