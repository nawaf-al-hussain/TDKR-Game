// lvc.js — dependency-free TDKR .lvc record parser (browser + node).
// Port of extraction/re/session26/lvc_pure.py (session 26/27 read-sequence
// table machine). Byte-exact vs the engine on every record of both islands.
//
// Usage (node):
//   const { parseLvc } = require('./lvc.js');
//   const table = JSON.parse(fs.readFileSync('lvc_readseq.json'));
//   const gol   = JSON.parse(fs.readFileSync('lvc_gol_templates.json'));
//   const res = parseLvc(new Uint8Array(fs.readFileSync(f)), table, gol);
// res = { records: [{rid, start, tid, end, kind}], tokens: [[kind, off, size, val], ...] }

'use strict';

var NAT = { i: 4, f: 4, c: 1, B: 1, s: 2, STR: 4 };

function Reader(data, strings) {
  this.d = data;
  this.strings = strings;
  this.p = 0;
  this.fields = [];          // scalar values, in read order (rep counts)
}

Reader.prototype.tok = function (kind, size, out) {
  if (size === undefined || size === null) size = NAT[kind];
  var off = this.p;
  var b = this.d.subarray(off, off + size);
  this.p += size;
  var val = null;
  if (kind === 'STR') {
    var idx = (b[0] << 24 | b[1] << 16 | b[2] << 8 | b[3]) | 0;
    if (idx >= 0 && idx < this.strings.length) val = this.strings[idx];
    else val = idx;
    this.fields.push(idx);
  } else if (kind === 'i') {
    val = (b[0] << 24 | b[1] << 16 | b[2] << 8 | b[3]) | 0;
    this.fields.push(val);
  } else if (kind === 'f') {
    // BIG-endian per lvc_pure ('>f') — the s45 collision export exposed the
    // LE read as a latent bug (uncaught: floats are rare in the s26 test paths)
    var u = (b[0] << 24 | b[1] << 16 | b[2] << 8 | b[3]) >>> 0;
    var buf = new ArrayBuffer(4), dv = new DataView(buf);
    dv.setUint32(0, u);
    val = dv.getFloat32(0);
    this.fields.push(val);
  } else if (kind === 'c' || kind === 'B') {
    val = b[0];
    this.fields.push(val);
  } else if (kind === 's') {
    val = (b[0] << 8 | b[1]) | 0;
    this.fields.push(val);
  }
  if (out) out.push([kind, off, size, val]);
};

Reader.prototype.raw = function (n, out) {
  var off = this.p;
  this.p += n;
  if (out) out.push(['raw', off, n, null]);
};

function replay(spec, r, out) {
  for (var i = 0; i < spec.length; i++) {
    var tok = spec[i];
    var k = tok[0];
    if (k === 'rep') {
      var count = r.fields[r.fields.length - 1];
      var sub = tok[2];
      for (var c = 0; c < Math.max(count, 0); c++) replay(sub, r, out);
    } else if (k === 'span') {
      throw new Error('SpanNeeded at ' + r.p);
    } else if (k === 'raw') {
      r.raw(tok[1], out);
    } else if (k === 'fat') {
      r.tok(tok[1], tok[2], out);
    } else if (k === 'i_nz') {
      // round 19: LevelInit trailing word read only when nonzero
      var dv2 = new DataView(r.d.buffer, r.d.byteOffset + r.p, 4);
      if (dv2.getInt32(0) !== 0) r.tok('i', undefined, out);
    } else {
      r.tok(k, tok.length > 1 ? tok[1] : undefined, out);
    }
  }
}

function parseLvc(data, table, gol, opts) {
  // opts (optional, s45): { census: bool -> collect a component census
  //   {tidString -> [[rid, startOff, size], ...]} mirroring lvc_pure.parse's
  //   census (the per-component offsets/sizes the collision exporter needs). }
  var dv = new DataView(data.buffer, data.byteOffset, data.byteLength);
  if (String.fromCharCode(data[0], data[1], data[2], data[3]) !== 'DICT')
    throw new Error('bad magic');
  var tableOff = dv.getUint32(4);
  var nrecHdr = dv.getUint32(13);
  var pos = tableOff;
  var nstr = dv.getInt32(pos);
  pos += 4;
  var strings = [];
  for (var i = 0; i < nstr; i++) {
    var ln = dv.getInt32(pos); pos += 4;
    var bytes = data.subarray(pos, pos + ln); pos += ln;
    strings.push(bytesToString(bytes));
  }
  var templates = {};
  Object.keys(gol.templates).forEach(function (k) {
    templates[parseInt(k, 16)] = gol.templates[k];
  });

  var r = new Reader(data, strings);
  r.p = 17;
  var dedicated = table.dedicated, engineCases = table.engine_cases;
  var components = table.components;
  var spansC = {}, spanToks = {};
  Object.keys(table.spans || {}).forEach(function (k) {
    spansC[k] = {};
    (table.spans[k] || []).forEach(function (e) { spansC[k][e[0]] = e[1]; });
  });
  Object.keys(table.span_toks || {}).forEach(function (k) {
    spanToks[k] = {};
    Object.keys(table.span_toks[k]).forEach(function (o) {
      spanToks[k][parseInt(o, 10)] = table.span_toks[k][o];
    });
  });

  var records = [], tokens = [];
  var census = (opts && opts.census) ? {} : null;
  var cur = 17, rid = 0;
  while (cur < tableOff) {
    rid++;
    var recStart = cur;
    var tid = dv.getInt32(cur);
    var t0 = tokens.length;
    r.p = cur;
    var kind;
    if (tid === -1) {
      r.tok('i', undefined, tokens);
      kind = 'skip';
    } else if (engineCases[String(tid)]) {
      var spec = engineCases[String(tid)];
      if (spec.length && spec[0][0] === 'span') {
        var stE = (table.span_toks_e || {})[String(tid)] || {};
        var st = stE[String(tableOff)];
        if (st) {
          st.forEach(function (t) { tokens.push(t.slice()); });
          r.p += st.reduce(function (a, t) { return a + t[2]; }, 0);
        } else {
          var lenE = (table.spans_e || {})[String(tid)][String(tableOff)];
          r.raw(lenE, tokens);
        }
      } else replay(spec, r, tokens);
      kind = 'engine 0x' + tid.toString(16);
    } else if (dedicated[String(tid)]) {
      replay(dedicated[String(tid)], r, tokens);
      kind = 'ded 0x' + tid.toString(16);
    } else if (templates[tid]) {
      r.tok('i', undefined, tokens);
      templates[tid].forEach(function (comp) {
        var flag = comp[0], ctid = comp[1];
        if (flag) return;
        var ks = String(ctid);
        var cspec = components[ks];
        if (!cspec) throw new Error('no spec for component ' + ks +
          ' in record ' + rid + ' @' + cur);
        var cstart = r.p;
        if (cspec.length && cspec[0][0] === 'span') {
          var stc = (spanToks[ks] || {})[cstart];
          if (stc) {
            stc.forEach(function (t) { tokens.push(t.slice()); });
            r.p += stc.reduce(function (a, t) { return a + t[2]; }, 0);
          } else {
            r.raw(spansC[ks][cstart], tokens);
          }
        } else replay(cspec, r, tokens);
        if (census) {
          (census[ks] = census[ks] || []).push([rid, cstart, r.p - cstart]);
        }
      });
      kind = 'tmpl 0x' + tid.toString(16);
    } else {
      r.tok('i', undefined, tokens);
      kind = 'skip';
    }
    records.push({ rid: rid, start: recStart, tid: tid, end: r.p, kind: kind });
    cur = r.p;
  }
  if (cur !== tableOff) {
    // s37 T4: shop.lvc end-of-data table-sentinel record (0xFFFFFF00) puts the
    // cursor 1 past the table end (python's sequential reader tolerates this;
    // byte-explained in r25). Accept ONLY that documented case.
    var lastRec = records[records.length - 1];
    if (typeof process !== 'undefined' && process.env.LVC_DEBUG)
      console.error('LVC framing debug: cur=' + cur + ' table=' + tableOff +
        ' last=' + JSON.stringify(lastRec));
    var sentinelOK = cur === tableOff + 1 && lastRec &&
      ((lastRec.tid >>> 0) === 0xFFFFFF00 || (lastRec.rid >>> 0) === 0xFFFFFF00);
    if (!sentinelOK)
      throw new Error('framing error: cursor ' + cur + ' != table ' + tableOff);
  }
  return { records: records, tokens: tokens, tableOff: tableOff,
           nrecHdr: nrecHdr, strings: strings, census: census };
}

function bytesToString(bytes) {
  // latin1 per lvc_pure ('utf-8' with replace — latin1 is the lossless
  // superset for hashing; tests hash raw bytes, not the string)
  var s = '';
  for (var i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  return s;
}

if (typeof module !== 'undefined') module.exports = { parseLvc: parseLvc, replay: replay, Reader: Reader };
if (typeof window !== 'undefined') window.TDKRLvc = { parseLvc: parseLvc };
