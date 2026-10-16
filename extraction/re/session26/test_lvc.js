// test_lvc.js — node test: JS parser must equal the Python parser on both
// islands, record boundary for boundary and token for token (SHA1 per
// record over [kind letter + raw bytes] of every token, exported by
// s27_export_expected.py from lvc_pure.py's token stream).
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { parseLvc } = require('./lvc.js');

const HERE = __dirname;
const DATA = '/home/z/my-project/work/data';
const table = JSON.parse(fs.readFileSync(path.join(HERE, 'lvc_readseq.json'), 'utf8'));
const gol = JSON.parse(fs.readFileSync(path.join(HERE, 'lvc_gol_templates.json'), 'utf8'));
const expected = JSON.parse(fs.readFileSync(path.join(HERE, 's27_expected.json'), 'utf8'));

let fail = 0;
for (const lv of ['GothamCity', 'GothamCity_Island2']) {
  const data = new Uint8Array(fs.readFileSync(path.join(DATA, lv + '.lvc')));
  const t0 = Date.now();
  const res = parseLvc(data, table, gol);
  const ms = Date.now() - t0;
  const exp = expected[lv];
  let ok = res.records.length === exp.nrec &&
           res.tableOff === exp.table_off;
  if (!ok) { console.log(`${lv}: COUNT MISMATCH js=${res.records.length} py=${exp.nrec}`); fail++; continue; }
  let firstBad = -1;
  for (let i = 0; i < res.records.length; i++) {
    const a = res.records[i], b = exp.records[i];
    if (a.rid !== b[0] || a.start !== b[1] || a.tid !== b[2] || a.end !== b[3]) {
      ok = false; firstBad = i; break;
    }
    // token hash over this record's tokens
    // (token ranges: walk records' token counts by re-scan — the JS parser
    //  returns one flat list; recompute ranges from record boundaries by
    //  grouping tokens whose off falls inside [start,end))
    // For exactness, the parser also returns tokens; group by rec index
    // via a parallel array is avoided here: hash per record using the
    // token list slice recorded during parse — see tokensByRec below.
  }
  // group tokens per record by offset containment (records are contiguous)
  const recTokHash = [];
  let ti = 0;
  for (const a of res.records) {
    const h = crypto.createHash('sha1');
    while (ti < res.tokens.length && res.tokens[ti][1] >= a.start &&
           res.tokens[ti][1] < a.end) {
      const t = res.tokens[ti];
      h.update(t[0]);
      const bytes = data.subarray(t[1], t[1] + t[2]);
      h.update(bytes);
      ti++;
    }
    recTokHash.push(h.digest('hex'));
  }
  let hashBad = -1;
  for (let i = 0; i < recTokHash.length; i++) {
    if (recTokHash[i] !== exp.records[i][4]) { hashBad = i; break; }
  }
  const status = ok && hashBad === -1 ? 'PASS' : 'FAIL';
  if (status === 'FAIL') fail++;
  console.log(`${lv}: ${status} — ${res.records.length} records, ` +
    `${res.tokens.length} tokens, ${ms} ms` +
    (firstBad >= 0 ? ` first boundary mismatch @${firstBad}` : '') +
    (hashBad >= 0 ? ` first token-hash mismatch @${hashBad}` : ''));
}
console.log(fail === 0 ? 'JS == PYTHON on both islands (boundaries + token streams)' :
  `${fail} ISLAND(S) FAILED`);
process.exit(fail === 0 ? 0 : 1);
