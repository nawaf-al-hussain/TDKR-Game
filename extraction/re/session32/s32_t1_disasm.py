#!/tmp/my-project/scripts/venv/bin/python3
"""S32 T1k: engine convention — disassemble CHardwareMatrixSkinTechnique
init/skin + software skin path to determine palette = world x invBind order."""
import struct, json, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
d = open(SO, 'rb').read()
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/'
                      'session25/so_syms.json'))
by_addr = syms['by_addr']
by_name = syms['by_name']

# ELF program headers -> vaddr map (so is mapped identically: vaddr==offset
# for this lib typically; verify with a known symbol)
def sym_addr(name_sub):
    for k, v in by_name.items():
        if name_sub in k:
            return k, v
    return None, None


k_init, a_init = sym_addr('CHardwareMatrixSkinTechnique4initE')
k_skin, a_skin = sym_addr('CHardwareMatrixSkinTechnique4skinE')
a_init = int(a_init, 16) if isinstance(a_init, str) else a_init
a_skin = int(a_skin, 16) if isinstance(a_skin, str) else a_skin
k_soft, a_soft = sym_addr('createSoftwareSkinTechnique')
k_sw, a_sw = sym_addr('ISkinTechnique')
print('init @', hex(a_init) if a_init else None, k_init)
print('skin @', hex(a_skin) if a_skin else None, k_skin)


def disasm(addr, n=400, thumb=True):
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB if thumb else CS_MODE_ARM)
    md.detail = False
    code = d[addr:addr + n * 4]
    out = []
    for ins in md.disasm(code, addr):
        out.append(ins)
        if len(out) >= n:
            break
    return out


def annotate(insns):
    lines = []
    for ins in insns:
        tag = ''
        m = re.search(r'\bbl\s+#?0x([0-9a-f]+)', ins.op_str)
        if m or ins.mnemonic.startswith('bl'):
            tgt = None
            mm = re.search(r'0x([0-9a-f]+)', ins.op_str)
            if mm:
                tgt = int(mm.group(1), 16)
            if tgt and tgt in by_addr:
                nm = by_addr[tgt]
                nm = re.sub(r'_ZN\d+', ' ', nm)
                tag = '  ; ' + nm[:90]
        lines.append(f'{ins.address:x}: {ins.mnemonic} {ins.op_str}{tag}')
    return lines


for title, addr in (('INIT-BODY', 0x7cb722), ('SKIN-BODY', 0x7cb766)):
    print(f'\n===== {title} @ {addr:x} =====')
    ins = disasm(addr, 260)
    for ln in annotate(ins):
        print(ln)
