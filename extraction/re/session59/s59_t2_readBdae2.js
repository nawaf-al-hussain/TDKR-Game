function readBdae2(u8) {
  // s59 T2: GENERALIZED bdae reader — every offset derived from the file's own
  // structure (BRES header -> pools/sections; validated node scan; stride run;
  // inverse-bind run w/ backward extension; palette; skin-record run gives NV;
  // bbox-validated vertex scan; u16 index run). No per-file constants.
  // Validated: reproduces batman.bdae layout exactly (s22 constants) and derives
  // the merc layout (NV 1294, stride 52, 16-B/3-influence skinrecs, 31 bones).
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  const u32 = o => dv.getUint32(o, true), u16 = o => dv.getUint16(o, true),
        f32 = o => dv.getFloat32(o, true);
  function poolstr(o) {
    if (o <= 0 || o >= u8.length) return null;
    let e = o;
    while (e < u8.length && u8[e] !== 0 && e - o < 4096) e++;
    if (e >= u8.length || e - o > 4096) return null;
    let s = '';
    for (let i = o; i < e; i++) s += String.fromCharCode(u8[i]);
    return s;
  }
  const pool0 = u32(0x1c), pool1 = u32(0x20), off4 = u32(0x28);
  if (u8[0] !== 0x42 || u8[1] !== 0x52 || u8[2] !== 0x45 || u8[3] !== 0x53) throw new Error('bdae2: not BRES');
  // ---- nodes (validated 0x50 records, 4-B stepping) ----
  const nodes = [];
  for (let o = pool1; o < off4 - 0x50; o += 4) {
    const n1 = poolstr(u32(o)), n2 = poolstr(u32(o + 4)), al = poolstr(u32(o + 8));
    if (n1 === null || n2 === null || al === null) continue;
    const t = [f32(o + 0xc), f32(o + 0x10), f32(o + 0x14)];
    const q = [f32(o + 0x18), f32(o + 0x1c), f32(o + 0x20), f32(o + 0x24)];
    const s = [f32(o + 0x28), f32(o + 0x2c), f32(o + 0x30)];
    const ql = Math.hypot(q[0], q[1], q[2], q[3]);
    if (!(ql > 0.96 && ql < 1.04)) continue;
    if (!(Math.abs(t[0]) < 1e4 && Math.abs(t[1]) < 1e4 && Math.abs(t[2]) < 1e4)) continue;
    if (!(Math.abs(s[0]) > 0.01 && Math.abs(s[0]) < 100 && Math.abs(s[1]) > 0.01 &&
          Math.abs(s[1]) < 100 && Math.abs(s[2]) > 0.01 && Math.abs(s[2]) < 100)) continue;
    if (u32(o + 0x34) !== 1 || u32(o + 0x38) > 32) continue;
    nodes.push({ off: o, name: n2, alias: al, t, q, s });
  }
  // ---- vertex stride: first run of >=4 equal u32 in [off4, off4+0x200) ----
  let stridesAt = -1, stride = 0;
  for (let o = off4; o < off4 + 0x200; o += 4) {
    const v = u32(o);
    if (v >= 8 && v <= 256 && u32(o + 4) === v && u32(o + 8) === v && u32(o + 12) === v) {
      stridesAt = o; stride = v; break;
    }
  }
  if (stridesAt < 0) throw new Error('bdae2: stride run not found');
  // ---- inverse binds: 64-B mats, row3 (m3,m7,m11,m15) = (0,0,0,1); run >= 10;
  //      backward-extend while preceding mat validates ----
  const matOk = o => Math.abs(f32(o + 12)) < 1e-5 && Math.abs(f32(o + 28)) < 1e-5 &&
    Math.abs(f32(o + 44)) < 1e-5 && Math.abs(f32(o + 60) - 1) < 1e-5 &&
    [0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14].every(i => Math.abs(f32(o + 4 * i)) < 1e4);
  let invbOff = -1, nBones = 0;
  for (let o = off4; o + 64 <= u8.length;) {
    if (u32(o + 60) === 0x3f800000) {
      let run = 0, p = o;
      while (p + 64 <= u8.length && matOk(p)) { run++; p += 64; }
      if (run >= 10) {
        let s0 = o;
        while (s0 - 64 >= off4 && matOk(s0 - 64)) { s0 -= 64; run++; }
        invbOff = s0; nBones = run; break;
      }
      o = (p > o ? p : o) + 4;
    } else o += 4;
  }
  if (invbOff < 0) throw new Error('bdae2: inverse-bind run not found');
  // ---- palette: nBones 8-B entries containing 'Bone' at +0 or +2, after INVB ----
  const BONE = [0x42, 0x6f, 0x6e, 0x65];
  const hasBone = b => BONE.every((c, i) => b[i] === c) || BONE.every((c, i) => b[i + 2] === c);
  let palOff = -1;
  for (let o = invbOff + nBones * 64; o < invbOff + nBones * 64 + 0x200; o += 4) {
    let ok = 0;
    for (let k = 0; k < Math.min(nBones, 12); k++) if (hasBone(u8.subarray(o + 8 * k, o + 8 * k + 8))) ok++;
    if (ok >= Math.min(nBones, 12)) { palOff = o; break; }
  }
  if (palOff < 0) throw new Error('bdae2: palette not found');
  const pal = [];
  for (let o = palOff; o < palOff + nBones * 8; o += 8) {
    const a = String.fromCharCode(u8[o], u8[o + 1]), b = String.fromCharCode(u8[o + 4], u8[o + 5]);
    const tag = (u8[o + 4] === 0x42 && u8[o + 5] === 0x6f) ? a : b;
    pal.push('Bone' + tag.replace(/[^0-9]/g, ''));
  }
  // ---- skin records: try (stride, #weights) in {(20,4),(16,3),(24,5),(12,2),(28,6)};
  //      run >= 200 right after palette -> NV + record geometry ----
  let srOff = -1, NV = 0, srStride = 0, srW = 0, maxJoint = 0;
  outer:
  for (const [ss, wn] of [[20, 4], [16, 3], [24, 5], [12, 2], [28, 6]]) {
    for (let s = palOff + nBones * 8; s < palOff + nBones * 8 + 0x40; s += 4) {
      let n = 0, o = s, mj = 0;
      while (o + ss <= u8.length && n < 8000) {
        let ok = true, wsum = 0;
        for (let k = 0; k < wn; k++) {
          const w = f32(o + 4 + 4 * k);
          if (u8[o + k] >= nBones || w < -1e-6 || w > 1.0001) { ok = false; break; }
          wsum += w;
        }
        if (!ok || !(wsum > 0.9 && wsum < 1.1)) break;
        for (let k = 0; k < wn; k++) mj = Math.max(mj, u8[o + k]);
        n++; o += ss;
      }
      if (n >= 200) { srOff = s; NV = n; srStride = ss; srW = wn; maxJoint = mj; break outer; }
    }
  }
  if (srOff < 0) throw new Error('bdae2: skin-record run not found');
  // ---- verts: bbox from descriptor (6 floats at stridesAt-0x18); scan candidate
  //      starts where ALL NV records' positions lie inside the bbox ----
  const bmin = [f32(stridesAt - 0x18), f32(stridesAt - 0x14), f32(stridesAt - 0x10)];
  const bmax = [f32(stridesAt - 0xc), f32(stridesAt - 8), f32(stridesAt - 4)];
  const EPS = 0.02;
  let vertsOff = -1;
  outerV:
  for (let s = stridesAt + 0x40; s < stridesAt + 0x300; s += 4) {
    for (let i = 0; i < NV; i++) {
      const b = s + i * stride;
      if (b + stride > u8.length) { continue outerV; }
      const px = f32(b), py = f32(b + 4), pz = f32(b + 8);
      if (!(bmin[0] - EPS <= px && px <= bmax[0] + EPS && bmin[1] - EPS <= py &&
            py <= bmax[1] + EPS && bmin[2] - EPS <= pz && pz <= bmax[2] + EPS)) continue outerV;
    }
    vertsOff = s; break;
  }
  if (vertsOff < 0) throw new Error('bdae2: vertex block not found');
  // ---- indices: first >=32 run of u16 < NV after the vertex block ----
  let idxOff = -1, IDXN = 0;
  for (let s = (vertsOff + NV * stride + 3) & ~3; s < Math.min(vertsOff + NV * stride + 0x400, u8.length - 64); s += 2) {
    let n = 0, o = s;
    while (o + 2 <= u8.length && n < 0x40000 && u16(o) < NV) { n++; o += 2; }
    if (n >= 32) { idxOff = s; IDXN = n; break; }
  }
  if (idxOff < 0) throw new Error('bdae2: index run not found');
  // ---- assemble (same output shape as readBdae) ----
  const byAlias = {};
  for (const nd of nodes) if (nd.alias.startsWith('Bone')) byAlias[nd.alias] = nd.name;
  const jointNodes = pal.map(p => byAlias[p]);
  const BIPED = { Bip01_Pelvis: 'Bip01', Bip01_Spine: 'Bip01_Pelvis', Bip01_Spine1: 'Bip01_Spine',
    Bip01_Neck: 'Bip01_Spine1', Bip01_Head: 'Bip01_Neck', Bip01_L_Thigh: 'Bip01_Pelvis',
    Bip01_L_Calf: 'Bip01_L_Thigh', Bip01_L_Foot: 'Bip01_L_Calf', Bip01_R_Thigh: 'Bip01_Pelvis',
    Bip01_R_Calf: 'Bip01_R_Thigh', Bip01_R_Foot: 'Bip01_R_Calf',
    Bip01_L_Clavicle: 'Bip01_Neck', Bip01_L_UpperArm: 'Bip01_L_Clavicle',
    Bip01_L_Forearm: 'Bip01_L_UpperArm', Bip01_L_Hand: 'Bip01_L_Forearm',
    Bip01_R_Clavicle: 'Bip01_Neck', Bip01_R_UpperArm: 'Bip01_R_Clavicle',
    Bip01_R_Forearm: 'Bip01_R_UpperArm', Bip01_R_Hand: 'Bip01_R_Forearm',
    Bip01_L_Finger0: 'Bip01_L_Hand', Bip01_L_Finger01: 'Bip01_L_Finger0',
    Bip01_L_Finger1: 'Bip01_L_Hand', Bip01_L_Finger11: 'Bip01_L_Finger1',
    Bip01_L_Finger2: 'Bip01_L_Hand', Bip01_L_Finger21: 'Bip01_L_Finger2',
    Bip01_R_Finger0: 'Bip01_R_Hand', Bip01_R_Finger01: 'Bip01_R_Finger0',
    Bip01_R_Finger1: 'Bip01_R_Hand', Bip01_R_Finger11: 'Bip01_R_Finger1',
    Bip01_R_Finger2: 'Bip01_R_Hand', Bip01_R_Finger21: 'Bip01_R_Finger2' };
  const parentName = nm => BIPED[nm] || null;
  const invB = [];
  for (let k = 0; k < nBones; k++) {
    const o = invbOff + k * 64, m = new Float64Array(16);
    for (let i = 0; i < 16; i++) m[i] = f32(o + 4 * i);
    invB.push(m);
  }
  const verts = new Float32Array(NV * 3);
  const uvs = new Float32Array(NV * 2);
  const skinJ = new Uint8Array(NV * 4);
  const skinW = new Float32Array(NV * 4);
  for (let i = 0; i < NV; i++) {
    const b = vertsOff + i * stride;
    verts[3 * i] = f32(b); verts[3 * i + 1] = f32(b + 4); verts[3 * i + 2] = f32(b + 8);
    uvs[2 * i] = u16(b + stride - 8) / 4096.0;
    uvs[2 * i + 1] = u16(b + stride - 4) / 4096.0;
    const s = srOff + i * srStride;
    for (let j = 0; j < 4; j++) skinJ[4 * i + j] = u8[s + j];
    for (let j = 0; j < srW; j++) skinW[4 * i + j] = f32(s + 4 + 4 * j);
  }
  const idx = new Uint16Array(IDXN);
  for (let i = 0; i < IDXN; i++) idx[i] = u16(idxOff + 2 * i);
  return { nodes, jointNodes, pnameOf: {}, parentName, invB, verts, uvs, skinJ, skinW, idx,
           _layout: { pool0, pool1, off4, stridesAt, stride, invbOff, nBones, palOff,
                      srOff, srStride, srW, maxJoint, NV, vertsOff, idxOff, IDXN } };
}
