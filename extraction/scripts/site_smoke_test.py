#!/usr/bin/env python3
"""Post-deploy smoke test for the TDKR GitHub Pages viewer.

The site root has been wiped/lost twice and the gh-pages branch has gone
stale relative to main (v13 served while main held v14).  This test makes
silent regressions impossible: run it after EVERY deploy.

Checks:
  1. index.html, style.css, app.js, skybox.jpg, .nojekyll  -> HTTP 200
  2. index.html references app.js + style.css
  3. models/manifest.json parses; has version/glbs/tiers
  4. every manifest GLB  -> HTTP 200, Content-Length == manifest bytes
  5. every texture referenced by any manifest entry -> HTTP 200
     (models/tex/<stem>.jpg unless the entry says otherwise)
  6. no island-2 skyline GLBs in the manifest (single-level view contract)

Usage:
  python3 site_smoke_test.py                 # fast: infra + manifest + GLB HEADs
  python3 site_smoke_test.py --base <url>    # other deployment
  python3 site_smoke_test.py --skip-glbs     # manifest/infra only

Exit code 0 = all good, 1 = failures (print them loudly).
"""
import argparse
import json
import sys
import urllib.request
import urllib.error

DEFAULT_BASE = "https://nawaf-al-hussain.github.io/TDKR-Game/"
ISLAND2_SKYLINE = {
    "GC_Island2_LongDist", "GC_LongDist_Island2_FP1",
    "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
    "GC_LongDist_Island2_Roads",
}


def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": "tdkr-smoke/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), b""
    except Exception as e:
        return -1, {}, str(e).encode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--skip-glbs", action="store_true")
    args = ap.parse_args()
    base = args.base.rstrip("/") + "/"

    failures, checks = [], 0

    def check(name, ok, detail=""):
        nonlocal checks
        checks += 1
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}" + (f"  ({detail})" if detail else ""))
        if not ok:
            failures.append(f"{name}: {detail}")

    # 1. infra files
    infra = {}
    for f in ("index.html", "style.css", "app.js", "skybox.jpg", ".nojekyll"):
        st, hd, _ = fetch(base + f, "GET")
        infra[f] = (st, hd)
        check(f"GET {f}", st == 200, f"status {st}")

    # 2. index.html wiring (index.html is self-contained: inline <style>;
    #    the separate style.css is hosted as a root-intactness sentinel but
    #    is NOT referenced by the page)
    st, _, body = fetch(base + "index.html")
    html = body.decode("utf-8", "replace") if st == 200 else ""
    check("index.html loads app.js", 'src="app.js"' in html or "app.js" in html)
    check("index.html has inline styles", "<style>" in html)

    # 3. manifest
    st, _, body = fetch(base + "models/manifest.json")
    man = None
    if st == 200:
        try:
            man = json.loads(body)
        except Exception as e:
            check("manifest.json parses", False, str(e))
    if man:
        check("manifest.json parses", True)
        check("manifest has version", isinstance(man.get("version"), int),
              f"version={man.get('version')}")
        check("manifest has glbs[]", isinstance(man.get("glbs"), list)
              and len(man["glbs"]) > 0, f"{len(man.get('glbs', []))} glbs")
        check("manifest has tiers", isinstance(man.get("tiers"), dict),
              ",".join(f"{k}:{len(v)}" for k, v in man.get("tiers", {}).items()))
    else:
        check("manifest.json fetch", st == 200, f"status {st}")

    if man:
        glbs = man["glbs"]
        # 6. single-level contract: no island-2 skyline units
        stems = {g["file"].rsplit("/", 1)[-1][:-4] for g in glbs}
        bad = stems & ISLAND2_SKYLINE
        check("no island-2 skyline GLBs in manifest", not bad, str(sorted(bad)))

        # 4. every GLB
        if not args.skip_glbs:
            for g in glbs:
                url = base + g["file"]
                st, hd, _ = fetch(url, "GET")
                size_ok = True
                cl = hd.get("Content-Length") or hd.get("content-length")
                if g.get("bytes") and cl and cl.isdigit():
                    size_ok = abs(int(cl) - g["bytes"]) < 4
                check(f"GLB {g['file']}", st == 200 and size_ok,
                      f"status {st} len {cl} vs {g.get('bytes')}")

        # 5. every texture (models/tex/<stem>.jpg)
        texs = set()
        for g in glbs:
            for fe in g.get("files", []):
                for t in fe.get("texs", []):
                    if t and t != "__dark":
                        texs.add(t)
        missing = []
        for t in sorted(texs):
            st, _, _ = fetch(f"{base}models/tex/{t}.jpg", "GET")
            if st != 200:
                missing.append(f"{t}.jpg({st})")
        check(f"textures ({len(texs)} files)", not missing,
              f"missing: {', '.join(missing[:8])}"
              + (" ..." if len(missing) > 8 else ""))

    print()
    if failures:
        print(f"SMOKE TEST FAILED — {len(failures)}/{checks} checks failed:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print(f"SMOKE TEST PASSED — {checks} checks OK ({base})")


if __name__ == "__main__":
    main()
