#!/usr/bin/env python3
"""S40 T5: end-to-end memory measurement of the pipeline page.
zip -> actors.gla -> anims -> skin -> READY, in headless Chromium:
- JS heap via performance.memory sampled in-page every 200 ms
- renderer process RSS via /proc polling (250 ms) from the OS side
- CDP Performance.getMetrics at READY
Also verifies the page still works after the s40 fixes (street SHA).
"""
import threading, http.server, functools, logging, time, json, subprocess, os, glob
logging.getLogger("http.server").disabled = True
from playwright.sync_api import sync_playwright

ROOT = '/tmp/my-project/work/ghpages_site_wt'
PORT = 8127
OUT = '/home/z/my-project/scripts/s40_t5_memory.json'
SHOT = '/home/z/my-project/scripts/s40_t5_street.png'
REF = '52fcbf324bdd24146b6261da45fc74f4dc9a1dd3715a9c1f71c83bc615331736'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

rss_samples = []
polling = [True]

def find_renderers():
    pids = []
    for p in glob.glob('/proc/[0-9]*/cmdline'):
        try:
            cl = open(p, 'rb').read().decode('latin1', 'replace')
            if '--type=renderer' in cl:
                pid = int(p.split('/')[2])
                pids.append(pid)
        except Exception:
            pass
    return pids

def poll_rss():
    while polling[0]:
        for pid in find_renderers():
            try:
                st = open(f'/proc/{pid}/status').read()
                rss = int([l for l in st.splitlines() if l.startswith('VmRSS')][0].split()[1])  # kB
                when = time.time()
                rss_samples.append((when, pid, rss))
            except Exception:
                pass
        time.sleep(0.25)

def main():
    th = threading.Thread(target=poll_rss, daemon=True)
    th.start()
    t_start = time.time()
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = b.new_context(viewport={'width': 1100, 'height': 800})
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(f'http://127.0.0.1:{PORT}/playable/pipeline.html')
        t_click = time.time()
        pg.set_input_files('#f', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
        pg.wait_for_function("document.querySelector('#log').textContent.includes('READY')",
                             timeout=240000)
        t_ready = time.time()
        pg.wait_for_timeout(4000)   # let GC settle + final samples
        memlog = pg.evaluate('window.__memLog')
        held = pg.evaluate('window.__held')
        street_sha = pg.evaluate("""async () => {
            if (!window.__streetRGBA) return null;
            const h = await crypto.subtle.digest('SHA-256', window.street_hash_probe || window.__streetRGBA);
            return [...new Uint8Array(h)].map(x => x.toString(16).padStart(2,'0')).join('');
        }""")
        cdp = ctx.new_cdp_session(pg)
        cdp.send('Performance.enable')
        metrics = cdp.send('Performance.getMetrics')['metrics']
        pg.screenshot(path=SHOT)
        b.close()
    polling[0] = False
    peak_heap = max((s[1] for s in memlog), default=0)
    peak_total = max((s[2] for s in memlog), default=0)
    end_heap = memlog[-1][1] if memlog else 0
    # renderer RSS: take per-pid peaks, then overall peak across pids
    by_pid = {}
    for when, pid, rss in rss_samples:
        by_pid.setdefault(pid, []).append((when, rss))
    peak_rss_pid, peak_rss = max(((pid, max(r for _, r in v)) for pid, v in by_pid.items()),
                                 key=lambda kv: kv[1], default=(None, 0))
    final_rss = min(((min(v, key=lambda x: abs(x[0] - t_ready))[1]) for v in by_pid.values()),
                    default=0)
    res = {
        'load_seconds': round(t_ready - t_click, 2),
        'js_heap_used_peak_bytes': peak_heap,
        'js_heap_total_peak_bytes': peak_total,
        'js_heap_used_at_ready_end_bytes': end_heap,
        'renderer_rss_peak_bytes': peak_rss * 1024,
        'renderer_rss_peak_pid': peak_rss_pid,
        'renderer_rss_near_ready_bytes': final_rss * 1024,
        'cdp_metrics': {m['name']: m['value'] for m in metrics
                        if m['name'] in ('JSHeapUsedSize', 'JSHeapTotalSize', 'Documents', 'Frames', 'JSEventListeners')},
        'held_buffers_reported_by_page': held,
        'street_sha_match': street_sha == REF,
        'page_errors': errs,
        'n_rss_samples': len(rss_samples),
        'timeline_kb': [[s[0], s[2]] for s in rss_samples[::8]],
    }
    json.dump(res, open(OUT, 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'timeline_kb'}, indent=1))

if __name__ == '__main__':
    main()
