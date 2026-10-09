#!/usr/bin/env python3
"""Release gate: branch-drift + cache-version consistency (session 15).

Fails (exit 1) when a deploy would repeat the v13 stale-branch regression:
  1. main's gh-pages/models/manifest.json version must equal the version on
     the origin/gh-pages BRANCH (the actually-served one).
  2. app.js APP_CACHE_VERSION must equal 'v<manifest.version>' on BOTH sides
     (busts the manifest fetch itself).
  3. index.html must exist on origin/gh-pages (the thrice-lost root file).

Run BEFORE pushing gh-pages, and again after, as the release gate.
"""
import json
import re
import subprocess
import sys

REPO = "/home/z/my-project/work/TDKR-Game"


def git(args):
    return subprocess.run(["git", "-C", REPO] + args, capture_output=True,
                          text=True).stdout


def manifest_of(ref):
    if ref == "main":  # working tree (pre-commit gate)
        try:
            return json.load(open(f"{REPO}/gh-pages/models/manifest.json"))
        except Exception as e:
            print(f"FAIL: cannot parse working-tree manifest: {e}")
            return None
    out = git(["show", f"{ref}:models/manifest.json"])
    try:
        return json.loads(out)
    except Exception as e:
        print(f"FAIL: cannot parse manifest from {ref}: {e.strip()[:80]}")
        return None


def app_cache_version(ref):
    if ref == "main":
        txt = open(f"{REPO}/gh-pages/app.js").read()
    else:
        txt = git(["show", f"{ref}:app.js"])
    m = re.search(r"APP_CACHE_VERSION = '([^']+)'", txt)
    return m.group(1) if m else None


def has_index(ref):
    if ref.startswith("origin/gh-pages"):
        out = git(["ls-tree", ref, "--name-only"])
        return "index.html" in out.split()
    out = git(["ls-tree", f"{ref}:gh-pages", "--name-only"])
    return "index.html" in out.split()


def main():
    fails = []
    main_m = manifest_of("main")
    gh_m = manifest_of("origin/gh-pages")
    if main_m and gh_m:
        if main_m.get("version") != gh_m.get("version"):
            fails.append(f"manifest version drift: main={main_m.get('version')} "
                         f"origin/gh-pages={gh_m.get('version')}")
    elif main_m or gh_m:
        fails.append("manifest missing on one ref")

    for ref in ("main", "origin/gh-pages"):
        v = app_cache_version(ref)
        mv = (main_m if ref == "main" else gh_m)
        expect = f"v{mv.get('version')}" if mv else None
        if v != expect:
            fails.append(f"app.js APP_CACHE_VERSION on {ref} = {v}, "
                         f"expected {expect}")

    if not has_index("origin/gh-pages"):
        fails.append("gh-pages/index.html MISSING on origin/gh-pages "
                     "(third-loss guard)")
    if not has_index("main"):
        fails.append("gh-pages/index.html MISSING on main")

    # GLB inventory equality: same file set on both refs
    if main_m and gh_m:
        a = sorted(g["file"] for g in main_m["glbs"])
        b = sorted(g["file"] for g in gh_m["glbs"])
        if a != b:
            fails.append(f"GLB inventory drift: only-main={set(a)-set(b)} "
                         f"only-ghpages={set(b)-set(a)}")

    if fails:
        print("RELEASE GATE: FAIL")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("RELEASE GATE: PASS "
          f"(manifest v{gh_m.get('version') if gh_m else '?'} on main == "
          f"origin/gh-pages; cache versions consistent; index.html present)")


if __name__ == "__main__":
    main()
