#!/usr/bin/env python3
"""S30 T1a: build the reader-call SPINE of CComponentCinematic::Load
(@0x2dce20) and CContainerTracksAnimatedObject::Load (@0x2d9118) from the
capstone dumps, with loop/branch structure, as the basis of a full spec.
"""
import re, sys, json, collections

READERS = {
    0x339510: ('B', 'ReadBool_ref'), 0x339574: ('B', 'Read_boolref'),
    0x3395D8: ('c', 'ReadChar'), 0x339634: ('c', 'Read_charref'),
    0x339690: ('B', 'ReadByte'), 0x3396EC: ('B', 'Read_ucharref'),
    0x339758: ('s', 'ReadShort'), 0x3397DC: ('s', 'Read_shortref'),
    0x339868: ('S', 'Read_ushortref'), 0x339914: ('i', 'ReadInt'),
    0x3399D4: ('i', 'Read_intref'), 0x339AB4: ('i', 'Read_uintref'),
    0x339B94: ('f', 'ReadFloat'), 0x339C58: ('f', 'Read_floatref'),
    0x33A0D4: ('STR', 'ReadString_ref'), 0x33AB94: ('STR', 'ReadString'),
    0x33AD74: ('STR', 'ReadStringC_ref'), 0x33B01C: ('STR', 'ReadStringW_ref'),
    0x33B3D0: ('v3', 'Read_vector3d'), 0x33B4DC: ('v2', 'Read_vector2d'),
    0x33B6AC: ('v4', 'Read_vector4d'),
    0x33BB10: ('DATA?', 'ReadData_ptr'), 0x33BB40: ('DATA?', 'ReadData_int'),
}
KNOWN_CALLS = {
    0x2d9118: 'CContainerTracksAnimatedObject::Load',
    0x2dce20: 'CComponentCinematic::Load',
}

def parse(path):
    insns = []
    rx = re.compile(r'^(0x[0-9a-f]+):\s+(\S+)\s*(.*?)\s*(?:;\s*(.*))?$')
    for line in open(path):
        m = rx.match(line.rstrip('\n'))
        if not m:
            continue
        addr = int(m.group(1), 16)
        mn = m.group(2)
        ops = (m.group(3) or '').strip()
        ann = m.group(4) or ''
        insns.append((addr, mn, ops, ann))
    return insns

def analyze(path, name):
    insns = parse(path)
    lo, hi = insns[0][0], insns[-1][0]
    print(f'=== {name}: {len(insns)} insns, 0x{lo:x}..0x{hi:x} ({hi+4-lo} B) ===')
    idx_of = {a: i for i, (a, *_ ) in enumerate(insns)}
    targets = collections.Counter()
    bl_calls = []
    for addr, mn, ops, ann in insns:
        m = re.match(r'#?(0x[0-9a-f]+)', ops)
        t = int(m.group(1), 16) if m else None
        if mn == 'bl' and t is not None:
            bl_calls.append((addr, t, ann))
        elif mn.startswith('b') and mn != 'bic' and t is not None:
            if lo <= t <= hi:
                targets[t] += 1
    call_kinds = collections.Counter()
    for a, t, ann in bl_calls:
        if t in READERS:
            call_kinds[READERS[t][1]] += 1
        elif t in KNOWN_CALLS:
            call_kinds[KNOWN_CALLS[t]] += 1
        else:
            call_kinds[f'sub_{t:x}'] += 1
    print('BL target histogram:')
    for k, v in sorted(call_kinds.items(), key=lambda x: -x[1]):
        print(f'   {v:4d}  {k}')
    print(f'intra-function branch targets: {len(targets)}')
    print('loop heads (targets reached from later addresses):')
    nloops = 0
    for t, c in sorted(targets.items()):
        srcs = [a for a, mn, ops, ann in insns
                if idx_of[a] > idx_of[t] and
                (mn.startswith('b') and mn != 'bic' and
                 re.match(r'#?(0x[0-9a-f]+)$', ops or '') and
                 int(re.match(r'#?(0x[0-9a-f]+)$', ops).group(1), 16) == t)]
        if srcs:
            nloops += 1
            cond = [mn for a, mn, ops, ann in zip(*[iter([])]*0)]  # noop
            print(f'   0x{t:x}  from {len(srcs)} later sites (e.g. 0x{srcs[0]:x})')
    print(f'   ({nloops} loop heads)')
    return insns, targets, bl_calls

if __name__ == '__main__':
    for path, nm in [
        ('/tmp/my-project/work/re29/compcine_load.asm', 'CComponentCinematic::Load @0x2dce20'),
        ('/tmp/my-project/work/re29/conttracks_load.asm', 'CContainerTracksAnimatedObject::Load @0x2d9118'),
    ]:
        analyze(path, nm)
        print()
