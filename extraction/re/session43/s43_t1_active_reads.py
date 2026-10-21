#!/usr/bin/env python3
"""s43 T1h: classify MC_MAX_DISTANCE occurrences as commented-out vs active code.
Line-based state machine over Lua source: '--' line comments + '--[[' block comments.
Arithmetic use = same line contains MC_MAX_DISTANCE adjacent to * / + - or is used
in numeric context; also record the enclosing call family."""
import struct, re, collections

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla'
raw = open(P, 'rb').read()
tag, idxsz, tabsz, nent = struct.unpack_from('>4I', raw, 0)
ents = [struct.unpack_from('>4I', raw, 16 + i * 16) for i in range(nent)]
pool = 16 + nent * 16
mem = {}
for (o, s, no, _p) in ents:
    e = raw.find(b'\0', pool + no)
    mem[raw[pool + no:e].decode('ascii', 'replace')] = (o, s)

NAME = b'MC_MAX_DISTANCE'


def classify_text(blob, label, results):
    text = blob.decode('latin-1')
    lines = text.split('\n')
    in_block = 0  # --[[ depth (Lua 5.1 has no nested block comments, but be safe)
    stats = collections.Counter()
    samples = {'active_arith': [], 'active_arg': [], 'commented': []}
    for ln_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if in_block:
            stats['commented'] += line.count(NAME.decode())
            for m in re.finditer(NAME.decode(), line):
                samples['commented'].append((label, ln_no, line.strip()[:110]))
            if ']]' in line:
                in_block = 0
            continue
        # find block-comment start NOT preceded by active code on same line
        body = line
        bidx = body.find('--[[')
        lidx = body.find('--')
        n = len(re.findall(NAME.decode(), body))
        if n == 0:
            continue
        if lidx >= 0 and body[:lidx].strip() == '':
            stats['commented'] += n
            for m in re.finditer(NAME.decode(), body):
                samples['commented'].append((label, ln_no, body.strip()[:110]))
            if bidx >= 0:
                in_block = 1
            continue
        # active line (possibly trailing comment after code)
        code_part = body[:lidx] if lidx >= 0 else body
        m = re.search(NAME.decode(), code_part)
        if not m:
            # name only in trailing comment
            stats['commented'] += n
            continue
        stats['active'] += len(re.findall(NAME.decode(), code_part))
        arith = bool(re.search(r'[\w\)\]]\s*[*+\-/%]\s*MC_MAX_DISTANCE|MC_MAX_DISTANCE\s*[*+\-/%]', code_part))
        calls = re.findall(r'(\w+)\s*\(', code_part[:m.start()])
        fam = calls[-1] if calls else '?'
        if arith:
            stats['active_arith'] += 1
            if len(samples['active_arith']) < 6:
                samples['active_arith'].append((label, ln_no, body.strip()[:110]))
        else:
            stats['active_arg'] += 1
            if len(samples['active_arg']) < 8:
                samples['active_arg'].append((label, ln_no, body.strip()[:110], fam))
    for k, v in stats.items():
        results[k] += v
    return samples


results = collections.Counter()
all_samples = {'active_arith': [], 'active_arg': [], 'commented': []}
targets = [nm for nm in mem if nm.endswith('.lvc')]
for nm in sorted(targets):
    o, s = mem[nm]
    smp = classify_text(raw[o:o + s], nm, results)
    for k in all_samples:
        all_samples[k].extend(smp[k])

print('=== .lvc members (line-classified) ===')
print(dict(results))
print('\nactive arithmetic samples:')
for s in all_samples['active_arith']:
    print('  ', s)
print('\nactive argument-use samples:')
for s in all_samples['active_arg'][:8]:
    print('  ', s)

# gol.bin: binary with embedded Lua — count name occurrences in printable runs
o, s = mem['gol.bin']
blob = raw[o:o + s]
runs = []
for m in re.finditer(rb'[\x20-\x7e\t\n\r]{40,}', blob):
    runs.append(m)
print(f'\n=== gol.bin: {len(runs)} printable runs >=40 B ===')
tot = 0
cls = collections.Counter()
arith_samples = []
for m in runs:
    txt = m.group(0).decode('latin-1')
    n = txt.count('MC_MAX_DISTANCE')
    if not n:
        continue
    tot += n
    for line in txt.split('\n'):
        if 'MC_MAX_DISTANCE' not in line:
            continue
        st = line.strip()
        if st.startswith('--'):
            cls['commented'] += 1
        else:
            if re.search(r'[\w\)\]]\s*[*+\-/%]\s*MC_MAX_DISTANCE|MC_MAX_DISTANCE\s*[*+\-/%]', st):
                cls['active_arith'] += 1
                if len(arith_samples) < 8:
                    arith_samples.append(st[:110])
            else:
                cls['active_arg'] += 1
print(f'MC_MAX_DISTANCE in gol.bin printable runs: {tot}; classify: {dict(cls)}')
print('gol.bin active-arithmetic samples:')
for s2 in arith_samples:
    print('  ', s2)
