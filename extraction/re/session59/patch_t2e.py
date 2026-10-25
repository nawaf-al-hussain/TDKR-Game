#!/usr/bin/env python3
"""s59 T2 part 5: hoist mercTick into the walk-phase branch + guard finishWalk."""

WT = '/tmp/my-project/work/ghpages_staged_wt/playable'
H = f'{WT}/integration_lazy.html'

def patch(old, new, tag):
    src = open(H, encoding='utf-8').read()
    assert src.count(old) == 1, f'{tag}: count={src.count(old)}'
    out = src.replace(old, new)
    assert out != src, f'{tag}: no change'
    open(H, 'wb').write(out.encode('utf-8'))
    print(f'patched {tag}')

patch("""    bCam.position.set(P.x, P.z + 1.9, -P.y + 3.8);
    bCam.lookAt(P.x, P.z - 0.75, -P.y);
    bRenderer.render(bScene, bCam);
  }
  // walk samples at +2s/+4s/+6s after walk phase start""",
      """    bCam.position.set(P.x, P.z + 1.9, -P.y + 3.8);
    bCam.lookAt(P.x, P.z - 0.75, -P.y);
    bRenderer.render(bScene, bCam);
  }
  if (merc) mercTick(now);   // s59 T2: enemy playback continues through the walk phase
  // walk samples at +2s/+4s/+6s after walk phase start""",
      'mercTick hoist')
patch("""  if (SAMP.s.length === 3) finishWalk();
}""",
      """  if (SAMP.s.length === 3 && !SAMP.walkFinished) { SAMP.walkFinished = true; finishWalk(); }
}""",
      'finishWalk guard')
print('OK')
