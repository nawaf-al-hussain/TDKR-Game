import json, time, socket, threading, http.server, functools, base64
PORT = 8141
WT = '/tmp/my-project/work/city_slice_wt'
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
socket.create_connection(('127.0.0.1', PORT), timeout=5)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    pg = b.new_page()
    pg.goto('http://127.0.0.1:%d/playable/city_zone2.html' % PORT)
    pg.wait_for_timeout(2000)
    pg.set_input_files('#f', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    for _ in range(200):
        time.sleep(1)
        if pg.evaluate('(window.__GATE||{}).done'):
            break
    # dump the GL canvas
    data = pg.evaluate('''() => {
      const c = document.createElement('canvas');
      return null; }''')
    png = pg.evaluate('''() => {
      const src = document.querySelector('#c');   // zone page canvas? check id
      return null; }''')
    # the zone page renders offscreen (glz) — expose via toDataURL hook
    png = pg.evaluate("window.__GLDUMP ? window.__GLDUMP() : 'nohook'")
    if png and png.startswith('data'):
        open('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_js_zone.png', 'wb') \
            .write(base64.b64decode(png.split(',')[1]))
        print('saved s49_js_zone.png')
    print(pg.evaluate("document.querySelector('#log').textContent").split('\n')[-4:])
    b.close()
