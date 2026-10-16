0x292b4c: ldr     ip, [pc, #0x6b8]   ; pool[0x29320c]=0x975f50
0x292b50: ldr     r3, [pc, #0x6b8]   ; pool[0x293210]=0xfffff0a8
0x292b54: push    {r4, r5, r6, r7, r8, sb, sl, fp, lr}
0x292b58: add     ip, pc, ip
0x292b5c: sub     sp, sp, #0xe4
0x292b60: subs    r6, r1, #0
0x292b64: mov     r4, r0
0x292b68: str     ip, [sp, #0x2c]
0x292b6c: ldr     r3, [ip, r3]
0x292b70: str     r3, [sp, #0x34]
0x292b74: ldr     r3, [r3]
0x292b78: str     r3, [sp, #0xdc]
0x292b7c: beq     #0x2931fc
0x292b80: ldr     r1, [pc, #0x68c]   ; pool[0x293214]=0x8a8344
0x292b84: mov     r2, #0x45
0x292b88: mov     r0, #0x50
0x292b8c: add     r1, pc, r1
0x292b90: bl      #0x3e9204
0x292b94: mov     r2, #0x50
0x292b98: mov     r1, #0
0x292b9c: mov     r5, r0
0x292ba0: bl      #0xa4e88
0x292ba4: ldr     r3, [pc, #0x66c]   ; pool[0x293218]=0x9407b0
0x292ba8: mov     r0, r5
0x292bac: mov     r1, r6
0x292bb0: add     r3, pc, r3
0x292bb4: add     r3, r3, #8
0x292bb8: str     r3, [r5]
0x292bbc: str     r5, [r4, #0x10]
0x292bc0: bl      #0x2dce20   ; <<_ZN19CComponentCinematic4LoadEP13CMemoryStream>>
0x292bc4: ldr     r2, [r4, #0x10]
0x292bc8: ldr     r3, [r2, #0x2c]
0x292bcc: ldr     r1, [r2, #0x30]
0x292bd0: rsb     r1, r3, r1
0x292bd4: asr     r1, r1, #2
0x292bd8: add     r0, r1, r1, lsl #2
0x292bdc: add     r0, r0, r0, lsl #4
0x292be0: add     r0, r0, r0, lsl #8
0x292be4: add     r0, r0, r0, lsl #16
0x292be8: add     r0, r1, r0, lsl #1
0x292bec: str     r0, [sp, #0x20]
0x292bf0: cmp     r0, #0
0x292bf4: ble     #0x292db4
0x292bf8: ldr     r1, [pc, #0x61c]   ; pool[0x29321c]=0x8a835c
0x292bfc: mov     ip, #0
0x292c00: str     ip, [sp, #0x1c]
0x292c04: add     r1, pc, r1
0x292c08: str     r1, [sp, #0x14]
0x292c0c: ldr     r1, [pc, #0x60c]   ; pool[0x293220]=0x8a8358
0x292c10: str     ip, [sp, #0x10]
0x292c14: add     r1, pc, r1
0x292c18: str     r1, [sp, #0x18]
0x292c1c: add     r7, r3, ip
0x292c20: ldr     r3, [r3, ip]
0x292c24: ldr     r1, [r7, #4]
0x292c28: rsb     r1, r3, r1
0x292c2c: asr     r1, r1, #2
0x292c30: add     r0, r1, r1, lsl #2
0x292c34: add     r0, r0, r0, lsl #4
0x292c38: add     r0, r0, r0, lsl #8
0x292c3c: add     r0, r0, r0, lsl #16
0x292c40: add     r1, r1, r0, lsl #1
0x292c44: cmp     r1, #0
0x292c48: beq     #0x292d84
0x292c4c: ldr     r2, [pc, #0x5d0]   ; pool[0x293224]=0xfffff508
0x292c50: mov     r5, #0
0x292c54: ldr     ip, [sp, #0x2c]
0x292c58: add     r8, sp, #0x3c
0x292c5c: add     sl, sp, #0x5c
0x292c60: mov     r6, r5
0x292c64: ldr     r2, [ip, r2]
0x292c68: str     r2, [sp, #0xc]
0x292c6c: b       #0x292cc4
0x292c70: cmp     ip, #0
0x292c74: addne   r3, sp, #0x4c
0x292c78: ldmne   r3, {r0, r1, r2, r3}
0x292c7c: stmne   ip, {r0, r1, r2, r3}
0x292c80: add     ip, ip, #0x10
0x292c84: str     ip, [r4, #0x28]
0x292c88: mov     r0, r8
0x292c8c: add     r6, r6, #1
0x292c90: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x292c94: ldr     r3, [r7]
0x292c98: ldr     r2, [r7, #4]
0x292c9c: add     r5, r5, #0xc
0x292ca0: rsb     r2, r3, r2
0x292ca4: asr     r2, r2, #2
0x292ca8: add     r1, r2, r2, lsl #2
0x292cac: add     r1, r1, r1, lsl #4
0x292cb0: add     r1, r1, r1, lsl #8
0x292cb4: add     r1, r1, r1, lsl #16
0x292cb8: add     r1, r2, r1, lsl #1
0x292cbc: cmp     r6, r1
0x292cc0: bhs     #0x292d80
0x292cc4: add     r3, r3, r5
0x292cc8: ldr     r1, [sp, #0x14]
0x292ccc: mov     r0, r8
0x292cd0: ldr     sb, [r3, #8]
0x292cd4: ldr     fp, [sb, #-0xc]
0x292cd8: bl      #0x2c47bc
0x292cdc: ldr     ip, [sp, #0xc]
0x292ce0: mov     r1, sb
0x292ce4: mov     r3, #1
0x292ce8: mov     r2, fp
0x292cec: ldr     r0, [ip]
0x292cf0: str     r3, [sp]
0x292cf4: ldr     r3, [sp, #0x3c]
0x292cf8: bl      #0x14813c
0x292cfc: ldr     r0, [r4, #4]
0x292d00: ldr     r3, [r0]
0x292d04: ldr     r3, [r3, #0x14]
0x292d08: blx     r3
0x292d0c: ldr     r3, [sp, #0x10]
0x292d10: ldr     r1, [sp, #0x18]
0x292d14: str     r6, [sp]
0x292d18: mov     r2, r0
0x292d1c: mov     r0, sl
0x292d20: bl      #0xa4edc
0x292d24: ldr     ip, [sp, #0xc]
0x292d28: mov     r1, sl
0x292d2c: ldr     r0, [ip]
0x292d30: bl      #0x14931c
0x292d34: ldr     r3, [r7]
0x292d38: ldr     r2, [r4, #0x2c]
0x292d3c: ldr     ip, [r4, #0x28]
0x292d40: ldr     r3, [r3, r5]
0x292d44: vmov    s14, r3
0x292d48: vcvt.f32.s32 s15, s14
0x292d4c: cmp     ip, r2
0x292d50: mov     r2, #0
0x292d54: strb    r2, [sp, #0x58]
0x292d58: mvn     r2, #0
0x292d5c: str     r2, [sp, #0x54]
0x292d60: vstr    s15, [sp, #0x50]
0x292d64: str     r0, [sp, #0x4c]
0x292d68: bne     #0x292c70
0x292d6c: add     r0, r4, #0x24
0x292d70: mov     r1, ip
0x292d74: add     r2, sp, #0x4c
0x292d78: bl      #0x2ce7f8
0x292d7c: b       #0x292c88
0x292d80: ldr     r2, [r4, #0x10]
0x292d84: ldr     ip, [sp, #0x10]
0x292d88: ldr     r0, [sp, #0x20]
0x292d8c: add     ip, ip, #1
0x292d90: str     ip, [sp, #0x10]
0x292d94: ldr     ip, [sp, #0x1c]
0x292d98: add     ip, ip, #0xc
0x292d9c: str     ip, [sp, #0x1c]
0x292da0: ldr     ip, [sp, #0x10]
0x292da4: cmp     ip, r0
0x292da8: ldrne   r3, [r2, #0x2c]
0x292dac: ldrne   ip, [sp, #0x1c]
0x292db0: bne     #0x292c1c
0x292db4: ldr     r1, [r2, #0x44]
0x292db8: movw    r3, #0x8ba3
0x292dbc: ldr     r0, [r2, #0x48]
0x292dc0: movt    r3, #0xba2e
0x292dc4: rsb     r0, r1, r0
0x292dc8: asr     r0, r0, #3
0x292dcc: mul     r3, r3, r0
0x292dd0: cmp     r3, #0
0x292dd4: str     r3, [sp, #0x30]
0x292dd8: ble     #0x2931e0
0x292ddc: ldr     r3, [pc, #0x444]   ; pool[0x293228]=0x8a8178
0x292de0: mov     ip, #0
0x292de4: str     ip, [sp, #0x14]
0x292de8: add     r3, pc, r3
0x292dec: str     r3, [sp, #0x1c]
0x292df0: ldr     r3, [pc, #0x434]   ; pool[0x29322c]=0x8a8190
0x292df4: str     ip, [sp, #0x18]
0x292df8: add     r3, pc, r3
0x292dfc: str     r3, [sp, #0x20]
0x292e00: ldr     ip, [sp, #0x14]
0x292e04: add     ip, r1, ip
0x292e08: str     ip, [sp, #0x28]
0x292e0c: ldr     r0, [sp, #0x28]
0x292e10: ldr     ip, [ip, #0x38]
0x292e14: ldr     r3, [r0, #0x34]
0x292e18: rsb     r0, r3, ip
0x292e1c: asr     r0, r0, #2
0x292e20: add     r5, r0, r0, lsl #2
0x292e24: add     r5, r5, r5, lsl #4
0x292e28: add     r5, r5, r5, lsl #8
0x292e2c: add     r5, r5, r5, lsl #16
0x292e30: add     r0, r0, r5, lsl #1
0x292e34: cmp     r0, #0
0x292e38: beq     #0x293020
0x292e3c: mov     r1, #0
0x292e40: mov     r0, r3
0x292e44: mov     r2, r1
0x292e48: str     r1, [sp, #0x24]
0x292e4c: str     r1, [sp, #0x10]
0x292e50: add     r7, r3, r2
0x292e54: ldr     r3, [r3, r2]
0x292e58: ldr     r2, [r7, #4]
0x292e5c: rsb     r2, r3, r2
0x292e60: asr     r2, r2, #2
0x292e64: add     r1, r2, r2, lsl #2
0x292e68: add     r1, r1, r1, lsl #4
0x292e6c: add     r1, r1, r1, lsl #8
0x292e70: add     r1, r1, r1, lsl #16
0x292e74: add     r1, r2, r1, lsl #1
0x292e78: cmp     r1, #0
0x292e7c: beq     #0x292fd4
0x292e80: ldr     r2, [pc, #0x39c]   ; pool[0x293224]=0xfffff508
0x292e84: mov     r5, #0
0x292e88: ldr     ip, [sp, #0x2c]
0x292e8c: add     r8, sp, #0x3c
0x292e90: add     sl, sp, #0x5c
0x292e94: mov     r6, r5
0x292e98: ldr     r2, [ip, r2]
0x292e9c: str     r2, [sp, #0xc]
0x292ea0: b       #0x292ef8
0x292ea4: cmp     ip, #0
0x292ea8: addne   r3, sp, #0x4c
0x292eac: ldmne   r3, {r0, r1, r2, r3}
0x292eb0: stmne   ip, {r0, r1, r2, r3}
0x292eb4: add     ip, ip, #0x10
0x292eb8: str     ip, [r4, #0x28]
0x292ebc: mov     r0, r8
0x292ec0: add     r6, r6, #1
0x292ec4: bl      #0x2069fc   ; <<_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_ME>>
0x292ec8: ldr     r3, [r7]
0x292ecc: ldr     r2, [r7, #4]
0x292ed0: add     r5, r5, #0xc
0x292ed4: rsb     r2, r3, r2
0x292ed8: asr     r2, r2, #2
0x292edc: add     r1, r2, r2, lsl #2
0x292ee0: add     r1, r1, r1, lsl #4
0x292ee4: add     r1, r1, r1, lsl #8
0x292ee8: add     r1, r1, r1, lsl #16
0x292eec: add     r1, r2, r1, lsl #1
0x292ef0: cmp     r6, r1
0x292ef4: bhs     #0x292fc8
0x292ef8: add     r3, r3, r5
0x292efc: ldr     r1, [sp, #0x1c]
0x292f00: mov     r0, r8
0x292f04: ldr     sb, [r3, #8]
0x292f08: ldr     fp, [sb, #-0xc]
0x292f0c: bl      #0x2c47bc
0x292f10: ldr     ip, [sp, #0xc]
0x292f14: mov     r1, sb
0x292f18: mov     r3, #1
0x292f1c: mov     r2, fp
0x292f20: ldr     r0, [ip]
0x292f24: str     r3, [sp]
0x292f28: ldr     r3, [sp, #0x3c]
0x292f2c: bl      #0x14813c
0x292f30: ldr     r0, [r4, #4]
0x292f34: ldr     r3, [r0]
0x292f38: ldr     r3, [r3, #0x14]
0x292f3c: blx     r3
0x292f40: ldr     ip, [sp, #0x10]
0x292f44: ldr     r3, [sp, #0x18]
0x292f48: ldr     r1, [sp, #0x20]
0x292f4c: str     ip, [sp]
0x292f50: str     r6, [sp, #4]
0x292f54: mov     r2, r0
0x292f58: mov     r0, sl
0x292f5c: bl      #0xa4edc
0x292f60: ldr     ip, [sp, #0xc]
0x292f64: mov     r1, sl
0x292f68: ldr     r0, [ip]
0x292f6c: bl      #0x14931c
0x292f70: ldr     r2, [r7]
0x292f74: ldr     r3, [r4, #0x10]
0x292f78: ldr     ip, [r4, #0x28]
0x292f7c: ldr     r1, [r2, r5]
0x292f80: vmov    s14, r1
0x292f84: vcvt.f32.s32 s15, s14
0x292f88: ldr     r2, [r3, #0x44]
0x292f8c: mov     r1, #0
0x292f90: strb    r1, [sp, #0x58]
0x292f94: ldr     r1, [sp, #0x14]
0x292f98: ldr     r3, [r4, #0x2c]
0x292f9c: ldr     r2, [r2, r1]
0x292fa0: cmp     ip, r3
0x292fa4: vstr    s15, [sp, #0x50]
0x292fa8: str     r2, [sp, #0x54]
0x292fac: str     r0, [sp, #0x4c]
0x292fb0: bne     #0x292ea4
0x292fb4: add     r0, r4, #0x24
0x292fb8: mov     r1, ip
0x292fbc: add     r2, sp, #0x4c
0x292fc0: bl      #0x2ce7f8
0x292fc4: b       #0x292ebc
0x292fc8: ldr     r2, [sp, #0x28]
0x292fcc: ldr     ip, [r2, #0x38]
0x292fd0: ldr     r0, [r2, #0x34]
0x292fd4: rsb     r3, r0, ip
0x292fd8: ldr     r2, [sp, #0x24]
0x292fdc: ldr     r1, [sp, #0x10]
0x292fe0: asr     r3, r3, #2
0x292fe4: add     r2, r2, #0xc
0x292fe8: str     r2, [sp, #0x24]
0x292fec: add     r1, r1, #1
0x292ff0: add     r2, r3, r3, lsl #2
0x292ff4: str     r1, [sp, #0x10]
0x292ff8: add     r2, r2, r2, lsl #4
0x292ffc: add     r2, r2, r2, lsl #8
0x293000: add     r2, r2, r2, lsl #16
0x293004: add     r2, r3, r2, lsl #1
0x293008: cmp     r1, r2
0x29300c: movlo   r3, r0
0x293010: ldrlo   r2, [sp, #0x24]
0x293014: blo     #0x292e50
0x293018: ldr     r2, [r4, #0x10]
0x29301c: ldr     r1, [r2, #0x44]
0x293020: ldr     ip, [sp, #0x18]
0x293024: ldr     r0, [sp, #0x30]
0x293028: add     ip, ip, #1
0x29302c: str     ip, [sp, #0x18]
0x293030: ldr     ip, [sp, #0x14]
0x293034: add     ip, ip, #0x58
0x293038: str     ip, [sp, #0x14]
0x29303c: ldr     ip, [sp, #0x18]
0x293040: cmp     ip, r0
0x293044: bne     #0x292e00
0x293048: ldr     r2, [r2, #0x48]
0x29304c: movw    r3, #0x8ba3
0x293050: movt    r3, #0xba2e
0x293054: rsb     r2, r1, r2
0x293058: asr     r2, r2, #3
0x29305c: mul     r3, r3, r2
0x293060: cmp     r3, #0
0x293064: str     r3, [sp, #0x18]
0x293068: ble     #0x2931e0
0x29306c: movw    r8, #0x6db7
0x293070: movt    r8, #0xb6db
0x293074: mov     sb, #0
0x293078: mov     r3, #0x58
0x29307c: mla     r1, r3, sb, r1
0x293080: ldr     r2, [r1, #0x50]
0x293084: str     r1, [sp, #0x10]
0x293088: ldr     r1, [r1, #0x4c]
0x29308c: rsb     r3, r1, r2
0x293090: asr     r3, r3, #2
0x293094: add     r0, r3, r3, lsl #2
0x293098: add     r0, r0, r0, lsl #4
0x29309c: add     r0, r0, r0, lsl #8
0x2930a0: add     r0, r0, r0, lsl #16
0x2930a4: add     r3, r3, r0, lsl #1
0x2930a8: cmp     r3, #0
0x2930ac: beq     #0x2931c8
0x2930b0: mov     fp, #0
0x2930b4: mov     r3, r1
0x2930b8: mov     ip, fp
0x2930bc: mov     r7, fp
0x2930c0: add     r6, r1, fp
0x2930c4: ldr     r1, [r1, fp]
0x2930c8: ldr     r0, [r6, #4]
0x2930cc: rsb     r1, r1, r0
0x2930d0: asr     r1, r1, #2
0x2930d4: mul     r1, r8, r1
0x2930d8: cmp     r1, #0
0x2930dc: beq     #0x293198
0x2930e0: add     r3, r4, #0x30
0x2930e4: uxtb    sl, ip
0x2930e8: str     r3, [sp, #0xc]
0x2930ec: mov     r5, #0
0x2930f0: str     ip, [sp, #0x14]
0x2930f4: b       #0x293134
0x2930f8: cmp     r3, #0
0x2930fc: add     r5, r5, #1
0x293100: addne   r2, sp, #0x40
0x293104: ldmne   r2, {r0, r1, r2}
0x293108: stmne   r3, {r0, r1, r2}
0x29310c: ldrne   r3, [r4, #0x34]
0x293110: ldr     r2, [r6, #4]
0x293114: add     r3, r3, #0xc
0x293118: str     r3, [r4, #0x34]
0x29311c: ldr     r3, [r6]
0x293120: rsb     r3, r3, r2
0x293124: asr     r3, r3, #2
0x293128: mul     r3, r8, r3
0x29312c: cmp     r5, r3
0x293130: bhs     #0x293188
0x293134: ldr     r3, [r4, #0x34]
0x293138: ldr     r2, [r4, #0x38]
0x29313c: str     sb, [sp, #0x44]
0x293140: cmp     r3, r2
0x293144: strb    sl, [sp, #0x48]
0x293148: strb    r5, [sp, #0x49]
0x29314c: str     r7, [sp, #0x40]
0x293150: strb    r7, [sp, #0x4a]
0x293154: bne     #0x2930f8
0x293158: mov     r1, r3
0x29315c: add     r2, sp, #0x40
0x293160: ldr     r0, [sp, #0xc]
0x293164: add     r5, r5, #1
0x293168: bl      #0x2eaf78   ; <<_ZNSt6vectorI12TEffectEventSaIS0_EE13_M_insert_auxEN9__gnu_cxx17__norm>>
0x29316c: ldr     r2, [r6, #4]
0x293170: ldr     r3, [r6]
0x293174: rsb     r3, r3, r2
0x293178: asr     r3, r3, #2
0x29317c: mul     r3, r8, r3
0x293180: cmp     r5, r3
0x293184: blo     #0x293134
0x293188: ldr     r3, [sp, #0x10]
0x29318c: ldr     ip, [sp, #0x14]
0x293190: ldr     r2, [r3, #0x50]
0x293194: ldr     r3, [r3, #0x4c]
0x293198: rsb     r1, r3, r2
0x29319c: add     ip, ip, #1
0x2931a0: add     fp, fp, #0xc
0x2931a4: asr     r1, r1, #2
0x2931a8: add     r0, r1, r1, lsl #2
0x2931ac: add     r0, r0, r0, lsl #4
0x2931b0: add     r0, r0, r0, lsl #8
0x2931b4: add     r0, r0, r0, lsl #16
0x2931b8: add     r0, r1, r0, lsl #1
0x2931bc: cmp     ip, r0
0x2931c0: movlo   r1, r3
0x2931c4: blo     #0x2930c0
0x2931c8: ldr     ip, [sp, #0x18]
0x2931cc: add     sb, sb, #1
0x2931d0: cmp     sb, ip
0x2931d4: ldrne   r3, [r4, #0x10]
0x2931d8: ldrne   r1, [r3, #0x44]
0x2931dc: bne     #0x293078
0x2931e0: ldr     ip, [sp, #0x34]
0x2931e4: ldr     r2, [sp, #0xdc]
0x2931e8: ldr     r3, [ip]
0x2931ec: cmp     r2, r3
0x2931f0: bne     #0x293208
0x2931f4: add     sp, sp, #0xe4
0x2931f8: pop     {r4, r5, r6, r7, r8, sb, sl, fp, pc}
0x2931fc: ldr     r2, [r0, #8]
0x293200: str     r2, [r0, #0x10]
0x293204: b       #0x292bc8
0x293208: bl      #0xa4dec