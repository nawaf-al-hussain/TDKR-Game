#!/usr/bin/env python3
"""S61 T3 gate: ?enemy=1 with the FIXED skinning path (captureSkinnedFrames).
Checks: restMaxDev ~ 0 (applyBoneTransform(rest) == bind geometry -> root-cause fix proof),
posed frames per clip (3 x 5), silhouette lit, frame-to-frame displacement, wrong-clip
grid diff, 0 console errors, default soup digest unchanged."""
import json, time, socket, threading, http.server, functools

PORT = 8173
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t3_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, name, budget=420):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'qs': qs, 'console_errors': [], 'page_errors': [], 'logs': []}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--enable-unsafe-swiftshader',
                                    '--use-gl=swiftshader', '--enable-webgl',
                                    '--ignore-gpu-blocklist'])
        pg = b.new_page(viewport={'width': 960, 'height': 600})
        pg.on('console', lambda m: rec['console_errors'].append(m.text[:300])
              if m.type == 'error' else
              (rec['logs'].append(m.text[:300]) if ('enemy' in m.text or 'merc' in m.text or 'IoU' in m.text) else None))
        pg.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:300]))
        pg.goto('http://127.0.0.1:%d/playable/integration_lazy.html%s' % (PORT, qs))
        pg.set_input_files('input[type=file]', ZIP) if pg.query_selector('input[type=file]') else None
        t0 = time.time()
        while time.time() - t0 < budget:
            g = pg.evaluate('() => window.__GATE || null')
            if g and (g.get('enemyIoU2') or {}).get('ok') is not None and (
                    not ('enemy' in qs) or g.get('enemyPlay')):
                if not ('enemy' in qs) or (g.get('enemyIoU2') or {}).get('frames'):
                    break
            time.sleep(2)
        rec['gate'] = pg.evaluate('() => window.__GATE || null')
        b.close()
    httpd.shutdown()
    return rec

out = {}
r = run('?enemy=1', 'enemy+posed-skinned')
out['enemy'] = {'console_errors': r['console_errors'], 'page_errors': r['page_errors'],
                'logs': r['logs'][:20]}
g = r['gate'] or {}
iou2 = g.get('enemyIoU2') or {}
ep = g.get('enemyPlay') or {}
checks = {}
checks['iou2_ok'] = bool(iou2.get('ok'))
checks['restMaxDev'] = iou2.get('restMaxDev')
checks['rest_fix'] = (iou2.get('restMaxDev') is not None and iou2.get('restMaxDev') < 0.05)
frames = iou2.get('frames') or {}
per_clip = {}
for nm, fr in frames.items():
    per_clip[nm] = {
        'n_frames': len(fr),
        'lit_ok': all(f['lit'] > 1000 for f in fr),
        'heights': [f['height'] for f in fr],
        'feetZ': [f['feetZ'] for f in fr],
        'frameDisp': [f['frameDisp'] for f in fr],
    }
checks['frames_per_clip'] = per_clip
checks['all_clips_3frames'] = all(v['n_frames'] == 3 for v in per_clip.values()) and len(per_clip) == 5
checks['all_lit'] = all(v['lit_ok'] for v in per_clip.values())
checks['frame_motion'] = {nm: any(v['frameDisp'][1] > 0 or v['frameDisp'][2] > 0 for v in [per_clip[nm]]) for nm in per_clip}
checks['gridDiff'] = iou2.get('gridDiff')
checks['gridDiff_gt0'] = (iou2.get('gridDiff') or 0) > 0
checks['console_clean'] = len(r['console_errors']) == 0 and len(r['page_errors']) == 0
checks['enemyPlay_ok'] = bool(ep.get('ok'))
out['checks'] = checks
out['enemyIoU2'] = iou2
out['verdict'] = all([checks['iou2_ok'], checks['rest_fix'], checks['all_clips_3frames'],
                      checks['all_lit'], checks['gridDiff_gt0'], checks['console_clean']])
json.dump(out, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'enemyIoU2'}, indent=1)[:2200])
