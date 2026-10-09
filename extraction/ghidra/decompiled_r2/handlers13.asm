
===== h2653_Occluder  0x48a808..0x48a9f0 =====
0x48a808: mov      r2, #0
0x48a80c: str      r2, [sp, #0x2c0]
0x48a810: str      r2, [sp, #0x2c4]
0x48a814: add      r0, sp, #0x2b4
0x48a818: str      r2, [sp, #0x2c8]
0x48a81c: mov      r7, #0x3f800000
0x48a820: str      r2, [sp, #0x2cc]
0x48a824: str      r2, [sp, #0x2d0]
0x48a828: str      r2, [sp, #0x2d4]
0x48a82c: str      r2, [sp, #0x2d8]
0x48a830: str      r2, [sp, #0x2dc]
0x48a834: str      r2, [sp, #0x2e0]
0x48a838: ldr      r2, [pc, #-0x190]
0x48a83c: ldr      r3, [pc, #-0x1cc]
0x48a840: ldr      r1, [r6]
0x48a844: add      r6, sp, #0x274
0x48a848: ldr      r2, [r4, r2]
0x48a84c: add      r3, pc, r3
0x48a850: add      r5, r3, #8
0x48a854: add      r3, r3, #0x24
0x48a858: add      r2, r2, #0xc
0x48a85c: str      r3, [sp, #0x2e8]
0x48a860: str      r2, [sp, #0x2ec]
0x48a864: str      r5, [sp, #0x2b4]
0x48a868: bl       #0x48d308  ; 17CTemplateOccluder4LoadEP13CMemoryStream
0x48a86c: mov      r1, #0
0x48a870: mov      r2, #0x40
0x48a874: add      r0, sp, #0xf4
0x48a878: bl       #0xa4e88  ; 0xa4e88
0x48a87c: mov      r1, #0
0x48a880: mov      r2, #0x40
0x48a884: add      r0, sp, #0x134
0x48a888: str      r7, [sp, #0xf4]
0x48a88c: str      r7, [sp, #0x108]
0x48a890: str      r7, [sp, #0x11c]
0x48a894: str      r7, [sp, #0x130]
0x48a898: bl       #0xa4e88  ; 0xa4e88
0x48a89c: mov      r1, #0
0x48a8a0: mov      r2, #0x40
0x48a8a4: add      r0, sp, #0x174
0x48a8a8: str      r7, [sp, #0x170]
0x48a8ac: bl       #0xa4e88  ; 0xa4e88
0x48a8b0: vldr     s15, [pc, #-0x204]
0x48a8b4: vldr     s14, [sp, #0x2cc]
0x48a8b8: vmul.f32 s16, s14, s15
0x48a8bc: ldr      r1, [sp, #0x2c0]
0x48a8c0: vldr     s14, [sp, #0x2d0]
0x48a8c4: ldr      r2, [sp, #0x2c4]
0x48a8c8: ldr      r3, [sp, #0x2c8]
0x48a8cc: str      r1, [sp, #0x124]
0x48a8d0: str      r2, [sp, #0x128]
0x48a8d4: str      r3, [sp, #0x12c]
0x48a8d8: str      r7, [sp, #0x1b0]
0x48a8dc: vmov     r0, s16
0x48a8e0: vmul.f32 s17, s14, s15
0x48a8e4: vldr     s14, [sp, #0x2d4]
0x48a8e8: vmul.f32 s18, s14, s15
0x48a8ec: bl       #0xa70f60  ; cosf
0x48a8f0: vmov     s9, r0
0x48a8f4: vmov     r0, s16
0x48a8f8: vcvt.f64.f32 d14, s9
0x48a8fc: bl       #0xa711c0  ; sinf
0x48a900: vmov     s12, r0
0x48a904: vmov     r0, s17
0x48a908: vcvt.f64.f32 d12, s12
0x48a90c: bl       #0xa70f60  ; cosf
0x48a910: vmov     s13, r0
0x48a914: vmov     r0, s17
0x48a918: vcvt.f64.f32 d13, s13
0x48a91c: bl       #0xa711c0  ; sinf
0x48a920: vmov     s16, r0
0x48a924: vmov     r0, s18
0x48a928: bl       #0xa70f60  ; cosf
0x48a92c: vcvt.f64.f32 d11, s16
0x48a930: vneg.f32 s16, s16
0x48a934: vmov     s15, r0
0x48a938: vmov     r0, s18
0x48a93c: vcvt.f64.f32 d10, s15
0x48a940: bl       #0xa711c0  ; sinf
0x48a944: ldr      lr, [sp, #0x2d8]
0x48a948: add      r1, sp, #0x134
0x48a94c: ldr      ip, [sp, #0x2dc]
0x48a950: add      r2, sp, #0x174
0x48a954: ldr      r3, [sp, #0x2e0]
0x48a958: vstr     s16, [sp, #0x13c]
0x48a95c: str      lr, [sp, #0x174]
0x48a960: str      ip, [sp, #0x188]
0x48a964: str      r3, [sp, #0x19c]
0x48a968: vmul.f64 d5, d11, d12
0x48a96c: vmul.f64 d7, d11, d14
0x48a970: vmov     s9, r0
0x48a974: add      r0, sp, #0x234
0x48a978: vcvt.f64.f32 d6, s9
0x48a97c: vmul.f64 d3, d10, d14
0x48a980: vmul.f64 d4, d6, d14
0x48a984: vmul.f64 d2, d6, d12
0x48a988: vmul.f64 d1, d10, d12
0x48a98c: vmla.f64 d3, d5, d6
0x48a990: vnmls.f64 d1, d7, d6
0x48a994: vnmls.f64 d4, d5, d10
0x48a998: vmla.f64 d2, d7, d10
0x48a99c: vmul.f64 d0, d6, d13
0x48a9a0: vmul.f64 d5, d10, d13
0x48a9a4: vmul.f64 d6, d13, d12
0x48a9a8: vmul.f64 d7, d13, d14
0x48a9ac: vcvt.f32.f64 s10, d5
0x48a9b0: vcvt.f32.f64 s0, d0
0x48a9b4: vstr     s10, [sp, #0x134]
0x48a9b8: vcvt.f32.f64 s8, d4
0x48a9bc: vstr     s0, [sp, #0x138]
0x48a9c0: vcvt.f32.f64 s6, d3
0x48a9c4: vstr     s8, [sp, #0x144]
0x48a9c8: vcvt.f32.f64 s12, d6
0x48a9cc: vstr     s6, [sp, #0x148]
0x48a9d0: vcvt.f32.f64 s4, d2
0x48a9d4: vstr     s12, [sp, #0x14c]
0x48a9d8: vcvt.f32.f64 s2, d1
0x48a9dc: vstr     s4, [sp, #0x154]
0x48a9e0: vcvt.f32.f64 s14, d7
0x48a9e4: vstr     s2, [sp, #0x158]
0x48a9e8: vstr     s14, [sp, #0x15c]
0x48a9ec: bl       #0x20e7dc  ; K6glitch4core6detail12CMatrix4BaseIfE4multERKS3_

===== h265e  0x48a240..0x48a2c0 =====
0x48a240: ldr      r4, [r6]
0x48a244: add      lr, sp, #0x400
0x48a248: ldr      r3, [pc, #0x400]
0x48a24c: mov      r6, #0
0x48a250: add      r0, sp, #0x3d4
0x48a254: str      r6, [sp, #0x3f8]
0x48a258: str      r6, [sp, #0x3fc]
0x48a25c: add      r3, pc, r3
0x48a260: str      r6, [lr]
0x48a264: mov      r1, r4
0x48a268: add      ip, r3, #8
0x48a26c: add      r2, r3, #0x24
0x48a270: mov      lr, #0
0x48a274: str      ip, [sp, #0x3d4]
0x48a278: str      lr, [sp, #0x40c]
0x48a27c: add      r3, r3, #0x40
0x48a280: str      r2, [sp, #0x408]
0x48a284: str      r3, [sp, #0x424]
0x48a288: str      r6, [sp, #0x3e0]
0x48a28c: str      r6, [sp, #0x3e4]
0x48a290: str      r6, [sp, #0x3e8]
0x48a294: str      r6, [sp, #0x3ec]
0x48a298: str      r6, [sp, #0x3f0]
0x48a29c: str      r6, [sp, #0x3f4]
0x48a2a0: bl       #0x1fe924  ; 14CComponentBase4LoadEP13CMemoryStream
0x48a2a4: add      r0, sp, #0x400
0x48a2a8: mov      r1, r4
0x48a2ac: add      r0, r0, #8
0x48a2b0: bl       #0x3c125c  ; 15CComponentLight4LoadEP13CMemoryStream
0x48a2b4: mov      r0, #0x170
0x48a2b8: bl       #0x3e91f8  ; _Znwj
0x48a2bc: add      r1, sp, #0x410

===== h2661  0x48aad0..0x48ad00 =====
0x48aad0: ldr      r2, [pc, #-0x428]
0x48aad4: add      r1, sp, #0x7c
0x48aad8: ldr      r5, [r6]
0x48aadc: ldr      r3, [pc, #-0x460]
0x48aae0: ldr      r2, [r4, r2]
0x48aae4: mov      r0, r5
0x48aae8: add      r3, pc, r3
0x48aaec: add      r2, r2, #0xc
0x48aaf0: add      r3, r3, #8
0x48aaf4: str      r2, [sp, #0x7c]
0x48aaf8: str      r3, [sp, #0x78]
0x48aafc: bl       #0x33a0d4  ; 13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAll
0x48ab00: mov      r0, r5
0x48ab04: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48ab08: adds     r3, r0, #0
0x48ab0c: mov      r0, r5
0x48ab10: movne    r3, #1
0x48ab14: strb     r3, [sp, #0x80]
0x48ab18: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48ab1c: str      r0, [sp, #0x84]
0x48ab20: mov      r0, r5
0x48ab24: bl       #0x339914  ; 13CMemoryStream7ReadIntEv
0x48ab28: ldr      r1, [pc, #-0x4a8]
0x48ab2c: mov      r2, #0x278
0x48ab30: ldr      r6, [sp, #0x7c]
0x48ab34: add      r1, pc, r1
0x48ab38: str      r0, [sp, #0x88]
0x48ab3c: mov      r0, #0x120
0x48ab40: bl       #0x3e9204  ; _ZnwjPKci
0x48ab44: mov      r1, r6
0x48ab48: ldr      r2, [sp, #0x88]
0x48ab4c: mov      r5, r0
0x48ab50: bl       #0x44212c  ; 22CCustomSkyBoxSceneNodeC1EPKci
0x48ab54: ldr      r3, [r5]
0x48ab58: mov      r0, r5
0x48ab5c: ldr      r1, [pc, #-0x4d8]
0x48ab60: ldr      r3, [r3, #0x34]
0x48ab64: add      r1, pc, r1
0x48ab68: blx      r3
0x48ab6c: ldr      r3, [pc, #-0x4e4]
0x48ab70: ldr      r6, [r4, r3]
0x48ab74: ldr      r3, [r6]
0x48ab78: ldr      r4, [r3, #0x180]
0x48ab7c: cmp      r4, #0
0x48ab80: beq      #0x48abb4
0x48ab84: ldr      r3, [r4]
0x48ab88: mov      r2, #1
0x48ab8c: ldr      r3, [r3, #-0x10]
0x48ab90: add      r3, r4, r3
0x48ab94: add      r3, r3, #4
0x48ab98: dmb      sy
0x48ab9c: ldrex    r1, [r3]
0x48aba0: add      r1, r1, r2
0x48aba4: strex    ip, r1, [r3]
0x48aba8: teq      ip, #0
0x48abac: bne      #0x48ab9c
0x48abb0: dmb      sy
0x48abb4: ldr      r2, [r5]
0x48abb8: mov      r1, #1
0x48abbc: ldr      r3, [r4]
0x48abc0: str      r5, [sp, #4]
0x48abc4: ldr      r2, [r2, #-0x10]
0x48abc8: ldr      r3, [r3, #0x68]
0x48abcc: add      r2, r5, r2
0x48abd0: add      r2, r2, #4
0x48abd4: dmb      sy
0x48abd8: ldrex    r0, [r2]
0x48abdc: add      r0, r0, r1
0x48abe0: strex    lr, r0, [r2]
0x48abe4: teq      lr, #0
0x48abe8: bne      #0x48abd8
0x48abec: dmb      sy
0x48abf0: add      r1, sp, #4
0x48abf4: mov      r0, r4
0x48abf8: blx      r3
0x48abfc: ldr      r3, [sp, #4]
0x48ac00: cmp      r3, #0
0x48ac04: beq      #0x48ac18
0x48ac08: ldr      r2, [r3]
0x48ac0c: ldr      r0, [r2, #-0x10]
0x48ac10: add      r0, r3, r0
0x48ac14: bl       #0x1fd770  ; 6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ac18: ldr      r3, [r4]
0x48ac1c: ldr      r0, [r3, #-0x10]
0x48ac20: add      r0, r4, r0
0x48ac24: bl       #0x1fd770  ; 6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ac28: ldr      r0, [r6]
0x48ac2c: mov      r1, #0xb
0x48ac30: mov      r2, r5
0x48ac34: bl       #0x32ad4c  ; 17CNovaSceneManager14SetRecursiveIdEiPN6glitch5scene10ISceneNodeE
0x48ac38: ldr      r3, [pc, #-0x5ac]
0x48ac3c: add      r0, sp, #0x7c
0x48ac40: add      r3, pc, r3
0x48ac44: add      r3, r3, #8
0x48ac48: str      r3, [sp, #0x78]
0x48ac4c: bl       #0x2069fc  ; SbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMOR
0x48ac50: mov      r0, #1
0x48ac54: b        #0x489f70  ; 6CLevel14LoadNextObjectEv
0x48ac58: mov      r3, #0
0x48ac5c: ldr      r1, [pc, #-0x5cc]
0x48ac60: str      r3, [sp, #0xcc]
0x48ac64: add      r0, sp, #0xc0
0x48ac68: str      r3, [sp, #0xd0]
0x48ac6c: add      r1, pc, r1
0x48ac70: str      r3, [sp, #0xd4]
0x48ac74: add      r1, r1, #8
0x48ac78: str      r3, [sp, #0xd8]
0x48ac7c: str      r3, [sp, #0xdc]
0x48ac80: str      r3, [sp, #0xe0]
0x48ac84: str      r3, [sp, #0xe4]
0x48ac88: str      r3, [sp, #0xe8]
0x48ac8c: str      r3, [sp, #0xec]
0x48ac90: ldr      r2, [pc, #-0x5fc]
0x48ac94: ldr      r3, [pc, #-0x5ec]
0x48ac98: add      r2, pc, r2
0x48ac9c: str      r1, [sp, #0xc0]
0x48aca0: add      r2, r2, #8
0x48aca4: str      r2, [sp, #0x30]
0x48aca8: ldr      r3, [r4, r3]
0x48acac: ldr      r1, [r6]
0x48acb0: add      r3, r3, #0xc
0x48acb4: str      r3, [sp, #0x34]
0x48acb8: bl       #0x1fe924  ; 14CComponentBase4LoadEP13CMemoryStream
0x48acbc: add      r0, sp, #0x30
0x48acc0: ldr      r1, [r6]
0x48acc4: bl       #0x2d6ddc  ; 14CComponentMesh4LoadEP13CMemoryStream
0x48acc8: ldr      r3, [pc, #-0x630]
0x48accc: ldr      r3, [r4, r3]
0x48acd0: ldr      r3, [r3]
0x48acd4: ldrb     r3, [r3, #0x3a]
0x48acd8: cmp      r3, #0
0x48acdc: bne      #0x48affc
0x48ace0: ldr      r3, [pc, #-0x644]
0x48ace4: add      r0, sp, #0x34
0x48ace8: add      r3, pc, r3
0x48acec: add      r3, r3, #8
0x48acf0: str      r3, [sp, #0x30]
0x48acf4: bl       #0x2069fc  ; SbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMOR
0x48acf8: mov      r0, #1
0x48acfc: b        #0x489f70  ; 6CLevel14LoadNextObjectEv

===== h1404051  0x48ad00..0x48aea0 =====
0x48ad00: mov      r3, #0
0x48ad04: ldr      r1, [pc, #-0x664]
0x48ad08: str      r3, [sp, #0xcc]
0x48ad0c: add      r0, sp, #0xc0
0x48ad10: str      r3, [sp, #0xd0]
0x48ad14: add      r1, pc, r1
0x48ad18: str      r3, [sp, #0xd4]
0x48ad1c: add      r1, r1, #8
0x48ad20: str      r3, [sp, #0xd8]
0x48ad24: add      r5, sp, #0x18
0x48ad28: str      r3, [sp, #0xdc]
0x48ad2c: str      r3, [sp, #0xe0]
0x48ad30: str      r3, [sp, #0xe4]
0x48ad34: str      r3, [sp, #0xe8]
0x48ad38: str      r3, [sp, #0xec]
0x48ad3c: ldr      r2, [pc, #-0x698]
0x48ad40: ldr      r3, [pc, #-0x698]
0x48ad44: add      r2, pc, r2
0x48ad48: str      r1, [sp, #0xc0]
0x48ad4c: add      r2, r2, #8
0x48ad50: str      r2, [sp, #0x30]
0x48ad54: ldr      r3, [r4, r3]
0x48ad58: ldr      r1, [r6]
0x48ad5c: add      r3, r3, #0xc
0x48ad60: str      r3, [sp, #0x34]
0x48ad64: bl       #0x1fe924  ; 14CComponentBase4LoadEP13CMemoryStream
0x48ad68: add      r0, sp, #0x30
0x48ad6c: ldr      r1, [r6]
0x48ad70: bl       #0x2d6ddc  ; 14CComponentMesh4LoadEP13CMemoryStream
0x48ad74: sub      r0, r5, #8
0x48ad78: ldr      r1, [sp, #0x34]
0x48ad7c: bl       #0x20414c  ; _Z21ConstructColladaScenePKc
0x48ad80: ldr      r0, [sp, #0x10]
0x48ad84: cmp      r0, #0
0x48ad88: beq      #0x48ae80
0x48ad8c: ldr      r3, [r0]
0x48ad90: add      r1, sp, #0xcc
0x48ad94: ldr      r3, [r3, #0xb8]
0x48ad98: blx      r3
0x48ad9c: ldr      r0, [sp, #0x10]
0x48ada0: add      r1, sp, #0xe4
0x48ada4: ldr      r3, [r0]
0x48ada8: ldr      r3, [r3, #0xa8]
0x48adac: blx      r3
0x48adb0: vldr     s15, [pc, #0x368]
0x48adb4: vldr     s14, [sp, #0xd8]
0x48adb8: vmul.f32 s13, s14, s15
0x48adbc: ldr      r4, [sp, #0x10]
0x48adc0: vldr     s14, [sp, #0xdc]
0x48adc4: add      r1, sp, #0x3c
0x48adc8: add      r0, sp, #0x68
0x48adcc: ldr      r3, [r4]
0x48add0: ldr      r6, [r3, #0xb0]
0x48add4: vmul.f32 s14, s14, s15
0x48add8: vstr     s13, [sp, #0x3c]
0x48addc: vldr     s13, [sp, #0xe0]
0x48ade0: vmul.f32 s15, s13, s15
0x48ade4: vstr     s14, [sp, #0x40]
0x48ade8: vstr     s15, [sp, #0x44]
0x48adec: bl       #0x48d1dc  ; 6glitch4core10quaternionC1ERKNS0_8vector3dIfEE
0x48adf0: mov      r0, r4
0x48adf4: add      r1, sp, #0x68
0x48adf8: blx      r6
0x48adfc: ldr      r3, [sp, #0x10]
0x48ae00: cmp      r3, #0
0x48ae04: str      r3, [sp, #0x14]
0x48ae08: beq      #0x48ae3c
0x48ae0c: ldr      r1, [r3]
0x48ae10: mov      r2, #1
0x48ae14: ldr      r1, [r1, #-0x10]
0x48ae18: add      r3, r3, r1
0x48ae1c: add      r3, r3, #4
0x48ae20: dmb      sy
0x48ae24: ldrex    r1, [r3]
0x48ae28: add      r1, r1, r2
0x48ae2c: strex    ip, r1, [r3]
0x48ae30: teq      ip, #0
0x48ae34: bne      #0x48ae24
0x48ae38: dmb      sy
0x48ae3c: mov      r0, r7
0x48ae40: sub      r1, r5, #4
0x48ae44: bl       #0x48b140  ; 6CLevel26AddLowPolyLongDistanceNodeEN5boost13intrusive_ptrIN6glitch5sc
0x48ae48: ldr      r3, [sp, #0x14]
0x48ae4c: cmp      r3, #0
0x48ae50: beq      #0x48ae64
0x48ae54: ldr      r2, [r3]
0x48ae58: ldr      r0, [r2, #-0x10]
0x48ae5c: add      r0, r3, r0
0x48ae60: bl       #0x1fd770  ; 6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ae64: ldr      r3, [sp, #0x10]
0x48ae68: cmp      r3, #0
0x48ae6c: beq      #0x48ae80
0x48ae70: ldr      r2, [r3]
0x48ae74: ldr      r0, [r2, #-0x10]
0x48ae78: add      r0, r3, r0
0x48ae7c: bl       #0x1fd770  ; 6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48ae80: ldr      r3, [pc, #0x29c]
0x48ae84: add      r0, sp, #0x34
0x48ae88: add      r3, pc, r3
0x48ae8c: add      r3, r3, #8
0x48ae90: str      r3, [sp, #0x30]
0x48ae94: bl       #0x2069fc  ; SbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMOR
0x48ae98: mov      r0, #1
0x48ae9c: b        #0x489f70  ; 6CLevel14LoadNextObjectEv

===== h1869f_branch  0x48aea0..0x48af48 =====
0x48aea0: mov      r3, #0
0x48aea4: str      r3, [sp, #0x304]
0x48aea8: str      r3, [sp, #0x308]
0x48aeac: add      r0, sp, #0x2f8
0x48aeb0: str      r3, [sp, #0x30c]
0x48aeb4: str      r3, [sp, #0x310]
0x48aeb8: str      r3, [sp, #0x314]
0x48aebc: str      r3, [sp, #0x318]
0x48aec0: str      r3, [sp, #0x31c]
0x48aec4: str      r3, [sp, #0x320]
0x48aec8: str      r3, [sp, #0x324]
0x48aecc: ldr      r3, [pc, #0x254]
0x48aed0: ldr      r2, [pc, #0x254]
0x48aed4: ldr      r1, [r6]
0x48aed8: ldr      r3, [r4, r3]
0x48aedc: add      r2, pc, r2
0x48aee0: add      r5, r2, #8
0x48aee4: add      r2, r2, #0x24
0x48aee8: add      r3, r3, #0xc
0x48aeec: str      r2, [sp, #0x32c]
0x48aef0: str      r3, [sp, #0x330]
0x48aef4: str      r3, [sp, #0x338]
0x48aef8: str      r5, [sp, #0x2f8]
0x48aefc: bl       #0x48d870  ; 18CTemplateBakeGroup4LoadEP13CMemoryStream
0x48af00: ldr      r3, [pc, #0x228]
0x48af04: add      r0, sp, #0x338
0x48af08: str      r5, [sp, #0x2f8]
0x48af0c: add      r3, pc, r3
0x48af10: add      r3, r3, #8
0x48af14: str      r3, [sp, #0x32c]
0x48af18: bl       #0x2069fc  ; SbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMOR
0x48af1c: add      r0, sp, #0x330
0x48af20: bl       #0x2069fc  ; SbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMOR
0x48af24: mov      r0, #1
0x48af28: b        #0x489f70  ; 6CLevel14LoadNextObjectEv
0x48af2c: ldr      r0, [r7, #0x114]
0x48af30: cmp      r0, #0
0x48af34: beq      #0x489f6c
0x48af38: ldr      r1, [r6]
0x48af3c: bl       #0x2b95dc  ; 5CZone20LoadIrradianceVolumeEP13CMemoryStream
0x48af40: mov      r0, #1
0x48af44: b        #0x489f70  ; 6CLevel14LoadNextObjectEv

===== h2669  0x48af48..0x48af5c =====
0x48af48: ldr      r0, [r7, #0xa98]
0x48af4c: ldr      r1, [r6]
0x48af50: bl       #0x40e994  ; 15CWeatherManager22LoadGlobalIlluminationEP13CMemoryStream
0x48af54: mov      r0, #1
0x48af58: b        #0x489f70  ; 6CLevel14LoadNextObjectEv

===== h2662  0x48af5c..0x48b0a8 =====
0x48af5c: mov      r0, #0x18c
0x48af60: bl       #0x3e91f8  ; _Znwj
0x48af64: mov      r1, r5
0x48af68: mov      r8, r0
0x48af6c: bl       #0x2a76c0  ; 17CSpawnPointObjectC1Ei
0x48af70: mov      r0, r8
0x48af74: ldr      r1, [r6]
0x48af78: bl       #0x2a7840  ; 17CSpawnPointObject6CreateEP13CMemoryStream
0x48af7c: mov      r0, r8
0x48af80: bl       #0x2a7a50  ; K17CSpawnPointObject17IsLevelStartPointEv
0x48af84: cmp      r0, #0
0x48af88: beq      #0x48afb4
0x48af8c: ldr      r3, [r8]
0x48af90: mov      r0, r8
0x48af94: ldr      r3, [r3, #0x14]
0x48af98: blx      r3
0x48af9c: ldr      r3, [pc, #0x190]
0x48afa0: mov      r2, #1
0x48afa4: str      r0, [r7, #0x10c]
0x48afa8: str      r0, [r7, #0x110]
0x48afac: ldr      r3, [r4, r3]
0x48afb0: strb     r2, [r3]
0x48afb4: mov      r0, r8
0x48afb8: ldr      r1, [r7, #0x114]
0x48afbc: mov      r2, #8
0x48afc0: bl       #0x35f424  ; 11CGameObject11SetInitZoneEP5CZonet
0x48afc4: mov      r0, #1
0x48afc8: b        #0x489f70  ; 6CLevel14LoadNextObjectEv
0x48afcc: mov      r0, #0x68
0x48afd0: bl       #0x3e91f8  ; _Znwj
0x48afd4: mov      r4, r0
0x48afd8: bl       #0x1d163c  ; 12CNavMeshNovaC1Ev
0x48afdc: mov      r0, r4
0x48afe0: ldr      r1, [r6]
0x48afe4: bl       #0x1d17cc  ; 12CNavMeshNova6CreateEP13CMemoryStream
0x48afe8: mov      r0, r7
0x48afec: mov      r1, r4
0x48aff0: bl       #0x484ac0  ; 6CLevel10SetNavMeshEP12CNavMeshNova
0x48aff4: mov      r0, #1
0x48aff8: b        #0x489f70  ; 6CLevel14LoadNextObjectEv
0x48affc: ldr      r1, [sp, #0x34]
0x48b000: add      r0, sp, #0x10
0x48b004: bl       #0x20414c  ; _Z21ConstructColladaScenePKc
0x48b008: ldr      r0, [sp, #0x10]
0x48b00c: add      r1, sp, #0xcc
0x48b010: ldr      r3, [r0]
0x48b014: ldr      r3, [r3, #0xb8]
0x48b018: blx      r3
0x48b01c: ldr      r0, [sp, #0x10]
0x48b020: add      r1, sp, #0xe4
0x48b024: ldr      r3, [r0]
0x48b028: ldr      r3, [r3, #0xa8]
0x48b02c: blx      r3
0x48b030: vldr     s15, [pc, #0xe8]
0x48b034: vldr     s14, [sp, #0xd8]
0x48b038: vmul.f32 s13, s14, s15
0x48b03c: ldr      r4, [sp, #0x10]
0x48b040: vldr     s14, [sp, #0xdc]
0x48b044: add      r1, sp, #0x24
0x48b048: add      r0, sp, #0x58
0x48b04c: ldr      r3, [r4]
0x48b050: ldr      r5, [r3, #0xb0]
0x48b054: vmul.f32 s14, s14, s15
0x48b058: vstr     s13, [sp, #0x24]
0x48b05c: vldr     s13, [sp, #0xe0]
0x48b060: vmul.f32 s15, s13, s15
0x48b064: vstr     s14, [sp, #0x28]
0x48b068: vstr     s15, [sp, #0x2c]
0x48b06c: bl       #0x48d1dc  ; 6glitch4core10quaternionC1ERKNS0_8vector3dIfEE
0x48b070: mov      r0, r4
0x48b074: add      r1, sp, #0x58
0x48b078: blx      r5
0x48b07c: mov      r0, r7
0x48b080: ldr      r1, [sp, #0x10]
0x48b084: bl       #0x479afc  ; 6CLevel22AddBatchNodeReflectionEPN6glitch5scene10ISceneNodeE
0x48b088: ldr      r3, [sp, #0x10]
0x48b08c: cmp      r3, #0
0x48b090: beq      #0x48ace0
0x48b094: ldr      r2, [r3]
0x48b098: ldr      r0, [r2, #-0x10]
0x48b09c: add      r0, r3, r0
0x48b0a0: bl       #0x1fd770  ; 6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
0x48b0a4: b        #0x48ace0  ; 6CLevel14LoadNextObjectEv

===== h2667d  0x48afcc..0x48b060 =====
0x48afcc: mov      r0, #0x68
0x48afd0: bl       #0x3e91f8  ; _Znwj
0x48afd4: mov      r4, r0
0x48afd8: bl       #0x1d163c  ; 12CNavMeshNovaC1Ev
0x48afdc: mov      r0, r4
0x48afe0: ldr      r1, [r6]
0x48afe4: bl       #0x1d17cc  ; 12CNavMeshNova6CreateEP13CMemoryStream
0x48afe8: mov      r0, r7
0x48afec: mov      r1, r4
0x48aff0: bl       #0x484ac0  ; 6CLevel10SetNavMeshEP12CNavMeshNova
0x48aff4: mov      r0, #1
0x48aff8: b        #0x489f70  ; 6CLevel14LoadNextObjectEv
0x48affc: ldr      r1, [sp, #0x34]
0x48b000: add      r0, sp, #0x10
0x48b004: bl       #0x20414c  ; _Z21ConstructColladaScenePKc
0x48b008: ldr      r0, [sp, #0x10]
0x48b00c: add      r1, sp, #0xcc
0x48b010: ldr      r3, [r0]
0x48b014: ldr      r3, [r3, #0xb8]
0x48b018: blx      r3
0x48b01c: ldr      r0, [sp, #0x10]
0x48b020: add      r1, sp, #0xe4
0x48b024: ldr      r3, [r0]
0x48b028: ldr      r3, [r3, #0xa8]
0x48b02c: blx      r3
0x48b030: vldr     s15, [pc, #0xe8]
0x48b034: vldr     s14, [sp, #0xd8]
0x48b038: vmul.f32 s13, s14, s15
0x48b03c: ldr      r4, [sp, #0x10]
0x48b040: vldr     s14, [sp, #0xdc]
0x48b044: add      r1, sp, #0x24
0x48b048: add      r0, sp, #0x58
0x48b04c: ldr      r3, [r4]
0x48b050: ldr      r5, [r3, #0xb0]
0x48b054: vmul.f32 s14, s14, s15
0x48b058: vstr     s13, [sp, #0x24]
0x48b05c: vldr     s13, [sp, #0xe0]

===== CTemplateZone::Load  0x48d5f4..0x48d6f8 =====
0x48d5f4: push     {r3, r4, r5, lr}
0x48d5f8: mov      r4, r0
0x48d5fc: mov      r0, r1
0x48d600: mov      r5, r1
0x48d604: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d608: add      r1, r4, #8
0x48d60c: adds     r3, r0, #0
0x48d610: mov      r0, r5
0x48d614: movne    r3, #1
0x48d618: strb     r3, [r4, #4]
0x48d61c: bl       #0x33a0d4  ; 13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAll
0x48d620: mov      r0, r5
0x48d624: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d628: str      r0, [r4, #0xc]
0x48d62c: mov      r0, r5
0x48d630: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d634: adds     r3, r0, #0
0x48d638: mov      r0, r5
0x48d63c: movne    r3, #1
0x48d640: strb     r3, [r4, #0x14]
0x48d644: bl       #0x339914  ; 13CMemoryStream7ReadIntEv
0x48d648: str      r0, [r4, #0x18]
0x48d64c: mov      r0, r5
0x48d650: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d654: str      r0, [r4, #0x1c]
0x48d658: mov      r0, r5
0x48d65c: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d660: str      r0, [r4, #0x20]
0x48d664: mov      r0, r5
0x48d668: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d66c: str      r0, [r4, #0x24]
0x48d670: mov      r0, r5
0x48d674: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d678: str      r0, [r4, #0x28]
0x48d67c: mov      r0, r5
0x48d680: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d684: str      r0, [r4, #0x2c]
0x48d688: mov      r0, r5
0x48d68c: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d690: str      r0, [r4, #0x30]
0x48d694: mov      r0, r5
0x48d698: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d69c: str      r0, [r4, #0x34]
0x48d6a0: mov      r0, r5
0x48d6a4: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d6a8: str      r0, [r4, #0x38]
0x48d6ac: mov      r0, r5
0x48d6b0: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d6b4: str      r0, [r4, #0x3c]
0x48d6b8: mov      r0, r5
0x48d6bc: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d6c0: adds     r3, r0, #0
0x48d6c4: mov      r0, r5
0x48d6c8: movne    r3, #1
0x48d6cc: strb     r3, [r4, #0x40]
0x48d6d0: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d6d4: adds     r3, r0, #0
0x48d6d8: mov      r0, r5
0x48d6dc: movne    r3, #1
0x48d6e0: strb     r3, [r4, #0x41]
0x48d6e4: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d6e8: adds     r0, r0, #0
0x48d6ec: movne    r0, #1
0x48d6f0: strb     r0, [r4, #0x42]
0x48d6f4: pop      {r3, r4, r5, pc}

===== CTemplateBakeGroup::Load  0x48d870..0x48d978 =====
0x48d870: push     {r3, r4, r5, lr}
0x48d874: mov      r4, r0
0x48d878: mov      r0, r1
0x48d87c: mov      r5, r1
0x48d880: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d884: adds     r3, r0, #0
0x48d888: mov      r0, r5
0x48d88c: movne    r3, #1
0x48d890: strb     r3, [r4, #4]
0x48d894: bl       #0x339914  ; 13CMemoryStream7ReadIntEv
0x48d898: str      r0, [r4, #8]
0x48d89c: mov      r0, r5
0x48d8a0: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8a4: str      r0, [r4, #0xc]
0x48d8a8: mov      r0, r5
0x48d8ac: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8b0: str      r0, [r4, #0x10]
0x48d8b4: mov      r0, r5
0x48d8b8: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8bc: str      r0, [r4, #0x14]
0x48d8c0: mov      r0, r5
0x48d8c4: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8c8: str      r0, [r4, #0x18]
0x48d8cc: mov      r0, r5
0x48d8d0: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8d4: str      r0, [r4, #0x1c]
0x48d8d8: mov      r0, r5
0x48d8dc: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8e0: str      r0, [r4, #0x20]
0x48d8e4: mov      r0, r5
0x48d8e8: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8ec: str      r0, [r4, #0x24]
0x48d8f0: mov      r0, r5
0x48d8f4: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d8f8: str      r0, [r4, #0x28]
0x48d8fc: mov      r0, r5
0x48d900: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d904: str      r0, [r4, #0x2c]
0x48d908: mov      r0, r5
0x48d90c: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d910: adds     r3, r0, #0
0x48d914: mov      r0, r5
0x48d918: movne    r3, #1
0x48d91c: strb     r3, [r4, #0x30]
0x48d920: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d924: adds     r3, r0, #0
0x48d928: mov      r0, r5
0x48d92c: movne    r3, #1
0x48d930: strb     r3, [r4, #0x31]
0x48d934: bl       #0x3395d8  ; 13CMemoryStream8ReadCharEv
0x48d938: add      r1, r4, #0x38
0x48d93c: adds     r3, r0, #0
0x48d940: mov      r0, r5
0x48d944: movne    r3, #1
0x48d948: strb     r3, [r4, #0x32]
0x48d94c: bl       #0x33a0d4  ; 13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAll
0x48d950: mov      r0, r5
0x48d954: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d958: add      r1, r4, #0x40
0x48d95c: str      r0, [r4, #0x3c]
0x48d960: mov      r0, r5
0x48d964: bl       #0x33a0d4  ; 13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAll
0x48d968: mov      r0, r5
0x48d96c: bl       #0x339b94  ; 13CMemoryStream9ReadFloatEv
0x48d970: str      r0, [r4, #0x44]
0x48d974: pop      {r3, r4, r5, pc}
