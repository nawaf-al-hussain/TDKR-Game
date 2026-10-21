#!/usr/bin/env python3
"""s44 T1: classify the ACTIVE MC_MAX_DISTANCE arithmetic uses by runtime reachability.

Scope model (line-based, best-effort): a stack of block types opened by
function/if/for/while/do(-while) and closed by end/until. A use is:
  TOPLEVEL      — no enclosing function (runs when the chunk is loaded)
  IN_FUNC       — inside a named function; the function's call sites are
                  searched across ALL .lvc members + gol.bin runs:
    CALLED      — a call site exists (funcname( or table.funcname()
    UNCALLED    — no call site in the shipped corpus (engine-registered or dead)
  IN_ANON       — inside an anonymous function (callback/event-handler shape)
Report per-class counts + consequence per class.
"""
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

NAME = 'MC_MAX_DISTANCE'
ARITH = re.compile(r'[\w\)\]]\s*[*+\-/%]\s*' + NAME + r'|' + NAME + r'\s*[*+\-/%]')
OPEN = re.compile(r'\b(function)\b|\b(if)\b|\b(for)\b|\b(while)\b|\b(do)\b')
FUNCPAT = re.compile(r'\bfunction\s+([A-Za-z_][\w\.:\[\]\'"]*)|local\s+function\s+([A-Za-z_]\w*)')

def strip_line_comment(line):
    # remove trailing -- comment (not inside a string — best effort)
    idx = line.find('--')
    return line[:idx] if idx >= 0 else line, idx

def classify_member(text, label, out, call_index):
    lines = text.split('\n')
    stack = []            # entries: 'func' / 'block' / 'anonfunc' / 'for' / 'while'
    func_names = []       # parallel stack: name of enclosing named functions
    in_block_comment = 0
    for ln_no, line in enumerate(lines, 1):
        if in_block_comment:
            if ']]' in line:
                in_block_comment = 0
            continue
        body, cidx = strip_line_comment(line)
        bstart = line.find('--[[')
        if bstart >= 0 and body[:bstart].strip() == '':
            in_block_comment = 1
            continue
        code = body
        # tokens on this line
        opens = []
        for m in re.finditer(r'\bfunction\b|\bif\b|\bfor\b|\bwhile\b|\bdo\b|\bend\b|\buntil\b|\brepeat\b', code):
            opens.append((m.start(), m.group(0)))
        # uses of NAME in this line's code part
        if NAME in code and not code.strip().startswith('--'):
            for m in re.finditer(re.escape(NAME), code):
                if ARITH.search(code, m.start() - 4, m.end() + 4):
                    scope = ('TOPLEVEL' if 'func' not in stack else
                             'IN_ANON' if stack[-1] == 'anonfunc' else 'IN_FUNC')
                    fname = None
                    for s in reversed(func_names):
                        if s:
                            fname = s
                            break
                    # find enclosing named function name (walk stack for funcs)
                    rec = {'file': label, 'line': ln_no, 'scope': scope, 'func': fname,
                           'text': code.strip()[:120]}
                    out.append(rec)
                    call_index.setdefault(fname, []).append(rec) if fname else None
        # update the block stack LEFT-TO-RIGHT
        for pos, kw in opens:
            if kw == 'function':
                # named? look at the text right after
                m2 = FUNCPAT.search(code, pos)
                nm = (m2.group(1) or m2.group(2)) if m2 and m2.start() == pos else None
                stack.append('func')
                func_names.append(nm)
            elif kw == 'if':
                stack.append('block')
                func_names.append(None)
            elif kw in ('for', 'while'):
                # a do follows later; approximate: push block now, the do is skipped
                stack.append('block')
                func_names.append(None)
            elif kw == 'do':
                # bare do (or after for/while — already pushed): push only if the
                # previous token isn't for/while
                prev = [k for _, k in opens if k in ('for', 'while') and _ < pos]
                if not prev or prev[-1] != prev[-1] or True:
                    # conservative: only push when the last pushed block wasn't just for/while
                    if not stack or stack[-1] not in ('block',) or True:
                        stack.append('block')
                        func_names.append(None)
            elif kw == 'repeat':
                stack.append('block')
                func_names.append(None)
            elif kw == 'until':
                if stack:
                    stack.pop()
                    func_names.pop()
            elif kw == 'end':
                if stack:
                    stack.pop()
                    func_names.pop()

# ---- pass 1: classify .lvc members ----
lvc_use = []
targets = [nm for nm in mem if nm.endswith('.lvc')]
for nm in sorted(targets):
    o, s = mem[nm]
    classify_member(raw[o:o + s].decode('latin-1'), nm, lvc_use, {})
print('active arithmetic uses found in .lvc:', len(lvc_use))
by_scope = collections.Counter(r['scope'] for r in lvc_use)
print('by scope:', dict(by_scope))

# ---- pass 2: build the call-site index over the whole corpus ----
corpus_calls = collections.Counter()
def index_calls(text, label):
    for m in re.finditer(r'([A-Za-z_][\w\.:\[\]\'"]*)\s*[\({]', text):
        corpus_calls[m.group(1)] += 1
for nm in sorted(targets):
    o, s = mem[nm]
    index_calls(raw[o:o + s].decode('latin-1'), nm)
# gol.bin printable runs
o, s = mem['gol.bin']
blob = raw[o:o + s]
for m in re.finditer(rb'[\x20-\x7e\t\n\r]{40,}', blob):
    index_calls(m.group(0).decode('latin-1'), 'gol.bin')

# ---- classify IN_FUNC uses by call sites ----
final = []
for r in lvc_use:
    sc = r['scope']
    if sc == 'IN_FUNC' and r['func']:
        base = r['func'].split('.')[-1].split(':')[-1].split('[')[0].strip("'\"")
        n = corpus_calls.get(base, 0) + corpus_calls.get(r['func'], 0)
        r['reach'] = 'CALLED' if n > 1 else 'UNCALLED-IN-CORPUS'   # >1: definition line + at least one other
        r['calls_seen'] = n
    elif sc == 'IN_FUNC':
        r['reach'] = 'IN_FUNC_UNNAMED'
    elif sc == 'IN_ANON':
        r['reach'] = 'IN_ANON'
    else:
        r['reach'] = 'TOPLEVEL'
    final.append(r)

by_reach = collections.Counter(r['reach'] for r in final)
print('\nreachability classification (best-effort scope model):')
for k, v in by_reach.most_common():
    print(f'  {k:24s} {v}')
print('\nTOPLEVEL samples (would error AT CHUNK LOAD):')
for r in final:
    if r['reach'] == 'TOPLEVEL':
        print('  ', r['file'], r['line'], r['text'])
print('\nIN_FUNC CALLED samples (error at call time):')
shown = 0
for r in final:
    if r['reach'] == 'CALLED' and shown < 8:
        print('  ', r['file'], r['line'], r['func'], 'calls=', r['calls_seen'], r['text'])
        shown += 1
print('\nIN_FUNC UNCALLED samples:')
shown = 0
for r in final:
    if r['reach'] == 'UNCALLED-IN-CORPUS' and shown < 8:
        print('  ', r['file'], r['line'], r['func'], 'calls=', r['calls_seen'], r['text'])
        shown += 1

import json
json.dump({'by_scope': dict(by_scope), 'by_reach': dict(by_reach), 'uses': final},
          open('/home/z/my-project/scripts/s44_t1_reach.json', 'w'), indent=1)
print('\nsaved s44_t1_reach.json')
