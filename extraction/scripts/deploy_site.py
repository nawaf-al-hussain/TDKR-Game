#!/usr/bin/env python3
"""Incremental gh-pages deploy — replaces the destructive `rm -rf models`.

Round-4 process rule: the v16 deploy wiped LUT/fog/skybox aux textures
(`rm -rf models` + partial rebuild -> whole-screen black render) and the
smoke test still passed 57/57 because it only checked GLBs/textures/infra,
not every URL the viewer requests.

This script:
  1. syncs work/ghpages_site -> repo/gh-pages INCREMENTALLY
     (copy new/changed files; delete only street GLBs that the new manifest
     no longer lists; NEVER touch aux textures LUT_*/GC_VerticalFOG/skybox
     or non-street tiers unless the source explicitly provides replacements)
  2. runs the pre-deploy gate locally: manifest parse + every URL referenced
     by app.js + manifest + index.html resolved against the staged tree
     (fails on any missing file)
  3. prints the git commands (the caller commits + pushes gh-pages)

Usage: python3 deploy_site.py [--source DIR] [--dest DIR]
"""
import argparse
import filecmp
import json
import os
import re
import shutil
import sys

SRC_DEFAULT = "/home/z/my-project/work/ghpages_site"
DST_DEFAULT = "/home/z/my-project/repo/gh-pages"

# files the viewer requests outside the manifest (from app.js/index.html)
AUX_PROTECTED = {
    "models/tex/LUT_000_default.png", "models/tex/LUT_023_lighting.png",
    "models/tex/GC_VerticalFOG.png", "skybox.jpg", "models/batarang.glb",
    "style.css", ".nojekyll", "index.html", "app.js",
}


def crawl_urls(root):
    """Every local asset URL referenced by app.js / index.html / manifest."""
    urls = set()
    js = open(os.path.join(root, "app.js"), encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"""['"]([A-Za-z0-9_./-]+\.(?:jpg|png|json|glb))['"]""", js):
        urls.add(m.group(1))
    html = open(os.path.join(root, "index.html"), encoding="utf-8",
                errors="replace").read()
    for m in re.finditer(r"""['"]\.?/?([A-Za-z0-9_./-]+\.(?:jpg|png|js|css))['"]""", html):
        urls.add(m.group(1).lstrip("./"))
    man = json.load(open(os.path.join(root, "models", "manifest.json")))
    for g in man["glbs"]:
        urls.add(g["file"])
        for fe in g.get("files", []):
            for t in fe.get("texs", []):
                if t and t != "__dark":
                    urls.add(f"models/tex/{t}.jpg")
    return sorted(urls), man


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=SRC_DEFAULT)
    ap.add_argument("--dest", default=DST_DEFAULT)
    ap.add_argument("--no-sync", action="store_true")
    args = ap.parse_args()
    src, dst = args.source, args.dest

    if not args.no_sync:
        # 1. incremental copy: new or changed files only
        n_copy = 0
        for base, _dirs, files in os.walk(src):
            rel = os.path.relpath(base, src)
            for f in files:
                s = os.path.join(base, f)
                d = os.path.join(dst, rel, f) if rel != "." else os.path.join(dst, f)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                if not os.path.exists(d) or not filecmp.cmp(s, d, shallow=False):
                    shutil.copy2(s, d)
                    n_copy += 1
        print(f"incremental sync: {n_copy} files copied (no deletions)")

        # 2. delete ONLY street GLBs dropped from the new manifest
        man = json.load(open(os.path.join(src, "models", "manifest.json")))
        keep = {os.path.basename(g["file"]) for g in man["glbs"]}
        models = os.path.join(dst, "models")
        removed = 0
        for f in os.listdir(models):
            if f.endswith(".glb") and f not in keep:
                # protect aux-adjacent glbs (none today, but be explicit)
                if f"models/{f}" in AUX_PROTECTED or f in AUX_PROTECTED:
                    continue
                os.remove(os.path.join(models, f))
                removed += 1
        print(f"street GLB cleanup: {removed} removed (not in manifest v{man['version']})")

    # 3. pre-deploy gate: every referenced URL must exist in the staged tree
    urls, man = crawl_urls(dst)
    missing = []
    for u in urls:
        p = os.path.join(dst, u)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            missing.append(u)
    print(f"pre-deploy URL gate: {len(urls)} referenced files, "
          f"{len(missing)} missing")
    for u in missing:
        print(f"  MISSING: {u}")
    if missing:
        print("DEPLOY GATE FAILED — fix the missing files first")
        sys.exit(1)
    print(f"DEPLOY GATE PASS — manifest v{man['version']}, "
          f"{sum(len(g.get('files', [])) for g in man['glbs'])} meshes")


if __name__ == "__main__":
    main()
