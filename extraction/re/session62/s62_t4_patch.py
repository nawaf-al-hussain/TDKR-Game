#!/usr/bin/env python3
"""S62 T4: REAL collision soup air-collision re-anchor for the glide (?s5reanchor=1&s5real=1).
- blocked() = the walker's capsule-vs-soup query (real lvc soup, grid-accelerated)
- try_slide  = the walker's wall-slide resolver (the ResolveAirCollision analogue:
  the resolved position goes into the glide cache / re-anchors the takeoff anchor)
- edge-triggered: a new re-anchor only on a not-blocked -> blocked transition, so
  sliding along one facade counts ONCE; a second facade entry = a second collision.
- staging: at grapnel time, pick an edge whose glide direction crosses a facade
  (first blocked along the ray at air height within 12..160 u).
Defaults unchanged (everything behind the flags)."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, encoding='utf-8').read()
n0 = len(src)

# 1) flag
A1 = "const S5REAN = QS2.get('s5reanchor') === '1';  // s60 T5: ResolveAirCollision re-anchor case (virtual wall)"
assert src.count(A1) == 1
N1 = A1 + "\nconst S5REAL = QS2.get('s5real') === '1';   // s62 T4: REAL soup air-collision re-anchor"
src = src.replace(A1, N1, 1)

# 2) real-collision check in the glide step (BEFORE the virtual-wall block)
A2 = """    if (S5REAN && S5.anchor && S5.wallHit === null) {"""
assert src.count(A2) == 1
N2 = """    if (S5REAL && S5.anchor) {
      // s62 T4: REAL soup air collision (blocked = the walker's capsule-vs-soup query
      // at the capsule's air altitude). Resolve via the walker's wall-slide, store the
      // RESOLVED position into the glide cache and RE-ANCHOR (ResolveAirCollision
      // analogue, 0x398570). Edge-triggered on a not-blocked -> blocked transition.
      const feet = nz - 0.9;
      const hitNow = blocked([gx, gy, feet], 0.45);
      if (hitNow && !S5.lastBlocked) {
        const mvx = gx - P.x, mvy = gy - P.y;
        const mvl = Math.hypot(mvx, mvy);
        const sl = try_slide([P.x, P.y, feet], mvx, mvy, Math.max(mvl, 0.05));
        if (sl) { gx = sl[0][0]; gy = sl[0][1]; }
        S5.anchor = [gx, gy, P.z];            // RE-ANCHOR at the resolved position
        if (!S5.reanchors) S5.reanchors = [];
        const rec = { tMs: Math.round(now - S5.tGlide), pos: [+gx.toFixed(3), +gy.toFixed(3)],
                      z: +P.z.toFixed(3), kind: 'real' };
        S5.reanchors.push(rec);
        if (!S5.wallHit) S5.wallHit = rec;
        S5.blendD = 0;   // blend distance restarts from the new anchor (dip restart)
        log('s5 REAL re-anchor #' + S5.reanchors.length + ' @' + rec.tMs + ' ms pos ' +
            rec.pos.join(','));
      }
      S5.lastBlocked = hitNow;
    }
    if (S5REAN && S5.anchor && S5.wallHit === null) {"""
src = src.replace(A2, N2, 1)

# 3) staging: at grapnel time with s5real, pick an edge whose direction crosses a facade
A3 = """  S5.from = [P.x, P.y, P.z];
  S5.tgt = tgt; S5.t0 = performance.now();"""
assert src.count(A3) == 1
N3 = """  S5.from = [P.x, P.y, P.z];
  if (S5REAL) {
    // s62 T4 staging: verify the glide direction crosses a facade (real soup) within
    // 12..160 u at air height; if not, rotate the target around the takeoff point in
    // 22.5-deg steps until one does (the glide then flies INTO the facade).
    const ft0 = P.z - 0.9;
    let dir = [tgt[0] - P.x, tgt[1] - P.y];
    let dl0 = Math.hypot(dir[0], dir[1]) || 1;
    let found = null;
    for (let a = 0; a < 16 && !found; a++) {
      const ang = a * Math.PI / 8;
      const ca = Math.cos(ang), sa = Math.sin(ang);
      const d2 = [dir[0] * ca - dir[1] * sa, dir[0] * sa + dir[1] * ca];
      const dn = Math.hypot(d2[0], d2[1]) || 1;
      let first = null;
      for (let dd = 12; dd <= 160; dd += 2) {
        const qx = P.x + d2[0] / dn * dd, qy = P.y + d2[1] / dn * dd;
        if (blocked([qx, qy, ft0 - 3.0], 0.45)) { first = dd; break; }  // facade at glide alt
      }
      if (first !== null && first <= 160) found = { d: d2, dn: dn, first: first };
    }
    if (found) {
      // retarget the grapple edge along the chosen direction (same dist class)
      tgt = [P.x + found.d[0], P.y + found.d[1], tgt[2]];
      S5.realStaged = { first: found.first, angDeg: Math.round(Math.atan2(found.d[1], found.d[0]) * 180 / Math.PI) };
      log('s5 REAL staging: facade at ' + found.first + ' u along ' + S5.realStaged.angDeg + ' deg');
    }
  }
  S5.tgt = tgt; S5.t0 = performance.now();"""
src = src.replace(A3, N3, 1)

# 4) expose realStaged in the gate object
A4 = "                 reanchors: S5.reanchors || [], wallHit: S5.wallHit };"
cnt = src.count(A4)
assert cnt >= 1
src = src.replace(A4, "                 reanchors: S5.reanchors || [], wallHit: S5.wallHit,\n                 realStaged: S5.realStaged || null, real: !!S5REAL };", 1)

assert len(src) != n0
open(PAGE, 'w', encoding='utf-8').write(src)
print('patched integration_lazy.html (T4), delta', len(src) - n0)
