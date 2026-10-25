#!/usr/bin/env python3
"""s59 T2 part 4: keep the rAF loop alive in enemy mode until mercTick reports,
then finalize the gate (finalizeGate deferral under ?enemy=1)."""

WT = '/tmp/my-project/work/ghpages_staged_wt/playable'
H = f'{WT}/integration_lazy.html'

def patch(old, new, tag):
    src = open(H, encoding='utf-8').read()
    assert src.count(old) == 1, f'{tag}: count={src.count(old)}'
    out = src.replace(old, new)
    assert out != src, f'{tag}: no change'
    open(H, 'wb').write(out.encode('utf-8'))
    print(f'patched {tag}')

patch("""  g.consoleErrors = window.__consoleErrors.slice(0, 10);
  g.heap_mb = heapMB();
  g.heap_mb_peak = Math.max(heapMB(), ...(g.heapSamples.filter(x => x > 0)));
  g.wall_ms = Math.round(performance.now() - T0GLOBAL);
  g.ready = true;
  g.done = true;
}""",
      """  g.consoleErrors = window.__consoleErrors.slice(0, 10);
  g.heap_mb = heapMB();
  g.heap_mb_peak = Math.max(heapMB(), ...(g.heapSamples.filter(x => x > 0)));
  g.wall_ms = Math.round(performance.now() - T0GLOBAL);
  g.ready = true;
  // s59 T2: in enemy mode, hold `done` until the merc playback report exists
  // (mercTick runs inside the rAF loop, which stops at done), then finish.
  if (QS2.get('enemy') === '1' && !g.enemyPlay) {
    g.pendingFinalize = extra || {};
    return;
  }
  g.done = true;
}""",
      'finalize deferral')
patch("""  if (t > 12 && !mercSeq.reported) {""",
      """  if (t > 12 && !mercSeq.reported && mercSkinProbe) {""",
      'report guard')
patch("""    log('enemy playback: wraps=' + mercSeq.wraps + ' disp=' + JSON.stringify(disp) + ' ctlWrong=' + dispCtl +
        ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');
  }
}""",
      """    log('enemy playback: wraps=' + mercSeq.wraps + ' disp=' + JSON.stringify(disp) + ' ctlWrong=' + dispCtl +
        ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');
    if (window.__GATE.pendingFinalize && !window.__GATE.done) {
      const extra = window.__GATE.pendingFinalize; window.__GATE.pendingFinalize = null;
      finalizeGate(extra);
    }
  }
}""",
      'finalize resume')
print('OK')
