// s46 T4: JS side value digests — parseLvc on the same lvc members, same
// canonicalization as s46_t4_lvc_values.py (floats as f64 BE bits, strings
// latin1-hex; lvc.js already decodes latin1).
'use strict';
const fs = require('fs');
const crypto = require('crypto');
const { parseLvc } = require('/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc.js');
const TAB = JSON.parse(fs.readFileSync('/tmp/my-project/work/re29/lvc_readseq_s30.json', 'utf8'));
const GOL = JSON.parse(fs.readFileSync('/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json', 'utf8'));

function digest(data) {
  const res = parseLvc(Buffer.from(data), TAB, GOL, {});
  const tokens = res.tokens;
  const h = crypto.createHash('sha256');
  const kinds = {};
  for (const tk of tokens) {
    const kind = tk[0], off = tk[1], size = tk[2], val = tk[3];
    kinds[kind] = (kinds[kind] || 0) + 1;
    let line;
    if (kind === 'i') line = `i|${off}|${val}`;
    else if (kind === 'f') {
      const b = Buffer.alloc(8);
      b.writeDoubleBE(val, 0);
      line = 'f|' + off + '|' + b.toString('hex');
    } else if (kind === 'STR') {
      if (typeof val === 'string') {
        const bytes = Buffer.from(val, 'latin1');
        line = 'S|' + off + '|' + bytes.toString('hex');
      } else line = `S|${off}|#${val}`;
    } else if (kind === 'c' || kind === 'B' || kind === 's') line = `${kind}|${off}|${val}`;
    else line = `${kind}|${off}|${size}|-`;
    h.update(line);
    h.update('\n');
  }
  return { count: tokens.length, sha: h.digest('hex'), kinds };
}

const out = {};
for (const nm of process.argv.slice(2)) {
  const data = fs.readFileSync(`/tmp/my-project/scripts_t4_${nm}.lvc`);
  out[nm] = digest(data);
}
console.log(JSON.stringify(out));
