#!/usr/bin/env python3
"""S38 T5.3: browser memory of the LAZY pipeline (target < 300 MB)."""
import json, subprocess, sys, time, glob
PAGE = '/tmp/my-project/work/TDKR-Game/gh-pages/playable'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8897', '-d', PAGE],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8897/pipeline.html')
        pg.set_input_files('#f', ZIP)
        peaks = []
        t0 = time.time()
        for i in range(400):
            try:
                m = pg.evaluate("performance.memory ? performance.memory.usedJSHeapSize : 0")
                if m: peaks.append(m)
            except Exception:
                break
            try:
                done = pg.evaluate("document.getElementById('log').textContent.includes('READY')")
            except Exception:
                done = False
            if done:
                m = pg.evaluate("performance.memory ? performance.memory.usedJSHeapSize : 0")
                peaks.append(m)
                break
            time.sleep(0.05)
        peak = max(peaks, default=0)
        log = pg.evaluate("document.getElementById('log').textContent")
        print(log[-600:])
        # boundary-key fix check: walk Pelvis track first quats
        chk = pg.evaluate('''(() => {
          const glb = window.__glb; if (!glb) return null;
          const jl = new DataView(glb.buffer, glb.byteOffset, glb.byteLength).getUint32(12, true);
          const js = JSON.parse(new TextDecoder().decode(glb.slice(20, 20 + jl)));
          const binOff = 20 + jl + 8;
          const an = js.animations.find(a => a.name === '_007_walk');
          if (!an) return 'no walk';
          const ch = an.channels.find(c => js.nodes[c.target.node].name === 'Bip01_Pelvis' && c.target.path === 'rotation');
          if (!ch) return 'no pelvis rot';
          const s = an.samplers[ch.sampler];
          const ta = js.accessors[s.input], oa = js.accessors[s.output];
          const tbv = js.bufferViews[ta.bufferView], obv = js.bufferViews[oa.bufferView];
          const tt = new Float32Array(glb.slice(binOff + tbv.byteOffset, binOff + tbv.byteOffset + ta.count * 4).slice().buffer);
          const qq = new Float32Array(glb.slice(binOff + obv.byteOffset, binOff + obv.byteOffset + oa.count * 16).slice().buffer);
          return { n: ta.count, t0: tt[0], t1: tt[1], q0: [qq[0], qq[1], qq[2], qq[3]].map(x => +x.toFixed(4)) };
        })()''')
        print('walk Pelvis track after fix:', chk)
        print(f'PEAK JS heap: {peak/1e6:.1f} MB over {len(peaks)} samples, total {time.time()-t0:.1f} s')
        print('errors:', errs[:3])
        json.dump({'peak_heap_mb': round(peak/1e6, 1), 'errors': errs,
                   'samples': peaks[-8:]},
                  open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t5_memory.json', 'w'), indent=1)
        b.close()
finally:
    srv.terminate()
