"""S37 T6: engine vertex value types — the format surface a cape vertex stream
could legally use. Read from the binary's own tables:
- E_VERTEX_ATTRIBUTE_VALUE_TYPE strings @0xbc8784: Byte, Unsigned Byte, Short,
  Unsigned Short, Int, Unsigned Int, Float
- ValueTypeSize @0xb8613c: 1,1,2,2,4,4,4  (NO half-float type exists)
- E_VERTEX_ATTRIBUTE strings @0xc12318: Position, TexCoord0-14, Normal,
  Color0-1, Tangent0-3, Binormal0-3, SkinWeights, SkinIndices, InstanceId, ...
Verdict for the cape: every loader-emittable stream uses one of the 7 value
types; the r37 scan covered Float (f32 strides 20-64) and the 16-bit space
(u16 fixed-point + f16); f16 is NOT an engine value type -> no loader path
can produce an f16 cape stream. Combined with r25/r26 (cape Load = 27 floats
+ 1 int, zero vertex reads; declared cape streams all-zero), the cape is
runtime-generated with the scan question now closed for every engine type.
"""
import struct, json

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for k in range(e_phnum):
    o = e_phoff + k * e_phentsize
    t, off, va, pa, fsz, msz = struct.unpack_from('<6I', d, o)
    if t == 1 and fsz:
        segs.append((va, off, fsz, msz))

def v2f(v):
    for va, off, fsz, msz in segs:
        if va <= v < va + fsz:
            return off + (v - va)

def C(v):
    f = v2f(v)
    e = d.index(b'\0', f)
    s = d[f:e]
    return s.decode('latin1') if s and all(9 <= c < 127 for c in s) else None

f = v2f(0xbc8784)
types = [C(struct.unpack_from('<I', d, f + 4 * i)[0]) for i in range(8)]
f = v2f(0xb8613c)
sizes = [d[f + i] for i in range(8)]
f = v2f(0xc12318)
attrs = [C(struct.unpack_from('<I', d, f + 4 * i)[0]) for i in range(40)]
print('value types:', types)
print('sizes:', sizes)
print('attributes:', [a for a in attrs if a])
json.dump({'value_types': types, 'value_type_sizes': sizes,
           'attributes': [a for a in attrs if a],
           'half_float_present': any('alf' in (t or '') for t in types)},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t6_vtxfmt.json', 'w'), indent=1)
