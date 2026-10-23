# s55 T1 — replace static `playable/batman.glb` with in-browser build (change list)

## Why
`playable/batman.glb` (299,388 B) is the only remaining *converted game asset* consumed
by a live page other than the root viewer's pre-packaged `models/` tree. The integration
pages already build the GLB in-browser from the user's zip (`buildGLB`, integration_lazy
@1154/@1403). Only `playable/index.html` still fetches the static file, so dropping the
static GLB removes the asset from the site with no capability loss (the page is
user-zip-driven anyway and already ships the bdae/anim decoders it needs).

## Consumers today (live tree 6145545)
| page | batman source |
|---|---|
| playable/index.html | `new GLTFLoader().load('./batman.glb')` @142 (fallback also used when no zip picked) |
| playable/integration.html | built from user zip (`buildGLB` @900/@1068) — no static fetch |
| playable/integration_lazy.html | built from user zip (`buildGLB` @1154/@1403) — no static fetch |
| playable/walktest.html | no Batman mesh |
| root viewer | none (`models/batarang.glb` is a different asset, the easter egg) |

## Change list (branch `s55-t1-batman-from-zip`, NOT deployed)
1. **playable/index.html**
   - Port `buildGLB` + its inputs from integration_lazy.html: `readBdae` skin/anim decode,
     clip whitelist (7 engine clips: _008_run, _057_glide_idle, _065_glide_idle_to_run,
     _088_grapnel_shoot, _089_grapnel_pull + 2 idle/breathing), RGB888 DataTexture path
     (~200 lines, self-contained; the page already parses actors.gla/actors_tex.gla from
     the user zip via tdkr_pipeline.js so no new parsing is needed).
   - Replace the `GLTFLoader().load('./batman.glb', ...)` block @142 with:
     `const glbBytes = buildGLB(skin, A, byNameC);` then
     `new GLTFLoader().parse(glbBytes.buffer, '', onLoad, onErr)` (parse keeps the same
     `g.animations` consumer code @166 unchanged).
   - Gate: when no user zip is picked, show the existing file prompt (the page already
     boots walker+renderer only after zip pick — confirm the Batman init is already inside
     the post-zip path; if not, defer the mesh build to it).
   - Validation hooks to keep: log the animation name+duration list (identical format),
     keep the silhouette/animation gate counters used by the gate runner.
2. **Delete `playable/batman.glb`** from the branch tree.
3. **No changes** needed to integration.html / integration_lazy.html (already zip-built),
   walktest, or the root viewer.
4. **Gate impact**: s49/s50/s53 gate receipts reference "Batman ok / silhouette px" from
   the zip-built path — identical expectations apply; the static GLB was only ever a
   fallback for playable/index.html's no-zip mode, which shows a prompt anyway.
5. **Rollout** (when instructed): branch → gates on playable/index.html (0 errors,
   animation log identical, silhouette counter) → deploy per deploy_site.py procedure.
   Site weight drops 299,388 B.

## Side note
`playable/index.html` also fetches `./patch.json` (1.06 MB game-derived). If the
default (no-zip) walker mode is retired, patch.json can be dropped in the same change;
checked: walktest.js has NO patch.json reference, so patch.json is consumed only by
playable/index.html — dropping both is viable in one pass.
