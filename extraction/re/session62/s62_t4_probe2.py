#!/usr/bin/env python3
"""S62 T4 diagnostic: WHY did the v2 gate glide fall straight down over void while the
v1 gate glide hit a facade and landed? Probes, in-page, after the run:
- S5.from / S5.tgt (the actual pick), __S5WPS presence + length (waypoint path vs BFS
  fallback), nm_ground at the tgt, s5PickEdge() re-evaluated now,
- the staging probe loop re-run from S5.from (blocked() along 16 rays x 3 altitudes),
- whether repeated gate runs pick the same edge (nondeterminism check across 3 loads)."""
import json, time, socket, threading, http.server, functools

PORT = 8179
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)

JS = """(() => {
  const D = window.__S5DBG || {};
  const F = D.from, T = D.tgt || null;
  const out = { from: F, tgt: T, wps: (window.__S5WPS || []).length,
                realStaged: (window.__GATE && window.__GATE.s5 && window.__GATE.s5.realStaged) || null };
  if (T) {
    const ft0 = F[2] - 0.9, ledgeFt = T[2] - 0.9;
    out.ft0 = +ft0.toFixed(2); out.ledgeFt = +ledgeFt.toFixed(2);
    out.nm_tgt = nm_ground(T[0], T[1], T[2] + 2.6);
    out.nm_from = nm_ground(F[0], F[1], F[2] + 2.6);
    out.blocked_at_tgt = blocked([T[0], T[1], T[2] - 0.9], 0.45);
    const dir = [T[0] - F[0], T[1] - F[1]];
    const rays = [];
    for (let a = 0; a < 16; a++) {
      const ang = a * Math.PI / 8, ca = Math.cos(ang), sa = Math.sin(ang);
      const d2 = [dir[0] * ca - dir[1] * sa, dir[0] * sa + dir[1] * ca];
      const dn = Math.hypot(d2[0], d2[1]) || 1;
      let first = null;
      const alts = [ledgeFt - 0.5, ledgeFt - 15.0, ft0 + 0.5];
      for (let dd = 12; dd <= 160 && first === null; dd += 2) {
        const qx = F[0] + d2[0] / dn * dd, qy = F[1] + d2[1] / dn * dd;
        for (let zi = 0; zi < alts.length; zi++) {
          if (blocked([qx, qy, alts[zi]], 0.45)) { first = dd; break; }
        }
      }
      if (first !== null) rays.push({ angDeg: Math.round(a * 22.5), first: first });
    }
    out.rays = rays;
  }
  return out;
})()"""

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
wait_port(PORT)
from playwright.sync_api import sync_playwright
out = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    for i in range(3):
        pg = b.new_page(viewport={'width': 960, 'height': 600})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/playable/integration_lazy.html?s5=1&s5blend=1&s5real=1' % PORT)
        pg.set_input_files('#f', ZIP)
        t0 = time.time()
        done = False
        while time.time() - t0 < 240:
            time.sleep(0.5)
            g = pg.evaluate('window.__GATE || {}')
            if g.get('done'):
                done = True
                break
        s5 = (g or {}).get('s5') or {}
        info = pg.evaluate(JS)
        info['run'] = i
        info['done'] = done
        info['landed'] = s5.get('landed')
        info['error'] = s5.get('error')
        info['s5_from'] = s5.get('from')
        info['s5_tgt'] = s5.get('tgt')
        info['s5_wpsN'] = s5.get('wpsN')
        info['n_reanchors'] = len(s5.get('reanchors') or [])
        info['n_traj'] = len(s5.get('traj') or [])
        info['pageerrors'] = errs
        out.append(info)
        pg.close()
    b.close()
httpd.shutdown(); httpd.server_close()
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t4_probe2.json', 'w'), indent=1)
for r in out:
    print('run', r['run'], 'done', r['done'], 'landed', r['landed'], 'err', r['error'],
          'reanchors', r['n_reanchors'], 'traj', r['n_traj'])
    print('  dbg from', r['from'], 'tgt', r['tgt'], 'wps', r['wps'], 'staged', r['realStaged'])
    print('  s5  from', r['s5_from'], 'tgt', r['s5_tgt'], 'wpsN', r['s5_wpsN'])
    if r.get('tgt'):
        print('  nm_tgt', r['nm_tgt'], 'nm_from', r['nm_from'], 'blocked_at_tgt', r['blocked_at_tgt'],
              'rays', r['rays'][:6])
    print('  pageerrors', r['pageerrors'])
