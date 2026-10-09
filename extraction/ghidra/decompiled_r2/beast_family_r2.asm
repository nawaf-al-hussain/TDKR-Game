
===== CComponentBeastObjectComponent::Load @ 0x2e1e8c (136 B) =====
0x2e1e8c: push     {r3, r4, r5, lr}
0x2e1e90: mov      r5, r0
0x2e1e94: mov      r0, r1
0x2e1e98: mov      r4, r1
0x2e1e9c: bl       #0x339b94  ; ReadF32
0x2e1ea0: str      r0, [r5, #4]  [field: r0, [r5, #4]]
0x2e1ea4: mov      r0, r4
0x2e1ea8: bl       #0x339b94  ; ReadF32
0x2e1eac: str      r0, [r5, #8]  [field: r0, [r5, #8]]
0x2e1eb0: mov      r0, r4
0x2e1eb4: bl       #0x339b94  ; ReadF32
0x2e1eb8: str      r0, [r5, #0xc]  [field: r0, [r5, #0xc]]
0x2e1ebc: mov      r0, r4
0x2e1ec0: bl       #0x339b94  ; ReadF32
0x2e1ec4: add      r1, r5, #0x14
0x2e1ec8: str      r0, [r5, #0x10]  [field: r0, [r5, #0x10]]
0x2e1ecc: mov      r0, r4
0x2e1ed0: bl       #0x33a0d4  ; ReadString
0x2e1ed4: mov      r0, r4
0x2e1ed8: bl       #0x339b94  ; ReadF32
0x2e1edc: str      r0, [r5, #0x18]  [field: r0, [r5, #0x18]]
0x2e1ee0: mov      r0, r4
0x2e1ee4: bl       #0x339b94  ; ReadF32
0x2e1ee8: str      r0, [r5, #0x1c]  [field: r0, [r5, #0x1c]]
0x2e1eec: mov      r0, r4
0x2e1ef0: bl       #0x339b94  ; ReadF32
0x2e1ef4: str      r0, [r5, #0x20]  [field: r0, [r5, #0x20]]
0x2e1ef8: mov      r0, r4
0x2e1efc: bl       #0x339b94  ; ReadF32
0x2e1f00: add      r1, r5, #0x28
0x2e1f04: str      r0, [r5, #0x24]  [field: r0, [r5, #0x24]]
0x2e1f08: mov      r0, r4
0x2e1f0c: pop      {r3, r4, r5, lr}
0x2e1f10: b        #0x33a0d4  ; ReadString

===== CComponentBeastObjectComponentGlobal::Load @ 0x2e1fb0 (52 B) =====
0x2e1fb0: push     {r3, r4, r5, lr}
0x2e1fb4: mov      r5, r0
0x2e1fb8: mov      r0, r1
0x2e1fbc: mov      r4, r1
0x2e1fc0: bl       #0x339914  ; 80
0x2e1fc4: str      r0, [r5, #4]  [field: r0, [r5, #4]]
0x2e1fc8: mov      r0, r4
0x2e1fcc: bl       #0x339914  ; 80
0x2e1fd0: add      r1, r5, #0xc
0x2e1fd4: str      r0, [r5, #8]  [field: r0, [r5, #8]]
0x2e1fd8: mov      r0, r4
0x2e1fdc: pop      {r3, r4, r5, lr}
0x2e1fe0: b        #0x33a0d4  ; ReadString

===== CComponentBeast_Area::Load @ 0x2e207c (120 B) =====
0x2e207c: push     {r3, r4, r5, lr}
0x2e2080: mov      r4, r0
0x2e2084: mov      r0, r1
0x2e2088: mov      r5, r1
0x2e208c: bl       #0x3395d8  ; 28
0x2e2090: strb     r0, [r4, #4]
0x2e2094: mov      r0, r5
0x2e2098: bl       #0x3395d8  ; 28
0x2e209c: strb     r0, [r4, #5]
0x2e20a0: mov      r0, r5
0x2e20a4: bl       #0x3395d8  ; 28
0x2e20a8: strb     r0, [r4, #6]
0x2e20ac: mov      r0, r5
0x2e20b0: bl       #0x3395d8  ; 28
0x2e20b4: strb     r0, [r4, #7]
0x2e20b8: mov      r0, r5
0x2e20bc: bl       #0x339b94  ; ReadF32
0x2e20c0: str      r0, [r4, #8]  [field: r0, [r4, #8]]
0x2e20c4: mov      r0, r5
0x2e20c8: bl       #0x3395d8  ; 28
0x2e20cc: adds     r3, r0, #0
0x2e20d0: mov      r0, r5
0x2e20d4: movne    r3, #1
0x2e20d8: strb     r3, [r4, #0xc]
0x2e20dc: bl       #0x339914  ; 80
0x2e20e0: str      r0, [r4, #0x10]  [field: r0, [r4, #0x10]]
0x2e20e4: mov      r0, r5
0x2e20e8: bl       #0x339914  ; 80
0x2e20ec: str      r0, [r4, #0x14]  [field: r0, [r4, #0x14]]
0x2e20f0: pop      {r3, r4, r5, pc}

===== CComponentBeast_Directional::Load @ 0x2e219c (132 B) =====
0x2e219c: push     {r3, r4, r5, lr}
0x2e21a0: mov      r4, r0
0x2e21a4: mov      r0, r1
0x2e21a8: mov      r5, r1
0x2e21ac: bl       #0x3395d8  ; 28
0x2e21b0: strb     r0, [r4, #4]
0x2e21b4: mov      r0, r5
0x2e21b8: bl       #0x3395d8  ; 28
0x2e21bc: strb     r0, [r4, #5]
0x2e21c0: mov      r0, r5
0x2e21c4: bl       #0x3395d8  ; 28
0x2e21c8: strb     r0, [r4, #6]
0x2e21cc: mov      r0, r5
0x2e21d0: bl       #0x3395d8  ; 28
0x2e21d4: strb     r0, [r4, #7]
0x2e21d8: mov      r0, r5
0x2e21dc: bl       #0x339b94  ; ReadF32
0x2e21e0: str      r0, [r4, #8]  [field: r0, [r4, #8]]
0x2e21e4: mov      r0, r5
0x2e21e8: bl       #0x3395d8  ; 28
0x2e21ec: adds     r3, r0, #0
0x2e21f0: mov      r0, r5
0x2e21f4: movne    r3, #1
0x2e21f8: strb     r3, [r4, #0xc]
0x2e21fc: bl       #0x339914  ; 80
0x2e2200: str      r0, [r4, #0x10]  [field: r0, [r4, #0x10]]
0x2e2204: mov      r0, r5
0x2e2208: bl       #0x339b94  ; ReadF32
0x2e220c: str      r0, [r4, #0x14]  [field: r0, [r4, #0x14]]
0x2e2210: mov      r0, r5
0x2e2214: bl       #0x339914  ; 80
0x2e2218: str      r0, [r4, #0x18]  [field: r0, [r4, #0x18]]
0x2e221c: pop      {r3, r4, r5, pc}

===== CComponentBeast_Omni::Load @ 0x2e22f8 (188 B) =====
0x2e22f8: push     {r3, r4, r5, lr}
0x2e22fc: mov      r4, r0
0x2e2300: mov      r0, r1
0x2e2304: mov      r5, r1
0x2e2308: bl       #0x3395d8  ; 28
0x2e230c: strb     r0, [r4, #4]
0x2e2310: mov      r0, r5
0x2e2314: bl       #0x3395d8  ; 28
0x2e2318: strb     r0, [r4, #5]
0x2e231c: mov      r0, r5
0x2e2320: bl       #0x3395d8  ; 28
0x2e2324: strb     r0, [r4, #6]
0x2e2328: mov      r0, r5
0x2e232c: bl       #0x3395d8  ; 28
0x2e2330: strb     r0, [r4, #7]
0x2e2334: mov      r0, r5
0x2e2338: bl       #0x339b94  ; ReadF32
0x2e233c: str      r0, [r4, #8]  [field: r0, [r4, #8]]
0x2e2340: mov      r0, r5
0x2e2344: bl       #0x3395d8  ; 28
0x2e2348: adds     r3, r0, #0
0x2e234c: mov      r0, r5
0x2e2350: movne    r3, #1
0x2e2354: strb     r3, [r4, #0xc]
0x2e2358: bl       #0x339914  ; 80
0x2e235c: str      r0, [r4, #0x10]  [field: r0, [r4, #0x10]]
0x2e2360: mov      r0, r5
0x2e2364: bl       #0x339b94  ; ReadF32
0x2e2368: str      r0, [r4, #0x14]  [field: r0, [r4, #0x14]]
0x2e236c: mov      r0, r5
0x2e2370: bl       #0x339914  ; 80
0x2e2374: str      r0, [r4, #0x18]  [field: r0, [r4, #0x18]]
0x2e2378: mov      r0, r5
0x2e237c: bl       #0x339b94  ; ReadF32
0x2e2380: str      r0, [r4, #0x1c]  [field: r0, [r4, #0x1c]]
0x2e2384: mov      r0, r5
0x2e2388: bl       #0x339b94  ; ReadF32
0x2e238c: str      r0, [r4, #0x20]  [field: r0, [r4, #0x20]]
0x2e2390: mov      r0, r5
0x2e2394: bl       #0x3395d8  ; 28
0x2e2398: adds     r3, r0, #0
0x2e239c: mov      r0, r5
0x2e23a0: movne    r3, #1
0x2e23a4: strb     r3, [r4, #0x24]
0x2e23a8: bl       #0x339914  ; 80
0x2e23ac: str      r0, [r4, #0x28]  [field: r0, [r4, #0x28]]
0x2e23b0: pop      {r3, r4, r5, pc}

===== CComponentBeast_Spot::Load @ 0x2e24b0 (224 B) =====
0x2e24b0: push     {r3, r4, r5, lr}
0x2e24b4: mov      r4, r0
0x2e24b8: mov      r0, r1
0x2e24bc: mov      r5, r1
0x2e24c0: bl       #0x3395d8  ; 28
0x2e24c4: strb     r0, [r4, #4]
0x2e24c8: mov      r0, r5
0x2e24cc: bl       #0x3395d8  ; 28
0x2e24d0: strb     r0, [r4, #5]
0x2e24d4: mov      r0, r5
0x2e24d8: bl       #0x3395d8  ; 28
0x2e24dc: strb     r0, [r4, #6]
0x2e24e0: mov      r0, r5
0x2e24e4: bl       #0x3395d8  ; 28
0x2e24e8: strb     r0, [r4, #7]
0x2e24ec: mov      r0, r5
0x2e24f0: bl       #0x339b94  ; ReadF32
0x2e24f4: str      r0, [r4, #8]  [field: r0, [r4, #8]]
0x2e24f8: mov      r0, r5
0x2e24fc: bl       #0x3395d8  ; 28
0x2e2500: adds     r3, r0, #0
0x2e2504: mov      r0, r5
0x2e2508: movne    r3, #1
0x2e250c: strb     r3, [r4, #0xc]
0x2e2510: bl       #0x339914  ; 80
0x2e2514: str      r0, [r4, #0x10]  [field: r0, [r4, #0x10]]
0x2e2518: mov      r0, r5
0x2e251c: bl       #0x339b94  ; ReadF32
0x2e2520: str      r0, [r4, #0x14]  [field: r0, [r4, #0x14]]
0x2e2524: mov      r0, r5
0x2e2528: bl       #0x339914  ; 80
0x2e252c: str      r0, [r4, #0x18]  [field: r0, [r4, #0x18]]
0x2e2530: mov      r0, r5
0x2e2534: bl       #0x339b94  ; ReadF32
0x2e2538: str      r0, [r4, #0x1c]  [field: r0, [r4, #0x1c]]
0x2e253c: mov      r0, r5
0x2e2540: bl       #0x339b94  ; ReadF32
0x2e2544: str      r0, [r4, #0x20]  [field: r0, [r4, #0x20]]
0x2e2548: mov      r0, r5
0x2e254c: bl       #0x3395d8  ; 28
0x2e2550: adds     r3, r0, #0
0x2e2554: mov      r0, r5
0x2e2558: movne    r3, #1
0x2e255c: strb     r3, [r4, #0x24]
0x2e2560: bl       #0x339b94  ; ReadF32
0x2e2564: str      r0, [r4, #0x28]  [field: r0, [r4, #0x28]]
0x2e2568: mov      r0, r5
0x2e256c: bl       #0x339b94  ; ReadF32
0x2e2570: str      r0, [r4, #0x2c]  [field: r0, [r4, #0x2c]]
0x2e2574: mov      r0, r5
0x2e2578: bl       #0x339b94  ; ReadF32
0x2e257c: str      r0, [r4, #0x30]  [field: r0, [r4, #0x30]]
0x2e2580: mov      r0, r5
0x2e2584: bl       #0x339914  ; 80
0x2e2588: str      r0, [r4, #0x34]  [field: r0, [r4, #0x34]]
0x2e258c: pop      {r3, r4, r5, pc}

===== CComponentBeast_Window::Load @ 0x2e2638 (132 B) =====
0x2e2638: push     {r3, r4, r5, lr}
0x2e263c: mov      r4, r0
0x2e2640: mov      r0, r1
0x2e2644: mov      r5, r1
0x2e2648: bl       #0x3395d8  ; 28
0x2e264c: strb     r0, [r4, #4]
0x2e2650: mov      r0, r5
0x2e2654: bl       #0x3395d8  ; 28
0x2e2658: strb     r0, [r4, #5]
0x2e265c: mov      r0, r5
0x2e2660: bl       #0x3395d8  ; 28
0x2e2664: strb     r0, [r4, #6]
0x2e2668: mov      r0, r5
0x2e266c: bl       #0x3395d8  ; 28
0x2e2670: strb     r0, [r4, #7]
0x2e2674: mov      r0, r5
0x2e2678: bl       #0x339b94  ; ReadF32
0x2e267c: str      r0, [r4, #8]  [field: r0, [r4, #8]]
0x2e2680: mov      r0, r5
0x2e2684: bl       #0x3395d8  ; 28
0x2e2688: adds     r3, r0, #0
0x2e268c: mov      r0, r5
0x2e2690: movne    r3, #1
0x2e2694: strb     r3, [r4, #0xc]
0x2e2698: bl       #0x339914  ; 80
0x2e269c: str      r0, [r4, #0x10]  [field: r0, [r4, #0x10]]
0x2e26a0: mov      r0, r5
0x2e26a4: bl       #0x339b94  ; ReadF32
0x2e26a8: str      r0, [r4, #0x14]  [field: r0, [r4, #0x14]]
0x2e26ac: mov      r0, r5
0x2e26b0: bl       #0x339914  ; 80
0x2e26b4: str      r0, [r4, #0x18]  [field: r0, [r4, #0x18]]
0x2e26b8: pop      {r3, r4, r5, pc}

===== CComponentBeastBakeGroup::Load(?) @ 0x3be548 (96 B) =====
0x3be548: push     {r3, r4, r5, lr}
0x3be54c: mov      r4, r0
0x3be550: mov      r5, r1
0x3be554: mov      r0, r1
0x3be558: add      r1, r4, #4
0x3be55c: bl       #0x33a0d4  ; ReadString
0x3be560: mov      r0, r5
0x3be564: bl       #0x339b94  ; ReadF32
0x3be568: add      r1, r4, #0xc
0x3be56c: str      r0, [r4, #8]  [field: r0, [r4, #8]]
0x3be570: mov      r0, r5
0x3be574: bl       #0x33a0d4  ; ReadString
0x3be578: mov      r0, r5
0x3be57c: bl       #0x339b94  ; ReadF32
0x3be580: str      r0, [r4, #0x10]  [field: r0, [r4, #0x10]]
0x3be584: pop      {r3, r4, r5, pc}
0x3be588: push     {r3, lr}
0x3be58c: mov      r0, #0x2c
0x3be590: bl       #0x3e91f8  ; 12
0x3be594: ldr      ip, [pc, #0x3c]
0x3be598: mov      r2, #0
0x3be59c: add      ip, pc, ip
0x3be5a0: add      ip, ip, #8
0x3be5a4: add      r3, r0, #8
