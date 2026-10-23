#!/usr/bin/env python3
"""s54 T5 (inline floors): empty-three and gl-textures-only RSS peaks measured
with a foreground inline harness (the file-based runner hit transient goto
timeouts; inline runs are reliable). Results -> s54_t5_mem.json (floors key)."""
import json, time, socket, threading, http.server, functools, subprocess, os

WT = '/tmp/my-project/work/ghpages_staged_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session54/s54_t5_mem.json'

EMPTY = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<script type="module">
  import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
  window.__THREE_OK = !!THREE.Scene;
  window.__GATE = { done: true, pass: true, kind: 'empty-three' };
</script></body></html>"""

GLONLY = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
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

def rss_rend():
    out2 = subprocess.run(['ps', '-eo', 'rss=,args='], capture_output=True, text=True).stdout
    rend = 0
    for l in out2.splitlines():
        if '--type=renderer' in l and 'chrome' in l.lower():
            try:
                rend = max(rend, int(l.split()[0]))
            except Exception:
                pass
    return rend / 1024.0

def measure(name, html, hold_s=8):
    os.makedirs(WT + '/_s54mem', exist_ok=True)
    open(WT + '/_s54mem/' + name + '.html', 'w').write(html)
    PORT = 8171
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    socket.create_connection(('127.0.0.1', PORT), timeout=2)
    from playwright.sync_api import sync_playwright
    samples = []
    stop = [False]
    def poll():
        while not stop[0]:
            samples.append(rss_rend())
            time.sleep(0.25)
    threading.Thread(target=poll, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        pg = b.new_page(viewport={'width': 960, 'height': 600})
        pg.goto('http://127.0.0.1:%d/_s54mem/%s.html' % (PORT, name), timeout=60000,
                wait_until='domcontentloaded')
        t0 = time.time()
        while time.time() - t0 < hold_s:
            time.sleep(0.5)
        ok = pg.evaluate('window.__GATE.pass')
        b.close()
    stop[0] = True
    time.sleep(0.4)
    httpd.shutdown(); httpd.server_close()
    peak = max(samples) if samples else 0
    print('%s: renderer RSS peak %.1f MB (gate %s)' % (name, peak, ok), flush=True)
    return {'rss_renderer_peak_mb': round(peak, 1), 'pass': bool(ok)}

out = json.load(open(OUT)) if os.path.exists(OUT) else {}
out['floors'] = {
    'empty_three': measure('empty', EMPTY),
    'gl_textures_only_170x512sq_rgba': measure('glonly', GLONLY),
}
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
