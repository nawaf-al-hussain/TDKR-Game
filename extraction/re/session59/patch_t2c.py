#!/usr/bin/env python3
"""s59 T2 part 3: buildGLB clip-list param + merc call + invB count generalization."""

WT = '/tmp/my-project/work/ghpages_staged_wt/playable'
H = f'{WT}/integration_lazy.html'

def patch(old, new, tag):
    src = open(H, encoding='utf-8').read()
    assert src.count(old) == 1, f'{tag}: count={src.count(old)}'
    out = src.replace(old, new)
    assert out != src, f'{tag}: no change'
    open(H, 'wb').write(out.encode('utf-8'))
    print(f'patched {tag}')

patch("const buildGLB = function buildGLB(skin, A, byNameC) {",
      "const buildGLB = function buildGLB(skin, A, byNameC, clipsToEmbed) {",
      'signature')
patch("""    for (const nm of ['_001_idle_stand', '_007_walk', '_008_run', '_057_glide_idle', '_089_grapnel_pull', '_088_grapnel_shoot', '_065_glide_idle_to_run']) {   // s53 T5 + s54 T3: state-table clips (Glide_Idle, Grapnel pull, Grapnel_Horizontal_To_Glide_Idle -> _065 landing transition)""",
      """    for (const nm of (clipsToEmbed || ['_001_idle_stand', '_007_walk', '_008_run', '_057_glide_idle', '_089_grapnel_pull', '_088_grapnel_shoot', '_065_glide_idle_to_run'])) {   // s53 T5 + s54 T3: state-table clips; s59 T2: caller-suppliable list (enemy clips)""",
      'clip list')
patch("    const ibmB = new Float32Array(31 * 16);",
      "    const ibmB = new Float32Array(skin.invB.length * 16);",
      'ibm count')
patch("    gltf.skins[0].inverseBindMatrices = addAcc(offs.ibm, ibmB.byteLength, 31, 5126, 'MAT4');",
      "    gltf.skins[0].inverseBindMatrices = addAcc(offs.ibm, ibmB.byteLength, skin.invB.length, 5126, 'MAT4');",
      'ibm accessor')
patch("  const glbBytes = buildGLB(skin, A, byNameC);\n  const g = await new Promise((res, rej) => new GLTFLoader().parse(glbBytes.buffer, '', res, rej));\n  merc = g.scene; merc.rotation.x = -Math.PI / 2;",
      "  const glbBytes = buildGLB(skin, A, byNameC, ENEMY_CLIPS);\n  const g = await new Promise((res, rej) => new GLTFLoader().parse(glbBytes.buffer, '', res, rej));\n  merc = g.scene; merc.rotation.x = -Math.PI / 2;",
      'merc buildGLB call')
print('OK')
