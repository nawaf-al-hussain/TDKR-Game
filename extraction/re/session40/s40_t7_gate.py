#!/usr/bin/env python3
"""S40 T7: gate for the user-zip slice (branch s40-user-zip-slice).
Loads playable/index.html#freeze0.5 from the branch worktree, feeds the REAL
release zip, waits for the in-memory GLB, and quantitatively checks:
- skinned mesh present (verts/idx from the log)
- 3 clips + STATE_TABLE
- frozen pose works (mixer time set)
- console/page errors 0
- screenshot saved
"""
import threading, http.server, functools, logging, json
logging.getLogger("http.server").disabled = True
from playwright.sync_api import sync_playwright

ROOT = '/tmp/my-project/work/ghpages_site_wt'
PORT = 8129
OUT = '/home/z/my-project/scripts/s40_t7_gate.json'
SHOT = '/home/z/my-project/scripts/s40_t7_slice.png'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width': 1100, 'height': 800})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)
    pg.goto(f'http://127.0.0.1:{PORT}/playable/index.html#freeze0.5')
    pg.set_input_files('#zf', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    pg.wait_for_function('window.__zipReady === true', timeout=240000)
    pg.wait_for_timeout(2500)
    info = pg.evaluate("""() => ({
        stateTable: !!window.__STATE_TABLE,
        frozen: !!(window.__frozen && window.__frozen.mixer),
        glbKB: window.__glb ? Math.round(window.__glb.length / 1024) : 0,
        clipNames: window.__frozen ? Object.keys(window.__frozen.actions) : [],
        hasSkinned: (() => { let s = false;
            window.__frozen.batman.traverse(o => { if (o.isSkinnedMesh) s = true; }); return s; })(),
        posHud: document.getElementById('pos').textContent,
    })""")
    pg.screenshot(path=SHOT)
    b.close()

info['page_errors'] = errs
info['pass'] = (info['stateTable'] and info['frozen'] and info['hasSkinned']
                and len(info['clipNames']) >= 3 and not errs)
json.dump(info, open(OUT, 'w'), indent=1)
print(json.dumps(info, indent=1))
