import threading, http.server, functools, time, socket
PORT = 8118
WT = '/tmp/my-project/work/city_slice_wt'
def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
print('server:', wait_port(PORT), flush=True)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    page = browser.new_page()
    msgs = []
    page.on('console', lambda m: msgs.append(m.type + ': ' + m.text[:200]))
    page.on('pageerror', lambda e: msgs.append('PAGEERROR: ' + str(e)[:300]))
    page.on('requestfailed', lambda r: msgs.append('REQFAIL: ' + r.url[:120] + ' ' + str(r.failure)[:80]))
    page.goto('http://127.0.0.1:%d/playable/city_slice9.html' % PORT)
    page.wait_for_timeout(3000)
    page.goto('http://127.0.0.1:%d/playable/city_slice9.html' % PORT)
    page.wait_for_timeout(2000)
    page.set_input_files('#f', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    for _ in range(90):
        page.wait_for_timeout(1000)
        g = page.evaluate('window.__GATE || {}')
        if g.get('done'):
            break
    for _ in range(120):
        page.wait_for_timeout(1000)
        g = page.evaluate('window.__GATE || {}')
        if g.get('done'):
            break
    print('blocks:', page.evaluate('(window.__GATE.blocks||[]).map(b=>({t:b.tag,c:(+b.corr).toFixed?(+b.corr).toFixed(4):b.corr,j:(+b.js_mean).toFixed?(+b.js_mean).toFixed(1):b.js_mean}))'), flush=True)
    print('error:', g.get('error'), flush=True)
    import base64
    pngs = page.evaluate('window.__PNGS || {}')
    for k, v in pngs.items():
        open('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_js_%s.png' % k, 'wb') \
            .write(base64.b64decode(v.split(',')[1]))
        print('saved s49_js_%s.png' % k, flush=True)
    print('UVBOX:', page.evaluate('window.__UVBOX || {}'), flush=True)
    for mode in ('real', 'solid'):
        print('ST2', mode, page.evaluate('window.__SELFTEST2(%r)' % mode), flush=True)
    print('TEXTEST:', page.evaluate('''(() => {
      const C = window.__CTX;
      const d = C.getTex('gothamcity_roads_details.tga');
      let s = 0, mx = 0;
      for (let i = 0; i < d.data.length; i += 4) { const v = (d.data[i]+d.data[i+1]+d.data[i+2])/3; s += v; if (v > mx) mx = v; }
      return { w: d.w, h: d.h, mean: (s/(d.data.length/4)).toFixed(1), max: mx,
               ctor: d.data.constructor.name, len: d.data.length };
    })()'''), flush=True)
    print('ST3:', page.evaluate('window.__ST3 ? window.__ST3() : null'), flush=True)
    print('PAGELOG:', page.evaluate("document.querySelector('#log').textContent.slice(-800)"), flush=True)
    print('V0:', page.evaluate("JSON.stringify([...window.__CTX ? [] : []])"), flush=True)
    print('VERT3:', page.evaluate('''(() => {
      const C = window.__CTX; const g = C.blockGeom(C.pairs, C.ldd, C.decls, 695, 73);
      return { nv: g.nv, idxlen: g.idx.length, v0: [...g.pos.slice(0, 8)],
               v1: [...g.pos.slice(28, 36)], stride: g.stride,
               idx0: [...g.idx.slice(0, 6)] };
    })()'''), flush=True)
    raise SystemExit(0)
    page.set_input_files('#f', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    for _ in range(90):
        page.wait_for_timeout(1000)
        g = page.evaluate('window.__GATE || {}')
        if g.get('done'):
            break
    print('GATE done:', g.get('done'), 'error:', g.get('error'), flush=True)
    print('DIAG:', page.evaluate('window.__DIAG || null'), flush=True)
    print('blocks:', page.evaluate('(window.__GATE.blocks||[]).map(b=>({t:b.tag,c:b.corr&&b.corr.toFixed?b.corr.toFixed(4):b.corr, j:b.js_mean&&b.js_mean.toFixed?b.js_mean.toFixed(1):b.js_mean}))'), flush=True)
    print('PAGELOG:', page.evaluate("document.querySelector('#log').textContent.slice(0, 900)"), flush=True)
    for m in msgs[:15]:
        print(m, flush=True)
    browser.close()
