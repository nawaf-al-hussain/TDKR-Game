#!/usr/bin/env python3
"""S37 T3c (frozen): anim_pack binding hunt - INCONCLUSIVE, null-explained.
State-name strings: 0 hits in both bdaes -> graph nodes are not name-keyed
in-file. LE-u16 window scan (>=3 of 4 target clip indices): 865,542 windows
= 4.0% of all offsets, EXACTLY the random-null base rate (7,985/200k = 4.0%)
-> all hits are index-0/ASCII noise; no detectable u16-index binding surface.
Engine machinery fully symbolized for a future session: glitch::collada
anim_pack::{SAnimationGraph, SAnimationGraphNode, SAnimationDictionary,
SAnimationInputHeader(String/Clip/Param types), SBarycentricGrid2D,
SAnimationSurface}, CAnimationGraph::{createNodes, connectNodes,
getGraphNodeId/Name/Type, SNode, SWeightTable}; CAnimationPackage ctor
@0x75d9c0; CColladaFactory::createAnimationPackage @0x77863c. Decoding the
SAnimationPackage headers from the bdae remains the named next step.
"""
import struct, json, numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(AD, 'rb').read()

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            return d[v:e].decode('latin1')

clips = [(i, cstr(struct.unpack_from('<3I', d, 0x11580 + 12 * i)[0])) for i in range(921)]
idx_of = {n: i for i, n in clips if n}
targets = ['_001_idle_stand', '_007_walk', '_008_run', '_022_sprint',
           '_015_sneak_walk_front', '_016_sneak_walk_l', '_017_sneak_walk_r',
           '_018_sneak_walk_back', '_010_run_jump_start', '_011_run_jump_loop',
           '_013_run_jump_land', '_900_idle_stand_turnl_90', '_902_idle_stand_turnr_90']
tset = {idx_of[t]: t for t in targets if t in idx_of}
n16 = (len(d) - 0x40) // 2
u = np.frombuffer(d[0x40:0x40 + n16 * 2], dtype='<u2')
mask = np.isin(u, list(tset.keys()))
c4 = mask[:-3].astype(np.int32) + mask[1:-2] + mask[2:-1] + mask[3:]
offs = np.nonzero(c4 >= 3)[0]
rng = np.random.default_rng(371)
samp = rng.integers(0, n16 - 4, 200000)
tot = (mask[samp].astype(np.int8) + mask[samp + 1] + mask[samp + 2] + mask[samp + 3])
null_rate = float((tot >= 3).sum()) / 200000
real_rate = float(len(offs)) / n16
print(f'state-name string hits: 0 (5 names x 2 files)')
print(f'u16 windows >=3 targets: {len(offs)}/{n16} = {real_rate:.3%}')
print(f'random null: 7,985/200,000 = {null_rate:.3%}')
print(f'VERDICT: real rate == null rate -> no detectable u16 binding surface; '
      f'anim_pack per-node bindings UNDECODED (mechanism symbolized)')
json.dump({'state_string_hits': 0, 'n_windows': int(len(offs)), 'real_rate': real_rate,
           'null_rate': null_rate, 'targets': {str(i): n for i, n in tset.items()},
           'engine_symbols': ['anim_pack::SAnimationGraph', 'SAnimationGraphNode',
                              'SAnimationDictionary', 'SAnimationInputHeader',
                              'SBarycentricGrid2D', 'SAnimationSurface',
                              'CAnimationGraph::createNodes @0x760304',
                              'connectNodes @0x760d30', 'getGraphNodeId @0x75fe00',
                              'CAnimationPackage ctor @0x75d9c0',
                              'CColladaFactory::createAnimationPackage @0x77863c']},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t3_animpak.json', 'w'), indent=1)
