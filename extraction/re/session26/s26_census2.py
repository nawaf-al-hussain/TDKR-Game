#!/usr/bin/env python3
"""Session 26 T1 — deep censuses: collision, trigger->Lua, spawns, mesh,
Lua API usage ranking (vs the 747 registry), Lua union accounting."""
import json, sys, struct, collections, re

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TABLE_DIR = '/home/z/my-project/work/TDKR-Game/extraction/re/session26'
DATA = '/home/z/my-project/work/data'
OUT = '/tmp/my-project/work/s26_t1'

CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(')


def main():
    table, templates = lvc_pure.load_table(TABLE_DIR)
    gol = json.load(open(f'{TABLE_DIR}/lvc_gol_templates.json'))
    tmpl_names = gol['names']
    registry = [l.strip() for l in open(
        '/home/z/my-project/work/TDKR-Game/extraction/ghidra/'
        'lua_api.txt') if l.strip()]
    reg = set(registry)
    lua_calls = collections.Counter()
    lua_bytes_by_owner = collections.Counter()
    trigger_count = 0
    trigger_lua_bytes = 0
    trigger_scripts = 0
    spawn_count = 0
    mesh_records = []
    collision = []          # (island, owner_name, prim_name, tris, bbox, flags)
    total_tri = 0
    str_bytes_lua = 0       # all string-pool bytes that look like Lua
    lua_pool_count = 0
    out = {}

    for isl in ('GothamCity', 'GothamCity_Island2'):
        toks = []
        res = lvc_pure.parse(f'{DATA}/{isl}.lvc', table, templates,
                             tokens_out=toks)
        recs = res['records']
        strings = res['strings']
        nstr = len(strings)
        # rebuild token slices by record id
        bounds = [(r[1], r[3], r[0], r[2]) for r in recs]
        slices = {}
        bi = 0
        cur = []
        for t in toks:
            while bi < len(bounds) and t[1] >= bounds[bi][1]:
                slices[bounds[bi][2]] = cur
                cur = []
                bi += 1
            cur.append(t)
        if cur:
            slices[bounds[bi][2]] = cur

        # pool-level Lua census
        for s in strings:
            if len(s) > 40 and ('function ' in s or s.startswith('--') or
                                'end' in s and '(' in s):
                str_bytes_lua += len(s)
                lua_pool_count += 1

        for rid, off, tid, end, _kind in [(r[0], r[1], r[2], r[3], r[4])
                                          for r in recs]:
            tk = slices.get(rid, [])
            # record owner name: first STR token (0x152b87 name comp or
            # spawn/mesh names)
            strs = [t[3] for t in tk if t[0] == 'STR' and
                    isinstance(t[3], str)]
            owner = strs[0] if strs else None
            # walk components: need per-component boundaries -> re-derive
            # from the template order by scanning tokens
            if tid in templates:
                comps = [c for f, c in templates[tid] if f == 0]
            else:
                comps = []
            # trigger components: CTriggerComponent = 0x37f7a8ae = 938977454
            # token pattern [i, 9f, i, c, STR(lua), i, c]
            i = 0
            n = len(tk)
            # find STR tokens that hold Lua source
            for j, t in enumerate(tk):
                if t[0] == 'STR' and isinstance(t[3], str) and \
                        len(t[3]) > 60 and ('function ' in t[3] or
                                            'end' in t[3]):
                    lua_bytes_by_owner[owner or f'tid{tid:#x}'] += len(t[3])
            # count triggers + spawns + meshes via dedicated handling
            if tid == 0x2662:
                spawn_count += 1
            if tid in (0x14050, 0x14051):
                mesh_records.append((isl, hex(tid), owner,
                                     [t[3] for t in tk if t[0] == 'f'][:3]))

        # collision census: components of class 766542306 — replay spec
        # semantics per record using the pure token stream: prefix
        # [c,c,STR,i,c,c,i][c nprims] then prims [STR, i, tris x (9f+c)]
        colspec_pos = []
        for rid, off, tid, end, _ in [(r[0], r[1], r[2], r[3], 0)
                                      for r in recs]:
            tk = slices.get(rid, [])
            if not tk:
                continue
            # locate collision components by re-walking the template
            if tid not in templates:
                continue
            pos = 1   # skip tid token
            for flag, ctid in templates[tid]:
                if flag:
                    continue
                ks = str(ctid)
                spec = table['components'].get(ks)
                if spec is None:
                    break
                comp_start = pos
                consumed = component_len(spec, tk, pos)
                if consumed is None:
                    break
                if ks == '766542306':
                    parse_collision(tk, comp_start, owner or f'tid{tid:#x}',
                                    isl, collision)
                if ks == '938977454':
                    trigger_count += 1
                    # trigger Lua = the STR at component-token index 12
                    # (component = [i, 9f, i, c, STR, i, c] = 15 tokens)
                    ct = tk[comp_start:comp_start + 15]
                    if len(ct) >= 13 and ct[12][0] == 'STR' and \
                            isinstance(ct[12][3], str):
                        lua = ct[12][3]
                        trigger_lua_bytes += len(lua)
                        lua_calls.update(m.group(1)
                                         for m in CALL_RE.finditer(lua)
                                         if m.group(1) in reg)
                        trigger_scripts += 1
                pos += consumed
        # count triangles from the collision census rows for this island
        isl_tris = sum(c[4] for c in collision if c[0] == isl)
        out[isl] = dict(triangles=isl_tris,
                        collision_comps=sum(1 for c in collision
                                            if c[0] == isl))

    total_tri = sum(c[4] for c in collision)
    out['collision_total'] = dict(components=len(collision),
                                  triangles=total_tri)
    out['triggers'] = trigger_count
    out['trigger_lua'] = dict(scripts=trigger_scripts,
                              bytes=trigger_lua_bytes)
    out['spawns'] = spawn_count
    out['mesh_records'] = len(mesh_records)
    out['lua_pool'] = dict(strings=lua_pool_count, bytes=str_bytes_lua)
    out['lua_trigger_bytes'] = dict(sum_bytes=sum(lua_bytes_by_owner.values()))
    top = lua_calls.most_common(30)
    out['lua_api_top30'] = top
    out['lua_api_distinct'] = len(lua_calls)
    json.dump(out, open(f'{OUT}_censuses.json', 'w'), indent=1)
    json.dump(collision[:4000], open(f'{OUT}_collision.json', 'w'))
    print('collision:', out['collision_total'])
    print('trigger lua:', trigger_scripts, 'scripts,', trigger_lua_bytes, 'B')
    print('triggers:', trigger_count, ' spawns:', spawn_count,
          ' mesh:', len(mesh_records))
    print('lua pool:', out['lua_pool'])
    print('lua trigger-owned bytes:', out['lua_trigger_bytes'])
    print('lua api distinct:', out['lua_api_distinct'])
    print('top:', top[:12])


def component_len(spec, tk, pos):
    """Compute token-count consumption of a spec starting at tk[pos]."""
    def size_of(tok):
        if tok[0] == 'raw':
            return tok[1]
        if tok[0] == 'fat':
            return tok[2]
        return {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}[tok[0]]
    n = 0
    i = 0
    start = pos
    while i < len(spec):
        tok = spec[i]
        if tok[0] == 'rep':
            if pos >= len(tk):
                return None
            count = tk[pos - 1][3]
            if not isinstance(count, int) or count < 0 or count > 100000:
                return None
            inner = 0
            for _ in range(count):
                for t2 in tok[2]:
                    if t2[0] == 'rep':
                        if pos >= len(tk):
                            return None
                        c2 = tk[pos - 1][3]
                        if not isinstance(c2, int) or c2 < 0 or c2 > 100000:
                            return None
                        inner2 = sum(size_of(x) for x in t2[2]) * 0
                        # inner-inner: only collision uses it; compute via
                        # sizes
                        sub = 0
                        for x in t2[2]:
                            sub += size_of(x)
                        # count c2 iterations of t2[2] (each = sub bytes)
                        consumed_bytes = sub * c2
                        # convert to token count via tk scan
                        b = 0
                        while b < consumed_bytes and pos < len(tk):
                            b += tk[pos][2]
                            pos += 1
                        inner += 1
                    else:
                        pos += 1
            i += 1
        else:
            pos += 1
            i += 1
    return pos - start


def parse_collision(tk, pos, owner, isl, out_rows):
    """Decode one collision component's census row from tokens."""
    try:
        # prefix [c,c,STR,i,c,c,i][c nprims]
        if pos + 8 > len(tk):
            return
        prim_name = tk[pos + 2][3]
        nprims = tk[pos + 7][3]
        if not isinstance(nprims, int) or nprims < 0 or nprims > 64:
            return
        p = pos + 8
        tris_total = 0
        bbox = [1e30, 1e30, 1e30, -1e30, -1e30, -1e30]
        flags = collections.Counter()
        names = []
        for _ in range(nprims):
            if p + 2 > len(tk):
                return
            nm = tk[p][3]
            tris = tk[p + 1][3]
            if not isinstance(tris, int) or tris < 0 or tris > 40000:
                return
            names.append(nm if isinstance(nm, str) else None)
            p += 2
            for _ in range(tris):
                if p + 10 > len(tk):
                    return
                vs = []
                for k in range(9):
                    v = tk[p + k][3]
                    vs.append(v)
                flags[tk[p + 9][3]] += 1
                for k in range(3):
                    bbox[k] = min(bbox[k], vs[k * 3 + 0]) if False else bbox[k]
                # bbox over all 9 components (3 verts x xyz)
                for k in range(9):
                    if k % 3 == 0:
                        bbox[0] = min(bbox[0], vs[k])
                    elif k % 3 == 1:
                        bbox[1] = min(bbox[1], vs[k])
                    else:
                        bbox[2] = min(bbox[2], vs[k])
                    if k % 3 == 0:
                        bbox[3] = max(bbox[3], vs[k])
                    elif k % 3 == 1:
                        bbox[4] = max(bbox[4], vs[k])
                    else:
                        bbox[5] = max(bbox[5], vs[k])
                p += 10
            tris_total += tris
        out_rows.append((isl, owner, prim_name,
                         '|'.join(n or '?' for n in names)[:40],
                         tris_total,
                         [round(v, 2) for v in bbox],
                         dict(flags)))
    except (IndexError, TypeError):
        return


if __name__ == '__main__':
    main()
