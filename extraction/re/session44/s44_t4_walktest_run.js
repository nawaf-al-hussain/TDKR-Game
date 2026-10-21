/* s44 T4 walker runner: snap_spawn_nm + follow_nm (1:1 port of s42) + the
 * 24-route in-browser run + gate (console capture, map render, pixel stats). */
'use strict';

/* np.linalg.norm equivalent (sequential sqrt-sum, matches BLAS ddot order for 3-vec) */
function norm3(ax, ay, az, bx, by, bz) {
  const dx = ax - bx, dy = ay - by, dz = az - bz;
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

function snap_spawn_nm(pos) {
  const z = nm_ground(pos[0], pos[1], pos[2] + 2.6);
  if (z === -1e9) return [null, 'no_navmesh'];
  const trial = [pos[0], pos[1], z];
  if (!blocked(trial)) return [trial, 'ok'];
  for (let ri = 0; ri < 8; ri++) {
    const r = 0.25 + ri * 0.25;
    const cnt = Math.max(Math.floor(2 * Math.PI * r / 0.25), 8);
    for (let ai = 0; ai < cnt; ai++) {
      const a = ai * (2 * Math.PI / cnt);
      const x = pos[0] + r * Math.cos(a), y = pos[1] + r * Math.sin(a);
      const zz = nm_ground(x, y, pos[2] + 2.6);
      if (zz === -1e9) continue;
      const t2 = [x, y, zz];
      if (!blocked(t2) && Math.abs(zz - pos[2]) < 1.5) return [t2, 'snapped'];
    }
  }
  return [null, 'all_blocked'];
}

function follow_nm(pts) {
  const fails = [];
  const [sp0, why] = snap_spawn_nm(pts[0]);
  if (sp0 === null) return { verdict: why, dist: 0.0, slides: 0, end: null, fails };
  let pos = sp0;
  let astar_len = 0.0;
  for (let i = 0; i < pts.length - 1; i++) {
    astar_len += norm3(pts[i + 1][0], pts[i + 1][1], pts[i + 1][2], pts[i][0], pts[i][1], pts[i][2]);
  }
  let s = 0.0, stuck = 0, stall = 0, slides = 0, iters = 0;
  const SUB = 0.2;
  const fail = (w, px, py, pz, extra) => fails.push(Object.assign({ why: w, x: px, y: py, z: pz }, extra || {}));
  for (let wi = 1; wi < pts.length; wi++) {
    const tgt = pts[wi];
    let d = norm3(tgt[0], tgt[1], tgt[2], pos[0], pos[1], pos[2]);
    const n = Math.max(Math.floor(d / 0.5), 1);
    for (let k = 0; k < n; k++) {
      const dl = Math.max(norm3(tgt[0], tgt[1], tgt[2], pos[0], pos[1], pos[2]), 1e-9);
      const dirx = (tgt[0] - pos[0]) / dl, diry = (tgt[1] - pos[1]) / dl, dirz = (tgt[2] - pos[2]) / dl;
      let remaining = Math.min(0.5, d);
      let guard = 0;
      while (remaining > 1e-6 && guard < 6) {
        iters++;
        if (iters > 40000) { fail('stuck_wall_timeout', pos[0], pos[1], pos[2]); return { verdict: 'stuck_wall', dist: s, slides, end: pos.slice(), fails }; }
        guard++;
        const mvlen = Math.min(SUB, remaining);
        const sp = [pos[0] + dirx * mvlen, pos[1] + diry * mvlen, pos[2] + dirz * mvlen];
        const g = nm_ground(sp[0], sp[1], pos[2] + 2.6);
        if (g === -1e9) { fail('fell', sp[0], sp[1], pos[2]); return { verdict: 'fell', dist: s, slides, end: pos.slice(), fails }; }
        const climb = g - pos[2];
        if (climb > 0.9) {
          const sl = try_slide(pos, dirx * mvlen, diry * mvlen, mvlen);
          if (sl !== null) { pos = sl[0]; s += sl[1]; remaining -= sl[1]; slides++; continue; }
          fail('step_too_high', sp[0], sp[1], pos[2], { climb });
          return { verdict: 'step_too_high', dist: s, slides, end: pos.slice(), fails };
        }
        const trial = [sp[0], sp[1], g];
        if (blocked(trial)) {
          const sl = try_slide(pos, dirx * mvlen, diry * mvlen, mvlen);
          if (sl !== null) {
            pos = sl[0]; s += sl[1];
            if (sl[1] < 0.02) stall++; else stall = 0;
            if (stall >= 3) { fail('stuck_wall_stall', pos[0], pos[1], pos[2]); return { verdict: 'stuck_wall', dist: s, slides, end: pos.slice(), fails }; }
            remaining -= Math.max(sl[1], 0.02);
            slides++; stuck = 0;
            continue;
          }
          stuck++;
          if (stuck > 6) { fail('stuck_wall', pos[0], pos[1], pos[2]); return { verdict: 'stuck_wall', dist: s, slides, end: pos.slice(), fails }; }
          remaining = 0;
          break;
        }
        pos = trial;
        s += mvlen;
        remaining -= mvlen;
      }
    }
  }
  return { verdict: 'ok', dist: s, slides, end: pos.slice(), fails };
}

/* ---------------- gate: console capture + map render + pixel stats ---------------- */
window.__consoleErrors = [];
window.addEventListener('error', e => window.__consoleErrors.push('window.onerror: ' + e.message));
const _origErr = console.error;
console.error = function () {
  try { window.__consoleErrors.push(Array.from(arguments).map(String).join(' ').slice(0, 300)); } catch (_) {}
  return _origErr.apply(console, arguments);
};

function renderRouteMap(results) {
  // top-down (x,y) map: soup walkable grey, route paths colored by verdict
  const SZ = 1024;
  const cv = document.createElement('canvas');
  cv.width = SZ; cv.height = SZ;
  cv.id = 'routemap';
  const ctx2 = cv.getContext('2d', { willReadFrequently: true });
  ctx2.fillStyle = '#0c0e12';
  ctx2.fillRect(0, 0, SZ, SZ);
  // bounds from the navmesh vertices
  let mnx = 1e9, mxx = -1e9, mny = 1e9, mxy = -1e9;
  for (let i = 0; i < nmV.length; i += 3) {
    if (nmV[i] < mnx) mnx = nmV[i];
    if (nmV[i] > mxx) mxx = nmV[i];
    if (nmV[i + 1] < mny) mny = nmV[i + 1];
    if (nmV[i + 1] > mxy) mxy = nmV[i + 1];
  }
  const SC = (SZ - 20) / Math.max(mxx - mnx, mxy - mny);
  const PX = (x, y) => [10 + (x - mnx) * SC, 10 + (y - mny) * SC];
  // navmesh cells (walkable surface)
  ctx2.strokeStyle = 'rgba(90,140,220,0.55)';
  ctx2.lineWidth = 0.7;
  ctx2.beginPath();
  for (let i = 0; i < nmCells.length / 7; i++) {
    const a = nmCells[i * 7] * 3, b = nmCells[i * 7 + 1] * 3, c = nmCells[i * 7 + 2] * 3;
    const p0 = PX(nmV[a], nmV[a + 1]), p1 = PX(nmV[b], nmV[b + 1]), p2 = PX(nmV[c], nmV[c + 1]);
    ctx2.moveTo(p0[0], p0[1]); ctx2.lineTo(p1[0], p1[1]); ctx2.lineTo(p2[0], p2[1]); ctx2.closePath();
  }
  ctx2.stroke();
  // walked routes
  const colors = { ok: '#35d07f', fell: '#e2b93b', step_too_high: '#e2693b', stuck_wall: '#d0483f', no_path: '#888888' };
  for (const r of results) {
    if (!r.path2d || r.path2d.length < 2) continue;
    ctx2.strokeStyle = colors[r.verdict] || '#ffffff';
    ctx2.lineWidth = 1.6;
    ctx2.beginPath();
    const p0 = PX(r.path2d[0][0], r.path2d[0][1]);
    ctx2.moveTo(p0[0], p0[1]);
    for (let i = 1; i < r.path2d.length; i++) {
      const p = PX(r.path2d[i][0], r.path2d[i][1]);
      ctx2.lineTo(p[0], p[1]);
    }
    ctx2.stroke();
  }
  document.body.appendChild(cv);
  const img = ctx2.getImageData(0, 0, SZ, SZ).data;
  let mr = 0, mg = 0, mb = 0;
  const n = img.length / 4;
  for (let i = 0; i < img.length; i += 4) { mr += img[i]; mg += img[i + 1]; mb += img[i + 2]; }
  mr /= n; mg /= n; mb /= n;
  let vr = 0;
  for (let i = 0; i < img.length; i += 4) { const d = img[i] - mr; vr += d * d; }
  vr = Math.sqrt(vr / n);
  return { canvas: SZ + 'x' + SZ, meanRGB: [+mr.toFixed(2), +mg.toFixed(2), +mb.toFixed(2)], stdR: +vr.toFixed(2) };
}

async function runWalktest(file) {
  const t0 = performance.now();
  const log = m => { const el = document.getElementById('log'); el.textContent += m + '\n'; };
  log('reading ' + file.name + ' (' + (file.size / 1e6).toFixed(0) + ' MB)');
  const dir = await TDKR.zipDirLazy(file);
  const names = [...dir.keys()];
  const find = re => names.find(n => re.test(n));
  // navmesh from the USER'S zip: game_config.gla -> GothamCity_502299_navdata.nm
  const gcPath = find(/data\/game_config\.gla$/i);
  if (!gcPath) throw new Error('game_config.gla not found in the zip');
  const gc = await TDKR.zipReadLazy(file, gcPath, dir);
  log('game_config.gla: ' + (gc.length / 1e6).toFixed(1) + ' MB');
  const nmMember = TDKR.glaSlice(gc, new Set(['GothamCity_502299_navdata.nm']));
  const nmBytes = nmMember['GothamCity_502299_navdata.nm'];
  if (!nmBytes) throw new Error('navdata member GothamCity_502299_navdata.nm not found in game_config.gla (members: ' + Object.keys(nmMember).join(',') + ')');
  const chk = loadNavmesh(nmBytes);
  log('.nm parsed from YOUR zip: vcount=' + chk.vcount + ' ccount=' + chk.ccount + ' self-check=' + (chk.ok ? 'PASS' : 'FAIL vs Python reference'));
  // soup (staged derived data; untracked file — the branch ships code only)
  const resp = await fetch('./gc_collision.bin');
  if (!resp.ok) throw new Error('gc_collision.bin not staged next to the page (derived data, untracked; see s44 notes)');
  const soup = loadSoup(await resp.arrayBuffer());
  log('soup: ' + soup.nTri + ' tris, ' + cmap.size + ' grid cells');
  // run the 24 routes
  const results = [];
  for (const r of WALKTEST_ROUTES) {
    const tR = performance.now();
    const p = astar(r.cells[0], r.cells[1]);
    if (p === null) { results.push({ route: r.route, verdict: 'no_path', dist: 0, slides: 0, ms: Math.round(performance.now() - tR) }); continue; }
    const pts = p.map(c => [nmCent[c * 3], nmCent[c * 3 + 1], nmCent[c * 3 + 2]]);
    const out = follow_nm(pts);
    results.push({
      route: r.route,
      verdict: out.verdict,
      dist: +out.dist.toFixed(3),
      slides: out.slides,
      expected: r.expected,
      expected_dist: r.expected_dist,
      agree: out.verdict === r.expected,
      dist_delta: (r.expected_dist != null) ? +(Math.abs(out.dist - r.expected_dist)).toFixed(3) : null,
      fail: out.fails.length ? out.fails[out.fails.length - 1] : null,
      ms: Math.round(performance.now() - tR),
      path2d: pts.map(q => [q[0], q[1]])
    });
    log('route ' + r.route + ': ' + out.verdict + ' d=' + out.dist.toFixed(1) + ' (expected ' + r.expected + ' ' + r.expected_dist + ') ' + Math.round(performance.now() - tR) + ' ms');
  }
  const okN = results.filter(r => r.verdict === 'ok').length;
  const agreeN = results.filter(r => r.agree).length;
  const agreeDist = results.filter(r => r.agree && r.dist_delta != null && r.dist_delta < 0.25).length;
  const pix = renderRouteMap(results);
  window.__walkResults = {
    gate: {
      ready: true,
      consoleErrors: window.__consoleErrors,
      nmSelfCheck: chk.ok,
      nm: { vcount: chk.vcount, ccount: chk.ccount },
      soup: { nTri: soup.nTri, nObj: soup.nObj },
      routes: results.length,
      browser_ok: okN,
      harness_expected_ok: WALKTEST_ROUTES.filter(r => r.expected === 'ok').length,
      verdict_agreement: agreeN + '/' + results.length,
      dist_agreement_lt025m: agreeDist + '/' + results.length,
      pixelStats: pix,
      wall_ms: Math.round(performance.now() - t0)
    },
    results
  };
  log('DONE: browser ok ' + okN + '/' + results.length + ', verdict agreement ' + agreeN + '/' + results.length +
      ', dist agreement(<0.25 m) ' + agreeDist + '/' + results.length + ' — see window.__walkResults');
}

if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('f').addEventListener('change', async ev => {
      try { await runWalktest(ev.target.files[0]); }
      catch (e) {
        document.getElementById('err').textContent = 'ERROR: ' + (e && e.message || e);
        console.error(e);
      }
    });
  });
}
if (typeof module !== 'undefined' && module.exports) module.exports = { loadSoup, loadNavmesh, astar, follow_nm, ground_at, nm_ground, blocked };
