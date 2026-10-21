/* s44 T4: navmesh-surface walker in the browser — 1:1 JS port of the s42/s44
 * Python harness (s41_t4_lib.py ground_at/Ctx.blocked/nearest_walls/try_slide/
 * astar + s42_t4_navmesh.py nm_ground/snap_spawn_nm/follow_nm).
 * Data: navmesh .nm parsed at runtime from the USER'S zip (game_config.gla,
 * member GothamCity_502299_navdata.nm) via TDKR.glaSlice; collision soup from
 * the staged gc_collision.bin (derived data, untracked — the branch ships
 * code only; a user-file soup path is future work). Walls = non-walkable soup
 * tris; stepignore 0.55 (s41 steppable fix); navmesh surface for heights.
 * Byte-order notes verified against the Python reference: .nm is BIG-endian
 * u16 headers + BIG-endian f32 verts; gc_collision.bin is LITTLE-endian. */
'use strict';

/* ---------------- soup (gc_collision.bin) ---------------- */
let nTri = 0, cpos = null, cflag = null, walkable = null, triZmax = null;
const CGRID = 10.0;
const cmap = new Map();          // "dx,dy" -> int[]

function loadSoup(buf) {
  const dv = new DataView(buf);
  nTri = dv.getUint32(4, true);
  const nObj = dv.getUint32(8, true);
  let p = 12;
  const nameLen = dv.getUint32(p, true); p += 4 + nameLen + nObj * 48;
  cpos = new Float64Array(nTri * 9);
  cflag = new Uint8Array(nTri);
  walkable = new Uint8Array(nTri);
  triZmax = new Float64Array(nTri);
  const bytes = new Uint8Array(buf);
  for (let i = 0; i < nTri; i++) {
    const b = p + i * 39;
    for (let k = 0; k < 9; k++) {
      cpos[i * 9 + k] = dv.getFloat32(b + 2 + k * 4, true);
    }
    cflag[i] = bytes[b + 38];
    walkable[i] = (cflag[i] === 0 || cflag[i] === 1 || cflag[i] === 5 || cflag[i] === 6) ? 1 : 0;
    const x0 = cpos[i * 9], x1 = cpos[i * 9 + 3], x2 = cpos[i * 9 + 6];
    const y0 = cpos[i * 9 + 1], y1 = cpos[i * 9 + 4], y2 = cpos[i * 9 + 7];
    const z0 = cpos[i * 9 + 2], z1 = cpos[i * 9 + 5], z2 = cpos[i * 9 + 8];
    triZmax[i] = Math.max(z0, z1, z2);
    const gxa0 = Math.min(x0, x1, x2), gxa1 = Math.max(x0, x1, x2);
    const gya0 = Math.min(y0, y1, y2), gya1 = Math.max(y0, y1, y2);
    if (!isFinite(gxa0) || !isFinite(gxa1) || !isFinite(gya0) || !isFinite(gya1) ||
        (gxa1 - gxa0) >= CGRID * 4096 || (gya1 - gya0) >= CGRID * 4096) continue;  // s45 gate guard
    const gxa = [Math.floor(x0 / CGRID), Math.floor(x1 / CGRID), Math.floor(x2 / CGRID)];
    const gya = [Math.floor(y0 / CGRID), Math.floor(y1 / CGRID), Math.floor(y2 / CGRID)];
    for (let dx = Math.min(gxa[0], gxa[1], gxa[2]); dx <= Math.max(gxa[0], gxa[1], gxa[2]); dx++) {
      for (let dy = Math.min(gya[0], gya[1], gya[2]); dy <= Math.max(gya[0], gya[1], gya[2]); dy++) {
        const key = dx + ',' + dy;
        let a = cmap.get(key);
        if (!a) { a = []; cmap.set(key, a); }
        a.push(i);
      }
    }
  }
  return { nTri, nObj };
}

/* ground height from soup (walkable tris only when walk_only) — port of s41 ground_at */
function ground_at(x, y, zmax, walk_only) {
  const gx = Math.floor(x / CGRID), gy = Math.floor(y / CGRID);
  let best = -1e9;
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const a = cmap.get((gx + dx) + ',' + (gy + dy));
      if (!a) continue;
      for (let ai = 0; ai < a.length; ai++) {
        const i = a[ai];
        if (walk_only && !walkable[i]) continue;
        const t0x = cpos[i * 9], t0y = cpos[i * 9 + 1], t0z = cpos[i * 9 + 2];
        const t1x = cpos[i * 9 + 3], t1y = cpos[i * 9 + 4], t1z = cpos[i * 9 + 5];
        const t2x = cpos[i * 9 + 6], t2y = cpos[i * 9 + 7], t2z = cpos[i * 9 + 8];
        const det = (t1y - t2y) * (t0x - t2x) + (t2x - t1x) * (t0y - t2y);
        if (Math.abs(det) < 1e-9) continue;
        const l1 = ((t1y - t2y) * (x - t2x) + (t2x - t1x) * (y - t2y)) / det;
        const l2 = ((t2y - t0y) * (x - t2x) + (t0x - t2x) * (y - t2y)) / det;
        const l3 = 1 - l1 - l2;
        if (l1 >= -0.02 && l2 >= -0.02 && l3 >= -0.02) {
          const z = l1 * t0z + l2 * t1z + l3 * t2z;
          if (z <= zmax + 0.6 && z > best) best = z;
        }
      }
    }
  }
  return best;
}

/* ---------------- navmesh (.nm from the user's zip) ---------------- */
let nmV = null;            // Float64Array 3*vcount
let nmCells = null;        // Int32Array 7*ccount (v0,v1,v2,n0,n1,n2,reg; 0xffff -> -1)
let nmCent = null;         // Float64Array 3*ccount
let NBS_OFF = null, NBS_ARR = null;
const NMCG = 10.0;
const nmCellgrid = new Map();
const NM_EXPECT = {        // Python-reference constants for the parse self-check
  vcount: 30824, ccount: 31647,
  v0: [-847.0369873046875, -343.71600341796875, 20.605600357055664],
  vlast: [-763.0369262695312, -1269.216064453125, -2.1944000720977783],
  cell0: [0, 1, 2, -1, 3, 13],
  celllast: [30817, 30816, 30823, 31645, -1, 31639]
};

function loadNavmesh(nmBytes) {
  const dv = new DataView(nmBytes.buffer, nmBytes.byteOffset, nmBytes.byteLength);
  const vcount = dv.getUint16(0, false);
  const soupEnd = 2 + vcount * 12;
  const ccount = dv.getUint16(soupEnd + 2, false);
  const cs = soupEnd + 4;
  nmV = new Float64Array(vcount * 3);
  for (let i = 0; i < vcount; i++) {
    nmV[i * 3] = dv.getFloat32(2 + i * 12, false);
    nmV[i * 3 + 1] = dv.getFloat32(2 + i * 12 + 4, false);
    nmV[i * 3 + 2] = dv.getFloat32(2 + i * 12 + 8, false);
  }
  nmCells = new Int32Array(ccount * 7);
  nmCent = new Float64Array(ccount * 3);
  const nbCount = new Int32Array(ccount);
  for (let i = 0; i < ccount; i++) {
    const o = cs + i * 15;
    for (let k = 0; k < 6; k++) {
      const w = dv.getUint16(o + k * 2, false);
      nmCells[i * 7 + k] = (w > 0x7fff) ? w - 0x10000 : w;
    }
    nmCells[i * 7 + 6] = dv.getUint16(o + 12, false);
    const a = nmCells[i * 7] * 3, b = nmCells[i * 7 + 1] * 3, c = nmCells[i * 7 + 2] * 3;
    nmCent[i * 3] = (nmV[a] + nmV[b] + nmV[c]) / 3;
    nmCent[i * 3 + 1] = (nmV[a + 1] + nmV[b + 1] + nmV[c + 1]) / 3;
    nmCent[i * 3 + 2] = (nmV[a + 2] + nmV[b + 2] + nmV[c + 2]) / 3;
    for (let k = 3; k < 6; k++) if (nmCells[i * 7 + k] >= 0) nbCount[i]++;
    const xs0 = nmV[a], xs1 = nmV[b], xs2 = nmV[c];
    const ys0 = nmV[a + 1], ys1 = nmV[b + 1], ys2 = nmV[c + 1];
    // s45 gate: non-finite coordinates (corrupt data) must not hang the grid
    // loop — skip the cell insert; the self-check catches the corruption.
    const gxmin = Math.min(xs0, xs1, xs2), gxmax = Math.max(xs0, xs1, xs2);
    const gymin = Math.min(ys0, ys1, ys2), gymax = Math.max(ys0, ys1, ys2);
    if (isFinite(gxmin) && isFinite(gxmax) && isFinite(gymin) && isFinite(gymax) &&
        (gxmax - gxmin) < NMCG * 4096 && (gymax - gymin) < NMCG * 4096)
    for (let dx = Math.floor(gxmin / NMCG); dx <= Math.floor(gxmax / NMCG); dx++) {
      for (let dy = Math.floor(Math.min(ys0, ys1, ys2) / NMCG); dy <= Math.floor(Math.max(ys0, ys1, ys2) / NMCG); dy++) {
        const key = dx + ',' + dy;
        let arr = nmCellgrid.get(key);
        if (!arr) { arr = []; nmCellgrid.set(key, arr); }
        arr.push(i);
      }
    }
  }
  NBS_OFF = new Int32Array(ccount + 1);
  for (let i = 0; i < ccount; i++) NBS_OFF[i + 1] = NBS_OFF[i] + nbCount[i];
  NBS_ARR = new Int32Array(NBS_OFF[ccount]);
  let w = 0;
  for (let i = 0; i < ccount; i++) {
    for (let k = 3; k < 6; k++) {
      const n = nmCells[i * 7 + k];
      if (n >= 0) NBS_ARR[w++] = n;
    }
  }
  // self-check against the Python reference (two independent signals: JS parse vs Python parse)
  const chk = { vcount, ccount, v0: [nmV[0], nmV[1], nmV[2]],
    vlast: [nmV[(vcount - 1) * 3], nmV[(vcount - 1) * 3 + 1], nmV[(vcount - 1) * 3 + 2]],
    cell0: [nmCells[0], nmCells[1], nmCells[2], nmCells[3], nmCells[4], nmCells[5]],
    celllast: [nmCells[(ccount - 1) * 7], nmCells[(ccount - 1) * 7 + 1], nmCells[(ccount - 1) * 7 + 2],
               nmCells[(ccount - 1) * 7 + 3], nmCells[(ccount - 1) * 7 + 4], nmCells[(ccount - 1) * 7 + 5]] };
  const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  chk.ok = (vcount === NM_EXPECT.vcount && ccount === NM_EXPECT.ccount &&
            eq(chk.v0.map(x => +x.toFixed(6)), NM_EXPECT.v0.map(x => +x.toFixed(6))) &&
            eq(chk.vlast.map(x => +x.toFixed(6)), NM_EXPECT.vlast.map(x => +x.toFixed(6))) &&
            eq(chk.cell0, NM_EXPECT.cell0) && eq(chk.celllast, NM_EXPECT.celllast));
  return chk;
}

/* highest navmesh-surface z at (x,y) with z <= zmax+0.6 — port of nm_ground */
function nm_ground(x, y, zmax) {
  const gx = Math.floor(x / NMCG), gy = Math.floor(y / NMCG);
  let best = -1e9;
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const arr = nmCellgrid.get((gx + dx) + ',' + (gy + dy));
      if (!arr) continue;
      for (let ai = 0; ai < arr.length; ai++) {
        const i = arr[ai];
        const a = nmCells[i * 7] * 3, b = nmCells[i * 7 + 1] * 3, c = nmCells[i * 7 + 2] * 3;
        const t0x = nmV[a], t0y = nmV[a + 1], t0z = nmV[a + 2];
        const t1x = nmV[b], t1y = nmV[b + 1], t1z = nmV[b + 2];
        const t2x = nmV[c], t2y = nmV[c + 1], t2z = nmV[c + 2];
        const det = (t1y - t2y) * (t0x - t2x) + (t2x - t1x) * (t0y - t2y);
        if (Math.abs(det) < 1e-12) continue;
        const l1 = ((t1y - t2y) * (x - t2x) + (t2x - t1x) * (y - t2y)) / det;
        const l2 = ((t2y - t0y) * (x - t2x) + (t0x - t2x) * (y - t2y)) / det;
        const l3 = 1 - l1 - l2;
        if (l1 >= -0.03 && l2 >= -0.03 && l3 >= -0.03) {
          const z = l1 * t0z + l2 * t1z + l3 * t2z;
          if (z <= zmax + 0.6 && z > best) best = z;
        }
      }
    }
  }
  return best;
}

/* ---------------- walker context (navmesh mode, stepignore 0.55) ---------------- */
const STEPIGNORE = 0.55;

function blocked(pos, rad) {
  rad = rad || 0.45;
  const gx = Math.floor(pos[0] / CGRID), gy = Math.floor(pos[1] / CGRID);
  let gref = ground_at(pos[0], pos[1], pos[2] + 2.6, true);
  if (gref === -1e9) gref = pos[2];
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const a = cmap.get((gx + dx) + ',' + (gy + dy));
      if (!a) continue;
      for (let ai = 0; ai < a.length; ai++) {
        const i = a[ai];
        if (walkable[i]) continue;
        const mz = (cpos[i * 9 + 2] + cpos[i * 9 + 5] + cpos[i * 9 + 8]) / 3;
        if (mz < pos[2] - 0.4 || mz > pos[2] + 1.8) continue;
        if (triZmax[i] <= gref + STEPIGNORE) continue;
        for (let e = 0; e < 3; e++) {
          const x1 = cpos[i * 9 + e * 3], y1 = cpos[i * 9 + e * 3 + 1];
          const j = (e + 1) % 3;
          const x2 = cpos[i * 9 + j * 3], y2 = cpos[i * 9 + j * 3 + 1];
          const vx = x2 - x1, vy = y2 - y1;
          const L2 = vx * vx + vy * vy;
          let tt = 0;
          if (L2 >= 1e-9) tt = Math.max(0, Math.min(1, ((pos[0] - x1) * vx + (pos[1] - y1) * vy) / L2));
          const ddx = pos[0] - (x1 + tt * vx), ddy = pos[1] - (y1 + tt * vy);
          if (Math.hypot(ddx, ddy) < rad) return true;
        }
      }
    }
  }
  return false;
}

function nearest_walls(pos, rad, k) {
  rad = rad || 0.45; k = k || 2;
  const gx = Math.floor(pos[0] / CGRID), gy = Math.floor(pos[1] / CGRID);
  const cands = [];
  let gref = null;
  if (STEPIGNORE !== null) {
    gref = ground_at(pos[0], pos[1], pos[2] + 2.6, true);
    if (gref === -1e9) gref = pos[2];
  }
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const a = cmap.get((gx + dx) + ',' + (gy + dy));
      if (!a) continue;
      for (let ai = 0; ai < a.length; ai++) {
        const i = a[ai];
        if (walkable[i]) continue;
        if (STEPIGNORE !== null && triZmax[i] <= gref + STEPIGNORE) continue;
        const mz = (cpos[i * 9 + 2] + cpos[i * 9 + 5] + cpos[i * 9 + 8]) / 3;
        if (mz < pos[2] - 0.4 || mz > pos[2] + 1.8) continue;
        for (let e = 0; e < 3; e++) {
          const x1 = cpos[i * 9 + e * 3], y1 = cpos[i * 9 + e * 3 + 1];
          const j = (e + 1) % 3;
          const x2 = cpos[i * 9 + j * 3], y2 = cpos[i * 9 + j * 3 + 1];
          const vx = x2 - x1, vy = y2 - y1;
          const L2 = vx * vx + vy * vy;
          if (L2 < 1e-9) continue;
          const tt = Math.max(0.0, Math.min(1.0, ((pos[0] - x1) * vx + (pos[1] - y1) * vy) / L2));
          const qx = x1 + tt * vx, qy = y1 + tt * vy;
          const d = Math.hypot(pos[0] - qx, pos[1] - qy);
          if (d < rad) cands.push([d, (pos[0] - qx) / Math.max(d, 1e-9), (pos[1] - qy) / Math.max(d, 1e-9)]);
        }
      }
    }
  }
  cands.sort((p, q) => p[0] - q[0]);
  return cands.slice(0, k);
}

function try_slide(pos, mvx, mvy, mvlen) {
  const probe = [pos[0] + mvx, pos[1] + mvy, pos[2]];
  const walls = nearest_walls(probe, 0.45, 2);
  if (walls.length === 0) return null;
  const cands = [];
  const mvl = Math.sqrt(mvx * mvx + mvy * mvy);   // np.linalg.norm(mv[:2])
  for (let wi = 0; wi < walls.length; wi++) {
    const nx = walls[wi][1], ny = walls[wi][2];
    const dot = mvx * nx + mvy * ny;
    const vx = mvx - dot * nx, vy = mvy - dot * ny;
    if (Math.sqrt(vx * vx + vy * vy) > 1e-4) cands.push([vx, vy]);
    if (wi === 0) {
      const tx = -ny, ty = nx;
      cands.push([tx * mvl, ty * mvl]);
      cands.push([-tx * mvl, -ty * mvl]);
    }
  }
  if (cands.length > 0 && Math.sqrt(cands[0][0] * cands[0][0] + cands[0][1] * cands[0][1]) > 1e-4) {
    const l0 = Math.sqrt(cands[0][0] * cands[0][0] + cands[0][1] * cands[0][1]);
    const v0x = cands[0][0] / l0, v0y = cands[0][1] / l0;
    const angs = [25, -25, 90, -90];
    for (const ang of angs) {
      const a = ang * Math.PI / 180;
      const ca = Math.cos(a), sa = Math.sin(a);
      cands.push([(v0x * ca - v0y * sa) * mvl, (v0x * sa + v0y * ca) * mvl]);
    }
  }
  for (const v of cands) {
    const L = Math.sqrt(v[0] * v[0] + v[1] * v[1]);
    if (L < 1e-4) continue;
    const sc = Math.min(1.0, mvlen / L);
    const sp2 = [pos[0] + v[0] * sc, pos[1] + v[1] * sc, pos[2]];
    const g2 = ground_at(sp2[0], sp2[1], pos[2] + 2.6, true);
    if (g2 === -1e9 || Math.abs(g2 - pos[2]) > 0.9) continue;
    sp2[2] = g2;
    if (blocked(sp2)) continue;
    const dx2 = sp2[0] - pos[0], dy2 = sp2[1] - pos[1];
    return [sp2, Math.sqrt(dx2 * dx2 + dy2 * dy2)];
  }
  return null;
}

/* ---------------- A* over the navmesh cell graph (port of s41 astar) ---------------- */
function astar(s, g) {
  if (s === g) return [s];
  const dist = new Map([[s, 0.0]]);
  const prev = new Map();
  // binary heap of [f, dd, u] with lexicographic comparison (Python heapq tuple order)
  const heap = new MinHeap();
  heap.push([edist(s, g), 0.0, s]);
  while (heap.size() > 0) {
    const top = heap.pop();
    const f_ = top[0], dd = top[1], u = top[2];
    if (u === g) {
      const path = [u];
      let cur = u;
      while (prev.has(cur)) { cur = prev.get(cur); path.push(cur); }
      return path.reverse();
    }
    if (dd > (dist.has(u) ? dist.get(u) : 1e18)) continue;
    for (let ni = NBS_OFF[u]; ni < NBS_OFF[u + 1]; ni++) {
      const v = NBS_ARR[ni];
      const climb = Math.max(0.0, nmCent[v * 3 + 2] - nmCent[u * 3 + 2]);
      const nd = dd + edist(u, v) * (1.0 + 2.0 * climb);
      if (nd < (dist.has(v) ? dist.get(v) : 1e18)) {
        dist.set(v, nd); prev.set(v, u);
        heap.push([nd + edist(v, g), nd, v]);
      }
    }
  }
  return null;
}

function edist(a, b) {
  const dx = nmCent[a * 3] - nmCent[b * 3];
  const dy = nmCent[a * 3 + 1] - nmCent[b * 3 + 1];
  const dz = nmCent[a * 3 + 2] - nmCent[b * 3 + 2];
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

/* min-heap with Python-heapq tuple semantics: compare [f, dd, u] lexicographically */
class MinHeap {
  constructor() { this.a = []; }
  size() { return this.a.length; }
  less(x, y) { return x[0] < y[0] || (x[0] === y[0] && (x[1] < y[1] || (x[1] === y[1] && x[2] < y[2]))); }
  push(x) {
    const a = this.a; a.push(x);
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.less(a[i], a[p])) { const t = a[i]; a[i] = a[p]; a[p] = t; i = p; }
      else break;
    }
  }
  pop() {
    const a = this.a;
    const top = a[0];
    const last = a.pop();
    if (a.length > 0) {
      a[0] = last;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < a.length && this.less(a[l], a[m])) m = l;
        if (r < a.length && this.less(a[r], a[m])) m = r;
        if (m === i) break;
        const t = a[i]; a[i] = a[m]; a[m] = t; i = m;
      }
    }
    return top;
  }
}

/* ---------------- s45 T2: soup FROM THE USER'S FILES (no shipped binary) ----------------
 * Parses GothamCity.lvc out of the user's game_config.gla with lvc.js (census
 * mode), extracts CCollisionComponent triangles + the C_BASE TRS, applies the
 * full euler transform and assembles the TCS1 buffer byte-identical to the
 * Python export (verified: whole-file sha256 00ce7970e45adc854ac7cae6d0f97797
 * b602342d101e1ecb5eb1c2c01016beb8, 137,893 tris / 794 objects). */
const C_BASE = 1362553, C_COLL = 766542306;

function buildSoupFromLvc(lvcU8, table, gol) {
  // lvc.js exposes parseLvc as window.TDKRLvc.parseLvc when script-tagged
  const plv = (typeof parseLvc !== 'undefined') ? parseLvc
            : (typeof TDKRLvc !== 'undefined' ? TDKRLvc.parseLvc : null);
  if (!plv) throw new Error('lvc.js not loaded');
  const res = plv(lvcU8, table, gol, { census: true });
  const census = res.census;
  const base = new Map();
  (census[String(C_BASE)] || []).forEach(e => base.set(e[0], e[1]));
  const coll = census[String(C_COLL)] || [];
  const dv = new DataView(lvcU8.buffer, lvcU8.byteOffset, lvcU8.byteLength);

  function readTrs(off) {
    // c(1) i(4 BE) then 9x f32 BIG-endian (lvc floats are BE — see lvc.js note)
    let p = off + 5;
    const f = [];
    for (let k = 0; k < 9; k++) { f.push(dv.getFloat32(p, false)); p += 4; }
    return f;
  }

  function parseCollision(off) {
    let p = off;
    const u8 = () => lvcU8[p++];
    const i32 = () => { const v = dv.getInt32(p); p += 4; return v; };
    const f32 = () => { const v = dv.getFloat32(p, false); p += 4; return v; };
    u8(); u8(); i32(); i32(); u8(); u8(); i32();
    const nOuter = u8();
    const tris = [];
    for (let o = 0; o < Math.max(nOuter, 0); o++) {
      i32();
      const cnt = i32();
      for (let t = 0; t < Math.max(cnt, 0); t++) {
        const f9 = [];
        for (let k = 0; k < 9; k++) f9.push(f32());
        tris.push([f9, u8()]);
      }
    }
    return tris;
  }

  function eulerToM(rx, ry, rz) {
    const cx = Math.cos(rx), sx = Math.sin(rx);
    const cy = Math.cos(ry), sy = Math.sin(ry);
    const cz = Math.cos(rz), sz = Math.sin(rz);
    return [cz * cy, cz * sy * sx - sz * cx, cz * sy * cx + sz * sx,
            sz * cy, sz * sy * sx + cz * cx, sz * sy * cx - cz * sx,
            -sy, cy * sx, cy * cx];
  }

  const objects = [];
  for (const [rid, off] of coll) {
    const trs = base.has(rid) ? readTrs(base.get(rid)) : null;
    objects.push({ rid, trs, tris: parseCollision(off) });
  }
  const ntris = objects.reduce((a, o) => a + o.tris.length, 0);
  const nameblob = [], nrec = [], trirec = [];
  const chunks = [];
  const pushF32 = (arr, v) => { const b = new Uint8Array(4); new DataView(b.buffer).setFloat32(0, v, true); chunks.length = 0; for (const x of b) arr.push(x); };
  objects.forEach((o, oid) => {
    const nm = o.tris.length ? 'obj' : '';
    const noff = nameblob.length;
    for (const ch of nm) nameblob.push(ch.charCodeAt(0));
    const t = o.trs || [0, 0, 0, 0, 0, 0, 0, 0, 0];
    const b = new Uint8Array(12);
    const bv = new DataView(b.buffer);
    bv.setUint32(0, noff, true); bv.setUint16(4, nm.length, true);
    bv.setUint16(6, oid & 0xffff, true); bv.setUint32(8, o.tris.length, true);
    for (const x of b) nrec.push(x);
    for (let k = 0; k < 9; k++) pushF32(nrec, t[k]);
    const m = o.trs ? eulerToM(t[3], t[4], t[5]) : null;
    for (const [t9, fl] of o.tris) {
      const ob = new Uint8Array(2);
      new DataView(ob.buffer).setUint16(0, oid & 0xffff, true);
      trirec.push(ob[0], ob[1]);
      for (let vi = 0; vi < 3; vi++) {
        const x = t9[vi * 3] * t[6], y = t9[vi * 3 + 1] * t[7], z = t9[vi * 3 + 2] * t[8];
        const pw = o.trs ? [
          m[0] * x + m[1] * y + m[2] * z + t[0],
          m[3] * x + m[4] * y + m[5] * z + t[1],
          m[6] * x + m[7] * y + m[8] * z + t[2]] : [t9[vi * 3], t9[vi * 3 + 1], t9[vi * 3 + 2]];
        pushF32(trirec, pw[0]); pushF32(trirec, pw[1]); pushF32(trirec, pw[2]);
      }
      trirec.push(fl & 0xff);
    }
  });
  const head = new Uint8Array(16);
  const hv = new DataView(head.buffer);
  head.set([0x54, 0x43, 0x53, 0x31], 0);   // 'TCS1'
  hv.setUint32(4, ntris, true); hv.setUint32(8, objects.length, true);
  hv.setUint32(12, nameblob.length, true);
  const total = 16 + nameblob.length + nrec.length + trirec.length;
  const out = new Uint8Array(total);
  out.set(head, 0); out.set(nameblob, 16);
  out.set(nrec, 16 + nameblob.length);
  out.set(trirec, 16 + nameblob.length + nrec.length);
  return { buf: out.buffer, nTri: ntris, nObj: objects.length, records: res.records.length };
}



if (typeof module !== 'undefined' && module.exports) module.exports = { loadSoup, loadNavmesh, astar, ground_at, nm_ground, blocked, buildSoupFromLvc };
