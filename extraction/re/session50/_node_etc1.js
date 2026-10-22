
const fs = require('fs');
const ETC1 = require(process.argv[2]);
const tex = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const buf = Buffer.from(tex.blocks, 'base64');
const rgba = ETC1.decodeRGBA(new Uint8Array(buf), tex.w, tex.h);
fs.writeFileSync(process.argv[4], JSON.stringify({w: tex.w, h: tex.h, rgba: Array.from(rgba)}));
