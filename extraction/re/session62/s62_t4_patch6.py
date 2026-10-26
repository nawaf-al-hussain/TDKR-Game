#!/usr/bin/env python3
"""S62 T4 staging v3: DETECT-ONLY (replaces the v2 retarget).
Why: v2 retargeted the glide start 8 u short of the facade, but (a) that point had NO
navmesh under it (nm_ground = -1e9 void) -> the glide fell straight down and timed out
(3 identical probe runs), and (b) with the engine-default glide (pitch0 fixed -45,
sink ~10 u/s) the reach from a ~9 u ledge is only ~3 u - a facade at 12+ u is
geometrically unreachable mid-glide. The engine-true pattern is the NATURAL one: the
picked ledge IS facade-adjacent, so the first glide step crosses real collision ->
slide -> re-anchor -> anchor/blendD reset -> land (v1 gate run: 2 re-anchors @17/300 ms,
dip restart, landed, 0 errors). v3 records the 16-ray facade census as provenance and
leaves the pick untouched. Also adds realStaged to the glide-timeout finalize object
(it was only on the landing path, which made staged look null in timeout runs)."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, encoding='utf-8').read()
n0 = len(src)

# 1) replace the staging v2 block (from the S5REAL gate to the S5.tgt assignment)
i0 = src.index("  if (S5REAL) {")
i1 = src.index("  S5.tgt = tgt; S5.t0 = performance.now();")
assert i0 < i1
v2_block = src[i0:i1]
assert "staging v2" in v2_block and "alts" in v2_block

N = """  if (S5REAL) {
    // s62 T4 staging v3 (s62_t4_patch6.py): DETECT-ONLY. v2's retarget placed the glide
    // start 8 u short of the facade, but that point had NO navmesh under it (nm_ground
    // void) -> the glide fell straight down and timed out; and with the engine-default
    // glide (pitch0 fixed, sink ~10 u/s) the reach from a ~9 u ledge is ~3 u, so a
    // 12+ u facade is unreachable mid-glide. The engine-true pattern is natural: the
    // picked ledge IS facade-adjacent -> first glide step crosses real collision ->
    // slide -> re-anchor -> blendD reset -> land. v3 records the facade census (16 rays
    // at glide altitudes) as provenance and leaves the pick untouched.
    const ft0 = P.z - 0.9;
    const ledgeFt = tgt[2] - 0.9;
    const reach = Math.max(0, (ledgeFt - ft0) / 2.86);   // u of flight until ground contact
    const alts = [ledgeFt - 0.5, ledgeFt - 15.0, ft0 + 0.5];
    const dir = [tgt[0] - P.x, tgt[1] - P.y];
    const rays = [];
    for (let a = 0; a < 16; a++) {
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
      if (first !== null) rays.push({ angDeg: Math.round(a * 22.5), first: first });
    }
    S5.realStaged = { mode: 'detect-only', reach: +reach.toFixed(2),
                      nRays: rays.length, rays: rays.slice(0, 6) };
    log('s5 REAL staging v3: detect-only, reach ' + reach.toFixed(1) +
        ' u, facades ' + rays.length + '/16');
  }
"""
src = src[:i0] + N + src[i1:]

# 2) realStaged on the timeout finalize path too
A3 = "glideClipActive: S5.clipActive, landed: false, error: 'glide timeout', traj: S5.traj,\n               from: S5.from.slice(), tgt: S5.tgt.slice(), wpsN: (window.__S5WPS || []).length };"
assert src.count(A3) == 1
src = src.replace(A3, A3[:-2] + ",\n               realStaged: S5.realStaged || null };", 1)

assert src.count("S5REAL") == 4 and src.count("s5real") == 1 and len(src) != n0
open(PAGE, 'w', encoding='utf-8').write(src)
print('staging v3 applied, delta', len(src) - n0)
