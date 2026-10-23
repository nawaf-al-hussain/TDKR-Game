#!/usr/bin/env python3
"""s54 T5: memory FLOOR components, measured separately in the same headless
Chromium (2-core, swiftshader):
  A. empty page (three r160 module import only, same CDN as the game page)
  B. integration_lazy.html default (full pipeline)
  C. integration_lazy.html ?poolchunk=1 (s53 best)
  D. three + WebGL context only (clear-only render loop, no scene)
Each run: renderer RSS peak + timeline + JS heap; the deltas give the floor
breakdown. No page changes -> digests unaffected (the s54 gate already passed)."""
import json, time, socket, threading, http.server, functools, subprocess, sys, os

PORT = 8161
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session54/'

EMPTY_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<script type="module">
  import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
  window.__THREE_OK = !!THREE.Scene;
  window.__GATE = { done: true, pass: true, kind: 'empty-three' };
</script></body></html>"""

GL_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<script type="module">
  import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
  const c = document.createElement('canvas'); c.width = 1024; c.height = 605;
  const gl = c.getContext('webgl', { antialias: false });
  const texs = [];
  for (let i = 0; i < 170; i++) {
    const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 512, 512, 0, gl.RGBA, gl.UNSIGNED_BYTE,
                  new Uint8Array(512 * 512 * 4));
    texs.push(t);
  }
  gl.clearColor(0.2, 0.3, 0.4, 1); gl.clear(gl.COLOR_BUFFER_BIT);
  window.__GL_ONLY = { texs: texs.length, three: !!THREE.Scene };
  window.__GATE = { done: true, pass: true, kind: 'gl-textures-only' };
</script></body></html>"""

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def rss_of_chromium():
    try:
        out2 = subprocess.run(['ps', '-eo', 'rss=,args='], capture_output=True, text=True).stdout
        vals = []
        rend = 0
        for l in out2.splitlines():
            low = l.lower()
            if ('chrome-headless-shell' in low or 'chrome' in low) and 'ps -eo' not in low and '/ps' not in low:
                try:
                    kb = int(l.strip().split()[0])
                    vals.append(kb)
                    if '--type=renderer' in l:
                        rend = max(rend, kb)
                except Exception:
                    pass
        return sum(vals) / 1024.0, rend / 1024.0
    except Exception:
        return 0.0, 0.0

def run_url(name, url, qs=None, zip_file=None, budget=420, min_s=6):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    wait_port(PORT)
    # serve the synthetic pages from a temp dir
    tmpdir = '/tmp/my-project/work/ghpages_staged_wt/_s54mem'
    os.makedirs(tmpdir, exist_ok=True)
    open(tmpdir + '/empty.html', 'w').write(EMPTY_HTML)
    open(tmpdir + '/glonly.html', 'w').write(GL_HTML)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'console_errors': [], 'page_errors': [],
           'rss_renderer_samples': [], 'rss_tree_samples': []}
    stop = [False]
    def poll():
        while not stop[0]:
            tot, rend = rss_of_chromium()
            rec['rss_renderer_samples'].append(round(rend, 1))
            rec['rss_tree_samples'].append(round(tot, 1))
            time.sleep(0.3)
    threading.Thread(target=poll, daemon=True).start()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: rec['console_errors'].append(m.text[:150]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:150]))
        t0 = time.time()
        last = None
        for attempt in range(3):
            try:
                page.goto(url, timeout=60000, wait_until='domcontentloaded')
                last = None
                break
            except Exception as e:
                last = e
                time.sleep(2)
        if last is not None:
            rec['page_errors'].append('goto failed: %r' % last)
            browser.close()
            stop[0] = True
            httpd.shutdown(); httpd.server_close()
            rec['rss_renderer_peak'] = 0; rec['rss_tree_peak'] = 0
            return rec
        if zip_file:
            page.set_input_files('#f', zip_file)
        gate = {}
        while time.time() - t0 < budget:
            time.sleep(1)
            try:
                gate = page.evaluate('window.__GATE || {}')
            except Exception:
                gate = {}
            if gate.get('done') and time.time() - t0 > min_s:
                break
        rec['elapsed_s'] = round(time.time() - t0, 1)
        try:
            rec['jsheap'] = page.evaluate(
                '(performance.memory && performance.memory.usedJSHeapSize / 1048576) || null')
        except Exception:
            rec['jsheap'] = None
        rec['gate'] = {k: gate.get(k) for k in ('done', 'pass', 'soup', 'first_image_ms', 'kind')}
        browser.close()
    stop[0] = True
    time.sleep(0.5)
    rec['rss_renderer_peak'] = max(rec['rss_renderer_samples']) if rec['rss_renderer_samples'] else 0
    rec['rss_tree_peak'] = max(rec['rss_tree_samples']) if rec['rss_tree_samples'] else 0
    httpd.shutdown(); httpd.server_close()
    print(name, '-> renderer peak %.1f MB, tree peak %.1f MB, %s errs' %
          (rec['rss_renderer_peak'], rec['rss_tree_peak'],
           len(rec['console_errors']) + len(rec['page_errors'])), flush=True)
    return rec

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    outp = OUTDIR + 's54_t5_mem.json'
    out = json.load(open(outp)) if os.path.exists(outp) else {}
    if which in ('all', 'empty'):
        out['empty_three'] = run_url('empty_three', 'http://127.0.0.1:%d/_s54mem/empty.html' % PORT)
    if which in ('all', 'glonly'):
        out['gl_textures_only'] = run_url('gl_textures_only', 'http://127.0.0.1:%d/_s54mem/glonly.html' % PORT)
    if which in ('all', 'default'):
        out['game_default'] = run_url('game_default', 'http://127.0.0.1:%d/playable/integration_lazy.html' % PORT,
                                      zip_file=ZIP)
    if which in ('all', 'poolchunk'):
        out['game_poolchunk'] = run_url('game_poolchunk', 'http://127.0.0.1:%d/playable/integration_lazy.html?poolchunk=1' % PORT,
                                        zip_file=ZIP)
    json.dump(out, open(outp, 'w'), indent=1)
    print('saved', outp)

if __name__ == '__main__':
    main()
