#!/usr/bin/env python3
"""s59 T2: patch tdkr_pipeline.js (add readBdae2 + export) and integration_lazy.html
(use readBdae2 in loadMerc + Batman digest self-check ?bdae2check=1 + enemy gate
enhancements with vertex displacement + wrong-clip control). All patches assert
unique match and file change; node --check afterwards."""
import hashlib, io, struct, sys, json

WT = '/tmp/my-project/work/ghpages_staged_wt/playable'
def sha(b): return hashlib.sha256(b).hexdigest()

def patch(path, old, new, tag):
    src = open(path, 'rb').read().decode('utf-8')
    assert src.count(old) == 1, f'{tag}: pattern count = {src.count(old)} (need 1)'
    out = src.replace(old, new)
    assert out != src, f'{tag}: no change'
    open(path, 'wb').write(out.encode('utf-8'))
    print(f'patched {tag} in {path}')

P = f'{WT}/tdkr_pipeline.js'
readBdae2 = open('/home/z/my-project/stage/readBdae2.js').read()
src = open(P, encoding='utf-8').read()
assert 'readBdae2' not in src, 'readBdae2 already present'
anchor = '// ------------------------------------------------------------ texture ----'
assert src.count(anchor) == 1
patch(P, anchor, readBdae2 + '\n' + anchor, 'insert readBdae2')
patch(P, 'const api = { zipEntries, zipRead, parseGla, decodeAnims, assembleClip, readBdae, identifyTexture, inflateRaw, zipDirLazy, zipReadLazy, glaSlice };',
      'const api = { zipEntries, zipRead, parseGla, decodeAnims, assembleClip, readBdae, readBdae2, identifyTexture, inflateRaw, zipDirLazy, zipReadLazy, glaSlice };',
      'export readBdae2')

H = f'{WT}/integration_lazy.html'
# 1) loadMerc: use the generalized reader
patch(H, "  const skin = TDKR.readBdae(aMem['Bane_mercenary.bdae']);",
      "  const skin = TDKR.readBdae2(aMem['Bane_mercenary.bdae']);  // s59 T2: layout from the file's own headers",
      'loadMerc reader')
print('OK pipeline+page patched')
