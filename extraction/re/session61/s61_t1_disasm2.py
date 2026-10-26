import struct, subprocess, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO='/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data=open(SO,'rb').read()
segs=[]
e_phoff=struct.unpack_from('<I',data,28)[0]; e_phnum=struct.unpack_from('<H',data,44)[0]
for i in range(e_phnum):
    p=e_phoff+i*struct.unpack_from('<H',data,42)[0]
    pt,po,pv,_,ps=struct.unpack_from('<5I',data,p)
    if pt==1: segs.append((pv,po,ps))
def v2o(v):
    for va,off,sz in segs:
        if va<=v<va+sz: return off+(v-va)
def rd32(v):
    o=v2o(v); return struct.unpack_from('<I',data,o)[0] if o is not None else None
nm=subprocess.run(['nm',SO],capture_output=True,text=True).stdout
syms=[]
for l in nm.splitlines():
    p=l.split()
    if len(p)==3:
        try: syms.append((int(p[0],16),p[2]))
        except: pass
syms.sort(); addrs=[a for a,_ in syms]
def sym_of(v):
    i=bisect.bisect_right(addrs,v)-1
    return (syms[i][1],v-syms[i][0]) if i>=0 else ('<none>',0)
def dem(n): return subprocess.run(['c++filt',n],capture_output=True,text=True).stdout.strip()
md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
def dump(start,end,title):
    print(f"=== {title} {start:#x}..{end:#x} = {dem(sym_of(start)[0])}")
    o=v2o(start); insns=list(md.disasm(data[o:o+(end-start)],start))
    lit={}
    for ins in insns:
        if ins.mnemonic=='ldr' and '[pc' in ins.op_str:
            try: imm=int(ins.op_str.split('#')[1].split(']')[0],0)
            except: continue
            pc=ins.address+8; lit[ins.address]=(pc+imm,rd32(pc+imm))
    for ins in insns:
        line=f"{ins.address:08x} {ins.mnemonic:8s} {ins.op_str}"
        ann=''
        if 'bl' in ins.mnemonic and ins.op_str.startswith('#'):
            try:
                t=int(ins.op_str[1:],0); s=sym_of(t); ann=f"  ; -> {dem(s[0])}"
            except: pass
        elif ins.address in lit:
            va,val=lit[ins.address]
            if val is not None:
                s=sym_of(val)
                ann=f"  ; [{va:#x}] = {val:#x} {dem(s[0])}" if s[0]!='<none>' else f"  ; [{va:#x}] = {val:#x}"
        print(line+ann)
dump(0x365f8c,0x366104,'CheckObjectCategory')
