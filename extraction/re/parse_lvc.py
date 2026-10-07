#!/usr/bin/env python3
"""
Definitive GothamCity.lvc.bin parser — follows the reversed game code exactly.

Chain of evidence (libKRHP.so, Ghidra 12.1.4):
  CLevel::LoadLevelProperties(const char* path):
    open file -> CMemoryStream(buf,size,1) -> BeginRead()
    BeginRead (CMemoryStream::BeginRead.part.2551 @Ghidra 0x3ae97c):
      magic  = ReadInt()   BE u32 == 0x44494354 'DICT'
      tblOff = ReadInt()   BE u32  (string table offset)
      flag   = byte[tblOff-4] i.e. file[8]  (wide-string flag; 0 here)
      if flag: wide table (count + len*4 wchar each)
      countC = ReadInt() at tblOff; then count x {BE u32 len + len bytes}
      pos = 9                       <-- object stream starts at 9
    then ReadShort(); ReadShort(); ReadInt(); typeId=ReadInt()
    typeId == 0x2657 -> CTemplateLevelProperties::Load
  All ReadInt/ReadFloat are BIG-ENDIAN (CMemoryStream::ReadInt @Ghidra 0x349914).
  ReadString with flag==0: idx = ReadInt() -> charTable[idx]  (interned).
"""
import struct, sys, json

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc.bin"
d = open(PATH, "rb").read()


class R:
    """CMemoryStream reader replica (BE primitives, interned strings)."""

    def __init__(self, data, pos):
        self.d = data
        self.pos = pos
        self.strings = []
        self.trace = []

    def tell(self):
        return self.pos

    def byte(self):
        v = self.d[self.pos]
        self.pos += 1
        return v

    def short(self):
        v = struct.unpack_from(">H", self.d, self.pos)[0]
        self.pos += 2
        return v

    def int(self):
        v = struct.unpack_from(">i", self.d, self.pos)[0]
        self.pos += 4
        return v

    def float(self):
        v = struct.unpack_from(">f", self.d, self.pos)[0]
        self.pos += 4
        return v

    def string(self):
        idx = self.int()
        if 0 <= idx < len(self.strings):
            return self.strings[idx]
        return f"<badidx {idx}>"


def fstr(v):
    return f"{v:.6g}"


# ---------- 1. BeginRead ----------
assert d[0:4] == b"DICT", "magic"
tbl_off = struct.unpack_from(">I", d, 4)[0]
flag = d[8]
r = R(d, 9)
print(f"magic=DICT  tableOffset={tbl_off:#x}  flag={flag}")

# ---------- 2. string table ----------
r.pos = tbl_off
count = r.int()
print(f"string table: {count} entries")
for i in range(count):
    ln = r.int()
    if ln < 0 or r.pos + ln > len(d):
        raise ValueError(f"string {i}: bad len {ln} @{r.pos:#x}")
    r.strings.append(d[r.pos:r.pos + ln].decode("utf-8", "replace"))
    r.pos += ln
print(f"  parsed {len(r.strings)} strings; table ends @{r.pos:#x}")

# ---------- 3. object stream ----------
r.pos = 9
h1 = r.short()          # 'NV'
h2 = r.short()          # version 3
cnt = r.int()           # 0x3a45 object count
tid = r.int()           # 0x2657 level properties
print(f"objstream: short1={h1:#x} ({bytes(reversed(struct.pack('>H', h1)))!r}) "
      f"short2={h2} objcount={cnt} typeId={tid:#x}")
assert tid == 0x2657, f"expected level properties 0x2657, got {tid:#x}"

# ---------- 4. CComponentLevelInit::Load ----------
li = {}
li["str0"] = r.string()
li["str1"] = r.string()
li["str2"] = r.string()
li["str3"] = r.string()
li["str4"] = r.string()
li["str5"] = r.string()
li["b1"] = r.byte()
li["str6"] = r.string()
n = r.int()
print(f"LevelInit: 6 strings + str6 + missions={n}")
print(f"  str0={li['str0']!r}")
print(f"  str1={li['str1']!r}")
print(f"  str2={li['str2']!r}")
print(f"  str3={li['str3']!r}")
print(f"  str4={li['str4']!r}")
print(f"  str5={li['str5']!r}")
print(f"  bool1={li['b1']} str6={li['str6']!r}")
missions = []
for m in range(n):
    mm = [r.string(), r.string(), r.string(), r.string()]
    b = r.byte()
    s4 = r.string()
    i1 = r.int()
    s5, s6 = r.string(), r.string()
    i2 = r.int()
    s7, s8, s9, s10 = r.string(), r.string(), r.string(), r.string()
    b2 = r.byte()
    missions.append((mm, b, s4, i1, (s5, s6), i2, (s7, s8, s9, s10), b2))
li["missions"] = missions
if n:
    print(f"  mission[0]: {missions[0]}")
li["b2"] = r.byte()
li["str7"] = r.string()
li["b3"] = r.byte()
li["f25"] = [r.float() for _ in range(25)]
li["b4"] = r.byte()
print(f"  bool2={li['b2']} str7={li['str7']!r} bool3={li['b3']}")
print(f"  25 floats: {[fstr(v) for v in li['f25']]}")
print(f"  bool4={li['b4']}   (cursor @{r.pos:#x})")

# ---------- 5. CTemplateLevelProperties::Load tail ----------
t = {}
t["f_a8"] = r.float()
t["s_ac"] = r.string()
t["f_b0"] = r.float()
t["f_b4"] = r.float()
print(f"\nTemplateLevelProperties: f_a8={fstr(t['f_a8'])} s_ac={t['s_ac']!r} "
      f"f_b0={fstr(t['f_b0'])} f_b4={fstr(t['f_b4'])}")

# ---------- 6. CComponentBaseGlobalIllum::Load ----------
gi = {}
gi["enable"] = r.byte()
gi["id"] = r.int()
gi["f0c"] = r.float()
gi["f10"] = r.float()
gi["rgba1"] = [r.byte() for _ in range(4)]
gi["f18"] = r.float()
gi["f1c"] = r.float()
gi["rgba2"] = [r.byte() for _ in range(4)]
npairs = r.int()
gi["pairs"] = [(r.int(), r.int()) for _ in range(npairs)]
gi["b30"] = r.byte()
gi["b31"] = r.byte()
gi["lut0"] = r.string()
gi["lut1"] = r.string()
gi["lut2"] = r.string()
gi["atlas"] = [r.float() for _ in range(4)]
gi["fogtex"] = r.string()
gi["f54"] = r.float()
gi["f58"] = r.float()
gi["rgba3"] = [r.byte() for _ in range(4)]
gi["fog"] = [r.float() for _ in range(3)]
gi["rgba4"] = [r.byte() for _ in range(4)]

print("\n=========== CComponentBaseGlobalIllum (night fog / LUT preset) ===========")
print(f"enable           : {gi['enable']}")
print(f"preset id        : {gi['id']}")
print(f"f0c              : {fstr(gi['f0c'])}")
print(f"f10              : {fstr(gi['f10'])}")
print(f"rgba1            : {gi['rgba1']}")
print(f"f18, f1c         : {fstr(gi['f18'])}, {fstr(gi['f1c'])}")
print(f"rgba2            : {gi['rgba2']}")
print(f"zone pairs ({npairs})  : {gi['pairs'][:8]}{' ...' if npairs > 8 else ''}")
print(f"bool30, bool31   : {gi['b30']}, {gi['b31']}")
print(f"LUT strings      : {gi['lut0']!r}, {gi['lut1']!r}, {gi['lut2']!r}")
print(f"atlas u,v,1/w,1/h: {[fstr(v) for v in gi['atlas']]}")
print(f"fogTex           : {gi['fogtex']!r}")
print(f"f54, f58         : {fstr(gi['f54'])}, {fstr(gi['f58'])}")
print(f"rgba3 (fogColor?): {gi['rgba3']}")
print(f"floats (fog...)  : {[fstr(v) for v in gi['fog']]}")
print(f"rgba4            : {gi['rgba4']}")
print(f"cursor after GI  : @{r.pos:#x}")

tail_int = r.int()
print(f"final int (+0x128): {tail_int}")

out = {"levelInit": {k: v for k, v in li.items() if k != "missions"},
       "template": {k: v for k, v in t.items()},
       "globalIllum": gi}
import os
outp = "/home/z/my-project/work/TDKR-Game/extraction/re/lvc_gothamcity_parsed.json"
os.makedirs(os.path.dirname(outp), exist_ok=True)
with open(outp, "w") as fh:
    json.dump(out, fh, indent=2, default=str)
print(f"\nsaved: {outp}")
