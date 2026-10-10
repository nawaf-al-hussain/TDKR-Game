#!/usr/bin/env python3
"""Incremental gh-pages deploy — the ONLY deploy path (round-5 process rule).

History this script exists to prevent:
  v16: `rm -rf models` + partial rebuild wiped LUT/fog/skybox aux textures ->
       whole-screen black render, smoke test still 57/57 (it never requested
       them).  v17: live batarang.glb 404 survived because nothing crawled
       app.js's easter-egg reference.

Guarantees (round-5 hardening):
  1. MANAGED PATHS are an explicit allowlist.  The only deletion this script
     can ever perform is `models/<name>.glb` where <name>.glb is NOT in the
     new manifest AND is not aux-protected.  Every planned delete is checked
     against the allowlist pattern immediately before execution; a delete
     outside it is IMPOSSIBLE (the script raises instead).
  2. Adds/changes come only from the staged tree (work/ghpages_site) and are
     copy semantics — nothing on gh-pages outside the staged tree is touched.
     Aux files (LUTs, fog, skybox, style.css, .nojekyll, batarang.glb,
     worklogs) are never deleted; they are overwritten ONLY if the staged
     tree itself provides a replacement.
  3. --dry-run prints every file that would be ADDED / CHANGED / DELETED and
     the URL-gate result, touching nothing.

Usage:
  python3 deploy_site.py [--dry-run] [--source DIR] [--dest DIR] [--no-sync]
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

# THE deletion allowlist: the single pattern of paths this script may remove.
DELETABLE = ("models/*.glb",)


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


def deletable(rel):
    """True only if rel matches the deletion allowlist AND is not aux."""
    import fnmatch
    if rel in AUX_PROTECTED or rel.lstrip("/") in AUX_PROTECTED:
        return False
    return any(fnmatch.fnmatch(rel, pat) for pat in DELETABLE)


def plan(src, dst, do_sync):
    """Compute (adds, changes, deletes, manifest) without touching dst."""
    adds, changes = [], []
    if do_sync:
        for base, _dirs, files in os.walk(src):
            rel_dir = os.path.relpath(base, src)
            for f in files:
                s = os.path.join(base, f)
                rel = f if rel_dir == "." else os.path.join(rel_dir, f)
                d = os.path.join(dst, rel)
                if not os.path.exists(d):
                    adds.append(rel)
                elif not filecmp.cmp(s, d, shallow=False):
                    changes.append(rel)
    deletes = []
    if do_sync:
        man = json.load(open(os.path.join(src, "models", "manifest.json")))
        keep = {os.path.basename(g["file"]) for g in man["glbs"]}
        models = os.path.join(dst, "models")
        if os.path.isdir(models):
            for f in os.listdir(models):
                if not f.endswith(".glb"):
                    continue
                rel = f"models/{f}"
                if f in keep or not deletable(rel):
                    continue
                deletes.append(rel)
    return sorted(adds), sorted(changes), sorted(deletes)


def enforce_allowlist(deletes):
    """Hard guarantee: abort before ANY filesystem mutation if a planned
    delete falls outside the allowlist."""
    bad = [rel for rel in deletes if not deletable(rel)]
    if bad:
        print("DEPLOY ABORT — planned deletes outside the allowlist:")
        for b in bad:
            print(f"  NOT ALLOWED: {b}")
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=SRC_DEFAULT)
    ap.add_argument("--dest", default=DST_DEFAULT)
    ap.add_argument("--no-sync", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the full add/change/delete plan + gate "
                         "result; write nothing")
    args = ap.parse_args()
    src, dst = args.source, args.dest
    do_sync = not args.no_sync

    # ---- plan (pure) ----
    adds, changes, deletes = plan(src, dst, do_sync)
    print(f"plan: {len(adds)} added, {len(changes)} changed, "
          f"{len(deletes)} deleted"
          f"{' (DRY RUN — nothing will be written)' if args.dry_run else ''}")
    for tag, rows in (("ADD", adds), ("CHANGE", changes), ("DELETE", deletes)):
        for r in rows:
            print(f"  {tag:6s} {r}")
    enforce_allowlist(deletes)

    # ---- URL gate (read-only) ----
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

    if args.dry_run:
        print(f"DRY RUN PASS — manifest v{man['version']}, "
              f"{sum(len(g.get('files', [])) for g in man['glbs'])} meshes; "
              f"no files were written")
        return

    # ---- execute ----
    if do_sync:
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
        print(f"incremental sync: {n_copy} files copied")
        removed = 0
        for rel in deletes:
            os.remove(os.path.join(dst, rel))
            removed += 1
        print(f"street GLB cleanup: {removed} removed "
              f"(allowlist {DELETABLE[0]}, not in manifest v{man['version']})")
    print(f"DEPLOY GATE PASS — manifest v{man['version']}, "
          f"{sum(len(g.get('files', [])) for g in man['glbs'])} meshes")


if __name__ == "__main__":
    main()
