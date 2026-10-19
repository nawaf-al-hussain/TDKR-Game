#!/usr/bin/env python3
"""S38 T5.2: skeleton-level parity digests, PYTHON side."""
import struct, hashlib, json
import numpy as np

src = open('/home/z/my-project/scripts/s36_t3_export.py').read()
head = src.split('# ---------- GLB assembly ----------')[0]
g = {'__name__': 'ctx'}
exec(head, g)

nodes = g['nodes']; joint_nodes = g['joint_nodes']
parent_name = g['parent_name']; invB = g['invB']; b4s = g['b4s']; w4s = g['w4s']

names_list = [n['name'] for n in nodes]
def parent_index(nm):
    p = parent_name(nm)
    return names_list.index(p) if p else -1
node_names = '|'.join(names_list)
parent_idx = ','.join(str(parent_index(nm)) for nm in names_list)
palette = '|'.join(joint_nodes)
ibm = b''.join(np.asarray(invB[b], '<f4').tobytes() for b in range(31))
skin_ids = b4s.astype(np.uint8).tobytes()
skin_w = w4s.astype('<f4').tobytes()

digests = {
    'node_names_sha': hashlib.sha256(node_names.encode()).hexdigest()[:16],
    'parent_idx_sha': hashlib.sha256(parent_idx.encode()).hexdigest()[:16],
    'palette_order_sha': hashlib.sha256(palette.encode()).hexdigest()[:16],
    'ibm_sha': hashlib.sha256(ibm).hexdigest()[:16],
    'skin_ids_sha': hashlib.sha256(skin_ids).hexdigest()[:16],
    'skin_w_sha': hashlib.sha256(skin_w).hexdigest()[:16],
    'n_nodes': len(nodes), 'n_palette': len(joint_nodes),
    'parent_idx': parent_idx,
    'palette': palette,
}
print(json.dumps({k: v for k, v in digests.items() if not k.endswith(('idx', 'palette'))}, indent=1))
json.dump(digests, open('/home/z/my-project/scripts/s38/s38_t5_digests_py.json', 'w'), indent=1)
print('parent_idx:', parent_idx)
print('palette:', palette)
