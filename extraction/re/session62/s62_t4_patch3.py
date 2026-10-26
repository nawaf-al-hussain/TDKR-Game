#!/usr/bin/env python3
"""S62 T4 staging v2 (fixes two s62_t4_patch.py defects, found by the first gate run):
1. v1 probed facades at ft0 - 3.0 = 3 u BELOW the ground plane -> blocked() found no
   triangles there (they live at/above the surface), staging never fired (staged=null
   while the glide still hit a real facade at ledge altitude). v2 probes GLIDE altitudes:
   ledge feet - 0.5, ledge feet - 15, ground + 0.5 (the glide descends ~2.86 u per u fwd).
2. v1 retargeted with the RAW rotated dir (length = the original edge distance, not the
   facade distance). v2 retargets along the UNIT direction, stopping short of the facade
   (max(6, first - 8) u) so the hit happens mid-glide when reach allows; skipped when the
   facade is too close to stop short (startShort: null, natural edge kept).
No change to the re-anchor block itself; flags unchanged (?s5real=1)."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, encoding='utf-8').read()
n0 = len(src)

A1 = """  if (S5REAL) {
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
  }"""
assert src.count(A1) == 1, 'v1 staging block not found verbatim'

N1 = """  if (S5REAL) {
    // s62 T4 staging v2 (s62_t4_patch3.py): find a facade the glide will cross. Probes at
    // GLIDE altitudes (v1 probed 3 u BELOW the ground plane where no triangles live ->
    // never fired): ledge feet - 0.5, ledge feet - 15, ground + 0.5 (sink ~2.86 u per u
    // fwd). Rotate the target in 22.5-deg steps until one direction crosses a facade
    // within 12..160 u; retarget along the UNIT direction stopping SHORT of the facade
    // (max(6, first-8) u) so the re-anchor happens mid-glide when reach allows.
    const ft0 = P.z - 0.9;
    const ledgeFt = tgt[2] - 0.9;
    const alts = [ledgeFt - 0.5, ledgeFt - 15.0, ft0 + 0.5];
    const dir = [tgt[0] - P.x, tgt[1] - P.y];
    let found = null;
    for (let a = 0; a < 16 && !found; a++) {
      const ang = a * Math.PI / 8;
      const ca = Math.cos(ang), sa = Math.sin(ang);
      const d2 = [dir[0] * ca - dir[1] * sa, dir[0] * sa + dir[1] * ca];
      const dn = Math.hypot(d2[0], d2[1]) || 1;
      let first = null;
      for (let dd = 12; dd <= 160 && first === null; dd += 2) {
        const qx = P.x + d2[0] / dn * dd, qy = P.y + d2[1] / dn * dd;
        for (let zi = 0; zi < alts.length; zi++) {
          if (blocked([qx, qy, alts[zi]], 0.45)) { first = dd; break; }
        }
      }
      if (first !== null) found = { ux: d2[0] / dn, uy: d2[1] / dn, first: first };
    }
    if (found) {
      const start = Math.max(6, found.first - 8);
      if (start < found.first - 1) {
        tgt = [P.x + found.ux * start, P.y + found.uy * start, tgt[2]];
        S5.realStaged = { first: found.first, startShort: start,
                          angDeg: Math.round(Math.atan2(found.uy, found.ux) * 180 / Math.PI) };
        log('s5 REAL staging: facade at ' + found.first + ' u along ' +
            S5.realStaged.angDeg + ' deg, glide start ' + start + ' u');
      } else {
        S5.realStaged = { first: found.first, startShort: null,
                          angDeg: Math.round(Math.atan2(found.uy, found.ux) * 180 / Math.PI) };
        log('s5 REAL staging: facade at ' + found.first + ' u too close to stop short');
      }
    }
  }"""
src = src.replace(A1, N1, 1)
assert src.count('S5REAL') == 4 and src.count('s5real') == 1 and len(src) != n0
open(PAGE, 'w', encoding='utf-8').write(src)
print('staging v2 applied, delta', len(src) - n0)
