#!/usr/bin/env python3
"""s60 T5 patch: ?s5reanchor=1 - ResolveAirCollision analogue in the exact-blend path.
A virtual wall at ?s5wall=<u> (default 40) along the glide heading: crossing it clamps
the horizontal step (collision response) and RESETS the takeoff anchor to the resolved
position (engine: ResolveAirCollision 0x398570 stores into [comp+0x1a4] @0x3987a4/74).
Default behaviour unchanged (flag off)."""
P = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(P, encoding='utf-8').read()

def rep(old, new, tag):
    global src
    assert src.count(old) == 1, 'PATCH %s: %d matches' % (tag, src.count(old))
    src = src.replace(old, new, 1)
    print('patched', tag)

rep("const S5BLEND = QS2.get('s5blend') === '1';    // s58 T1: exact engine blend (takeoff-anchor distance)",
    "const S5BLEND = QS2.get('s5blend') === '1';    // s58 T1: exact engine blend (takeoff-anchor distance)\n"
    "const S5REAN = QS2.get('s5reanchor') === '1';  // s60 T5: ResolveAirCollision re-anchor case (virtual wall)\n"
    "const S5WALL = parseFloat(QS2.get('s5wall') || '40');", 'FLAGS')

rep("""      if (S5P.mode === 'acc') S5.anchor = [P.x, P.y, P.z];   // s58 T1: engine blend anchor = takeoff pos""",
    """      if (S5P.mode === 'acc') S5.anchor = [P.x, P.y, P.z];   // s58 T1: engine blend anchor = takeoff pos
      if (S5REAN) { S5.reanchors = []; S5.wallHit = null; }  // s60 T5: collision-case receipt""", 'INIT')

# wall clamp + re-anchor right after the horizontal step is computed
rep("""    let gx = P.x + sdx / dl * S5.fwd * dt2, gy = P.y + sdy / dl * S5.fwd * dt2;
    if (nm_ground(gx, gy, P.z + 2.6) <= -1e8) { gx = P.x; gy = P.y; }""",
    """    let gx = P.x + sdx / dl * S5.fwd * dt2, gy = P.y + sdy / dl * S5.fwd * dt2;
    if (nm_ground(gx, gy, P.z + 2.6) <= -1e8) { gx = P.x; gy = P.y; }
    if (S5REAN && S5.anchor && S5.wallHit === null) {
      // s60 T5: virtual wall at S5WALL u from the TAKEOFF anchor along the heading
      const ax = P.x - S5.anchor[0], ay = P.y - S5.anchor[1];
      const dBefore = Math.hypot(ax, ay);
      const nx = gx - S5.anchor[0], ny = gy - S5.anchor[1];
      const dAfter = Math.hypot(nx, ny);
      if (dAfter >= S5WALL && dBefore < S5WALL) {
        // ResolveAirCollision analogue: clamp the horizontal step at the wall plane,
        // then store the RESOLVED position into the cache (0x398570 -> 0x3987a4/74)
        const f = (S5WALL - dBefore) / Math.max(1e-9, dAfter - dBefore);
        gx = P.x + (gx - P.x) * f; gy = P.y + (gy - P.y) * f;
        S5.anchor = [gx, gy, P.z];            // RE-ANCHOR at the resolved position
        S5.wallHit = { tMs: Math.round(now - S5.tGlide), pos: [+gx.toFixed(3), +gy.toFixed(3)] };
        if (!S5.reanchors) S5.reanchors = [];
        S5.reanchors.push(S5.wallHit);
        log('s5 re-anchor: wall at ' + S5WALL + ' u, anchor reset @' + S5.wallHit.tMs + ' ms');
      }
    }""", 'WALL')

# receipt: include reanchors in the landing gate
rep("""        g.s5 = { enabled: true, model: S5P.mode, ctl: !!S5CTL, targetReached: S5.reached, reachDist: S5.reachDist === null ? null : Math.round(S5.reachDist * 100) / 100,
                 glideClipActive: S5.clipActive, landed: true, landMs: S5.landMs, traj: S5.traj };""",
    """        g.s5 = { enabled: true, model: S5P.mode, ctl: !!S5CTL, targetReached: S5.reached, reachDist: S5.reachDist === null ? null : Math.round(S5.reachDist * 100) / 100,
                 glideClipActive: S5.clipActive, landed: true, landMs: S5.landMs, traj: S5.traj,
                 reanchors: S5.reanchors || [], wallHit: S5.wallHit };""", 'RECEIPT')

open(P, 'w', encoding='utf-8').write(src)
print('done, len', len(src))
