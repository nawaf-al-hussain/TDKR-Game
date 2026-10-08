#!/usr/bin/env python3
"""FUNC symbols from `readelf -sW` (robust vs manual section-header math;
libKRHP_symbols.txt has +0x10000 shifts from a sibling build, so this is the
ground-truth address source for the banked lib_libKRHP.so)."""
import subprocess, re

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'

def load_funcs():
    out = subprocess.run(['readelf', '-sW', SO], capture_output=True, text=True).stdout
    funcs = {}
    for ln in out.splitlines():
        m = re.match(r'\s*\d+:\s+([0-9a-f]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(\S+)', ln)
        if not m:
            continue
        va, size, name = int(m.group(1), 16), int(m.group(2)), m.group(3)
        if size == 0 or not name or name.startswith('$'):
            continue
        if va in funcs:
            old = funcs[va][0]
            if '4LoadE' in name and '4LoadE' not in old:
                funcs[va] = (name, size)
        else:
            funcs[va] = (name, size)
    return funcs

if __name__ == '__main__':
    f = load_funcs()
    print(len(f), 'funcs')
    print([ (hex(a), n, s) for a, (n, s) in sorted(f.items()) if 'CBeastObjectComponent4Load' in n ])
