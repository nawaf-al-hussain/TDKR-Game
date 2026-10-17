// test_lvc_s30.js — JS vs Python equivalence on every parsed level with the
// s30 table (static cinematic + traffic + shop-item specs, unconditional
// LevelInit trailing word; ZERO measured spans in the table).
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { parseLvc } = require('/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc.js');

const HERE = __dirname;
const DATA = '/tmp/my-project/work/data';
const table = JSON.parse(fs.readFileSync('/tmp/my-project/work/re29/lvc_readseq_s30.json', 'utf8'));
const gol = JSON.parse(fs.readFileSync('/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json', 'utf8'));
const expected = JSON.parse(fs.readFileSync(path.join(HERE, 's30_expected.json'), 'utf8'));

let fail = 0, pass = 0;
for (const lv of Object.keys(expected)) {
  const data = new Uint8Array(fs.readFileSync(path.join(DATA, lv + '.lvc')));
  const t0 = Date.now();
  let res;
  try { res = parseLvc(data, table, gol); }
  catch (e) { console.log(`${lv}: JS ERROR ${e.message}`); fail++; continue; }
  const exp = expected[lv];
  let ok = res.records.length === exp.nrec && res.tableOff === exp.table_off;
  if (!ok) { console.log(`${lv}: COUNT MISMATCH js=${res.records.length} py=${exp.nrec}`); fail++; continue; }
  let firstBad = -1;
  for (let i = 0; i < res.records.length; i++) {
    const a = res.records[i], b = exp.records[i];
    if (a.rid !== b[0] || a.start !== b[1] || a.tid !== b[2] || a.end !== b[3]) { firstBad = i; break; }
  }
  if (firstBad >= 0) { console.log(`${lv}: BOUNDARY MISMATCH @${firstBad}`); fail++; continue; }
  const recTokHash = [];
  let ti = 0, hashBad = -1;
  for (const a of res.records) {
    const h = crypto.createHash('sha1');
    while (ti < res.tokens.length && res.tokens[ti][1] >= a.start && res.tokens[ti][1] < a.end) {
      const t = res.tokens[ti];
      h.update(t[0]);
      h.update(data.subarray(t[1], t[1] + t[2]));
      ti++;
    }
    recTokHash.push(h.digest('hex'));
  }
  for (let i = 0; i < recTokHash.length; i++) {
    if (recTokHash[i] !== exp.records[i][4]) { hashBad = i; break; }
  }
  if (hashBad >= 0) { console.log(`${lv}: TOKEN-HASH MISMATCH @${hashBad}`); fail++; continue; }
  console.log(`${lv}: PASS ${res.records.length} records (${Date.now() - t0} ms)`);
  pass++;
}
console.log(`\n${pass}/${pass + fail} levels: JS == Python (boundaries + token streams)`);
process.exit(fail ? 1 : 0);
