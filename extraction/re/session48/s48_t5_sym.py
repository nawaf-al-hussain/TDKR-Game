import struct
data = open('/tmp/my-project/work/re29/libKRHP.so','rb').read()
# parse ELF section headers to find .symtab/.strtab
e_shoff = struct.unpack_from('<I', data, 0x20)[0]
e_shentsize = struct.unpack_from('<H', data, 0x2E)[0]
e_shnum = struct.unpack_from('<H', data, 0x30)[0]
e_shstrndx = struct.unpack_from('<H', data, 0x32)[0]
secs = []
for i in range(e_shnum):
    p = e_shoff + i * e_shentsize
    name, stype, flags, addr, off, size, link, info, align, entsize = struct.unpack_from('<10I', data, p)
    secs.append({'name': name, 'type': stype, 'off': off, 'size': size, 'entsize': entsize, 'link': link})
strtab = secs[e_shstrndx]
def sname(x):
    o = strtab['off'] + x
    e = data.index(b'\0', o)
    return data[o:e].decode('ascii', 'replace')
symtab = [s for s in secs if s['type'] == 2][0]
strsec = secs[symtab['link']]
def stname(x):
    o = strsec['off'] + x
    e = data.index(b'\0', o)
    return data[o:e].decode('ascii', 'replace')
n = symtab['size'] // 16
print('symbols:', n)
target = 0x368ac0
best = None
for i in range(n):
    p = symtab['off'] + i * 16
    st_name, st_value, st_size, st_info, st_other = struct.unpack_from('<IIIBB', data, p)
    if st_value <= target < st_value + max(st_size, 1):
        print('EXACT covering symbol:', hex(st_value), st_size, stname(st_name))
    if st_name and 0x368a00 <= st_value <= 0x368b80:
        print('near:', hex(st_value), st_size, stname(st_name))
# also find named GenerateComponentTemplate
for i in range(n):
    p = symtab['off'] + i * 16
    st_name, st_value, st_size, st_info, st_other = struct.unpack_from('<IIIBB', data, p)
    nm = stname(st_name)
    if 'GenerateComponentTemplate' in nm or 'ComponentTemplate' in nm:
        print('named:', hex(st_value), st_size, nm)
