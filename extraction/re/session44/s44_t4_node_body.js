// parity test body (appended after engine + routes + runner in the combined file)
const fs = require('fs');
const soupBuf = fs.readFileSync('/tmp/my-project/work/ghpages_staged_wt/playable/gc_collision.bin');
const ab = soupBuf.buffer.slice(soupBuf.byteOffset, soupBuf.byteOffset + soupBuf.byteLength);
const s = loadSoup(ab);
console.log('soup tris:', s.nTri, 'grid cells:', cmap.size);
const nmBytes = new Uint8Array(fs.readFileSync('/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'));
const chk = loadNavmesh(nmBytes);
console.log('nm vcount:', chk.vcount, 'ccount:', chk.ccount, 'self-check:', chk.ok);
(async () => {
  const routes = WALKTEST_ROUTES.filter(r => [3, 6, 10, 7].includes(r.route));
  for (const r of routes) {
    const p = astar(r.cells[0], r.cells[1]);
    if (p === null) { console.log('route', r.route, 'no_path'); continue; }
    const pts = p.map(c => [nmCent[c * 3], nmCent[c * 3 + 1], nmCent[c * 3 + 2]]);
    const out = follow_nm(pts);
    console.log('route', r.route, '->', out.verdict, 'dist', out.dist.toFixed(1), '| expected', r.expected, r.expected_dist, '| slides', out.slides);
  }
})();
