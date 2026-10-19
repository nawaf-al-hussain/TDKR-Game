#!/usr/bin/env python3
"""S38 T5.3b: CDP-tracked heap peak during the lazy pipeline load."""
import json, subprocess, sys, time
PAGE = '/tmp/my-project/work/TDKR-Game/gh-pages/playable'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8896', '-d', PAGE],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto('http://127.0.0.1:8896/pipeline.html')
        cdp = pg.context.new_cdp_session(pg)
        cdp.send('Performance.enable')
        samples = []
        pg.set_input_files('#f', ZIP)
        for _ in range(600):
            try:
                m = cdp.send('Performance.getMetrics')['metrics']
                d = {x['name']: x['value'] for x in m}
                samples.append((d.get('JSHeapUsedSize', 0), d.get('JSHeapTotalSize', 0)))
            except Exception:
                pass
            try:
                if pg.evaluate("document.getElementById('log').textContent.includes('READY')"):
                    m = cdp.send('Performance.getMetrics')['metrics']
                    d = {x['name']: x['value'] for x in m}
                    samples.append((d.get('JSHeapUsedSize', 0), d.get('JSHeapTotalSize', 0)))
                    break
            except Exception: break
        peak_used = max((s[0] for s in samples), default=0)
        peak_total = max((s[1] for s in samples), default=0)
        print(f'CDP peak used heap: {peak_used/1e6:.1f} MB; peak total: {peak_total/1e6:.1f} MB ({len(samples)} samples)')
        json.dump({'cdp_peak_used_mb': round(peak_used/1e6, 1), 'cdp_peak_total_mb': round(peak_total/1e6, 1),
                   'n_samples': len(samples)},
                  open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t5_memory_cdp.json', 'w'), indent=1)
        b.close()
finally:
    srv.terminate()
