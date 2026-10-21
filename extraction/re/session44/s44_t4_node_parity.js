// s44 T4 node parity check: run 2 harness routes through the ported walker
// (same code the browser page runs) and compare with the Python harness rows.
'use strict';
const fs = require('fs');
const TDKR = require('/tmp/my-project/work/ghpages_staged_wt/playable/tdkr_pipeline.js');

// engine + runner (they attach functions to this scope via eval in module scope)
const engineSrc = fs.readFileSync('/tmp/my-project/work/ghpages_staged_wt/playable/walktest.js', 'utf8');
const runSrc = fs.readFileSync('/tmp/my-project/work/ghpages_staged_wt/playable/walktest_run.js', 'utf8');
const routesSrc = fs.readFileSync('/tmp/my-project/work/ghpages_staged_wt/playable/walktest_routes.js', 'utf8');
// execute in this module's scope: wrap in a function with eval
(function () {
  eval(engineSrc);
  eval(routesSrc);
  // stub browser bits the runner expects
  const stubWindow = { __consoleErrors: [], addEventListener: () => {} };
  const stubDoc = { getElementById: () => ({ addEventListener: () => {}, textContent: '' }), createElement: () => ({ getContext: () => null, style: {}, width: 0, height: 0 }) };
  const runBody = runSrc
    .replace(/window\.__consoleErrors/g, 'stubWindow.__consoleErrors')
    .replace(/window\.addEventListener/g, 'stubWindow.addEventListener')
    .replace(/window\.__walkResults/g, 'stubWindow.__walkResults')
    .replace(/const _origErr[\s\S]*?return _origErr\.apply\(console, arguments\);\n\};/, '/* console hook stripped in node */')
    .replace(/function renderRouteMap[\s\S]*?\n\}\n\nasync function runWalktest/, 'function renderRouteMapStub() { return {}; }\n\nasync function runWalktest')
    .replace(/if \(typeof window !== 'undefined'\)[\s\S]*$/, '/* browser bootstrap stripped in node */')
    .replace(/if \(typeof module !== 'undefined'[\s\S]*$/, '/* module export stripped in node */');
  eval(runBody);

  // data
  const soupBuf = fs.readFileSync('/tmp/my-project/work/ghpages_staged_wt/playable/gc_collision.bin');
  const ab = soupBuf.buffer.slice(soupBuf.byteOffset, soupBuf.byteOffset + soupBuf.byteLength);
  const s = loadSoup(ab);
  console.log('soup tris:', s.nTri, 'grid cells:', cmap.size);
  const nmBytes = new Uint8Array(fs.readFileSync('/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'));
  const chk = loadNavmesh(nmBytes);
  console.log('nm vcount:', chk.vcount, 'ccount:', chk.ccount, 'self-check:', chk.ok);

  const routes = WALKTEST_ROUTES.filter(r => [3, 6, 10, 7].includes(r.route));
  for (const r of routes) {
    const p = astar(r.cells[0], r.cells[1]);
    if (p === null) { console.log('route', r.route, 'no_path'); continue; }
    const pts = p.map(c => [nmCent[c * 3], nmCent[c * 3 + 1], nmCent[c * 3 + 2]]);
    const out = follow_nm(pts);
    console.log('route', r.route, '->', out.verdict, 'dist', out.dist.toFixed(1), '| expected', r.expected, r.expected_dist, '| slides', out.slides);
  }
})();
