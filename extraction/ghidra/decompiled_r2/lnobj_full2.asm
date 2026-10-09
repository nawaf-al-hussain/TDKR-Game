0x489ecc: push    {r4, r5, r6, r7, r8, sb, sl, lr}
0x489ed0: vpush   {d8, d9, d10, d11, d12, d13, d14}
0x489ed4: mov     r7, r0
0x489ed8: ldr     r4, [pc, #0x74c]
0x489edc: sub     sp, sp, #0x420
0x489ee0: ldr     r3, [pc, #0x748]
0x489ee4: sub     sp, sp, #8
0x489ee8: add     r4, pc, r4
0x489eec: ldr     r6, [r4, r3]
0x489ef0: ldr     r0, [r6]
0x489ef4: cmp     r0, #0
0x489ef8: beq     #0x489f70
0x489efc: bl      #0x339914  ; _ZN13CMemoryStream7ReadIntEv
0x489f00: cmn     r0, #1
0x489f04: mov     r5, r0
0x489f08: moveq   r0, #0
0x489f0c: beq     #0x489f70
0x489f10: movw    r3, #0x2666
0x489f14: cmp     r5, r3
0x489f18: beq     #0x48a160
0x489f1c: bgt     #0x489f80
0x489f20: movw    r3, #0x265e
0x489f24: cmp     r5, r3
0x489f28: beq     #0x48a240
0x489f2c: bgt     #0x48a0a8
0x489f30: movw    r3, #0x1011
0x489f34: cmp     r5, r3
0x489f38: beq     #0x48af2c
0x489f3c: ble     #0x48a520
0x489f40: movw    r3, #0x2653
0x489f44: cmp     r5, r3
0x489f48: beq     #0x48a808
0x489f4c: add     r3, r3, #4
0x489f50: cmp     r5, r3
0x489f54: bne     #0x48a4b4
0x489f58: ldr     r3, [pc, #0x6d4]
0x489f5c: ldr     sl, [r4, r3]
0x489f60: ldr     r8, [sl]
0x489f64: cmp     r8, #0
0x489f68: beq     #0x48a6b8
0x489f6c: mov     r0, #1
0x489f70: add     sp, sp, #0x28
0x489f74: add     sp, sp, #0x400
0x489f78: vpop    {d8, d9, d10, d11, d12, d13, d14}
0x489f7c: pop     {r4, r5, r6, r7, r8, sb, sl, pc}
0x489f80: movw    r3, #0x798f
0x489f84: cmp     r5, r3
0x489f88: beq     #0x48a160
0x489f8c: bgt     #0x48a0e0
0x489f90: movw    r3, #0x2669
0x489f94: cmp     r5, r3
0x489f98: beq     #0x48af48
0x489f9c: bgt     #0x48a148
0x489fa0: movw    r3, #0x2667
0x489fa4: cmp     r5, r3
0x489fa8: bne     #0x48a4b4
0x489fac: ldr     r1, [pc, #0x6fc]
0x489fb0: add     r0, sp, #0x340
0x489fb4: ldr     ip, [r6]
0x489fb8: mov     r3, #0
0x489fbc: ldr     r2, [pc, #0x674]
0x489fc0: ldr     r5, [r4, r1]
0x489fc4: add     r2, pc, r2
0x489fc8: mov     r1, ip
0x489fcc: ldr     r4, [ip, #0xc]
0x489fd0: add     lr, r2, #8
0x489fd4: add     ip, r2, #0x24
0x489fd8: str     r3, [sp, #0x35c]
0x489fdc: add     r2, r2, #0x40
0x489fe0: str     r3, [sp, #0x360]
0x489fe4: str     r3, [sp, #0x364]
0x489fe8: add     r5, r5, #0xc
0x489fec: str     r3, [sp, #0x368]
0x489ff0: str     r3, [sp, #0x36c]
0x489ff4: str     r3, [sp, #0x370]
0x489ff8: str     r3, [sp, #0x374]
0x489ffc: str     r3, [sp, #0x378]
0x48a000: str     r3, [sp, #0x37c]
0x48a004: str     lr, [sp, #0x340]
0x48a008: str     ip, [sp, #0x350]
0x48a00c: str     r2, [sp, #0x384]
0x48a010: str     r5, [sp, #0x348]
0x48a014: bl      #0x48d5f4  ; _ZN13CTemplateZone4LoadEP13CMemoryStream
0x48a018: ldr     r0, [r6]
0x48a01c: mov     r1, sp
0x48a020: bl      #0x3399d4  ; _ZN13CMemoryStream4ReadERi
0x48a024: ldr     r0, [r7, #0x140]
0x48a028: ldr     r1, [sp, #0x358]
0x48a02c: bl      #0x2bd360  ; _ZN13CZonesManager13IsMissionZoneEi
0x48a030: cmp     r0, #0
0x48a034: bne     #0x48b0a8
0x48a038: ldr     r1, [pc, #0x5fc]
0x48a03c: mov     r2, #0x218
0x48a040: mov     r0, #0x1e8
0x48a044: add     r1, pc, r1
0x48a048: bl      #0x3e9204  ; _ZnwjPKci
0x48a04c: movw    r1, #0x2667
0x48a050: mov     r4, r0
0x48a054: bl      #0x2b5850  ; _ZN5CZoneC1Ei
0x48a058: mov     r0, r4
0x48a05c: add     r1, sp, #0x340
0x48a060: bl      #0x2b5d68  ; _ZN5CZone6CreateERK13CTemplateZone
0x48a064: ldr     r0, [r7, #0x140]
0x48a068: mov     r1, r4
0x48a06c: bl      #0x2c14f8  ; _ZN13CZonesManager7AddZoneEP5CZone
0x48a070: ldr     r2, [pc, #0x5c8]
0x48a074: ldr     r3, [pc, #0x5c8]
0x48a078: add     r0, sp, #0x348
0x48a07c: add     r2, pc, r2
0x48a080: str     r4, [r7, #0x114]
0x48a084: add     r3, pc, r3
0x48a088: add     r2, r2, #8
0x48a08c: add     r3, r3, #8
0x48a090: str     r2, [sp, #0x384]
0x48a094: str     r2, [sp, #0x350]
0x48a098: str     r3, [sp, #0x340]
0x48a09c: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48a0a0: mov     r0, #1
0x48a0a4: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a0a8: movw    r3, #0x2661
0x48a0ac: cmp     r5, r3
0x48a0b0: beq     #0x48aad0
0x48a0b4: ble     #0x48a4d0
0x48a0b8: movw    r3, #0x2662
0x48a0bc: cmp     r5, r3
0x48a0c0: beq     #0x48af5c
0x48a0c4: add     r3, r3, #2
0x48a0c8: cmp     r5, r3
0x48a0cc: bne     #0x48a4b4
0x48a0d0: ldr     r0, [r6]
0x48a0d4: bl      #0x339914  ; _ZN13CMemoryStream7ReadIntEv
0x48a0d8: mov     r0, #1
0x48a0dc: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a0e0: movw    r3, #0x4051
0x48a0e4: movt    r3, #1
0x48a0e8: cmp     r5, r3
0x48a0ec: beq     #0x48ad00
0x48a0f0: ble     #0x48a4a4
0x48a0f4: movw    r3, #0x869f
0x48a0f8: movt    r3, #1
0x48a0fc: cmp     r5, r3
0x48a100: beq     #0x48aea0
0x48a104: movw    r3, #0xbbb8
0x48a108: movt    r3, #0xd
0x48a10c: cmp     r5, r3
0x48a110: bne     #0x48a4b4
0x48a114: ldr     r1, [pc, #0x52c]
0x48a118: movw    r2, #0x256
0x48a11c: mov     r0, #0x1c
0x48a120: add     r1, pc, r1
0x48a124: bl      #0x3e9204  ; _ZnwjPKci
0x48a128: ldr     r1, [r6]
0x48a12c: mov     r4, r0
0x48a130: bl      #0x2b56f4  ; _ZN9CWorldBoxC1EP13CMemoryStream
0x48a134: ldr     r0, [r7, #0x114]
0x48a138: mov     r1, r4
0x48a13c: bl      #0x2b86b8  ; _ZN5CZone11AddWorldBoxEP9CWorldBox
0x48a140: mov     r0, #1
0x48a144: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a148: movw    r3, #0x267d
0x48a14c: cmp     r5, r3
0x48a150: beq     #0x48afcc
0x48a154: movw    r3, #0x4741
0x48a158: cmp     r5, r3
0x48a15c: bne     #0x48a4b4
0x48a160: mov     r0, #0xb0
0x48a164: bl      #0x3e91f8  ; _Znwj
0x48a168: ldr     r1, [r7, #0x114]
0x48a16c: mov     r4, r0
0x48a170: bl      #0x2a7bb8  ; _ZN15CWayPointObjectC1EP5CZone
0x48a174: mov     r0, r4
0x48a178: ldr     r1, [r6]
0x48a17c: str     r4, [sp, #8]
0x48a180: bl      #0x2a8220  ; _ZN15CWayPointObject6CreateEP13CMemoryStream
0x48a184: ldr     r1, [sp, #8]
0x48a188: ldr     r0, [r7, #0x114]
0x48a18c: bl      #0x2b7f70  ; _ZN5CZone11AddWayPointEP15CWayPointObject
0x48a190: ldr     r2, [r7, #0xe4]
0x48a194: ldr     r1, [r7, #0xe0]
0x48a198: ldr     r3, [sp, #8]
0x48a19c: cmp     r1, r2
0x48a1a0: mov     r2, #0
0x48a1a4: strb    r2, [r3, #0x49]
0x48a1a8: beq     #0x48b110
0x48a1ac: cmp     r1, r2
0x48a1b0: strne   r3, [r1]
0x48a1b4: ldrne   r1, [r7, #0xe0]
0x48a1b8: add     r1, r1, #4
0x48a1bc: str     r1, [r7, #0xe0]
0x48a1c0: movw    r3, #0x798f
0x48a1c4: cmp     r5, r3
0x48a1c8: bne     #0x489f6c
0x48a1cc: ldr     r3, [sp, #8]
0x48a1d0: mov     r4, #1
0x48a1d4: ldr     r5, [r6]
0x48a1d8: strb    r4, [r3, #0x49]
0x48a1dc: mov     r0, r5
0x48a1e0: bl      #0x339b94  ; _ZN13CMemoryStream9ReadFloatEv
0x48a1e4: vmov    s16, r0
0x48a1e8: mov     r0, r5
0x48a1ec: bl      #0x339b94  ; _ZN13CMemoryStream9ReadFloatEv
0x48a1f0: mov     r0, r5
0x48a1f4: bl      #0x339b94  ; _ZN13CMemoryStream9ReadFloatEv
0x48a1f8: ldr     r2, [pc, #0x44c]
0x48a1fc: add     r0, sp, #0x8c
0x48a200: ldr     r1, [r6]
0x48a204: add     r2, pc, r2
0x48a208: mov     r3, #0
0x48a20c: add     r2, r2, #8
0x48a210: str     r3, [sp, #0xa0]
0x48a214: str     r3, [sp, #0xa8]
0x48a218: str     r3, [sp, #0xb8]
0x48a21c: str     r3, [sp, #0xbc]
0x48a220: str     r2, [sp, #0x8c]
0x48a224: bl      #0x2e1000  ; _ZN25CComponentBuiltinCylinder4LoadEP13CMemoryStream
0x48a228: vldr    s15, [sp, #0x90]
0x48a22c: vmul.f32s15, s16, s15
0x48a230: ldr     r3, [sp, #8]
0x48a234: mov     r0, r4
0x48a238: vstr    s15, [r3, #0x50]
0x48a23c: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a240: ldr     r4, [r6]
0x48a244: add     lr, sp, #0x400
0x48a248: ldr     r3, [pc, #0x400]
0x48a24c: mov     r6, #0
0x48a250: add     r0, sp, #0x3d4
0x48a254: str     r6, [sp, #0x3f8]
0x48a258: str     r6, [sp, #0x3fc]
0x48a25c: add     r3, pc, r3
0x48a260: str     r6, [lr]
0x48a264: mov     r1, r4
0x48a268: add     ip, r3, #8
0x48a26c: add     r2, r3, #0x24
0x48a270: mov     lr, #0
0x48a274: str     ip, [sp, #0x3d4]
0x48a278: str     lr, [sp, #0x40c]
0x48a27c: add     r3, r3, #0x40
0x48a280: str     r2, [sp, #0x408]
0x48a284: str     r3, [sp, #0x424]
0x48a288: str     r6, [sp, #0x3e0]
0x48a28c: str     r6, [sp, #0x3e4]
0x48a290: str     r6, [sp, #0x3e8]
0x48a294: str     r6, [sp, #0x3ec]
0x48a298: str     r6, [sp, #0x3f0]
0x48a29c: str     r6, [sp, #0x3f4]
0x48a2a0: bl      #0x1fe924  ; _ZN14CComponentBase4LoadEP13CMemoryStream
0x48a2a4: add     r0, sp, #0x400
0x48a2a8: mov     r1, r4
0x48a2ac: add     r0, r0, #8
0x48a2b0: bl      #0x3c125c  ; _ZN15CComponentLight4LoadEP13CMemoryStream
0x48a2b4: mov     r0, #0x170
0x48a2b8: bl      #0x3e91f8  ; _Znwj
0x48a2bc: add     r1, sp, #0x410
0x48a2c0: add     r1, r1, #4
0x48a2c4: add     r2, sp, #0x3e0
0x48a2c8: ldr     r3, [r1]
0x48a2cc: ldr     r1, [sp, #0x3dc]
0x48a2d0: mov     r4, r0
0x48a2d4: bl      #0x2a0814  ; _ZN21CCustomLightSceneNodeC1EiRKN6glitch4core8vector3dIfEEf
0x48a2d8: vldr    s14, [pc, #0x348]
0x48a2dc: add     r2, sp, #0x410
0x48a2e0: vldr    s15, [r2]
0x48a2e4: vmul.f32s15, s15, s14
0x48a2e8: ldrb    lr, [sp, #0x40c]
0x48a2ec: vmov    s9, lr
0x48a2f0: ldrb    ip, [sp, #0x40d]
0x48a2f4: vmov    s12, ip
0x48a2f8: ldrb    r2, [sp, #0x40e]
0x48a2fc: mov     r0, r4
0x48a300: ldrb    r3, [sp, #0x40f]
0x48a304: add     r1, sp, #0x48
0x48a308: vcvt.f32.s32s11, s12
0x48a30c: vcvt.f32.s32s10, s9
0x48a310: vmov    s9, r2
0x48a314: vcvt.f32.s32s13, s9
0x48a318: vmov    s9, r3
0x48a31c: vcvt.f32.s32s12, s9
0x48a320: vmul.f32s10, s10, s15
0x48a324: vmul.f32s12, s12, s14
0x48a328: vstr    s10, [sp, #0x48]
0x48a32c: vmul.f32s14, s11, s15
0x48a330: vstr    s12, [sp, #0x54]
0x48a334: vmul.f32s15, s13, s15
0x48a338: vstr    s14, [sp, #0x4c]
0x48a33c: vstr    s15, [sp, #0x50]
0x48a340: bl      #0x2a0adc  ; _ZN21CCustomLightSceneNode8setColorERKN6glitch5video7SColorfE
0x48a344: vmov.f32s15, #1.000000e+00
0x48a348: add     r1, sp, #0x410
0x48a34c: add     r1, r1, #4
0x48a350: vldr    s14, [r1]
0x48a354: ldr     r3, [r4, #0x10c]
0x48a358: mov     r0, r4
0x48a35c: ldrb    r2, [r3, #0x66]
0x48a360: str     r6, [r3, #0x40]
0x48a364: orr     r2, r2, #4
0x48a368: strb    r2, [r3, #0x66]
0x48a36c: add     r2, sp, #0x420
0x48a370: vdiv.f32s14, s15, s14
0x48a374: vstr    s15, [r3, #0x38]
0x48a378: vldr    s15, [r2]
0x48a37c: vcvt.s32.f32s15, s15
0x48a380: vstr    s14, [r3, #0x3c]
0x48a384: vmov    r1, s15
0x48a388: bl      #0x2a0b0c  ; _ZN21CCustomLightSceneNode7setTimeEi
0x48a38c: mov     r0, r4
0x48a390: ldr     r1, [sp, #0x418]
0x48a394: bl      #0x2a0b2c  ; _ZN21CCustomLightSceneNode15setMinIntensityEj
0x48a398: ldr     r1, [sp, #0x41c]
0x48a39c: mov     r0, r4
0x48a3a0: bl      #0x2a0b34  ; _ZN21CCustomLightSceneNode15setMaxIntensityEj
0x48a3a4: mov     r0, #0x134
0x48a3a8: bl      #0x3e91f8  ; _Znwj
0x48a3ac: mov     r1, r5
0x48a3b0: mov     r6, r0
0x48a3b4: bl      #0x35aad0  ; _ZN11CGameObjectC1Ei
0x48a3b8: ldr     r3, [r4]
0x48a3bc: mov     r0, r4
0x48a3c0: ldr     r2, [r6]
0x48a3c4: ldr     r3, [r3, #0x58]
0x48a3c8: ldr     r5, [r2, #0x24]
0x48a3cc: blx     r3
0x48a3d0: mov     r1, r0
0x48a3d4: mov     r0, r6
0x48a3d8: blx     r5
0x48a3dc: ldr     r3, [r4]
0x48a3e0: mov     r2, #1
0x48a3e4: str     r4, [sp, #0xc]
0x48a3e8: ldr     r3, [r3, #-0x10]
0x48a3ec: add     r3, r4, r3
0x48a3f0: add     r3, r3, #4
0x48a3f4: dmb     sy
0x48a3f8: ldrex   r1, [r3]
0x48a3fc: add     r1, r1, r2
0x48a400: strex   ip, r1, [r3]
0x48a404: teq     ip, #0
0x48a408: bne     #0x48a3f8
0x48a40c: dmb     sy
0x48a410: add     r5, sp, #0x18
0x48a414: mov     r0, r6
0x48a418: sub     r1, r5, #0xc
0x48a41c: bl      #0x35dc24  ; _ZN11CGameObject12SetSceneNodeEN5boost13intrusive_ptrIN6glitch5scene10ISceneNode
0x48a420: ldr     r3, [sp, #0xc]
0x48a424: cmp     r3, #0
0x48a428: beq     #0x48a43c
0x48a42c: ldr     r2, [r3]
0x48a430: ldr     r0, [r2, #-0x10]
0x48a434: add     r0, r3, r0
0x48a438: bl      #0x1fd770  ; _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48a43c: ldr     r3, [r6]
0x48a440: mov     r1, r4
0x48a444: mov     r0, r5
0x48a448: ldr     r4, [r3, #0x28]
0x48a44c: bl      #0x965d9c  ; _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
0x48a450: mov     r2, #1
0x48a454: mov     r0, r6
0x48a458: mov     r1, r5
0x48a45c: blx     r4
0x48a460: ldr     r3, [r6]
0x48a464: ldrb    r1, [sp, #0x3d8]
0x48a468: mov     r0, r6
0x48a46c: ldr     r3, [r3, #0x50]
0x48a470: blx     r3
0x48a474: mov     r0, r6
0x48a478: ldrb    r1, [sp, #0x405]
0x48a47c: bl      #0x35dc8c  ; _ZN11CGameObject16SetAlwaysVisibleEb
0x48a480: mov     r0, r6
0x48a484: ldrb    r1, [sp, #0x406]
0x48a488: bl      #0x35dd84  ; _ZN11CGameObject15SetAlwaysUpdateEb
0x48a48c: mov     r0, r6
0x48a490: ldr     r1, [r7, #0x114]
0x48a494: mov     r2, #2
0x48a498: bl      #0x35f424  ; _ZN11CGameObject11SetInitZoneEP5CZonet
0x48a49c: mov     r0, #1
0x48a4a0: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a4a4: movw    r3, #0x4050
0x48a4a8: movt    r3, #1
0x48a4ac: cmp     r5, r3
0x48a4b0: beq     #0x48ac58
0x48a4b4: ldr     r0, [r7, #0xa94]
0x48a4b8: mov     r1, r5
0x48a4bc: ldr     r2, [r6]
0x48a4c0: ldr     r3, [r7, #0x114]
0x48a4c4: bl      #0x36774c  ; _ZN18CGameObjectManager12CreateObjectEiP13CMemoryStreamP5CZone
0x48a4c8: mov     r0, #1
0x48a4cc: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a4d0: movw    r3, #0x265f
0x48a4d4: cmp     r5, r3
0x48a4d8: bne     #0x48a4b4
0x48a4dc: ldr     r1, [pc, #0x170]
0x48a4e0: movw    r2, #0x24e
0x48a4e4: mov     r0, #0xb0
0x48a4e8: add     r1, pc, r1
0x48a4ec: bl      #0x3e9204  ; _ZnwjPKci
0x48a4f0: mov     r5, r0
0x48a4f4: bl      #0x2b9cf4  ; _ZN11CZonePortalC1Ev
0x48a4f8: mov     r0, r5
0x48a4fc: ldr     r1, [r6]
0x48a500: bl      #0x2b9dec  ; _ZN11CZonePortal6CreateEP13CMemoryStream
0x48a504: ldr     r3, [pc, #0x14c]
0x48a508: mov     r1, r5
0x48a50c: ldr     r3, [r4, r3]
0x48a510: ldr     r0, [r3]
0x48a514: bl      #0x2b544c  ; _ZN20CPortalVisibilityMgr9AddPortalEP11CZonePortal
0x48a518: mov     r0, #1
0x48a51c: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a520: movw    r3, #0xbba
0x48a524: cmp     r5, r3
0x48a528: bne     #0x48a4b4
0x48a52c: mov     r3, #0
0x48a530: ldr     sb, [pc, #0x124]
0x48a534: str     r3, [sp, #0x394]
0x48a538: mov     r2, #0
0x48a53c: str     r3, [sp, #0x398]
0x48a540: add     sb, pc, sb
0x48a544: str     r3, [sp, #0x39c]
0x48a548: add     sl, sb, #8
0x48a54c: str     r3, [sp, #0x3a0]
0x48a550: add     r8, sb, #0x24
0x48a554: str     r3, [sp, #0x3a4]
0x48a558: add     sb, sb, #0x40
0x48a55c: str     r3, [sp, #0x3a8]
0x48a560: add     r0, sp, #0x388
0x48a564: str     r3, [sp, #0x3ac]
0x48a568: str     r3, [sp, #0x3b0]
0x48a56c: str     r3, [sp, #0x3b4]
0x48a570: ldr     r3, [pc, #0x138]
0x48a574: str     r2, [sp, #0x3c0]
0x48a578: str     r2, [sp, #0x3c4]
0x48a57c: str     r2, [sp, #0x3c8]
0x48a580: str     sl, [sp, #0x388]
0x48a584: str     r8, [sp, #0x3bc]
0x48a588: str     sb, [sp, #0x3cc]
0x48a58c: ldr     r3, [r4, r3]
0x48a590: ldr     r1, [r6]
0x48a594: add     r3, r3, #0xc
0x48a598: str     r3, [sp, #0x3d0]
0x48a59c: bl      #0x48d708  ; _ZN17CTemplateMetaZone4LoadEP13CMemoryStream
0x48a5a0: ldr     r1, [pc, #0xb8]
0x48a5a4: mov     r2, #0x238
0x48a5a8: mov     r0, #0x1e8
0x48a5ac: add     r1, pc, r1
0x48a5b0: bl      #0x3e9204  ; _ZnwjPKci
0x48a5b4: mov     r1, r5
0x48a5b8: mov     r4, r0
0x48a5bc: bl      #0x2b5850  ; _ZN5CZoneC1Ei
0x48a5c0: mov     r0, r4
0x48a5c4: add     r1, sp, #0x388
0x48a5c8: bl      #0x2b5fc8  ; _ZN5CZone14CreateMetaZoneERK17CTemplateMetaZone
0x48a5cc: ldr     r0, [r7, #0x140]
0x48a5d0: mov     r1, r4
0x48a5d4: bl      #0x2c14f8  ; _ZN13CZonesManager7AddZoneEP5CZone
0x48a5d8: str     r4, [r7, #0x114]
0x48a5dc: add     r0, sp, #0x3d0
0x48a5e0: str     sl, [sp, #0x388]
0x48a5e4: str     r8, [sp, #0x3bc]
0x48a5e8: str     sb, [sp, #0x3cc]
0x48a5ec: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48a5f0: ldr     r0, [sp, #0x3c0]
0x48a5f4: ldr     r2, [pc, #0x68]
0x48a5f8: ldr     r3, [pc, #0x68]
0x48a5fc: cmp     r0, #0
0x48a600: add     r2, pc, r2
0x48a604: add     r3, pc, r3
0x48a608: add     r2, r2, #8
0x48a60c: add     r3, r3, #8
0x48a610: str     r2, [sp, #0x3cc]
0x48a614: str     r3, [sp, #0x3bc]
0x48a618: beq     #0x489f6c
0x48a61c: bl      #0x3e9260  ; _ZdlPv
0x48a620: mov     r0, #1
0x48a624: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a628: bllo    #0xfe4aa834
0x48a62c: rsbseq  lr, r7, r0, asr #23
0x48a630: .word 0xfffff5a4   (data/skipped)
0x48a634: .word 0xfffff4a4   (data/skipped)
0x48a638: .word 0x0075399c   (data/skipped)
0x48a63c: rsbeq   sl, fp, ip, lsr #30
0x48a640: rsbseq  r6, r4, r4, ror #24
0x48a644: rsbseq  lr, r4, r4, ror #16
0x48a648: rsbeq   sl, fp, r0, asr lr
0x48a64c: rsbseq  sb, r4, ip, asr r0
0x48a650: rsbseq  r3, r5, ip, ror r7
0x48a654: rsbeq   sl, fp, r8, lsl #21
0x48a658: .word 0xfffff488   (data/skipped)
0x48a65c: rsbseq  r3, r5, r8, asr #7
0x48a660: rsbeq   sl, fp, r4, asr #19
0x48a664: rsbseq  r6, r4, r0, ror #13
0x48a668: rsbseq  lr, r4, r4, lsl #5
0x48a66c: rsbeq   sl, fp, ip, lsr #17
0x48a670: .word 0x00746390   (data/skipped)
0x48a674: rsbeq   sl, fp, r8, lsl #15
0x48a678: rsbseq  r3, r5, r4, ror #3
0x48a67c: .word 0xfffff590   (data/skipped)
0x48a680: rsbseq  sb, r4, r0, asr #1
0x48a684: ldrsbteqr2, [r5], #-0xe0
0x48a688: rsbeq   sl, fp, ip, lsr r4
0x48a68c: rsbeq   sl, fp, r8, asr r4
0x48a690: .word 0xfffff464   (data/skipped)
0x48a694: rsbseq  sp, r4, r8, ror #29
0x48a698: rsbseq  r6, r4, ip, lsl r0
0x48a69c: rsbseq  r8, r4, r0, ror #29
0x48a6a0: .word 0xfffff468   (data/skipped)
0x48a6a4: .word 0x00748e90   (data/skipped)
0x48a6a8: rsbseq  r5, r4, r4, ror pc
0x48a6ac: rsbseq  r8, r4, r4, lsr lr
0x48a6b0: .word 0xfffff20c   (data/skipped)
0x48a6b4: vstmialolr, {s30, s31}
0x48a6b8: ldr     r1, [pc, #-0x54]
0x48a6bc: mov     r2, #0x260
0x48a6c0: mov     r0, #0x12c
0x48a6c4: add     r1, pc, r1
0x48a6c8: bl      #0x3e9204  ; _ZnwjPKci
0x48a6cc: mov     r1, r8
0x48a6d0: mov     r2, #0x12c
0x48a6d4: mov     r5, r0
0x48a6d8: bl      #0xa4e88  ; 0xa4e88
0x48a6dc: ldr     r2, [pc, #-0x34]
0x48a6e0: mov     ip, #0
0x48a6e4: ldr     r3, [pc, #-0x7c]
0x48a6e8: mov     r0, r5
0x48a6ec: ldr     r1, [r4, r2]
0x48a6f0: add     r3, pc, r3
0x48a6f4: add     lr, r3, #8
0x48a6f8: add     r2, r3, #0x24
0x48a6fc: add     r1, r1, #0xc
0x48a700: add     r3, r3, #0x40
0x48a704: str     ip, [r5, #0xc4]
0x48a708: str     ip, [r5, #0xc8]
0x48a70c: str     ip, [r5, #0xd0]
0x48a710: str     ip, [r5, #0xd4]
0x48a714: str     ip, [r5, #0xf8]
0x48a718: str     ip, [r5, #0xfc]
0x48a71c: str     ip, [r5, #0x100]
0x48a720: str     ip, [r5, #0x104]
0x48a724: str     ip, [r5, #0x118]
0x48a728: str     ip, [r5, #0x11c]
0x48a72c: str     r1, [r5, #4]
0x48a730: str     r1, [r5, #8]
0x48a734: str     r1, [r5, #0xc]
0x48a738: str     r1, [r5, #0x10]
0x48a73c: str     r1, [r5, #0x14]
0x48a740: str     r1, [r5, #0x18]
0x48a744: str     r1, [r5, #0x20]
0x48a748: str     r1, [r5, #0x34]
0x48a74c: str     r1, [r5, #0xac]
0x48a750: str     r1, [r5, #0xec]
0x48a754: str     r1, [r5, #0xf0]
0x48a758: str     r1, [r5, #0xf4]
0x48a75c: str     r1, [r5, #0x108]
0x48a760: str     r8, [r5, #0x24]
0x48a764: str     r8, [r5, #0x28]
0x48a768: str     r8, [r5, #0x2c]
0x48a76c: str     r8, [r5, #0xcc]
0x48a770: str     r8, [r5, #0xd8]
0x48a774: str     r8, [r5, #0xdc]
0x48a778: str     r8, [r5, #0xe0]
0x48a77c: str     r8, [r5, #0xe4]
0x48a780: str     r8, [r5, #0x114]
0x48a784: str     ip, [r5, #0x120]
0x48a788: str     lr, [r5]
0x48a78c: str     r3, [r5, #0xb8]
0x48a790: ldr     r1, [r6]
0x48a794: str     r2, [r5, #0xa4]
0x48a798: str     r8, [r5, #0x124]
0x48a79c: str     r5, [sl]
0x48a7a0: bl      #0x2023bc  ; _ZN24CTemplateLevelProperties4LoadEP13CMemoryStream
0x48a7a4: bl      #0x3dac58  ; _ZN11Application11GetInstanceEv
0x48a7a8: movw    r3, #0x1fc6
0x48a7ac: movt    r3, #1
0x48a7b0: ldrb    r3, [r0, r3]
0x48a7b4: cmp     r3, #0
0x48a7b8: beq     #0x48a7dc
0x48a7bc: vmov.f32s15, #3.000000e+00
0x48a7c0: ldr     r3, [sl]
0x48a7c4: vldr    s14, [r3, #0x58]
0x48a7c8: vldr    s13, [r3, #0x5c]
0x48a7cc: vmul.f32s14, s14, s15
0x48a7d0: vmul.f32s15, s13, s15
0x48a7d4: vstr    s14, [r3, #0x58]
0x48a7d8: vstr    s15, [r3, #0x5c]
0x48a7dc: ldr     r1, [pc, #-0x170]
0x48a7e0: movw    r2, #0x269
0x48a7e4: mov     r0, #0xec
0x48a7e8: add     r1, pc, r1
0x48a7ec: bl      #0x3e9204  ; _ZnwjPKci
0x48a7f0: ldr     r1, [sl]
0x48a7f4: mov     r4, r0
0x48a7f8: bl      #0x40ce18  ; _ZN15CWeatherManagerC1EP24CTemplateLevelProperties
0x48a7fc: str     r4, [r7, #0xa98]
0x48a800: mov     r0, #1
0x48a804: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48a808: mov     r2, #0
0x48a80c: str     r2, [sp, #0x2c0]
0x48a810: str     r2, [sp, #0x2c4]
0x48a814: add     r0, sp, #0x2b4
0x48a818: str     r2, [sp, #0x2c8]
0x48a81c: mov     r7, #0x3f800000
0x48a820: str     r2, [sp, #0x2cc]
0x48a824: str     r2, [sp, #0x2d0]
0x48a828: str     r2, [sp, #0x2d4]
0x48a82c: str     r2, [sp, #0x2d8]
0x48a830: str     r2, [sp, #0x2dc]
0x48a834: str     r2, [sp, #0x2e0]
0x48a838: ldr     r2, [pc, #-0x190]
0x48a83c: ldr     r3, [pc, #-0x1cc]
0x48a840: ldr     r1, [r6]
0x48a844: add     r6, sp, #0x274
0x48a848: ldr     r2, [r4, r2]
0x48a84c: add     r3, pc, r3
0x48a850: add     r5, r3, #8
0x48a854: add     r3, r3, #0x24
0x48a858: add     r2, r2, #0xc
0x48a85c: str     r3, [sp, #0x2e8]
0x48a860: str     r2, [sp, #0x2ec]
0x48a864: str     r5, [sp, #0x2b4]
0x48a868: bl      #0x48d308  ; _ZN17CTemplateOccluder4LoadEP13CMemoryStream
0x48a86c: mov     r1, #0
0x48a870: mov     r2, #0x40
0x48a874: add     r0, sp, #0xf4
0x48a878: bl      #0xa4e88  ; 0xa4e88
0x48a87c: mov     r1, #0
0x48a880: mov     r2, #0x40
0x48a884: add     r0, sp, #0x134
0x48a888: str     r7, [sp, #0xf4]
0x48a88c: str     r7, [sp, #0x108]
0x48a890: str     r7, [sp, #0x11c]
0x48a894: str     r7, [sp, #0x130]
0x48a898: bl      #0xa4e88  ; 0xa4e88
0x48a89c: mov     r1, #0
0x48a8a0: mov     r2, #0x40
0x48a8a4: add     r0, sp, #0x174
0x48a8a8: str     r7, [sp, #0x170]
0x48a8ac: bl      #0xa4e88  ; 0xa4e88
0x48a8b0: vldr    s15, [pc, #-0x204]
0x48a8b4: vldr    s14, [sp, #0x2cc]
0x48a8b8: vmul.f32s16, s14, s15
0x48a8bc: ldr     r1, [sp, #0x2c0]
0x48a8c0: vldr    s14, [sp, #0x2d0]
0x48a8c4: ldr     r2, [sp, #0x2c4]
0x48a8c8: ldr     r3, [sp, #0x2c8]
0x48a8cc: str     r1, [sp, #0x124]
0x48a8d0: str     r2, [sp, #0x128]
0x48a8d4: str     r3, [sp, #0x12c]
0x48a8d8: str     r7, [sp, #0x1b0]
0x48a8dc: vmov    r0, s16
0x48a8e0: vmul.f32s17, s14, s15
0x48a8e4: vldr    s14, [sp, #0x2d4]
0x48a8e8: vmul.f32s18, s14, s15
0x48a8ec: bl      #0xa70f60  ; cosf
0x48a8f0: vmov    s9, r0
0x48a8f4: vmov    r0, s16
0x48a8f8: vcvt.f64.f32d14, s9
0x48a8fc: bl      #0xa711c0  ; sinf
0x48a900: vmov    s12, r0
0x48a904: vmov    r0, s17
0x48a908: vcvt.f64.f32d12, s12
0x48a90c: bl      #0xa70f60  ; cosf
0x48a910: vmov    s13, r0
0x48a914: vmov    r0, s17
0x48a918: vcvt.f64.f32d13, s13
0x48a91c: bl      #0xa711c0  ; sinf
0x48a920: vmov    s16, r0
0x48a924: vmov    r0, s18
0x48a928: bl      #0xa70f60  ; cosf
0x48a92c: vcvt.f64.f32d11, s16
0x48a930: vneg.f32s16, s16
0x48a934: vmov    s15, r0
0x48a938: vmov    r0, s18
0x48a93c: vcvt.f64.f32d10, s15
0x48a940: bl      #0xa711c0  ; sinf
0x48a944: ldr     lr, [sp, #0x2d8]
0x48a948: add     r1, sp, #0x134
0x48a94c: ldr     ip, [sp, #0x2dc]
0x48a950: add     r2, sp, #0x174
0x48a954: ldr     r3, [sp, #0x2e0]
0x48a958: vstr    s16, [sp, #0x13c]
0x48a95c: str     lr, [sp, #0x174]
0x48a960: str     ip, [sp, #0x188]
0x48a964: str     r3, [sp, #0x19c]
0x48a968: vmul.f64d5, d11, d12
0x48a96c: vmul.f64d7, d11, d14
0x48a970: vmov    s9, r0
0x48a974: add     r0, sp, #0x234
0x48a978: vcvt.f64.f32d6, s9
0x48a97c: vmul.f64d3, d10, d14
0x48a980: vmul.f64d4, d6, d14
0x48a984: vmul.f64d2, d6, d12
0x48a988: vmul.f64d1, d10, d12
0x48a98c: vmla.f64d3, d5, d6
0x48a990: vnmls.f64d1, d7, d6
0x48a994: vnmls.f64d4, d5, d10
0x48a998: vmla.f64d2, d7, d10
0x48a99c: vmul.f64d0, d6, d13
0x48a9a0: vmul.f64d5, d10, d13
0x48a9a4: vmul.f64d6, d13, d12
0x48a9a8: vmul.f64d7, d13, d14
0x48a9ac: vcvt.f32.f64s10, d5
0x48a9b0: vcvt.f32.f64s0, d0
0x48a9b4: vstr    s10, [sp, #0x134]
0x48a9b8: vcvt.f32.f64s8, d4
0x48a9bc: vstr    s0, [sp, #0x138]
0x48a9c0: vcvt.f32.f64s6, d3
0x48a9c4: vstr    s8, [sp, #0x144]
0x48a9c8: vcvt.f32.f64s12, d6
0x48a9cc: vstr    s6, [sp, #0x148]
0x48a9d0: vcvt.f32.f64s4, d2
0x48a9d4: vstr    s12, [sp, #0x14c]
0x48a9d8: vcvt.f32.f64s2, d1
0x48a9dc: vstr    s4, [sp, #0x154]
0x48a9e0: vcvt.f32.f64s14, d7
0x48a9e4: vstr    s2, [sp, #0x158]
0x48a9e8: vstr    s14, [sp, #0x15c]
0x48a9ec: bl      #0x20e7dc  ; _ZNK6glitch4core6detail12CMatrix4BaseIfE4multERKS3_
0x48a9f0: add     lr, sp, #0x234
0x48a9f4: add     ip, sp, #0x1b4
0x48a9f8: ldm     lr!, {r0, r1, r2, r3}
0x48a9fc: stm     ip!, {r0, r1, r2, r3}
0x48aa00: ldm     lr!, {r0, r1, r2, r3}
0x48aa04: stm     ip!, {r0, r1, r2, r3}
0x48aa08: ldm     lr!, {r0, r1, r2, r3}
0x48aa0c: stm     ip!, {r0, r1, r2, r3}
0x48aa10: ldm     lr, {r0, r1, r2, r3}
0x48aa14: stm     ip, {r0, r1, r2, r3}
0x48aa18: add     r0, sp, #0x274
0x48aa1c: add     r1, sp, #0xf4
0x48aa20: add     r2, sp, #0x1b4
0x48aa24: bl      #0x20e7dc  ; _ZNK6glitch4core6detail12CMatrix4BaseIfE4multERKS3_
0x48aa28: ldm     r6!, {r0, r1, r2, r3}
0x48aa2c: add     ip, sp, #0x1f4
0x48aa30: add     lr, sp, #0xf4
0x48aa34: mov     r7, ip
0x48aa38: stm     ip!, {r0, r1, r2, r3}
0x48aa3c: ldm     r6!, {r0, r1, r2, r3}
0x48aa40: stm     ip!, {r0, r1, r2, r3}
0x48aa44: ldm     r6!, {r0, r1, r2, r3}
0x48aa48: stm     ip!, {r0, r1, r2, r3}
0x48aa4c: ldm     r6, {r0, r1, r2, r3}
0x48aa50: stm     ip, {r0, r1, r2, r3}
0x48aa54: ldm     r7!, {r0, r1, r2, r3}
0x48aa58: stm     lr!, {r0, r1, r2, r3}
0x48aa5c: ldm     r7!, {r0, r1, r2, r3}
0x48aa60: stm     lr!, {r0, r1, r2, r3}
0x48aa64: ldm     r7!, {r0, r1, r2, r3}
0x48aa68: stm     lr!, {r0, r1, r2, r3}
0x48aa6c: ldm     ip, {r0, r1, r2, r3}
0x48aa70: stm     lr, {r0, r1, r2, r3}
0x48aa74: mov     r0, #0x54
0x48aa78: bl      #0x3e91f8  ; _Znwj
0x48aa7c: mov     r6, r0
0x48aa80: bl      #0x191b20  ; _ZN3occ8OccluderC1Ev
0x48aa84: mov     r0, r6
0x48aa88: add     r1, sp, #0xf4
0x48aa8c: ldr     r3, [sp, #0x2f4]
0x48aa90: ldr     r2, [sp, #0x2ec]
0x48aa94: bl      #0x191c5c  ; _ZN3occ8Occluder4initERN6glitch4core8CMatrix4IfEEPKcf
0x48aa98: ldr     r3, [pc, #-0x424]
0x48aa9c: mov     r1, r6
0x48aaa0: ldr     r2, [sp, #0x2bc]
0x48aaa4: ldr     r0, [r4, r3]
0x48aaa8: bl      #0x196268  ; _ZN3occ16OcclusionManager11addOccluderEPNS_8OccluderEi
0x48aaac: ldr     r3, [pc, #-0x434]
0x48aab0: add     r0, sp, #0x2ec
0x48aab4: str     r5, [sp, #0x2b4]
0x48aab8: add     r3, pc, r3
0x48aabc: add     r3, r3, #8
0x48aac0: str     r3, [sp, #0x2e8]
0x48aac4: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48aac8: mov     r0, #1
0x48aacc: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48aad0: ldr     r2, [pc, #-0x428]
0x48aad4: add     r1, sp, #0x7c
0x48aad8: ldr     r5, [r6]
0x48aadc: ldr     r3, [pc, #-0x460]
0x48aae0: ldr     r2, [r4, r2]
0x48aae4: mov     r0, r5
0x48aae8: add     r3, pc, r3
0x48aaec: add     r2, r2, #0xc
0x48aaf0: add     r3, r3, #8
0x48aaf4: str     r2, [sp, #0x7c]
0x48aaf8: str     r3, [sp, #0x78]
0x48aafc: bl      #0x33a0d4  ; _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorI
0x48ab00: mov     r0, r5
0x48ab04: bl      #0x3395d8  ; _ZN13CMemoryStream8ReadCharEv
0x48ab08: adds    r3, r0, #0
0x48ab0c: mov     r0, r5
0x48ab10: movne   r3, #1
0x48ab14: strb    r3, [sp, #0x80]
0x48ab18: bl      #0x339b94  ; _ZN13CMemoryStream9ReadFloatEv
0x48ab1c: str     r0, [sp, #0x84]
0x48ab20: mov     r0, r5
0x48ab24: bl      #0x339914  ; _ZN13CMemoryStream7ReadIntEv
0x48ab28: ldr     r1, [pc, #-0x4a8]
0x48ab2c: mov     r2, #0x278
0x48ab30: ldr     r6, [sp, #0x7c]
0x48ab34: add     r1, pc, r1
0x48ab38: str     r0, [sp, #0x88]
0x48ab3c: mov     r0, #0x120
0x48ab40: bl      #0x3e9204  ; _ZnwjPKci
0x48ab44: mov     r1, r6
0x48ab48: ldr     r2, [sp, #0x88]
0x48ab4c: mov     r5, r0
0x48ab50: bl      #0x44212c  ; _ZN22CCustomSkyBoxSceneNodeC1EPKci
0x48ab54: ldr     r3, [r5]
0x48ab58: mov     r0, r5
0x48ab5c: ldr     r1, [pc, #-0x4d8]
0x48ab60: ldr     r3, [r3, #0x34]
0x48ab64: add     r1, pc, r1
0x48ab68: blx     r3
0x48ab6c: ldr     r3, [pc, #-0x4e4]
0x48ab70: ldr     r6, [r4, r3]
0x48ab74: ldr     r3, [r6]
0x48ab78: ldr     r4, [r3, #0x180]
0x48ab7c: cmp     r4, #0
0x48ab80: beq     #0x48abb4
0x48ab84: ldr     r3, [r4]
0x48ab88: mov     r2, #1
0x48ab8c: ldr     r3, [r3, #-0x10]
0x48ab90: add     r3, r4, r3
0x48ab94: add     r3, r3, #4
0x48ab98: dmb     sy
0x48ab9c: ldrex   r1, [r3]
0x48aba0: add     r1, r1, r2
0x48aba4: strex   ip, r1, [r3]
0x48aba8: teq     ip, #0
0x48abac: bne     #0x48ab9c
0x48abb0: dmb     sy
0x48abb4: ldr     r2, [r5]
0x48abb8: mov     r1, #1
0x48abbc: ldr     r3, [r4]
0x48abc0: str     r5, [sp, #4]
0x48abc4: ldr     r2, [r2, #-0x10]
0x48abc8: ldr     r3, [r3, #0x68]
0x48abcc: add     r2, r5, r2
0x48abd0: add     r2, r2, #4
0x48abd4: dmb     sy
0x48abd8: ldrex   r0, [r2]
0x48abdc: add     r0, r0, r1
0x48abe0: strex   lr, r0, [r2]
0x48abe4: teq     lr, #0
0x48abe8: bne     #0x48abd8
0x48abec: dmb     sy
0x48abf0: add     r1, sp, #4
0x48abf4: mov     r0, r4
0x48abf8: blx     r3
0x48abfc: ldr     r3, [sp, #4]
0x48ac00: cmp     r3, #0
0x48ac04: beq     #0x48ac18
0x48ac08: ldr     r2, [r3]
0x48ac0c: ldr     r0, [r2, #-0x10]
0x48ac10: add     r0, r3, r0
0x48ac14: bl      #0x1fd770  ; _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ac18: ldr     r3, [r4]
0x48ac1c: ldr     r0, [r3, #-0x10]
0x48ac20: add     r0, r4, r0
0x48ac24: bl      #0x1fd770  ; _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ac28: ldr     r0, [r6]
0x48ac2c: mov     r1, #0xb
0x48ac30: mov     r2, r5
0x48ac34: bl      #0x32ad4c  ; _ZN17CNovaSceneManager14SetRecursiveIdEiPN6glitch5scene10ISceneNodeE
0x48ac38: ldr     r3, [pc, #-0x5ac]
0x48ac3c: add     r0, sp, #0x7c
0x48ac40: add     r3, pc, r3
0x48ac44: add     r3, r3, #8
0x48ac48: str     r3, [sp, #0x78]
0x48ac4c: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48ac50: mov     r0, #1
0x48ac54: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48ac58: mov     r3, #0
0x48ac5c: ldr     r1, [pc, #-0x5cc]
0x48ac60: str     r3, [sp, #0xcc]
0x48ac64: add     r0, sp, #0xc0
0x48ac68: str     r3, [sp, #0xd0]
0x48ac6c: add     r1, pc, r1
0x48ac70: str     r3, [sp, #0xd4]
0x48ac74: add     r1, r1, #8
0x48ac78: str     r3, [sp, #0xd8]
0x48ac7c: str     r3, [sp, #0xdc]
0x48ac80: str     r3, [sp, #0xe0]
0x48ac84: str     r3, [sp, #0xe4]
0x48ac88: str     r3, [sp, #0xe8]
0x48ac8c: str     r3, [sp, #0xec]
0x48ac90: ldr     r2, [pc, #-0x5fc]
0x48ac94: ldr     r3, [pc, #-0x5ec]
0x48ac98: add     r2, pc, r2
0x48ac9c: str     r1, [sp, #0xc0]
0x48aca0: add     r2, r2, #8
0x48aca4: str     r2, [sp, #0x30]
0x48aca8: ldr     r3, [r4, r3]
0x48acac: ldr     r1, [r6]
0x48acb0: add     r3, r3, #0xc
0x48acb4: str     r3, [sp, #0x34]
0x48acb8: bl      #0x1fe924  ; _ZN14CComponentBase4LoadEP13CMemoryStream
0x48acbc: add     r0, sp, #0x30
0x48acc0: ldr     r1, [r6]
0x48acc4: bl      #0x2d6ddc  ; _ZN14CComponentMesh4LoadEP13CMemoryStream
0x48acc8: ldr     r3, [pc, #-0x630]
0x48accc: ldr     r3, [r4, r3]
0x48acd0: ldr     r3, [r3]
0x48acd4: ldrb    r3, [r3, #0x3a]
0x48acd8: cmp     r3, #0
0x48acdc: bne     #0x48affc
0x48ace0: ldr     r3, [pc, #-0x644]
0x48ace4: add     r0, sp, #0x34
0x48ace8: add     r3, pc, r3
0x48acec: add     r3, r3, #8
0x48acf0: str     r3, [sp, #0x30]
0x48acf4: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48acf8: mov     r0, #1
0x48acfc: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48ad00: mov     r3, #0
0x48ad04: ldr     r1, [pc, #-0x664]
0x48ad08: str     r3, [sp, #0xcc]
0x48ad0c: add     r0, sp, #0xc0
0x48ad10: str     r3, [sp, #0xd0]
0x48ad14: add     r1, pc, r1
0x48ad18: str     r3, [sp, #0xd4]
0x48ad1c: add     r1, r1, #8
0x48ad20: str     r3, [sp, #0xd8]
0x48ad24: add     r5, sp, #0x18
0x48ad28: str     r3, [sp, #0xdc]
0x48ad2c: str     r3, [sp, #0xe0]
0x48ad30: str     r3, [sp, #0xe4]
0x48ad34: str     r3, [sp, #0xe8]
0x48ad38: str     r3, [sp, #0xec]
0x48ad3c: ldr     r2, [pc, #-0x698]
0x48ad40: ldr     r3, [pc, #-0x698]
0x48ad44: add     r2, pc, r2
0x48ad48: str     r1, [sp, #0xc0]
0x48ad4c: add     r2, r2, #8
0x48ad50: str     r2, [sp, #0x30]
0x48ad54: ldr     r3, [r4, r3]
0x48ad58: ldr     r1, [r6]
0x48ad5c: add     r3, r3, #0xc
0x48ad60: str     r3, [sp, #0x34]
0x48ad64: bl      #0x1fe924  ; _ZN14CComponentBase4LoadEP13CMemoryStream
0x48ad68: add     r0, sp, #0x30
0x48ad6c: ldr     r1, [r6]
0x48ad70: bl      #0x2d6ddc  ; _ZN14CComponentMesh4LoadEP13CMemoryStream
0x48ad74: sub     r0, r5, #8
0x48ad78: ldr     r1, [sp, #0x34]
0x48ad7c: bl      #0x20414c  ; _Z21ConstructColladaScenePKc
0x48ad80: ldr     r0, [sp, #0x10]
0x48ad84: cmp     r0, #0
0x48ad88: beq     #0x48ae80
0x48ad8c: ldr     r3, [r0]
0x48ad90: add     r1, sp, #0xcc
0x48ad94: ldr     r3, [r3, #0xb8]
0x48ad98: blx     r3
0x48ad9c: ldr     r0, [sp, #0x10]
0x48ada0: add     r1, sp, #0xe4
0x48ada4: ldr     r3, [r0]
0x48ada8: ldr     r3, [r3, #0xa8]
0x48adac: blx     r3
0x48adb0: vldr    s15, [pc, #0x368]
0x48adb4: vldr    s14, [sp, #0xd8]
0x48adb8: vmul.f32s13, s14, s15
0x48adbc: ldr     r4, [sp, #0x10]
0x48adc0: vldr    s14, [sp, #0xdc]
0x48adc4: add     r1, sp, #0x3c
0x48adc8: add     r0, sp, #0x68
0x48adcc: ldr     r3, [r4]
0x48add0: ldr     r6, [r3, #0xb0]
0x48add4: vmul.f32s14, s14, s15
0x48add8: vstr    s13, [sp, #0x3c]
0x48addc: vldr    s13, [sp, #0xe0]
0x48ade0: vmul.f32s15, s13, s15
0x48ade4: vstr    s14, [sp, #0x40]
0x48ade8: vstr    s15, [sp, #0x44]
0x48adec: bl      #0x48d1dc  ; _ZN6glitch4core10quaternionC1ERKNS0_8vector3dIfEE
0x48adf0: mov     r0, r4
0x48adf4: add     r1, sp, #0x68
0x48adf8: blx     r6
0x48adfc: ldr     r3, [sp, #0x10]
0x48ae00: cmp     r3, #0
0x48ae04: str     r3, [sp, #0x14]
0x48ae08: beq     #0x48ae3c
0x48ae0c: ldr     r1, [r3]
0x48ae10: mov     r2, #1
0x48ae14: ldr     r1, [r1, #-0x10]
0x48ae18: add     r3, r3, r1
0x48ae1c: add     r3, r3, #4
0x48ae20: dmb     sy
0x48ae24: ldrex   r1, [r3]
0x48ae28: add     r1, r1, r2
0x48ae2c: strex   ip, r1, [r3]
0x48ae30: teq     ip, #0
0x48ae34: bne     #0x48ae24
0x48ae38: dmb     sy
0x48ae3c: mov     r0, r7
0x48ae40: sub     r1, r5, #4
0x48ae44: bl      #0x48b140  ; _ZN6CLevel26AddLowPolyLongDistanceNodeEN5boost13intrusive_ptrIN6glitch5scene10IS
0x48ae48: ldr     r3, [sp, #0x14]
0x48ae4c: cmp     r3, #0
0x48ae50: beq     #0x48ae64
0x48ae54: ldr     r2, [r3]
0x48ae58: ldr     r0, [r2, #-0x10]
0x48ae5c: add     r0, r3, r0
0x48ae60: bl      #0x1fd770  ; _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ae64: ldr     r3, [sp, #0x10]
0x48ae68: cmp     r3, #0
0x48ae6c: beq     #0x48ae80
0x48ae70: ldr     r2, [r3]
0x48ae74: ldr     r0, [r2, #-0x10]
0x48ae78: add     r0, r3, r0
0x48ae7c: bl      #0x1fd770  ; _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ae80: ldr     r3, [pc, #0x29c]
0x48ae84: add     r0, sp, #0x34
0x48ae88: add     r3, pc, r3
0x48ae8c: add     r3, r3, #8
0x48ae90: str     r3, [sp, #0x30]
0x48ae94: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48ae98: mov     r0, #1
0x48ae9c: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48aea0: mov     r3, #0
0x48aea4: str     r3, [sp, #0x304]
0x48aea8: str     r3, [sp, #0x308]
0x48aeac: add     r0, sp, #0x2f8
0x48aeb0: str     r3, [sp, #0x30c]
0x48aeb4: str     r3, [sp, #0x310]
0x48aeb8: str     r3, [sp, #0x314]
0x48aebc: str     r3, [sp, #0x318]
0x48aec0: str     r3, [sp, #0x31c]
0x48aec4: str     r3, [sp, #0x320]
0x48aec8: str     r3, [sp, #0x324]
0x48aecc: ldr     r3, [pc, #0x254]
0x48aed0: ldr     r2, [pc, #0x254]
0x48aed4: ldr     r1, [r6]
0x48aed8: ldr     r3, [r4, r3]
0x48aedc: add     r2, pc, r2
0x48aee0: add     r5, r2, #8
0x48aee4: add     r2, r2, #0x24
0x48aee8: add     r3, r3, #0xc
0x48aeec: str     r2, [sp, #0x32c]
0x48aef0: str     r3, [sp, #0x330]
0x48aef4: str     r3, [sp, #0x338]
0x48aef8: str     r5, [sp, #0x2f8]
0x48aefc: bl      #0x48d870  ; _ZN18CTemplateBakeGroup4LoadEP13CMemoryStream
0x48af00: ldr     r3, [pc, #0x228]
0x48af04: add     r0, sp, #0x338
0x48af08: str     r5, [sp, #0x2f8]
0x48af0c: add     r3, pc, r3
0x48af10: add     r3, r3, #8
0x48af14: str     r3, [sp, #0x32c]
0x48af18: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48af1c: add     r0, sp, #0x330
0x48af20: bl      #0x2069fc  ; _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE
0x48af24: mov     r0, #1
0x48af28: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48af2c: ldr     r0, [r7, #0x114]
0x48af30: cmp     r0, #0
0x48af34: beq     #0x489f6c
0x48af38: ldr     r1, [r6]
0x48af3c: bl      #0x2b95dc  ; _ZN5CZone20LoadIrradianceVolumeEP13CMemoryStream
0x48af40: mov     r0, #1
0x48af44: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48af48: ldr     r0, [r7, #0xa98]
0x48af4c: ldr     r1, [r6]
0x48af50: bl      #0x40e994  ; _ZN15CWeatherManager22LoadGlobalIlluminationEP13CMemoryStream
0x48af54: mov     r0, #1
0x48af58: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48af5c: mov     r0, #0x18c
0x48af60: bl      #0x3e91f8  ; _Znwj
0x48af64: mov     r1, r5
0x48af68: mov     r8, r0
0x48af6c: bl      #0x2a76c0  ; _ZN17CSpawnPointObjectC1Ei
0x48af70: mov     r0, r8
0x48af74: ldr     r1, [r6]
0x48af78: bl      #0x2a7840  ; _ZN17CSpawnPointObject6CreateEP13CMemoryStream
0x48af7c: mov     r0, r8
0x48af80: bl      #0x2a7a50  ; _ZNK17CSpawnPointObject17IsLevelStartPointEv
0x48af84: cmp     r0, #0
0x48af88: beq     #0x48afb4
0x48af8c: ldr     r3, [r8]
0x48af90: mov     r0, r8
0x48af94: ldr     r3, [r3, #0x14]
0x48af98: blx     r3
0x48af9c: ldr     r3, [pc, #0x190]
0x48afa0: mov     r2, #1
0x48afa4: str     r0, [r7, #0x10c]
0x48afa8: str     r0, [r7, #0x110]
0x48afac: ldr     r3, [r4, r3]
0x48afb0: strb    r2, [r3]
0x48afb4: mov     r0, r8
0x48afb8: ldr     r1, [r7, #0x114]
0x48afbc: mov     r2, #8
0x48afc0: bl      #0x35f424  ; _ZN11CGameObject11SetInitZoneEP5CZonet
0x48afc4: mov     r0, #1
0x48afc8: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48afcc: mov     r0, #0x68
0x48afd0: bl      #0x3e91f8  ; _Znwj
0x48afd4: mov     r4, r0
0x48afd8: bl      #0x1d163c  ; _ZN12CNavMeshNovaC1Ev
0x48afdc: mov     r0, r4
0x48afe0: ldr     r1, [r6]
0x48afe4: bl      #0x1d17cc  ; _ZN12CNavMeshNova6CreateEP13CMemoryStream
0x48afe8: mov     r0, r7
0x48afec: mov     r1, r4
0x48aff0: bl      #0x484ac0  ; _ZN6CLevel10SetNavMeshEP12CNavMeshNova
0x48aff4: mov     r0, #1
0x48aff8: b       #0x489f70  ; _ZN6CLevel14LoadNextObjectEv
0x48affc: ldr     r1, [sp, #0x34]
0x48b000: add     r0, sp, #0x10
0x48b004: bl      #0x20414c  ; _Z21ConstructColladaScenePKc
0x48b008: ldr     r0, [sp, #0x10]
0x48b00c: add     r1, sp, #0xcc
0x48b010: ldr     r3, [r0]
0x48b014: ldr     r3, [r3, #0xb8]
0x48b018: blx     r3
0x48b01c: ldr     r0, [sp, #0x10]
0x48b020: add     r1, sp, #0xe4
0x48b024: ldr     r3, [r0]
0x48b028: ldr     r3, [r3, #0xa8]
0x48b02c: blx     r3
0x48b030: vldr    s15, [pc, #0xe8]
0x48b034: vldr    s14, [sp, #0xd8]
0x48b038: vmul.f32s13, s14, s15
0x48b03c: ldr     r4, [sp, #0x10]
0x48b040: vldr    s14, [sp, #0xdc]
0x48b044: add     r1, sp, #0x24
0x48b048: add     r0, sp, #0x58
0x48b04c: ldr     r3, [r4]
0x48b050: ldr     r5, [r3, #0xb0]
0x48b054: vmul.f32s14, s14, s15
0x48b058: vstr    s13, [sp, #0x24]
0x48b05c: vldr    s13, [sp, #0xe0]
0x48b060: vmul.f32s15, s13, s15
0x48b064: vstr    s14, [sp, #0x28]
0x48b068: vstr    s15, [sp, #0x2c]
0x48b06c: bl      #0x48d1dc  ; _ZN6glitch4core10quaternionC1ERKNS0_8vector3dIfEE
0x48b070: mov     r0, r4
0x48b074: add     r1, sp, #0x58
0x48b078: blx     r5
0x48b07c: mov     r0, r7
0x48b080: ldr     r1, [sp, #0x10]
0x48b084: bl      #0x479afc  ; _ZN6CLevel22AddBatchNodeReflectionEPN6glitch5scene10ISceneNodeE
0x48b088: ldr     r3, [sp, #0x10]
0x48b08c: cmp     r3, #0
0x48b090: beq     #0x48ace0
0x48b094: ldr     r2, [r3]
0x48b098: ldr     r0, [r2, #-0x10]
0x48b09c: add     r0, r3, r0
0x48b0a0: bl      #0x1fd770  ; _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48b0a4: b       #0x48ace0  ; _ZN6CLevel14LoadNextObjectEv
0x48b0a8: ldr     r0, [r7, #0x140]
0x48b0ac: ldr     r1, [sp, #0x358]
0x48b0b0: bl      #0x2bd3e4  ; _ZN13CZonesManager20IsCurrentMissionZoneEi
0x48b0b4: cmp     r0, #0
0x48b0b8: bne     #0x48a038
0x48b0bc: ldr     r3, [r6]
0x48b0c0: sub     r4, r4, #4
0x48b0c4: ldr     r0, [r7, #0x140]
0x48b0c8: mov     r2, r4
0x48b0cc: ldr     r1, [sp, #0x358]
0x48b0d0: ldr     r3, [r3, #0xc]
0x48b0d4: rsb     r4, r4, r3
0x48b0d8: ldr     r3, [sp]
0x48b0dc: add     r3, r4, r3
0x48b0e0: bl      #0x2bd1d8  ; _ZN13CZonesManager16UpdateZoneOffsetEiii
0x48b0e4: ldr     r1, [r6]
0x48b0e8: ldr     r2, [pc, #0x48]
0x48b0ec: add     r0, sp, #0x348
0x48b0f0: ldr     r3, [pc, #0x44]
0x48b0f4: ldr     lr, [r1, #0xc]
0x48b0f8: add     r2, pc, r2
0x48b0fc: ldr     ip, [sp]
0x48b100: add     r3, pc, r3
0x48b104: add     ip, lr, ip
0x48b108: str     ip, [r1, #0xc]
0x48b10c: b       #0x48a088  ; _ZN6CLevel14LoadNextObjectEv
0x48b110: add     r0, r7, #0xdc
0x48b114: add     r2, sp, #8
0x48b118: bl      #0x2eb5a0  ; _ZNSt6vectorIP15CWayPointObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_ite
0x48b11c: b       #0x48a1c0  ; _ZN6CLevel14LoadNextObjectEv
0x48b120: vstmialolr, {s30, s31}
0x48b124: ldrshteqr8, [r4], #-0xc0
0x48b128: .word 0xfffff20c   (data/skipped)
0x48b12c: ldrshteqr2, [r5], #-0x94
0x48b130: ldrshteqsp, [r4], #-0xcc
0x48b134: .word 0xfffff6e0   (data/skipped)
0x48b138: rsbseq  r5, r4, r8, ror #23
0x48b13c: rsbseq  sp, r4, r8, ror #15
