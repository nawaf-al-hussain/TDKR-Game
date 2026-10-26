#!/usr/bin/env python3
"""S60 T1 step 2 (v2): reader spec extraction with inline stream reads + loop forest.
- register track: stream regs (from r1), base regs ([stream]), inline ldrb/ldr reads
- loops: backward branches -> forest nesting -> rep wrapping over linear token list
- inner ::Load calls spliced inline
Output: s60_reader_specs.json
"""
import struct, subprocess, bisect, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
data = open(SO, 'rb').read()
segs = []
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
for i in range(e_phnum):
    p = e_phoff + i * struct.unpack_from('<H', data, 42)[0]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

nmout = subprocess.run(['nm', SO], capture_output=True, text=True).stdout
syms = []
for line in nmout.splitlines():
    p = line.split()
    if len(p) == 3:
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]

def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return (syms[i][1], v - syms[i][0]) if i >= 0 else ('<none>', 0)

def dem(n):
    return subprocess.run(['c++filt', n], capture_output=True, text=True).stdout.strip()

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
READS = {}
for a, t in ((0x339510, 'c'), (0x339574, 'c'), (0x3395d8, 'c'), (0x339634, 'c'),
             (0x339690, 'c'), (0x3396ec, 'c'),
             (0x339758, 's'), (0x3397dc, 's'), (0x339868, 's'),
             (0x339914, 'i'), (0x3399d4, 'i'), (0x339ab4, 'i'),
             (0x339b94, 'f'), (0x339c58, 'f'),
             (0x33a0d4, 'STR'), (0x33ab94, 'STR'), (0x33ad74, 'STR'), (0x33a730, 'STRW'), (0x33b01c, 'STRW'),
             (0x33b3d0, '3f'), (0x33b4dc, '2f'), (0x33b6ac, '4f')):
    READS[a] = t
BLK = {0x33b6e8: 'BLKSTART', 0x33b718: 'BLKEND', 0x33b728: 'SKIPBLK'}

def func_bounds(fn):
    i = bisect.bisect_right(addrs, fn) - 1
    start, name = syms[i]
    nxt = syms[i + 1][0] if i + 1 < len(syms) else start + 0x1000
    return start, min(nxt, start + 0x5000), name

def parse(fn, depth=0, seen=None):
    """returns (items, notes): items = list of (idx, kind, payload) in ADDRESS order.
    kind: 'tok' (token str), 'call' (demangled), 'inline:<n>' (n bytes)."""
    if seen is None:
        seen = set()
    if fn in seen or depth > 5:
        return [('?', 'call', 'RECURSION 0x%x' % fn)], []
    seen = seen | {fn}
    s, e, name = func_bounds(fn)
    o = v2o(fn)
    insns = list(md.disasm(data[o:o + (e - fn)], fn))
    notes = []
    items = []
    stream_regs = {'r1'}
    base_regs = set()
    pend = []  # pending ldrb candidates (idx, count)
    for k, ins in enumerate(insns):
        m, ops = ins.mnemonic, ins.op_str
        regs = ops.split(',')
        r0 = regs[0].strip()
        if m == 'mov' and len(regs) >= 2:
            src = regs[1].strip()
            if src in stream_regs and r0.startswith('r'):
                stream_regs.add(r0)
        elif m == 'ldr' and '[pc' not in ops:
            if len(regs) >= 2:
                mem = ','.join(regs[1:]).strip()
                base = mem.lstrip('[').split(']')[0].split(',')[0].strip()
                if base in stream_regs and ',' not in mem:
                    # ldr rX, [stream] -> base pointer
                    base_regs.add(r0)
        elif m in ('ldrb', 'ldrsb', 'ldr', 'ldrh', 'ldrsh') and '[pc' not in ops and len(regs) >= 2:
            mem = ','.join(regs[1:]).strip()
            mm = mem.lstrip('[').rstrip(']')
            parts = [x.strip() for x in mm.split(',')]
            if parts and parts[0] in base_regs:
                # candidate inline stream read: check pos-store within 8 insns
                win = insns[k + 1:k + 9]
                hit = False
                for w in win:
                    if w.mnemonic == 'str' and ('#0xc]' in w.op_str.replace(' ', '')):
                        wr = w.op_str.split(',')[-1].strip().rstrip(']').split('#')[0]
                        if wr.strip() in stream_regs or True:
                            hit = True
                        break
                    if w.mnemonic in ('bl', 'b') or (w.mnemonic.startswith('b') and w.mnemonic != 'bx'):
                        break
                if hit:
                    n = 4 if (m == 'ldr' and 'b' not in m) else (2 if m in ('ldrh', 'ldrsh') else 1)
                    items.append((k, 'inline', n))
                    continue
        elif m in ('bl', 'blx') and ops.startswith('#'):
            t = int(ops.lstrip('#'), 16)
            if t in READS:
                items.append((k, 'tok', READS[t]))
            elif t in BLK:
                items.append((k, 'tok', BLK[t]))
            else:
                sn, off = sym_of(t)
                d = dem(sn)
                if '::Load' in sn and off == 0 and depth < 5:
                    sub, subn = parse(t, depth + 1, seen)
                    notes.extend(subn)
                    items.append((k, 'inlinecall', (d.split('(')[0], sub)))
                else:
                    items.append((k, 'call', d[:60]))
                    notes.append('CALL %s @0x%x in %s' % (d[:60], ins.address, dem(name)[:50]))
    # loops: backward conditional branches
    idxbyaddr = {i.address: k for k, i in enumerate(insns)}
    loops = []
    for k, ins in enumerate(insns):
        if ins.mnemonic[0] == 'b' and ins.mnemonic not in ('b', 'bl', 'blx', 'bx') and ins.op_str.startswith('#'):
            t = int(ins.op_str.lstrip('#'), 16)
            if t < ins.address and t in idxbyaddr:
                h = idxbyaddr[t]
                if h < k:
                    loops.append((h, k))
    return items, notes, loops, insns

def wrap(loops, nitems):
    """nest loop ranges -> list of (h, t) top-level with children"""
    if not loops:
        return []
    loops = sorted(set(loops))
    # drop duplicate/overlapping-identical
    def inner(lp, parent):
        h, t = lp
        out = []
        for l2 in loops:
            if l2 == parent:
                continue
            h2, t2 = l2
            if h <= h2 and t2 <= t and l2 != lp:
                if not any(contained(l2, x) for x in out):
                    out.append(l2)
        return sorted(out)
    def contained(a, b):
        return b[0] <= a[0] and a[1] <= b[1] and a != b
    tops = []
    for lp in loops:
        if not any(contained(lp, other) and other != lp for other in loops):
            tops.append(lp)
    return tops, loops

def build(items, loops, insns, depth=0):
    """build token tree; loops = (tops, allL); wrap by insn-index ranges."""
    tops, allL = loops
    if not allL:
        return [it for it in items if it[1] in ('tok', 'inline', 'inlinecall', 'call')]
    heads = {}
    for (h, t) in allL:
        if h not in heads or t > heads[h]:
            heads[h] = t
    used = set()

    def emit(h, t, into):
        k = h
        while k <= t:
            if k in heads and heads[k] <= t and not (k == h and heads[k] == t and False):
                tt = heads[k]
                if tt > k:
                    body = []
                    emit(k + 1, tt, body)
                    # include any item AT the head itself (rare: read at loop head)
                    for it in items:
                        if it[0] == k and it[0] not in used:
                            body.insert(0, it)
                            used.add(it[0])
                    into.append(['rep', 'last', body])
                    for j in range(k, tt + 1):
                        used.add(j)
                    k = tt + 1
                    continue
            for it in items:
                if it[0] == k and it[0] not in used:
                    into.append(it)
                    used.add(it[0])
            k += 1
        return into

    out = []
    # top-level = whole range [0..max_insn]
    maxidx = max([it[0] for it in items] + [t for (_, t) in allL]) if (items or allL) else 0
    emit(0, maxidx + 1, out)
    return out

def to_spec(items):
    toks = []
    SKIP = ('$d', 'std::', 'operator new', 'operator delete', '__throw', 'RECURSION')
    for it in items:
        if it[1] == 'tok':
            toks.append(it[2])
        elif it[1] == 'inline':
            n = it[2]
            toks.append('c' if n == 1 else ('s' if n == 2 else 'i'))
        elif it[1] == 'inlinecall':
            toks.append(['inline', it[2][0], to_spec(it[2][1])])
        elif it[1] == 'call':
            if any(it[2].startswith(s) for s in SKIP):
                continue
            toks.append(['call', it[2]])
        elif it[1] == '?':
            toks.append(['call', it[2]])
    return toks

cases = {k: {'reader': v['reader']} for k, v in json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_readers_merged.json')).items() if 'reader' in v}
out = {}
for cid, v in sorted(cases.items()):
    fn = int(v['reader'], 16)
    items, notes, loops, insns = parse(fn)
    tops = wrap(loops, len(items))
    tree = build(items, (tops, loops), insns) if loops else items
    spec = to_spec(tree)
    s, e, name = func_bounds(fn)
    out[cid] = {'reader': v['reader'], 'sym': dem(name), 'size': e - s,
                'spec': spec, 'notes': notes[:12], 'n_loops': len(loops)}
    print(cid, dem(name)[:50], 'size=%d loops=%d' % (e - s, len(loops)), json.dumps(spec)[:100])

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json', 'w'), indent=1)
print('saved')
