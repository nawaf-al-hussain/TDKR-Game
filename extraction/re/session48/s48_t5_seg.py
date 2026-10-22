import struct
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
e_phoff = struct.unpack_from('<I', data, 0x1C)[0]
e_phentsize = struct.unpack_from('<H', data, 0x2A)[0]
e_phnum = struct.unpack_from('<H', data, 0x2C)[0]
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _pa, p_filesz, p_memsz = struct.unpack_from('<IIIIII', data, p)
    print('type %d off %#x vaddr %#x filesz %#x memsz %#x' % (p_type, p_offset, p_vaddr, p_filesz, p_memsz))
