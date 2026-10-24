// gol_parse.js — s57 T5: in-browser gol.bin parser (header, offsets, string table,
// template table, per-comp payload walks with the s57 engine-derived sequences).
// Dependency-free; used by the migration branch so triggers/enemies come straight
// from the user's files. Digest parity vs the Python walk is the acceptance gate.
'use strict';
var NAT = { i: 4, f: 4, c: 1, B: 1, s: 2, STR: 4 };
// s57 engine-derived template sequences (extraction/re/session57/s57_t2_note.md)
var SEQ57 = {
  0x5441a117: { kind: 'stateset' },                       // 8 STR state-name list
  0x3ef5108d: { kind: 'dropc' },                          // i + n*(i,i)
  0x44c6e9e5: { kind: 'fixed', n: 38 },                   // i,c6,i4,f3
  0x3e2bb040: { kind: 'fixed', n: 16 },                   // i,i,f,i
  0x54989cb1: { kind: 'actorbase' },                      // 78 + 5n
  0x592ce07c: { kind: 'motion' },                         // [c,f,f,c,f,f] = 18
  0x40c6b80a: { kind: 'unknown' }                         // CustomizeActor template variant unresolved
};
function parseGol(d, specTable) {
  var dv = new DataView(d.buffer, d.byteOffset, d.byteLength);
  var u32 = function (o) { return dv.getUint32(o); };
  var i32 = function (o) { return dv.getInt32(o); };
  var f32 = function (o) { return dv.getFloat32(o); };
  var tableOff = u32(4);
  var nrec = u32(13);
  var offs = [];
  for (var i = 0; i < nrec; i++) offs.push(u32(17 + 4 * i));
  var pos = tableOff;
  var nstr = i32(pos); pos += 4;
  var strings = [];
  for (i = 0; i < nstr; i++) {
    var l = i32(pos); pos += 4;
    var s = '';
    for (var k = 0; k < l; k++) s += String.fromCharCode(d[pos + k]);
    strings.push(s); pos += l;
  }
  var templates = [];
  for (var ri = 0; ri < nrec; ri++) {
    var ro = offs[ri];
    var oid = u32(ro);
    var m = u32(ro + 4);
    var p = ro + 8 + 4 * m;
    var n = dv.getUint16(p);
    var nameidx = u32(p + 2);
    var nxt = (ri + 1 < nrec) ? offs[ri + 1] : d.length;
    var payloadStart = p + 6 + 6 * n;
    var payloadLen = nxt - payloadStart;
    var comps = [];
    for (var ci = 0; ci < n; ci++) comps.push({ id: u32(p + 6 + 6 * ci), flag: dv.getUint16(p + 10 + 6 * ci) });
    templates.push({ oid: oid, name: strings[nameidx] || '?', comps: comps,
                     payloadStart: payloadStart, payloadLen: payloadLen });
  }
  function walkComp(cid, q, end, pl) {
    var seq = SEQ57[cid];
    if (seq) {
      if (seq.kind === 'stateset') return (q + 32 <= end) ? q + 32 : -1;
      if (seq.kind === 'dropc') {
        if (q + 4 > end) return -1;
        var nn = i32(q);
        return (nn >= 0 && q + 4 + 8 * nn <= end) ? q + 4 + 8 * nn : -1;
      }
      if (seq.kind === 'fixed') return (q + seq.n <= end) ? q + seq.n : -1;
      if (seq.kind === 'actorbase') {
        if (q + 78 > end) return -1;
        var na = i32(q + 74);
        return (na >= 0 && q + 78 + 5 * na <= end) ? q + 78 + 5 * na : -1;
      }
      if (seq.kind === 'motion') {
        if (q + 18 <= end) {
          var ok = true;
          for (var fi = 0; fi < 4; fi++) { var v = f32(q + 1 + 4 * fi); if (!isFinite(v) || Math.abs(v) > 1e9) ok = false; }
          if (ok && d[q] <= 1 && d[q + 9] <= 1) return q + 18;
        }
        if (q + 4 > end) return -1;
        var ln = i32(q);
        return (ln >= 0 && q + 4 + ln <= end) ? q + 4 + ln : -1;
      }
      return -1; // unknown (CustomizeActor)
    }
    var toks = specTable[String(cid)];
    if (!toks) return -1;
    function replay(toks2, q2) {
      for (var ti = 0; ti < toks2.length; ti++) {
        var t = toks2[ti], kk = t[0];
        if (kk === 'rep') {
          return -1; // rep-bearing specs are unresolved for the template walk (parity with py)
        } else if (kk === 'raw') { q2 += t[1]; }
        else if (kk === 'fat') { q2 += t[2]; }
        else { q2 += (t.length > 1) ? t[1] : NAT[kk]; walkRepCount = 0; }
        if (q2 > end) return -1;
      }
      return q2;
    }
    var walkRepCount = 0;
    return replay(toks, q);
  }
  // canonical digest: per template [oid, name, comp ids, per-comp walk ends or null]
  var lines = [];
  var closed = 0, walked = 0;
  for (i = 0; i < templates.length; i++) {
    var T = templates[i];
    var ends = [];
    var q = T.payloadStart, end = T.payloadStart + T.payloadLen, ok = true;
    for (var cj = 0; cj < T.comps.length; cj++) {
      var cid = T.comps[cj].id;
      var e = walkComp(cid, q, end, d);
      if (e < 0) { ends.push(null); ok = false; break; }
      ends.push(e - T.payloadStart);
      q = e;
    }
    if (ok && q === end && T.comps.length && ends.length === T.comps.length) closed++;
    if (ok) walked++;
    lines.push(T.oid.toString(16) + '|' + T.name + '|' + T.comps.map(function (c) { return c.id.toString(16); }).join(',') + '|' + ends.join(','));
  }
  return { nrec: nrec, nstr: nstr, templates: templates, lines: lines,
           closed: closed, walkedPartial: walked };
}
if (typeof module !== 'undefined') module.exports = { parseGol: parseGol };
