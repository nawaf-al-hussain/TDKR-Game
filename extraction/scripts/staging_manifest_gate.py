#!/usr/bin/env python3
"""STAGING-FROM-MANIFEST GATE (round-7 process hardening).

Builds the expected site tree FROM models/manifest.json (every glb entry's
`file`, every referenced texture as models/tex/<stem>.jpg, the manifest
itself) plus the known aux set the viewer requests outside the manifest
(index.html, app.js, style.css, skybox.jpg, .nojekyll, batarang.glb, LUT +
fog textures), then diffs that expected tree against the actual gh-pages
tree (git ls-tree).  ANY difference -- missing file, stray file, or glb
byte-size mismatch against the manifest -- FAILS the gate.

This closes the round-5/6 gap pair: the URL crawl only sees static
references, and the deploy allowlist only constrains deletes.  Here the
manifest itself is the staging contract.

Usage:
  python3 staging_manifest_gate.py [--remote origin/gh-pages | --dir DIR]

Exit 0 = PASS, 1 = FAIL (differences printed).
"""
import argparse
import json
import subprocess
import sys

AUX = {
    ".nojekyll", "app.js", "index.html", "style.css", "skybox.jpg",
    "models/batarang.glb",
    "models/tex/LUT_000_default.png", "models/tex/LUT_023_lighting.png",
    "models/tex/GC_VerticalFOG.png",
}
# session worklogs are intentionally published (deploy_site.py AUX doc:
# "worklogs ... never deleted")
AUX_PATTERNS = ("worklog_session",)


def is_aux(path):
    return path in AUX or any(p in path for p in AUX_PATTERNS)


REPO = "/home/z/my-project/repo"


def gh_tree(remote):
    out = subprocess.run(
        ["git", "-C", REPO, "ls-tree", "-r", remote, "--name-only"],
        capture_output=True, text=True, check=True)
    files = [l for l in out.stdout.splitlines() if l.strip()]
    sizes = {}
    for f in files:
        p = subprocess.run(
            ["git", "-C", REPO, "cat-file", "-s", f"{remote}:{f}"],
            capture_output=True, text=True)
        sizes[f] = int(p.stdout.strip()) if p.returncode == 0 else None
    return files, sizes


def dir_tree(d):
    import os
    files, sizes = [], {}
    for root, _, fns in os.walk(d):
        for fn in fns:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, d)
            files.append(rel)
            sizes[rel] = os.path.getsize(p)
    return files, sizes


def glb_tex_names(blob):
    """Texture stems a GLB's material names reference.
    app.js contract: material name = '<dif>|<lm>|<mode>' (lightmapped) or
    '<tex>|<mode>'; '__dark' = no texture."""
    import struct
    out = set()
    try:
        clen, _ = struct.unpack_from("<2I", blob, 12)
        j = json.loads(blob[20:20 + clen])
    except Exception:
        return out
    for m in j.get("materials", []):
        raw = m.get("name", "")
        if not raw or raw == "__dark":
            continue
        pipe = raw.split("|")
        if len(pipe) >= 3:
            for t in pipe[:2]:          # '<dif>|<lm>|<mode>'
                if t:
                    out.add(t)
        else:
            if pipe[0]:                 # '<tex>|<mode>'
                out.add(pipe[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--remote", default="origin/gh-pages")
    src.add_argument("--dir")
    args = ap.parse_args()

    if args.dir:
        files, sizes = dir_tree(args.dir)
        man = json.load(open(f"{args.dir}/models/manifest.json"))
    else:
        files, sizes = gh_tree(args.remote)
        p = subprocess.run(
            ["git", "-C", REPO, "show", f"{args.remote}:models/manifest.json"],
            capture_output=True, text=True, check=True)
        man = json.loads(p.stdout)

    expected = {"models/manifest.json"}
    for g in man.get("glbs", []):
        expected.add(g["file"])
        for f in g.get("files", []):
            for t in f.get("texs", []):
                expected.add(f"models/tex/{t}.jpg")
    expected |= AUX

    # textures referenced INSIDE each glb via material names
    for g in man.get("glbs", []):
        f = g["file"]
        p = subprocess.run(
            ["git", "-C", REPO, "cat-file", "-p", f"{args.remote}:{f}"]
            if not args.dir else ["cat", f"{args.dir}/{f}"],
            capture_output=True)
        if p.returncode == 0 and p.stdout[:4] == b"glTF":
            for t in glb_tex_names(p.stdout):
                expected.add(f"models/tex/{t}.jpg")

    actual = set(files) - {".gitignore"}
    missing = sorted(expected - actual)
    stray = sorted(p for p in (actual - expected) if not is_aux(p))

    size_bad = []
    for g in man.get("glbs", []):
        f = g["file"]
        if f in sizes and sizes[f] is not None and sizes[f] != g["bytes"]:
            size_bad.append((f, g["bytes"], sizes[f]))

    ok = not missing and not stray and not size_bad
    print(f"manifest v{man.get('version')}: expected {len(expected)} files, "
          f"actual {len(actual)}")
    if missing:
        print(f"MISSING on site ({len(missing)}):")
        for f in missing[:20]:
            print("   -", f)
    if stray:
        print(f"STRAY on site, not in manifest/aux ({len(stray)}):")
        for f in stray[:20]:
            print("   +", f)
    if size_bad:
        print(f"GLB SIZE MISMATCH vs manifest ({len(size_bad)}):")
        for f, a, b in size_bad[:20]:
            print(f"   ! {f}: manifest {a} != site {b}")
    print(f"STAGING-FROM-MANIFEST GATE: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
