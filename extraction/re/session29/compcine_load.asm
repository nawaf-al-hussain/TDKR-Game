0x2dce20: push    {r4, r5, r6, r7, r8, sb, sl, fp, lr}
0x2dce24: sub     sp, sp, #0x11c
0x2dce28: mov     r4, r1
0x2dce2c: str     r0, [sp, #0x10]
0x2dce30: mov     r0, r1
0x2dce34: bl      #0x339914   ; <<READER i>>
0x2dce38: ldr     ip, [sp, #0x10]
0x2dce3c: str     r0, [ip, #4]
0x2dce40: mov     r0, r4
0x2dce44: bl      #0x3395d8   ; <<READER c>>
0x2dce48: ldr     ip, [sp, #0x10]
0x2dce4c: adds    r3, r0, #0
0x2dce50: mov     r0, r4
0x2dce54: movne   r3, #1
0x2dce58: strb    r3, [ip, #8]
0x2dce5c: bl      #0x339b94   ; <<READER f>>
0x2dce60: ldr     ip, [sp, #0x10]
0x2dce64: str     r0, [ip, #0xc]
0x2dce68: mov     r0, r4
0x2dce6c: bl      #0x3395d8   ; <<READER c>>
0x2dce70: ldr     ip, [sp, #0x10]
0x2dce74: adds    r3, r0, #0
0x2dce78: mov     r0, r4
0x2dce7c: movne   r3, #1
0x2dce80: strb    r3, [ip, #0x10]
0x2dce84: bl      #0x339914   ; <<READER i>>
0x2dce88: ldr     r3, [sp, #0x10]
0x2dce8c: ldr     ip, [sp, #0x10]
0x2dce90: ldr     r3, [r3, #0x18]
0x2dce94: ldr     ip, [ip, #0x14]
0x2dce98: rsb     r5, ip, r3
0x2dce9c: str     r3, [sp, #0xc]
0x2dcea0: str     ip, [sp, #0x14]
0x2dcea4: asr     r5, r5, #4
0x2dcea8: cmp     r0, r5
0x2dceac: str     r0, [sp, #8]
0x2dceb0: bls     #0x2dd07c
0x2dceb4: subs    r3, r0, r5
0x2dceb8: str     r3, [sp, #0x18]
0x2dcebc: beq     #0x2dd080
0x2dcec0: ldr     ip, [sp, #0x10]
0x2dcec4: ldr     r3, [ip, #0x1c]
0x2dcec8: ldr     ip, [sp, #0xc]
0x2dcecc: rsb     r3, ip, r3
0x2dced0: ldr     ip, [sp, #0x18]
0x2dced4: cmp     ip, r3, asr #4
0x2dced8: bls     #0x2decd4
0x2dcedc: movw    r3, #0xffff
0x2dcee0: movt    r3, #0xfff
0x2dcee4: rsb     r3, r5, r3
0x2dcee8: mvn     r2, #0xf0000000
0x2dceec: cmp     ip, r3
0x2dcef0: bhi     #0x2dee28
0x2dcef4: cmp     ip, r5
0x2dcef8: addhs   r3, r5, ip
0x2dcefc: addlo   r3, r5, r5
0x2dcf00: cmp     r5, r3
0x2dcf04: strhi   r2, [sp, #0x20]
0x2dcf08: movhi   r3, r2
0x2dcf0c: bhi     #0x2dcf28
0x2dcf10: cmp     r3, r2
0x2dcf14: movhs   r3, r2
0x2dcf18: str     r3, [sp, #0x20]
0x2dcf1c: cmp     r3, #0
0x2dcf20: ldrne   r3, [sp, #0x20]
0x2dcf24: beq     #0x2deb04
0x2dcf28: lsl     r0, r3, #4
0x2dcf2c: bl      #0x3e91f8
0x2dcf30: ldr     ip, [sp, #0x10]
0x2dcf34: ldr     ip, [ip, #0x14]
0x2dcf38: str     ip, [sp, #0x14]
0x2dcf3c: mov     ip, r0
0x2dcf40: str     r0, [sp, #0x1c]
0x2dcf44: add     r5, ip, r5, lsl #4
0x2dcf48: ldr     r3, [sp, #0x18]
0x2dcf4c: add     r2, r5, #0xc
0x2dcf50: mov     r1, #0
0x2dcf54: cmp     r5, #0
0x2dcf58: strne   r1, [r5]
0x2dcf5c: strne   r1, [r2, #-8]
0x2dcf60: add     r5, r5, #0x10
0x2dcf64: strne   r1, [r2, #-4]
0x2dcf68: strne   r1, [r2]
0x2dcf6c: subs    r3, r3, #1
0x2dcf70: add     r2, r2, #0x10
0x2dcf74: bne     #0x2dcf54
0x2dcf78: ldr     ip, [sp, #0xc]
0x2dcf7c: ldr     lr, [sp, #0x14]
0x2dcf80: cmp     ip, lr
0x2dcf84: beq     #0x2ded7c
0x2dcf88: ldr     ip, [sp, #0x1c]
0x2dcf8c: add     sl, lr, #4
0x2dcf90: mov     r8, lr
0x2dcf94: ldr     r7, [sp, #0x1c]
0x2dcf98: add     r5, ip, #0xc
0x2dcf9c: add     ip, ip, #4
0x2dcfa0: str     r4, [sp, #0x24]
0x2dcfa4: mov     r6, ip
0x2dcfa8: b       #0x2dcfd0
0x2dcfac: add     sb, sb, r6
0x2dcfb0: add     r4, r4, fp
0x2dcfb4: str     r4, [sb, #4]
0x2dcfb8: ldr     r3, [sp, #0xc]
0x2dcfbc: add     r8, r8, #0x10
0x2dcfc0: add     r7, r7, #0x10
0x2dcfc4: add     r5, r5, #0x10
0x2dcfc8: cmp     r3, r8
0x2dcfcc: beq     #0x2de934
0x2dcfd0: cmp     r7, #0
0x2dcfd4: beq     #0x2dcfb8
0x2dcfd8: ldr     r3, [sp, #0x14]
0x2dcfdc: mov     lr, #0
0x2dcfe0: ldr     r2, [r8]
0x2dcfe4: rsb     fp, r3, r8
0x2dcfe8: ldr     ip, [sp, #0x1c]
0x2dcfec: add     r3, fp, sl
0x2dcff0: str     r2, [r7]
0x2dcff4: rsb     sb, ip, r7
0x2dcff8: ldr     r0, [r3, #4]
0x2dcffc: ldr     r2, [fp, sl]
0x2dd000: mov     r1, sb
0x2dd004: str     lr, [r1, r6]!
0x2dd008: rsb     r2, r2, r0
0x2dd00c: str     lr, [r1, #4]
0x2dd010: str     lr, [r5]
0x2dd014: asrs    r2, r2, #4
0x2dd018: beq     #0x2de914
0x2dd01c: cmn     r2, #0xf0000001
0x2dd020: bhi     #0x2dee34
0x2dd024: lsl     r2, r2, #4
0x2dd028: str     r3, [sp]
0x2dd02c: str     r2, [sp, #4]
0x2dd030: mov     r0, r2
0x2dd034: bl      #0x3e91f8
0x2dd038: ldr     r2, [sp, #4]
0x2dd03c: ldr     r3, [sp]
0x2dd040: mov     r4, r0
0x2dd044: str     r4, [r5, #-8]
0x2dd048: add     r2, r4, r2
0x2dd04c: str     r4, [r5, #-4]
0x2dd050: str     r2, [r5]
0x2dd054: ldr     r1, [fp, sl]
0x2dd058: ldr     fp, [r3, #4]
0x2dd05c: rsb     fp, r1, fp
0x2dd060: asrs    fp, fp, #4
0x2dd064: beq     #0x2dcfac
0x2dd068: lsl     fp, fp, #4
0x2dd06c: mov     r0, r4
0x2dd070: mov     r2, fp
0x2dd074: bl      #0xa4ee8
0x2dd078: b       #0x2dcfac
0x2dd07c: blo     #0x2dd528
0x2dd080: ldr     r3, [sp, #8]
0x2dd084: cmp     r3, #0
0x2dd088: ble     #0x2dd178
0x2dd08c: mov     sb, #0
0x2dd090: mov     r8, sb
0x2dd094: ldr     ip, [sp, #0x10]
0x2dd098: mov     r0, r4
0x2dd09c: ldr     r5, [ip, #0x14]
0x2dd0a0: bl      #0x339914   ; <<READER i>>
0x2dd0a4: add     r7, r5, sb, lsl #4
0x2dd0a8: str     r0, [r5, sb, lsl #4]
0x2dd0ac: mov     r0, r4
0x2dd0b0: bl      #0x339914   ; <<READER i>>
0x2dd0b4: ldmib   r7, {r5, fp}
0x2dd0b8: rsb     r3, r5, fp
0x2dd0bc: asr     r3, r3, #4
0x2dd0c0: cmp     r0, r3
0x2dd0c4: mov     r6, r0
0x2dd0c8: mov     r0, r3
0x2dd0cc: bls     #0x2dd578
0x2dd0d0: subs    sl, r6, r3
0x2dd0d4: beq     #0x2dd114
0x2dd0d8: ldr     r2, [r7, #0xc]
0x2dd0dc: rsb     r2, fp, r2
0x2dd0e0: cmp     sl, r2, asr #4
0x2dd0e4: bhi     #0x2dd584
0x2dd0e8: add     r3, fp, #0x10
0x2dd0ec: mov     r2, sl
0x2dd0f0: subs    r2, r2, #1
0x2dd0f4: str     r8, [r3, #-0x10]
0x2dd0f8: str     r8, [r3, #-0xc]
0x2dd0fc: str     r8, [r3, #-8]
0x2dd100: str     r8, [r3, #-4]
0x2dd104: add     r3, r3, #0x10
0x2dd108: bne     #0x2dd0f0
0x2dd10c: add     sl, fp, sl, lsl #4
0x2dd110: str     sl, [r7, #8]
0x2dd114: cmp     r6, #0
0x2dd118: movgt   sl, #0
0x2dd11c: bgt     #0x2dd128
0x2dd120: b       #0x2dd168
0x2dd124: ldr     r5, [r7, #4]
0x2dd128: mov     r0, r4
0x2dd12c: add     fp, r5, sl, lsl #4
0x2dd130: bl      #0x339914   ; <<READER i>>
0x2dd134: str     r0, [r5, sl, lsl #4]
0x2dd138: mov     r0, r4
0x2dd13c: bl      #0x339914   ; <<READER i>>
0x2dd140: add     sl, sl, #1
0x2dd144: str     r0, [fp, #4]
0x2dd148: mov     r0, r4
0x2dd14c: bl      #0x339914   ; <<READER i>>
0x2dd150: str     r0, [fp, #8]
0x2dd154: mov     r0, r4
0x2dd158: bl      #0x339914   ; <<READER i>>
0x2dd15c: cmp     sl, r6
0x2dd160: str     r0, [fp, #0xc]
0x2dd164: bne     #0x2dd124
0x2dd168: ldr     r3, [sp, #8]
0x2dd16c: add     sb, sb, #1
0x2dd170: cmp     sb, r3
0x2dd174: bne     #0x2dd094
0x2dd178: mov     r0, r4
0x2dd17c: mov     fp, #0
0x2dd180: bl      #0x339914   ; <<READER i>>
0x2dd184: ldr     ip, [sp, #0x10]
0x2dd188: str     fp, [sp, #0x44]
0x2dd18c: str     fp, [sp, #0x48]
0x2dd190: ldr     r5, [ip, #0x24]
0x2dd194: ldr     r2, [ip, #0x20]
0x2dd198: str     fp, [sp, #0x4c]
0x2dd19c: rsb     r3, r2, r5
0x2dd1a0: asr     r3, r3, #2
0x2dd1a4: add     r6, r3, r3, lsl #2
0x2dd1a8: add     r6, r6, r6, lsl #4
0x2dd1ac: add     r6, r6, r6, lsl #8
0x2dd1b0: add     r6, r6, r6, lsl #16
0x2dd1b4: add     r6, r3, r6, lsl #1
0x2dd1b8: cmp     r0, r6
0x2dd1bc: str     r0, [sp, #0x14]
0x2dd1c0: bls     #0x2dd698
0x2dd1c4: subs    r2, r0, r6
0x2dd1c8: str     r2, [sp, #8]
0x2dd1cc: beq     #0x2dd738
0x2dd1d0: ldr     r3, [ip, #0x28]
0x2dd1d4: ldr     ip, [sp, #8]
0x2dd1d8: rsb     r3, r5, r3
0x2dd1dc: asr     r3, r3, #2
0x2dd1e0: add     r2, r3, r3, lsl #2
0x2dd1e4: add     r2, r2, r2, lsl #4
0x2dd1e8: add     r2, r2, r2, lsl #8
0x2dd1ec: add     r2, r2, r2, lsl #16
0x2dd1f0: add     r3, r3, r2, lsl #1
0x2dd1f4: cmp     ip, r3
0x2dd1f8: bls     #0x2deb20
0x2dd1fc: movw    r3, #0x5555
0x2dd200: movt    r3, #0x1555
0x2dd204: rsb     r3, r6, r3
0x2dd208: movw    r2, #0x5555
0x2dd20c: cmp     ip, r3
0x2dd210: movt    r2, #0x1555
0x2dd214: bhi     #0x2dee50
0x2dd218: cmp     ip, r6
0x2dd21c: addhs   r3, r6, ip
0x2dd220: addlo   r3, r6, r6
0x2dd224: cmp     r6, r3
0x2dd228: strhi   r2, [sp, #0xc]
0x2dd22c: bhi     #0x2dd248
0x2dd230: cmp     r3, r2
0x2dd234: movhs   r3, r2
0x2dd238: str     r3, [sp, #0xc]
0x2dd23c: cmp     r3, #0
0x2dd240: ldrne   r2, [sp, #0xc]
0x2dd244: beq     #0x2deaf8
0x2dd248: add     r0, r2, r2, lsl #1
0x2dd24c: lsl     r0, r0, #2
0x2dd250: bl      #0x3e91f8
0x2dd254: mov     ip, r0
0x2dd258: str     r0, [sp, #0x1c]
0x2dd25c: add     r6, r6, r6, lsl #1
0x2dd260: ldr     fp, [sp, #8]
0x2dd264: mov     sb, #0
0x2dd268: add     sl, ip, r6, lsl #2
0x2dd26c: cmp     sl, #0
0x2dd270: beq     #0x2dd308
0x2dd274: ldr     r7, [sp, #0x48]
0x2dd278: ldr     r3, [sp, #0x44]
0x2dd27c: str     sb, [sl]
0x2dd280: rsb     r7, r3, r7
0x2dd284: str     sb, [sl, #4]
0x2dd288: str     sb, [sl, #8]
0x2dd28c: asrs    r7, r7, #4
0x2dd290: beq     #0x2de92c
0x2dd294: cmn     r7, #0xf0000001
0x2dd298: bhi     #0x2dee34
0x2dd29c: lsl     r7, r7, #4
0x2dd2a0: mov     r0, r7
0x2dd2a4: bl      #0x3e91f8
0x2dd2a8: mov     r6, r0
0x2dd2ac: str     r6, [sl]
0x2dd2b0: add     r7, r6, r7
0x2dd2b4: stmib   sl, {r6, r7}
0x2dd2b8: ldr     r7, [sp, #0x44]
0x2dd2bc: ldr     r8, [sp, #0x48]
0x2dd2c0: cmp     r7, r8
0x2dd2c4: beq     #0x2dd304
0x2dd2c8: cmp     r6, #0
0x2dd2cc: beq     #0x2dd2f4
0x2dd2d0: ldr     r3, [r7]
0x2dd2d4: add     r0, r6, #8
0x2dd2d8: add     r1, r7, #8
0x2dd2dc: str     r3, [r6]
0x2dd2e0: ldr     r3, [r7, #4]
0x2dd2e4: str     r3, [r6, #4]
0x2dd2e8: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd2ec: ldrb    r3, [r7, #0xc]
0x2dd2f0: strb    r3, [r6, #0xc]
0x2dd2f4: add     r7, r7, #0x10
0x2dd2f8: add     r6, r6, #0x10
0x2dd2fc: cmp     r8, r7
0x2dd300: bne     #0x2dd2c8
0x2dd304: str     r6, [sl, #4]
0x2dd308: subs    fp, fp, #1
0x2dd30c: add     sl, sl, #0xc
0x2dd310: bne     #0x2dd26c
0x2dd314: ldr     ip, [sp, #0x10]
0x2dd318: ldr     sl, [sp, #0x1c]
0x2dd31c: ldr     sb, [ip, #0x20]
0x2dd320: cmp     r5, sb
0x2dd324: beq     #0x2dd3cc
0x2dd328: cmp     sl, #0
0x2dd32c: beq     #0x2dd3bc
0x2dd330: ldm     sb, {r3, r7}
0x2dd334: str     fp, [sl]
0x2dd338: rsb     r7, r3, r7
0x2dd33c: str     fp, [sl, #4]
0x2dd340: str     fp, [sl, #8]
0x2dd344: asrs    r7, r7, #4
0x2dd348: beq     #0x2de924
0x2dd34c: cmn     r7, #0xf0000001
0x2dd350: bhi     #0x2dee34
0x2dd354: lsl     r7, r7, #4
0x2dd358: mov     r0, r7
0x2dd35c: bl      #0x3e91f8
0x2dd360: mov     r6, r0
0x2dd364: add     r7, r6, r7
0x2dd368: str     r6, [sl]
0x2dd36c: stmib   sl, {r6, r7}
0x2dd370: ldm     sb, {r7, r8}
0x2dd374: cmp     r7, r8
0x2dd378: beq     #0x2dd3b8
0x2dd37c: cmp     r6, #0
0x2dd380: beq     #0x2dd3a8
0x2dd384: ldr     r3, [r7]
0x2dd388: add     r0, r6, #8
0x2dd38c: add     r1, r7, #8
0x2dd390: str     r3, [r6]
0x2dd394: ldr     r3, [r7, #4]
0x2dd398: str     r3, [r6, #4]
0x2dd39c: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd3a0: ldrb    r3, [r7, #0xc]
0x2dd3a4: strb    r3, [r6, #0xc]
0x2dd3a8: add     r7, r7, #0x10
0x2dd3ac: add     r6, r6, #0x10
0x2dd3b0: cmp     r8, r7
0x2dd3b4: bne     #0x2dd37c
0x2dd3b8: str     r6, [sl, #4]
0x2dd3bc: add     sb, sb, #0xc
0x2dd3c0: add     sl, sl, #0xc
0x2dd3c4: cmp     r5, sb
0x2dd3c8: bne     #0x2dd328
0x2dd3cc: ldr     ip, [sp, #0x10]
0x2dd3d0: ldr     r2, [sp, #8]
0x2dd3d4: ldr     fp, [ip, #0x24]
0x2dd3d8: add     r3, r2, r2, lsl #1
0x2dd3dc: cmp     r5, fp
0x2dd3e0: add     sl, sl, r3, lsl #2
0x2dd3e4: beq     #0x2dd498
0x2dd3e8: mov     sb, #0
0x2dd3ec: cmp     sl, #0
0x2dd3f0: beq     #0x2dd480
0x2dd3f4: ldm     r5, {r3, r7}
0x2dd3f8: str     sb, [sl]
0x2dd3fc: rsb     r7, r3, r7
0x2dd400: str     sb, [sl, #4]
0x2dd404: str     sb, [sl, #8]
0x2dd408: asrs    r7, r7, #4
0x2dd40c: beq     #0x2de91c
0x2dd410: cmn     r7, #0xf0000001
0x2dd414: bhi     #0x2dee34
0x2dd418: lsl     r7, r7, #4
0x2dd41c: mov     r0, r7
0x2dd420: bl      #0x3e91f8
0x2dd424: mov     r6, r0
0x2dd428: add     r7, r6, r7
0x2dd42c: str     r6, [sl]
0x2dd430: stmib   sl, {r6, r7}
0x2dd434: ldm     r5, {r7, r8}
0x2dd438: cmp     r7, r8
0x2dd43c: beq     #0x2dd47c
0x2dd440: cmp     r6, #0
0x2dd444: beq     #0x2dd46c
0x2dd448: ldr     r3, [r7]
0x2dd44c: add     r0, r6, #8
0x2dd450: add     r1, r7, #8
0x2dd454: str     r3, [r6]
0x2dd458: ldr     r3, [r7, #4]
0x2dd45c: str     r3, [r6, #4]
0x2dd460: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd464: ldrb    r3, [r7, #0xc]
0x2dd468: strb    r3, [r6, #0xc]
0x2dd46c: add     r7, r7, #0x10
0x2dd470: add     r6, r6, #0x10
0x2dd474: cmp     r8, r7
0x2dd478: bne     #0x2dd440
0x2dd47c: str     r6, [sl, #4]
0x2dd480: add     r5, r5, #0xc
0x2dd484: add     sl, sl, #0xc
0x2dd488: cmp     fp, r5
0x2dd48c: bne     #0x2dd3ec
0x2dd490: ldr     ip, [sp, #0x10]
0x2dd494: ldr     fp, [ip, #0x24]
0x2dd498: ldr     r7, [ip, #0x20]
0x2dd49c: cmp     fp, r7
0x2dd4a0: beq     #0x2dd4ec
0x2dd4a4: ldm     r7, {r5, r6}
0x2dd4a8: cmp     r5, r6
0x2dd4ac: beq     #0x2dd4c8
0x2dd4b0: add     r0, r5, #8
0x2dd4b4: add     r5, r5, #0x10
0x2dd4b8: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd4bc: cmp     r6, r5
0x2dd4c0: bne     #0x2dd4b0
0x2dd4c4: ldr     r5, [r7]
0x2dd4c8: cmp     r5, #0
0x2dd4cc: beq     #0x2dd4d8
0x2dd4d0: mov     r0, r5
0x2dd4d4: bl      #0x3e9260
0x2dd4d8: add     r7, r7, #0xc
0x2dd4dc: cmp     fp, r7
0x2dd4e0: bne     #0x2dd4a4
0x2dd4e4: ldr     ip, [sp, #0x10]
0x2dd4e8: ldr     r7, [ip, #0x20]
0x2dd4ec: cmp     r7, #0
0x2dd4f0: beq     #0x2dd4fc
0x2dd4f4: mov     r0, r7
0x2dd4f8: bl      #0x3e9260
0x2dd4fc: ldr     r2, [sp, #0xc]
0x2dd500: ldr     lr, [sp, #0x10]
0x2dd504: ldr     ip, [sp, #0x1c]
0x2dd508: add     r3, r2, r2, lsl #1
0x2dd50c: ldr     r5, [sp, #0x44]
0x2dd510: str     sl, [lr, #0x24]
0x2dd514: add     r3, ip, r3, lsl #2
0x2dd518: str     ip, [lr, #0x20]
0x2dd51c: str     r3, [lr, #0x28]
0x2dd520: ldr     fp, [sp, #0x48]
0x2dd524: b       #0x2dd708
0x2dd528: ldr     ip, [sp, #8]
0x2dd52c: ldr     r3, [sp, #0x14]
0x2dd530: add     r6, r3, ip, lsl #4
0x2dd534: ldr     r3, [sp, #0xc]
0x2dd538: cmp     r3, r6
0x2dd53c: beq     #0x2dd56c
0x2dd540: add     r7, r6, #4
0x2dd544: mov     r5, r6
0x2dd548: mov     r8, r3
0x2dd54c: rsb     r3, r6, r5
0x2dd550: ldr     r0, [r7, r3]
0x2dd554: cmp     r0, #0
0x2dd558: beq     #0x2dd560
0x2dd55c: bl      #0x3e9260
0x2dd560: add     r5, r5, #0x10
0x2dd564: cmp     r8, r5
0x2dd568: bne     #0x2dd54c
0x2dd56c: ldr     ip, [sp, #0x10]
0x2dd570: str     r6, [ip, #0x18]
0x2dd574: b       #0x2dd080
0x2dd578: addlo   r3, r5, r6, lsl #4
0x2dd57c: strlo   r3, [r7, #8]
0x2dd580: b       #0x2dd114
0x2dd584: movw    r2, #0xffff
0x2dd588: movt    r2, #0xfff
0x2dd58c: rsb     r2, r3, r2
0x2dd590: cmp     sl, r2
0x2dd594: bhi     #0x2dee68
0x2dd598: cmp     sl, r3
0x2dd59c: addhs   r2, r3, sl
0x2dd5a0: addlo   r2, r3, r3
0x2dd5a4: cmp     r3, r2
0x2dd5a8: mvnhi   ip, #0xf
0x2dd5ac: strhi   ip, [sp, #0xc]
0x2dd5b0: bhi     #0x2dd5d0
0x2dd5b4: mvn     lr, #0xf0000000
0x2dd5b8: cmp     r2, lr
0x2dd5bc: movhs   r2, lr
0x2dd5c0: cmp     r2, #0
0x2dd5c4: lsl     ip, r2, #4
0x2dd5c8: str     ip, [sp, #0xc]
0x2dd5cc: beq     #0x2deaec
0x2dd5d0: ldr     r0, [sp, #0xc]
0x2dd5d4: str     r3, [sp]
0x2dd5d8: bl      #0x3e91f8
0x2dd5dc: ldr     r1, [r7, #4]
0x2dd5e0: ldr     r3, [sp]
0x2dd5e4: mov     r5, r0
0x2dd5e8: rsb     r0, r1, fp
0x2dd5ec: asr     r0, r0, #4
0x2dd5f0: add     r3, r5, r3, lsl #4
0x2dd5f4: mov     ip, sl
0x2dd5f8: add     r2, r3, #0x10
0x2dd5fc: subs    ip, ip, #1
0x2dd600: str     r8, [r2, #-0x10]
0x2dd604: str     r8, [r2, #-0xc]
0x2dd608: str     r8, [r2, #-8]
0x2dd60c: str     r8, [r2, #-4]
0x2dd610: add     r2, r2, #0x10
0x2dd614: bne     #0x2dd5fc
0x2dd618: cmp     r0, #0
0x2dd61c: moveq   r3, r0
0x2dd620: beq     #0x2dd63c
0x2dd624: lsl     r3, r0, #4
0x2dd628: mov     r0, r5
0x2dd62c: str     r3, [sp]
0x2dd630: mov     r2, r3
0x2dd634: bl      #0xa4ee8
0x2dd638: ldr     r3, [sp]
0x2dd63c: ldr     r2, [r7, #8]
0x2dd640: add     r3, r5, r3
0x2dd644: add     r3, r3, sl, lsl #4
0x2dd648: rsb     r2, fp, r2
0x2dd64c: asrs    sl, r2, #4
0x2dd650: beq     #0x2dd670
0x2dd654: lsl     sl, sl, #4
0x2dd658: mov     r0, r3
0x2dd65c: mov     r1, fp
0x2dd660: str     r3, [sp]
0x2dd664: mov     r2, sl
0x2dd668: bl      #0xa4ee8
0x2dd66c: ldr     r3, [sp]
0x2dd670: ldr     r0, [r7, #4]
0x2dd674: add     sl, r3, sl
0x2dd678: cmp     r0, #0
0x2dd67c: beq     #0x2dd684
0x2dd680: bl      #0x3e9260
0x2dd684: ldr     ip, [sp, #0xc]
0x2dd688: stmib   r7, {r5, sl}
0x2dd68c: add     r3, r5, ip
0x2dd690: str     r3, [r7, #0xc]
0x2dd694: b       #0x2dd114
0x2dd698: bhs     #0x2dd738
0x2dd69c: ldr     r3, [sp, #0x14]
0x2dd6a0: add     sl, r3, r3, lsl #1
0x2dd6a4: add     sl, r2, sl, lsl #2
0x2dd6a8: cmp     r5, sl
0x2dd6ac: moveq   r5, fp
0x2dd6b0: beq     #0x2dd700
0x2dd6b4: mov     r8, sl
0x2dd6b8: ldm     r8, {r6, r7}
0x2dd6bc: cmp     r6, r7
0x2dd6c0: beq     #0x2dd6dc
0x2dd6c4: add     r0, r6, #8
0x2dd6c8: add     r6, r6, #0x10
0x2dd6cc: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd6d0: cmp     r7, r6
0x2dd6d4: bne     #0x2dd6c4
0x2dd6d8: ldr     r6, [r8]
0x2dd6dc: cmp     r6, #0
0x2dd6e0: beq     #0x2dd6ec
0x2dd6e4: mov     r0, r6
0x2dd6e8: bl      #0x3e9260
0x2dd6ec: add     r8, r8, #0xc
0x2dd6f0: cmp     r5, r8
0x2dd6f4: bne     #0x2dd6b8
0x2dd6f8: ldr     r5, [sp, #0x44]
0x2dd6fc: ldr     fp, [sp, #0x48]
0x2dd700: ldr     ip, [sp, #0x10]
0x2dd704: str     sl, [ip, #0x24]
0x2dd708: cmp     fp, r5
0x2dd70c: beq     #0x2dd728
0x2dd710: add     r0, r5, #8
0x2dd714: add     r5, r5, #0x10
0x2dd718: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd71c: cmp     r5, fp
0x2dd720: bne     #0x2dd710
0x2dd724: ldr     r5, [sp, #0x44]
0x2dd728: cmp     r5, #0
0x2dd72c: beq     #0x2dd738
0x2dd730: mov     r0, r5
0x2dd734: bl      #0x3e9260
0x2dd738: ldr     r3, [sp, #0x14]
0x2dd73c: cmp     r3, #0
0x2dd740: ble     #0x2deb10
0x2dd744: ldr     ip, [pc, #0xf7c]   ; pool[0x2de6c8]=0x92a564
0x2dd748: mov     r8, #0
0x2dd74c: str     r8, [sp, #8]
0x2dd750: ldr     ip, [pc, ip]
0x2dd754: str     ip, [sp, #0x24]
0x2dd758: add     r2, ip, #0xc
0x2dd75c: str     r2, [sp, #0x1c]
0x2dd760: ldr     ip, [sp, #0x10]
0x2dd764: mov     r0, r4
0x2dd768: ldr     r7, [ip, #0x20]
0x2dd76c: bl      #0x339914   ; <<READER i>>
0x2dd770: ldr     r2, [sp, #0x1c]
0x2dd774: mov     lr, #0
0x2dd778: add     r5, r7, r8
0x2dd77c: str     lr, [sp, #0x90]
0x2dd780: ldr     r3, [r7, r8]
0x2dd784: ldr     r7, [r5, #4]
0x2dd788: str     lr, [sp, #0x94]
0x2dd78c: rsb     sb, r3, r7
0x2dd790: strb    lr, [sp, #0x9c]
0x2dd794: str     r2, [sp, #0x98]
0x2dd798: asr     sb, sb, #4
0x2dd79c: cmp     r0, sb
0x2dd7a0: mov     r6, r0
0x2dd7a4: bls     #0x2ddfa0
0x2dd7a8: subs    r3, r0, sb
0x2dd7ac: str     r3, [sp, #0xc]
0x2dd7b0: beq     #0x2ddf90
0x2dd7b4: mov     ip, r3
0x2dd7b8: ldr     r3, [r5, #8]
0x2dd7bc: rsb     r3, r7, r3
0x2dd7c0: cmp     ip, r3, asr #4
0x2dd7c4: bls     #0x2de440
0x2dd7c8: movw    r3, #0xffff
0x2dd7cc: movt    r3, #0xfff
0x2dd7d0: rsb     r3, sb, r3
0x2dd7d4: cmp     ip, r3
0x2dd7d8: bhi     #0x2dee5c
0x2dd7dc: cmp     ip, sb
0x2dd7e0: addhs   r3, sb, ip
0x2dd7e4: addlo   r3, sb, sb
0x2dd7e8: cmp     sb, r3
0x2dd7ec: mvnhi   r3, #0xf
0x2dd7f0: strhi   r3, [sp, #0x20]
0x2dd7f4: bhi     #0x2dd814
0x2dd7f8: mvn     lr, #0xf0000000
0x2dd7fc: cmp     r3, lr
0x2dd800: movhs   r3, lr
0x2dd804: cmp     r3, #0
0x2dd808: lsl     r2, r3, #4
0x2dd80c: str     r2, [sp, #0x20]
0x2dd810: beq     #0x2de8fc
0x2dd814: ldr     r0, [sp, #0x20]
0x2dd818: bl      #0x3e91f8
0x2dd81c: mov     ip, r0
0x2dd820: str     r0, [sp, #0x18]
0x2dd824: ldr     fp, [sp, #0xc]
0x2dd828: add     sb, ip, sb, lsl #4
0x2dd82c: add     sl, sp, #0x98
0x2dd830: cmp     sb, #0
0x2dd834: beq     #0x2dd85c
0x2dd838: ldr     r3, [sp, #0x90]
0x2dd83c: add     r0, sb, #8
0x2dd840: mov     r1, sl
0x2dd844: str     r3, [sb]
0x2dd848: ldr     r3, [sp, #0x94]
0x2dd84c: str     r3, [sb, #4]
0x2dd850: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd854: ldrb    r3, [sp, #0x9c]
0x2dd858: strb    r3, [sb, #0xc]
0x2dd85c: subs    fp, fp, #1
0x2dd860: add     sb, sb, #0x10
0x2dd864: bne     #0x2dd830
0x2dd868: ldr     fp, [r5]
0x2dd86c: ldr     sb, [sp, #0x18]
0x2dd870: cmp     r7, fp
0x2dd874: beq     #0x2dd8b4
0x2dd878: cmp     sb, #0
0x2dd87c: beq     #0x2dd8a4
0x2dd880: ldr     r3, [fp]
0x2dd884: add     r0, sb, #8
0x2dd888: add     r1, fp, #8
0x2dd88c: str     r3, [sb]
0x2dd890: ldr     r3, [fp, #4]
0x2dd894: str     r3, [sb, #4]
0x2dd898: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd89c: ldrb    r3, [fp, #0xc]
0x2dd8a0: strb    r3, [sb, #0xc]
0x2dd8a4: add     fp, fp, #0x10
0x2dd8a8: add     sb, sb, #0x10
0x2dd8ac: cmp     r7, fp
0x2dd8b0: bne     #0x2dd878
0x2dd8b4: ldr     fp, [r5, #4]
0x2dd8b8: ldr     r2, [sp, #0xc]
0x2dd8bc: cmp     r7, fp
0x2dd8c0: add     sb, sb, r2, lsl #4
0x2dd8c4: beq     #0x2dd908
0x2dd8c8: cmp     sb, #0
0x2dd8cc: beq     #0x2dd8f4
0x2dd8d0: ldr     r3, [r7]
0x2dd8d4: add     r0, sb, #8
0x2dd8d8: add     r1, r7, #8
0x2dd8dc: str     r3, [sb]
0x2dd8e0: ldr     r3, [r7, #4]
0x2dd8e4: str     r3, [sb, #4]
0x2dd8e8: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd8ec: ldrb    r3, [r7, #0xc]
0x2dd8f0: strb    r3, [sb, #0xc]
0x2dd8f4: add     r7, r7, #0x10
0x2dd8f8: add     sb, sb, #0x10
0x2dd8fc: cmp     fp, r7
0x2dd900: bne     #0x2dd8c8
0x2dd904: ldr     fp, [r5, #4]
0x2dd908: ldr     r7, [r5]
0x2dd90c: cmp     fp, r7
0x2dd910: beq     #0x2dd92c
0x2dd914: add     r0, r7, #8
0x2dd918: add     r7, r7, #0x10
0x2dd91c: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd920: cmp     fp, r7
0x2dd924: bne     #0x2dd914
0x2dd928: ldr     r7, [r5]
0x2dd92c: cmp     r7, #0
0x2dd930: beq     #0x2dd93c
0x2dd934: mov     r0, r7
0x2dd938: bl      #0x3e9260
0x2dd93c: ldr     ip, [sp, #0x18]
0x2dd940: ldr     r2, [sp, #0x20]
0x2dd944: str     sb, [r5, #4]
0x2dd948: add     r3, ip, r2
0x2dd94c: str     ip, [r5]
0x2dd950: str     r3, [r5, #8]
0x2dd954: mov     r0, sl
0x2dd958: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dd95c: cmp     r6, #0
0x2dd960: ble     #0x2dd9b4
0x2dd964: mov     r7, #0
0x2dd968: mov     r0, r4
0x2dd96c: ldr     sb, [r5]
0x2dd970: bl      #0x339914   ; <<READER i>>
0x2dd974: add     sl, sb, r7, lsl #4
0x2dd978: str     r0, [sb, r7, lsl #4]
0x2dd97c: mov     r0, r4
0x2dd980: bl      #0x339914   ; <<READER i>>
0x2dd984: add     r1, sl, #8
0x2dd988: add     r7, r7, #1
0x2dd98c: str     r0, [sl, #4]
0x2dd990: mov     r0, r4
0x2dd994: bl      #0x33a0d4   ; <<READER STR>>
0x2dd998: mov     r0, r4
0x2dd99c: bl      #0x3395d8   ; <<READER c>>
0x2dd9a0: adds    r0, r0, #0
0x2dd9a4: movne   r0, #1
0x2dd9a8: cmp     r7, r6
0x2dd9ac: strb    r0, [sl, #0xc]
0x2dd9b0: bne     #0x2dd968
0x2dd9b4: ldr     r3, [sp, #8]
0x2dd9b8: add     r8, r8, #0xc
0x2dd9bc: ldr     ip, [sp, #0x14]
0x2dd9c0: add     r3, r3, #1
0x2dd9c4: str     r3, [sp, #8]
0x2dd9c8: cmp     r3, ip
0x2dd9cc: bne     #0x2dd760
0x2dd9d0: mov     r0, r4
0x2dd9d4: mov     r6, #0
0x2dd9d8: bl      #0x339914   ; <<READER i>>
0x2dd9dc: ldr     ip, [sp, #0x10]
0x2dd9e0: str     r6, [sp, #0x50]
0x2dd9e4: str     r6, [sp, #0x54]
0x2dd9e8: ldr     sl, [ip, #0x30]
0x2dd9ec: ldr     r1, [ip, #0x2c]
0x2dd9f0: str     r6, [sp, #0x58]
0x2dd9f4: rsb     r3, r1, sl
0x2dd9f8: asr     r3, r3, #2
0x2dd9fc: add     r2, r3, r3, lsl #2
0x2dda00: add     r2, r2, r2, lsl #4
0x2dda04: add     r2, r2, r2, lsl #8
0x2dda08: add     r2, r2, r2, lsl #16
0x2dda0c: add     r2, r3, r2, lsl #1
0x2dda10: cmp     r0, r2
0x2dda14: str     r0, [sp, #0x14]
0x2dda18: bls     #0x2de654
0x2dda1c: add     r0, ip, #0x2c
0x2dda20: ldr     ip, [sp, #0x14]
0x2dda24: mov     r1, sl
0x2dda28: add     r3, sp, #0x50
0x2dda2c: rsb     r2, r2, ip
0x2dda30: bl      #0x2d391c
0x2dda34: ldr     r5, [sp, #0x50]
0x2dda38: ldr     r6, [sp, #0x54]
0x2dda3c: cmp     r5, r6
0x2dda40: beq     #0x2dda5c
0x2dda44: add     r0, r5, #8
0x2dda48: add     r5, r5, #0xc
0x2dda4c: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2dda50: cmp     r5, r6
0x2dda54: bne     #0x2dda44
0x2dda58: ldr     r5, [sp, #0x50]
0x2dda5c: cmp     r5, #0
0x2dda60: beq     #0x2dda6c
0x2dda64: mov     r0, r5
0x2dda68: bl      #0x3e9260
0x2dda6c: ldr     ip, [sp, #0x14]
0x2dda70: cmp     ip, #0
0x2dda74: ble     #0x2ddd1c
0x2dda78: ldr     r3, [sp, #0x24]
0x2dda7c: mov     sb, #0
0x2dda80: movw    r2, #0x5555
0x2dda84: str     sb, [sp, #8]
0x2dda88: add     r3, r3, #0xc
0x2dda8c: movt    r2, #0x1555
0x2dda90: str     r3, [sp, #0x1c]
0x2dda94: str     r2, [sp, #0x28]
0x2dda98: ldr     ip, [sp, #0x10]
0x2dda9c: mov     r0, r4
0x2ddaa0: ldr     r7, [ip, #0x2c]
0x2ddaa4: bl      #0x339914   ; <<READER i>>
0x2ddaa8: ldr     ip, [sp, #0x1c]
0x2ddaac: mov     lr, #0
0x2ddab0: add     r5, r7, sb
0x2ddab4: str     lr, [sp, #0x5c]
0x2ddab8: ldr     r2, [r7, sb]
0x2ddabc: ldr     sl, [r5, #4]
0x2ddac0: str     lr, [sp, #0x60]
0x2ddac4: rsb     r3, r2, sl
0x2ddac8: str     ip, [sp, #0x64]
0x2ddacc: asr     r3, r3, #2
0x2ddad0: add     r7, r3, r3, lsl #2
0x2ddad4: add     r7, r7, r7, lsl #4
0x2ddad8: add     r7, r7, r7, lsl #8
0x2ddadc: add     r7, r7, r7, lsl #16
0x2ddae0: add     r7, r3, r7, lsl #1
0x2ddae4: cmp     r0, r7
0x2ddae8: mov     r6, r0
0x2ddaec: bls     #0x2ddfd4
0x2ddaf0: subs    r2, r0, r7
0x2ddaf4: str     r2, [sp, #0xc]
0x2ddaf8: beq     #0x2ddf98
0x2ddafc: ldr     r3, [r5, #8]
0x2ddb00: rsb     r3, sl, r3
0x2ddb04: asr     r3, r3, #2
0x2ddb08: add     r2, r3, r3, lsl #2
0x2ddb0c: add     r2, r2, r2, lsl #4
0x2ddb10: add     r2, r2, r2, lsl #8
0x2ddb14: add     r2, r2, r2, lsl #16
0x2ddb18: add     r2, r3, r2, lsl #1
0x2ddb1c: ldr     r3, [sp, #0xc]
0x2ddb20: cmp     r3, r2
0x2ddb24: bls     #0x2de274
0x2ddb28: mov     r2, r3
0x2ddb2c: movw    r3, #0x5555
0x2ddb30: movt    r3, #0x1555
0x2ddb34: rsb     r3, r7, r3
0x2ddb38: cmp     r2, r3
0x2ddb3c: bhi     #0x2dee38
0x2ddb40: cmp     r2, r7
0x2ddb44: addhs   r3, r7, r2
0x2ddb48: addlo   r3, r7, r7
0x2ddb4c: cmp     r7, r3
0x2ddb50: mvnhi   r3, #3
0x2ddb54: strhi   r3, [sp, #0x20]
0x2ddb58: bhi     #0x2ddb7c
0x2ddb5c: ldr     r2, [sp, #0x28]
0x2ddb60: cmp     r3, r2
0x2ddb64: movhs   r3, r2
0x2ddb68: cmp     r3, #0
0x2ddb6c: add     r2, r3, r3, lsl #1
0x2ddb70: lsl     r2, r2, #2
0x2ddb74: str     r2, [sp, #0x20]
0x2ddb78: beq     #0x2de908
0x2ddb7c: ldr     r0, [sp, #0x20]
0x2ddb80: bl      #0x3e91f8
0x2ddb84: mov     ip, r0
0x2ddb88: str     r0, [sp, #0x18]
0x2ddb8c: add     r7, r7, r7, lsl #1
0x2ddb90: ldr     r8, [sp, #0xc]
0x2ddb94: add     fp, sp, #0x64
0x2ddb98: add     r7, ip, r7, lsl #2
0x2ddb9c: cmp     r7, #0
0x2ddba0: beq     #0x2ddbc0
0x2ddba4: ldr     r3, [sp, #0x5c]
0x2ddba8: add     r0, r7, #8
0x2ddbac: mov     r1, fp
0x2ddbb0: str     r3, [r7]
0x2ddbb4: ldr     r3, [sp, #0x60]
0x2ddbb8: str     r3, [r7, #4]
0x2ddbbc: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddbc0: subs    r8, r8, #1
0x2ddbc4: add     r7, r7, #0xc
0x2ddbc8: bne     #0x2ddb9c
0x2ddbcc: ldr     r7, [r5]
0x2ddbd0: ldr     r8, [sp, #0x18]
0x2ddbd4: cmp     sl, r7
0x2ddbd8: beq     #0x2ddc10
0x2ddbdc: cmp     r8, #0
0x2ddbe0: beq     #0x2ddc00
0x2ddbe4: ldr     r3, [r7]
0x2ddbe8: add     r0, r8, #8
0x2ddbec: add     r1, r7, #8
0x2ddbf0: str     r3, [r8]
0x2ddbf4: ldr     r3, [r7, #4]
0x2ddbf8: str     r3, [r8, #4]
0x2ddbfc: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddc00: add     r7, r7, #0xc
0x2ddc04: add     r8, r8, #0xc
0x2ddc08: cmp     sl, r7
0x2ddc0c: bne     #0x2ddbdc
0x2ddc10: ldr     r2, [sp, #0xc]
0x2ddc14: ldr     r7, [r5, #4]
0x2ddc18: add     r3, r2, r2, lsl #1
0x2ddc1c: cmp     sl, r7
0x2ddc20: add     r8, r8, r3, lsl #2
0x2ddc24: beq     #0x2ddc60
0x2ddc28: cmp     r8, #0
0x2ddc2c: beq     #0x2ddc4c
0x2ddc30: ldr     r3, [sl]
0x2ddc34: add     r0, r8, #8
0x2ddc38: add     r1, sl, #8
0x2ddc3c: str     r3, [r8]
0x2ddc40: ldr     r3, [sl, #4]
0x2ddc44: str     r3, [r8, #4]
0x2ddc48: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddc4c: add     sl, sl, #0xc
0x2ddc50: add     r8, r8, #0xc
0x2ddc54: cmp     r7, sl
0x2ddc58: bne     #0x2ddc28
0x2ddc5c: ldr     r7, [r5, #4]
0x2ddc60: ldr     sl, [r5]
0x2ddc64: cmp     sl, r7
0x2ddc68: beq     #0x2ddc84
0x2ddc6c: add     r0, sl, #8
0x2ddc70: add     sl, sl, #0xc
0x2ddc74: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddc78: cmp     sl, r7
0x2ddc7c: bne     #0x2ddc6c
0x2ddc80: ldr     sl, [r5]
0x2ddc84: cmp     sl, #0
0x2ddc88: beq     #0x2ddc94
0x2ddc8c: mov     r0, sl
0x2ddc90: bl      #0x3e9260
0x2ddc94: ldr     ip, [sp, #0x18]
0x2ddc98: ldr     r2, [sp, #0x20]
0x2ddc9c: str     r8, [r5, #4]
0x2ddca0: add     r3, ip, r2
0x2ddca4: str     ip, [r5]
0x2ddca8: str     r3, [r5, #8]
0x2ddcac: mov     r0, fp
0x2ddcb0: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddcb4: cmp     r6, #0
0x2ddcb8: ble     #0x2ddd00
0x2ddcbc: mov     r7, #0
0x2ddcc0: mov     r8, r7
0x2ddcc4: mov     r0, r4
0x2ddcc8: ldr     fp, [r5]
0x2ddccc: bl      #0x339914   ; <<READER i>>
0x2ddcd0: add     r8, r8, #1
0x2ddcd4: add     sl, fp, r7
0x2ddcd8: str     r0, [fp, r7]
0x2ddcdc: mov     r0, r4
0x2ddce0: bl      #0x339914   ; <<READER i>>
0x2ddce4: add     r1, sl, #8
0x2ddce8: add     r7, r7, #0xc
0x2ddcec: str     r0, [sl, #4]
0x2ddcf0: mov     r0, r4
0x2ddcf4: bl      #0x33a0d4   ; <<READER STR>>
0x2ddcf8: cmp     r8, r6
0x2ddcfc: bne     #0x2ddcc4
0x2ddd00: ldr     r3, [sp, #8]
0x2ddd04: add     sb, sb, #0xc
0x2ddd08: ldr     ip, [sp, #0x14]
0x2ddd0c: add     r3, r3, #1
0x2ddd10: str     r3, [sp, #8]
0x2ddd14: cmp     r3, ip
0x2ddd18: bne     #0x2dda98
0x2ddd1c: mov     r0, r4
0x2ddd20: bl      #0x339914   ; <<READER i>>
0x2ddd24: ldr     ip, [sp, #0x10]
0x2ddd28: mov     r3, #0
0x2ddd2c: str     r3, [sp, #0x84]
0x2ddd30: str     r3, [sp, #0x88]
0x2ddd34: ldr     r6, [ip, #0x3c]
0x2ddd38: ldr     r7, [ip, #0x38]
0x2ddd3c: ldr     ip, [sp, #0x24]
0x2ddd40: rsb     r2, r7, r6
0x2ddd44: str     r3, [sp, #0x8c]
0x2ddd48: add     r1, ip, #0xc
0x2ddd4c: str     r1, [sp, #0x80]
0x2ddd50: asr     r2, r2, #4
0x2ddd54: cmp     r0, r2
0x2ddd58: str     r0, [sp, #0xc]
0x2ddd5c: bls     #0x2de5f4
0x2ddd60: ldr     ip, [sp, #0x10]
0x2ddd64: add     r5, sp, #0x80
0x2ddd68: mov     r1, r6
0x2ddd6c: add     r0, ip, #0x38
0x2ddd70: ldr     ip, [sp, #0xc]
0x2ddd74: mov     r3, r5
0x2ddd78: rsb     r2, r2, ip
0x2ddd7c: bl      #0x2d4000
0x2ddd80: ldr     r0, [sp, #0x84]
0x2ddd84: cmp     r0, #0
0x2ddd88: beq     #0x2ddd90
0x2ddd8c: bl      #0x3e9260
0x2ddd90: mov     r0, r5
0x2ddd94: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddd98: ldr     ip, [sp, #0xc]
0x2ddd9c: cmp     ip, #0
0x2ddda0: ble     #0x2ddef0
0x2ddda4: mov     r7, #0
0x2ddda8: mov     r5, #0
0x2dddac: ldr     ip, [sp, #0x10]
0x2dddb0: mov     r0, r4
0x2dddb4: ldr     r6, [ip, #0x38]
0x2dddb8: add     r6, r6, r7, lsl #4
0x2dddbc: mov     r1, r6
0x2dddc0: bl      #0x33a0d4   ; <<READER STR>>
0x2dddc4: mov     r0, r4
0x2dddc8: bl      #0x339914   ; <<READER i>>
0x2dddcc: ldmib   r6, {r8, sb}
0x2dddd0: rsb     fp, r8, sb
0x2dddd4: asr     fp, fp, #5
0x2dddd8: cmp     r0, fp
0x2ddddc: mov     sl, r0
0x2ddde0: bls     #0x2de00c
0x2ddde4: subs    r1, r0, fp
0x2ddde8: str     r1, [sp, #8]
0x2dddec: beq     #0x2dde5c
0x2dddf0: ldr     r3, [r6, #0xc]
0x2dddf4: rsb     r3, sb, r3
0x2dddf8: cmp     r1, r3, asr #5
0x2dddfc: bhi     #0x2de018
0x2dde00: ldr     r0, [sp, #8]
0x2dde04: add     r1, sb, #0x1c
0x2dde08: add     r2, sb, #0x10
0x2dde0c: mov     r3, sb
0x2dde10: mov     ip, #0
0x2dde14: cmp     r3, #0
0x2dde18: beq     #0x2dde3c
0x2dde1c: str     ip, [r3]
0x2dde20: str     ip, [r3, #4]
0x2dde24: str     r5, [r2, #-8]
0x2dde28: str     r5, [r2, #-4]
0x2dde2c: str     r5, [r2]
0x2dde30: str     r5, [r1, #-8]
0x2dde34: str     r5, [r1, #-4]
0x2dde38: str     r5, [r1]
0x2dde3c: subs    r0, r0, #1
0x2dde40: add     r3, r3, #0x20
0x2dde44: add     r1, r1, #0x20
0x2dde48: add     r2, r2, #0x20
0x2dde4c: bne     #0x2dde14
0x2dde50: ldr     r2, [sp, #8]
0x2dde54: add     sb, sb, r2, lsl #5
0x2dde58: str     sb, [r6, #8]
0x2dde5c: cmp     sl, #0
0x2dde60: ble     #0x2ddee0
0x2dde64: mov     fp, #0
0x2dde68: b       #0x2dde70
0x2dde6c: ldr     r8, [r6, #4]
0x2dde70: mov     r0, r4
0x2dde74: add     sb, r8, fp, lsl #5
0x2dde78: bl      #0x339914   ; <<READER i>>
0x2dde7c: str     r0, [r8, fp, lsl #5]
0x2dde80: mov     r0, r4
0x2dde84: bl      #0x339914   ; <<READER i>>
0x2dde88: add     fp, fp, #1
0x2dde8c: str     r0, [sb, #4]
0x2dde90: mov     r0, r4
0x2dde94: bl      #0x339b94   ; <<READER f>>
0x2dde98: str     r0, [sb, #8]
0x2dde9c: mov     r0, r4
0x2ddea0: bl      #0x339b94   ; <<READER f>>
0x2ddea4: str     r0, [sb, #0xc]
0x2ddea8: mov     r0, r4
0x2ddeac: bl      #0x339b94   ; <<READER f>>
0x2ddeb0: str     r0, [sb, #0x10]
0x2ddeb4: mov     r0, r4
0x2ddeb8: bl      #0x339b94   ; <<READER f>>
0x2ddebc: str     r0, [sb, #0x14]
0x2ddec0: mov     r0, r4
0x2ddec4: bl      #0x339b94   ; <<READER f>>
0x2ddec8: str     r0, [sb, #0x18]
0x2ddecc: mov     r0, r4
0x2dded0: bl      #0x339b94   ; <<READER f>>
0x2dded4: cmp     fp, sl
0x2dded8: str     r0, [sb, #0x1c]
0x2ddedc: bne     #0x2dde6c
0x2ddee0: ldr     ip, [sp, #0xc]
0x2ddee4: add     r7, r7, #1
0x2ddee8: cmp     r7, ip
0x2ddeec: bne     #0x2dddac
0x2ddef0: mov     r0, r4
0x2ddef4: mov     r6, #0x58
0x2ddef8: bl      #0x339914   ; <<READER i>>
0x2ddefc: mov     r1, #0
0x2ddf00: mov     r2, r6
0x2ddf04: mov     r5, r0
0x2ddf08: add     r0, sp, #0xc0
0x2ddf0c: bl      #0xa4e88
0x2ddf10: ldr     ip, [sp, #0x10]
0x2ddf14: movw    r3, #0x8ba3
0x2ddf18: movt    r3, #0xba2e
0x2ddf1c: ldr     r8, [ip, #0x48]
0x2ddf20: ldr     r1, [ip, #0x44]
0x2ddf24: rsb     r2, r1, r8
0x2ddf28: asr     r2, r2, #3
0x2ddf2c: mul     r2, r3, r2
0x2ddf30: cmp     r5, r2
0x2ddf34: bls     #0x2de5c0
0x2ddf38: add     r0, ip, #0x44
0x2ddf3c: mov     r1, r8
0x2ddf40: rsb     r2, r2, r5
0x2ddf44: add     r3, sp, #0xc0
0x2ddf48: bl      #0x2ee8b8   ; <<_ZNSt6vectorI30CContainerTracksAnimatedObjectSaIS0_EE14_M_fill_insertE>>
0x2ddf4c: add     r0, sp, #0xc0
0x2ddf50: bl      #0x2df108   ; <<_ZN30CContainerTracksAnimatedObjectD1Ev>>
0x2ddf54: cmp     r5, #0
0x2ddf58: ble     #0x2ddf88
0x2ddf5c: ldr     r8, [sp, #0x10]
0x2ddf60: mov     r6, #0
0x2ddf64: mov     r7, r6
0x2ddf68: ldr     r0, [r8, #0x44]
0x2ddf6c: mov     r1, r4
0x2ddf70: add     r7, r7, #1
0x2ddf74: add     r0, r0, r6
0x2ddf78: add     r6, r6, #0x58
0x2ddf7c: bl      #0x2d9118   ; <<_ZN30CContainerTracksAnimatedObject4LoadEP13CMemoryStream>>
0x2ddf80: cmp     r7, r5
0x2ddf84: bne     #0x2ddf68
0x2ddf88: add     sp, sp, #0x11c
0x2ddf8c: pop     {r4, r5, r6, r7, r8, sb, sl, fp, pc}
0x2ddf90: add     sl, sp, #0x98
0x2ddf94: b       #0x2dd954
0x2ddf98: add     fp, sp, #0x64
0x2ddf9c: b       #0x2ddcac
0x2ddfa0: bhs     #0x2ddf90
0x2ddfa4: add     sb, r3, r0, lsl #4
0x2ddfa8: cmp     r7, sb
0x2ddfac: beq     #0x2ddfc8
0x2ddfb0: mov     sl, sb
0x2ddfb4: add     r0, sl, #8
0x2ddfb8: add     sl, sl, #0x10
0x2ddfbc: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddfc0: cmp     r7, sl
0x2ddfc4: bne     #0x2ddfb4
0x2ddfc8: add     sl, sp, #0x98
0x2ddfcc: str     sb, [r5, #4]
0x2ddfd0: b       #0x2dd954
0x2ddfd4: bhs     #0x2ddf98
0x2ddfd8: add     r7, r0, r0, lsl #1
0x2ddfdc: add     r7, r2, r7, lsl #2
0x2ddfe0: cmp     sl, r7
0x2ddfe4: beq     #0x2de000
0x2ddfe8: mov     r8, r7
0x2ddfec: add     r0, r8, #8
0x2ddff0: add     r8, r8, #0xc
0x2ddff4: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2ddff8: cmp     sl, r8
0x2ddffc: bne     #0x2ddfec
0x2de000: add     fp, sp, #0x64
0x2de004: str     r7, [r5, #4]
0x2de008: b       #0x2ddcac
0x2de00c: addlo   r3, r8, r0, lsl #5
0x2de010: strlo   r3, [r6, #8]
0x2de014: b       #0x2dde5c
0x2de018: movw    r3, #0xffff
0x2de01c: ldr     ip, [sp, #8]
0x2de020: movt    r3, #0x7ff
0x2de024: rsb     r3, fp, r3
0x2de028: cmp     ip, r3
0x2de02c: bhi     #0x2dee44
0x2de030: cmp     ip, fp
0x2de034: addhs   r3, fp, ip
0x2de038: addlo   r3, fp, fp
0x2de03c: mov     r1, ip
0x2de040: cmp     fp, r3
0x2de044: mvnhi   r1, #0x1f
0x2de048: strhi   r1, [sp, #0x18]
0x2de04c: bhi     #0x2de06c
0x2de050: mvn     r2, #0xf8000000
0x2de054: cmp     r3, r2
0x2de058: movhs   r3, r2
0x2de05c: cmp     r3, #0
0x2de060: lsl     ip, r3, #5
0x2de064: str     ip, [sp, #0x18]
0x2de068: beq     #0x2deadc
0x2de06c: ldr     r0, [sp, #0x18]
0x2de070: bl      #0x3e91f8
0x2de074: ldr     r2, [r6, #4]
0x2de078: ldr     r3, [r6, #8]
0x2de07c: str     r2, [sp, #0x14]
0x2de080: str     r3, [sp, #0x1c]
0x2de084: mov     r8, r0
0x2de088: add     fp, r8, fp, lsl #5
0x2de08c: ldr     r1, [sp, #8]
0x2de090: add     r2, fp, #0x1c
0x2de094: add     r3, fp, #0x10
0x2de098: mov     r0, #0
0x2de09c: cmp     fp, #0
0x2de0a0: beq     #0x2de0c4
0x2de0a4: str     r0, [fp]
0x2de0a8: str     r0, [fp, #4]
0x2de0ac: str     r5, [r3, #-8]
0x2de0b0: str     r5, [r3, #-4]
0x2de0b4: str     r5, [r3]
0x2de0b8: str     r5, [r2, #-8]
0x2de0bc: str     r5, [r2, #-4]
0x2de0c0: str     r5, [r2]
0x2de0c4: subs    r1, r1, #1
0x2de0c8: add     fp, fp, #0x20
0x2de0cc: add     r2, r2, #0x20
0x2de0d0: add     r3, r3, #0x20
0x2de0d4: bne     #0x2de09c
0x2de0d8: ldr     ip, [sp, #0x14]
0x2de0dc: cmp     sb, ip
0x2de0e0: moveq   r3, r8
0x2de0e4: beq     #0x2de184
0x2de0e8: mov     r1, ip
0x2de0ec: mov     r2, ip
0x2de0f0: add     lr, ip, #0x1c
0x2de0f4: add     r0, r1, #0x10
0x2de0f8: add     ip, r8, #0x1c
0x2de0fc: add     r1, r8, #0x10
0x2de100: mov     r3, r8
0x2de104: cmp     r3, #0
0x2de108: beq     #0x2de14c
0x2de10c: ldr     fp, [r2]
0x2de110: str     fp, [r3]
0x2de114: ldr     fp, [r2, #4]
0x2de118: str     fp, [r3, #4]
0x2de11c: ldr     fp, [r0, #-8]
0x2de120: str     fp, [r1, #-8]
0x2de124: ldr     fp, [r0, #-4]
0x2de128: str     fp, [r1, #-4]
0x2de12c: ldr     fp, [r0]
0x2de130: str     fp, [r1]
0x2de134: ldr     fp, [lr, #-8]
0x2de138: str     fp, [ip, #-8]
0x2de13c: ldr     fp, [lr, #-4]
0x2de140: str     fp, [ip, #-4]
0x2de144: ldr     fp, [lr]
0x2de148: str     fp, [ip]
0x2de14c: add     r2, r2, #0x20
0x2de150: add     r3, r3, #0x20
0x2de154: cmp     sb, r2
0x2de158: add     lr, lr, #0x20
0x2de15c: add     ip, ip, #0x20
0x2de160: add     r0, r0, #0x20
0x2de164: add     r1, r1, #0x20
0x2de168: bne     #0x2de104
0x2de16c: ldr     r2, [sp, #0x14]
0x2de170: add     r3, r2, #0x20
0x2de174: rsb     r3, r3, sb
0x2de178: bic     r3, r3, #0x1f
0x2de17c: add     r3, r3, #0x20
0x2de180: add     r3, r8, r3
0x2de184: ldr     ip, [sp, #0x1c]
0x2de188: ldr     r1, [sp, #8]
0x2de18c: cmp     sb, ip
0x2de190: add     r3, r3, r1, lsl #5
0x2de194: str     r3, [sp, #8]
0x2de198: beq     #0x2de244
0x2de19c: add     lr, sb, #0x1c
0x2de1a0: add     r0, sb, #0x10
0x2de1a4: mov     r2, r3
0x2de1a8: mov     fp, ip
0x2de1ac: add     r1, r3, #0x10
0x2de1b0: add     ip, r3, #0x1c
0x2de1b4: mov     r3, sb
0x2de1b8: str     r7, [sp, #0x20]
0x2de1bc: cmp     r2, #0
0x2de1c0: beq     #0x2de204
0x2de1c4: ldr     r7, [r3]
0x2de1c8: str     r7, [r2]
0x2de1cc: ldr     r7, [r3, #4]
0x2de1d0: str     r7, [r2, #4]
0x2de1d4: ldr     r7, [r0, #-8]
0x2de1d8: str     r7, [r1, #-8]
0x2de1dc: ldr     r7, [r0, #-4]
0x2de1e0: str     r7, [r1, #-4]
0x2de1e4: ldr     r7, [r0]
0x2de1e8: str     r7, [r1]
0x2de1ec: ldr     r7, [lr, #-8]
0x2de1f0: str     r7, [ip, #-8]
0x2de1f4: ldr     r7, [lr, #-4]
0x2de1f8: str     r7, [ip, #-4]
0x2de1fc: ldr     r7, [lr]
0x2de200: str     r7, [ip]
0x2de204: add     r3, r3, #0x20
0x2de208: add     r2, r2, #0x20
0x2de20c: cmp     r3, fp
0x2de210: add     lr, lr, #0x20
0x2de214: add     ip, ip, #0x20
0x2de218: add     r0, r0, #0x20
0x2de21c: add     r1, r1, #0x20
0x2de220: bne     #0x2de1bc
0x2de224: add     sb, sb, #0x20
0x2de228: ldr     r7, [sp, #0x20]
0x2de22c: rsb     r3, sb, r3
0x2de230: ldr     r2, [sp, #8]
0x2de234: bic     r3, r3, #0x1f
0x2de238: add     r3, r3, #0x20
0x2de23c: add     r2, r2, r3
0x2de240: str     r2, [sp, #8]
0x2de244: ldr     r3, [sp, #0x14]
0x2de248: cmp     r3, #0
0x2de24c: beq     #0x2de258
0x2de250: mov     r0, r3
0x2de254: bl      #0x3e9260
0x2de258: ldr     r1, [sp, #8]
0x2de25c: ldr     ip, [sp, #0x18]
0x2de260: str     r8, [r6, #4]
0x2de264: add     r3, r8, ip
0x2de268: str     r1, [r6, #8]
0x2de26c: str     r3, [r6, #0xc]
0x2de270: b       #0x2dde5c
0x2de274: add     fp, sp, #0x64
0x2de278: add     r0, sp, #0x7c
0x2de27c: mov     ip, #0
0x2de280: str     ip, [sp, #0x74]
0x2de284: mov     r1, fp
0x2de288: str     ip, [sp, #0x78]
0x2de28c: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de290: ldr     r2, [r5, #4]
0x2de294: rsb     r3, sl, r2
0x2de298: str     r2, [sp, #0x18]
0x2de29c: asr     r3, r3, #2
0x2de2a0: add     r2, r3, r3, lsl #2
0x2de2a4: add     r2, r2, r2, lsl #4
0x2de2a8: add     r2, r2, r2, lsl #8
0x2de2ac: add     r2, r2, r2, lsl #16
0x2de2b0: add     r2, r3, r2, lsl #1
0x2de2b4: ldr     r3, [sp, #0xc]
0x2de2b8: str     r2, [sp, #0x20]
0x2de2bc: cmp     r3, r2
0x2de2c0: bhs     #0x2de800
0x2de2c4: add     r3, r3, r3, lsl #1
0x2de2c8: ldr     r2, [sp, #0x18]
0x2de2cc: lsl     r3, r3, #2
0x2de2d0: str     r3, [sp, #0x20]
0x2de2d4: rsb     r2, r3, r2
0x2de2d8: ldr     r3, [sp, #0x18]
0x2de2dc: str     r2, [sp, #0xc]
0x2de2e0: cmp     r3, r2
0x2de2e4: moveq   r2, r3
0x2de2e8: beq     #0x2de338
0x2de2ec: str     r5, [sp, #0x2c]
0x2de2f0: mov     r8, r2
0x2de2f4: mov     r7, r3
0x2de2f8: mov     r5, r3
0x2de2fc: cmp     r7, #0
0x2de300: beq     #0x2de320
0x2de304: ldr     r3, [r8]
0x2de308: add     r0, r7, #8
0x2de30c: add     r1, r8, #8
0x2de310: str     r3, [r7]
0x2de314: ldr     r3, [r8, #4]
0x2de318: str     r3, [r7, #4]
0x2de31c: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de320: add     r8, r8, #0xc
0x2de324: add     r7, r7, #0xc
0x2de328: cmp     r5, r8
0x2de32c: bne     #0x2de2fc
0x2de330: ldr     r5, [sp, #0x2c]
0x2de334: ldr     r2, [r5, #4]
0x2de338: ldr     ip, [sp, #0xc]
0x2de33c: rsb     r3, sl, ip
0x2de340: ldr     ip, [sp, #0x20]
0x2de344: asr     r3, r3, #2
0x2de348: add     r2, r2, ip
0x2de34c: str     r2, [r5, #4]
0x2de350: add     r8, r3, r3, lsl #2
0x2de354: add     r8, r8, r8, lsl #4
0x2de358: add     r8, r8, r8, lsl #8
0x2de35c: add     r8, r8, r8, lsl #16
0x2de360: add     r8, r3, r8, lsl #1
0x2de364: cmp     r8, #0
0x2de368: ble     #0x2de400
0x2de36c: ldr     r3, [sp, #0x18]
0x2de370: ldr     r2, [sp, #0xc]
0x2de374: sub     r1, r3, #0xc
0x2de378: str     r5, [sp, #0x2c]
0x2de37c: sub     r0, r2, #0xc
0x2de380: mov     r2, r3
0x2de384: ldr     r3, [sp, #0xc]
0x2de388: str     r6, [sp, #0x30]
0x2de38c: mov     r6, r2
0x2de390: str     sl, [sp, #0x34]
0x2de394: mov     sl, r1
0x2de398: str     sb, [sp, #0xc]
0x2de39c: mov     r5, r3
0x2de3a0: str     r4, [sp, #0x38]
0x2de3a4: mov     r7, r3
0x2de3a8: mov     r4, r2
0x2de3ac: mov     sb, r0
0x2de3b0: str     fp, [sp, #0x3c]
0x2de3b4: rsb     lr, r7, r5
0x2de3b8: rsb     ip, r6, r4
0x2de3bc: sub     r0, r4, #4
0x2de3c0: sub     r1, r5, #4
0x2de3c4: ldr     fp, [lr, sb]!
0x2de3c8: sub     r4, r4, #0xc
0x2de3cc: sub     r5, r5, #0xc
0x2de3d0: str     fp, [ip, sl]!
0x2de3d4: ldr     r3, [lr, #4]
0x2de3d8: str     r3, [ip, #4]
0x2de3dc: bl      #0x206c64   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de3e0: subs    r8, r8, #1
0x2de3e4: bne     #0x2de3b4
0x2de3e8: add     r5, sp, #0x2c
0x2de3ec: ldr     sb, [sp, #0xc]
0x2de3f0: ldr     r4, [sp, #0x38]
0x2de3f4: ldm     r5, {r5, r6, sl}
0x2de3f8: ldr     fp, [sp, #0x3c]
0x2de3fc: ldr     ip, [sp, #0x20]
0x2de400: add     r7, sl, ip
0x2de404: cmp     sl, r7
0x2de408: beq     #0x2de434
0x2de40c: ldr     r3, [sp, #0x74]
0x2de410: add     r0, sl, #8
0x2de414: add     r1, sp, #0x7c
0x2de418: str     r3, [sl]
0x2de41c: ldr     r3, [sp, #0x78]
0x2de420: str     r3, [sl, #4]
0x2de424: add     sl, sl, #0xc
0x2de428: bl      #0x206c64   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de42c: cmp     r7, sl
0x2de430: bne     #0x2de40c
0x2de434: add     r0, sp, #0x7c
0x2de438: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de43c: b       #0x2ddcac
0x2de440: add     sl, sp, #0x98
0x2de444: add     r0, sp, #0xb8
0x2de448: mov     lr, #0
0x2de44c: str     lr, [sp, #0xb0]
0x2de450: mov     r1, sl
0x2de454: str     lr, [sp, #0xb4]
0x2de458: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de45c: ldr     r3, [r5, #4]
0x2de460: ldrb    r2, [sp, #0x9c]
0x2de464: rsb     r1, r7, r3
0x2de468: strb    r2, [sp, #0xbc]
0x2de46c: asr     r1, r1, #4
0x2de470: ldr     r2, [sp, #0xc]
0x2de474: str     r1, [sp, #0x18]
0x2de478: cmp     r2, r1
0x2de47c: bhs     #0x2de6e8
0x2de480: lsl     ip, r2, #4
0x2de484: str     ip, [sp, #0xc]
0x2de488: rsb     r2, ip, r3
0x2de48c: cmp     r3, r2
0x2de490: moveq   r1, r3
0x2de494: beq     #0x2de4f8
0x2de498: str     r5, [sp, #0x18]
0x2de49c: mov     fp, r2
0x2de4a0: mov     sb, r3
0x2de4a4: mov     r5, r3
0x2de4a8: str     r2, [sp, #0x20]
0x2de4ac: cmp     sb, #0
0x2de4b0: beq     #0x2de4d8
0x2de4b4: ldr     r3, [fp]
0x2de4b8: add     r0, sb, #8
0x2de4bc: add     r1, fp, #8
0x2de4c0: str     r3, [sb]
0x2de4c4: ldr     r3, [fp, #4]
0x2de4c8: str     r3, [sb, #4]
0x2de4cc: bl      #0x206a60   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de4d0: ldrb    r3, [fp, #0xc]
0x2de4d4: strb    r3, [sb, #0xc]
0x2de4d8: add     fp, fp, #0x10
0x2de4dc: add     sb, sb, #0x10
0x2de4e0: cmp     r5, fp
0x2de4e4: bne     #0x2de4ac
0x2de4e8: mov     r3, r5
0x2de4ec: ldr     r5, [sp, #0x18]
0x2de4f0: ldr     r2, [sp, #0x20]
0x2de4f4: ldr     r1, [r5, #4]
0x2de4f8: rsb     ip, r7, r2
0x2de4fc: ldr     lr, [sp, #0xc]
0x2de500: asr     ip, ip, #4
0x2de504: add     r1, r1, lr
0x2de508: cmp     ip, #0
0x2de50c: str     r1, [r5, #4]
0x2de510: ble     #0x2de574
0x2de514: sub     sb, r2, #4
0x2de518: sub     fp, r3, #4
0x2de51c: str     r5, [sp, #0x18]
0x2de520: mov     r5, ip
0x2de524: str     r6, [sp, #0x20]
0x2de528: mov     r6, r2
0x2de52c: str     r7, [sp, #0x28]
0x2de530: mov     r7, r3
0x2de534: ldr     ip, [sb, #-0xc]
0x2de538: sub     r0, r7, #8
0x2de53c: sub     r1, r6, #8
0x2de540: sub     r7, r7, #0x10
0x2de544: sub     r6, r6, #0x10
0x2de548: str     ip, [fp, #-0xc]
0x2de54c: ldr     r3, [sb, #-8]
0x2de550: str     r3, [fp, #-8]
0x2de554: bl      #0x206c64   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de558: ldrb    r3, [sb], #-0x10
0x2de55c: subs    r5, r5, #1
0x2de560: strb    r3, [fp], #-0x10
0x2de564: bne     #0x2de534
0x2de568: ldr     r5, [sp, #0x18]
0x2de56c: ldr     r6, [sp, #0x20]
0x2de570: ldr     r7, [sp, #0x28]
0x2de574: ldr     r2, [sp, #0xc]
0x2de578: add     sb, r7, r2
0x2de57c: cmp     r7, sb
0x2de580: beq     #0x2de5b4
0x2de584: ldr     r3, [sp, #0xb0]
0x2de588: add     r0, r7, #8
0x2de58c: add     r1, sp, #0xb8
0x2de590: str     r3, [r7]
0x2de594: ldr     r3, [sp, #0xb4]
0x2de598: str     r3, [r7, #4]
0x2de59c: bl      #0x206c64   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de5a0: ldrb    r3, [sp, #0xbc]
0x2de5a4: strb    r3, [r7, #0xc]
0x2de5a8: add     r7, r7, #0x10
0x2de5ac: cmp     sb, r7
0x2de5b0: bne     #0x2de584
0x2de5b4: add     r0, sp, #0xb8
0x2de5b8: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de5bc: b       #0x2dd954
0x2de5c0: bhs     #0x2ddf4c
0x2de5c4: mla     r6, r6, r5, r1
0x2de5c8: cmp     r8, r6
0x2de5cc: beq     #0x2de5e8
0x2de5d0: mov     r7, r6
0x2de5d4: mov     r0, r7
0x2de5d8: add     r7, r7, #0x58
0x2de5dc: bl      #0x2df108   ; <<_ZN30CContainerTracksAnimatedObjectD1Ev>>
0x2de5e0: cmp     r8, r7
0x2de5e4: bne     #0x2de5d4
0x2de5e8: ldr     ip, [sp, #0x10]
0x2de5ec: str     r6, [ip, #0x48]
0x2de5f0: b       #0x2ddf4c
0x2de5f4: addhs   r5, sp, #0x80
0x2de5f8: bhs     #0x2ddd90
0x2de5fc: ldr     ip, [sp, #0xc]
0x2de600: add     r7, r7, ip, lsl #4
0x2de604: cmp     r6, r7
0x2de608: moveq   r0, r3
0x2de60c: beq     #0x2de644
0x2de610: add     r8, r7, #4
0x2de614: mov     r5, r7
0x2de618: rsb     r3, r7, r5
0x2de61c: ldr     r0, [r8, r3]
0x2de620: cmp     r0, #0
0x2de624: beq     #0x2de62c
0x2de628: bl      #0x3e9260
0x2de62c: mov     r0, r5
0x2de630: add     r5, r5, #0x10
0x2de634: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de638: cmp     r6, r5
0x2de63c: bne     #0x2de618
0x2de640: ldr     r0, [sp, #0x84]
0x2de644: ldr     ip, [sp, #0x10]
0x2de648: add     r5, sp, #0x80
0x2de64c: str     r7, [ip, #0x3c]
0x2de650: b       #0x2ddd84
0x2de654: bhs     #0x2dda6c
0x2de658: ldr     ip, [sp, #0x14]
0x2de65c: add     r8, ip, ip, lsl #1
0x2de660: add     r8, r1, r8, lsl #2
0x2de664: cmp     sl, r8
0x2de668: moveq   r5, r6
0x2de66c: beq     #0x2de6bc
0x2de670: mov     r7, r8
0x2de674: ldm     r7, {r5, r6}
0x2de678: cmp     r5, r6
0x2de67c: beq     #0x2de698
0x2de680: add     r0, r5, #8
0x2de684: add     r5, r5, #0xc
0x2de688: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x2de68c: cmp     r6, r5
0x2de690: bne     #0x2de680
0x2de694: ldr     r5, [r7]
0x2de698: cmp     r5, #0
0x2de69c: beq     #0x2de6a8
0x2de6a0: mov     r0, r5
0x2de6a4: bl      #0x3e9260
0x2de6a8: add     r7, r7, #0xc
0x2de6ac: cmp     sl, r7
0x2de6b0: bne     #0x2de674
0x2de6b4: ldr     r5, [sp, #0x50]
0x2de6b8: ldr     r6, [sp, #0x54]
0x2de6bc: ldr     ip, [sp, #0x10]
0x2de6c0: str     r8, [ip, #0x30]
0x2de6c4: b       #0x2dda3c