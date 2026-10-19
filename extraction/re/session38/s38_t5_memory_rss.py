#!/usr/bin/env python3
"""S38 T5.3c: true RSS of the browser during the lazy load (ArrayBuffers are
external memory — CDP JSHeapUsedSize excludes them)."""
import json, subprocess, sys, time, os
import psutil
PAGE = '/tmp/my-project/work/TDKR-Game/gh-pages/playable'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8895', '-d', PAGE],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto('http://127.0.0.1:8895/pipeline.html')
        chrome_pid = None
        for p in psutil.process_iter(['name', 'cmdline', 'create_time']):
            try:
                cl = ' '.join(p.info['cmdline'] or [])
                if 'headless' in cl or ('chrome' in cl.lower() and 'type=' not in cl):
                    if p.info['create_time'] > time.time() - 30:
                        chrome_pid = p.pid; break
            except Exception: pass
        print('chrome main pid:', chrome_pid)
        root = psutil.Process(chrome_pid)
        def rss_all():
            total = 0
            for p in [root] + root.children(recursive=True):
                try: total += p.memory_info().rss
                except Exception: pass
            return total
        base = rss_all()
        pg.set_input_files('#f', ZIP)
        peaks = [base]
        for _ in range(300):
            peaks.append(rss_all())
            try:
                if pg.evaluate("document.getElementById('log').textContent.includes('READY')"):
                    peaks.append(rss_all())
                    break
            except Exception: break
        peak = max(peaks)
        print(f'browser RSS: baseline {base/1e6:.0f} MB -> PEAK {peak/1e6:.0f} MB (delta {(peak-base)/1e6:.0f} MB)')
        json.dump({'rss_baseline_mb': round(base/1e6), 'rss_peak_mb': round(peak/1e6),
                   'rss_delta_mb': round((peak-base)/1e6)},
                  open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t5_memory_rss.json', 'w'), indent=1)
        b.close()
finally:
    srv.terminate()
