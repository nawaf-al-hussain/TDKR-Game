#!/usr/bin/env python3
"""S38 T8: asset distribution inventory (REPORT ONLY — no deletions).
Enumerates every converted/original Gameloft asset in: main repo tracked files,
the gh-pages branch (live site), and release bundles; sizes, paths, and which
pages depend on each. Proposes the user-supplied-only layout."""
import subprocess, json, os

REPO = '/tmp/my-project/work/TDKR-Game'
def git(args):
    return subprocess.run(['git', '-C', REPO] + args, capture_output=True, text=True).stdout

inv = {'gh_pages': [], 'main_repo': [], 'release_assets': []}
# gh-pages tree (the LIVE v20 site content)
for line in git(['ls-tree', '-r', '-l', 'gh-pages']).splitlines():
    parts = line.split()
    if len(parts) >= 4:
        size, path = parts[3], parts[-1]
        inv['gh_pages'].append({'path': path, 'bytes': int(size)})
# main tracked files that are game-derived (GLB, textures, collision, extracted data)
game_ext = ('.glb', '.bin', '.nm', '.gla', '.bdae', '.lvc', '.tga', '.jpg', '.png')
for line in git(['ls-tree', '-r', '-l', 'main']).splitlines():
    parts = line.split()
    if len(parts) >= 4:
        path, size = parts[-1], int(parts[3])
        if path.endswith(game_ext) and any(k in path for k in ('asset', 'model', 'texture', 'collision', 'extraction/data', 'TDKR_data')):
            inv['main_repo'].append({'path': path, 'bytes': size})

tot_gh = sum(a['bytes'] for a in inv['gh_pages'])
bydir = {}
for a in inv['gh_pages']:
    d = a['path'].split('/')[0] if '/' in a['path'] else '.'
    bydir[d] = bydir.get(d, 0) + a['bytes']
print(f'gh-pages (live v20): {len(inv["gh_pages"])} files, {tot_gh/1e6:.1f} MB total')
for d, s in sorted(bydir.items(), key=lambda kv: -kv[1]):
    print(f'  {d}: {s/1e6:.1f} MB')
# playable/ dependency map
play = [a for a in inv['gh_pages'] if a['path'].startswith('playable/')]
print('\nplayable/ (the interactive page) — every file and its role:')
roles = {
    'index.html': 'walk-as-Batman page (code)',
    'batman.glb': 'CONVERTED GAMELOFT ASSET (rig+mesh+5 anims+embedded diffuse PNG, 1.33 MB)',
    'patch.json': 'CONVERTED GAMELOFT DATA (12,512-tri collision patch + 13 trigger volumes + spawn)',
    'fengari-web.js': 'code (Lua VM)',
    'pipeline.html': 'user-files-only pipeline page (code)',
    'tdkr_pipeline.js': 'code (asset pipeline)',
}
for a in play:
    print(f"  {a['path']}: {a['bytes']} B — {roles.get(os.path.basename(a['path']), 'support')}")
print(f'\nplayable/ asset total (game-derived): {sum(a["bytes"] for a in play if "batman.glb" in a["path"] or "patch.json" in a["path"])/1e6:.2f} MB')
print(f'gh-pages viewer assets (street GLBs + textures): {sum(a["bytes"] for a in inv["gh_pages"] if a["path"].startswith("models/"))/1e6:.1f} MB')

# user-supplied-only proposal
print('\n=== USER-SUPPLIED-ONLY LAYOUT (what the public site would keep) ===')
print('  index.html (viewer), app.js, style.css, .nojekyll — site shell (code)')
print('  playable/index.html, pipeline.html, tdkr_pipeline.js, fengari-web.js — code')
print('  REMOVED from repo, decoded at runtime from the user zip:')
print('    - playable/batman.glb (1.33 MB) -> assembled in-memory by the pipeline (T5 path)')
print('    - playable/patch.json (1.06 MB) -> collision/triggers parsed from the level data')
print('    - models/*.glb (street viewer) -> would need the full city pipeline (not built)')
print('    - models/tex/*.jpg -> engine texture decode (PVRTC gap, T2 open item)')
print(f'  Net: {tot_gh/1e6:.1f} MB -> ~0.5 MB of pure code; all game data user-supplied.')
json.dump(inv, open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t8_inventory.json', 'w'), indent=1)
print('saved s38_t8_inventory.json')
