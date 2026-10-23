#!/usr/bin/env python3
"""s55 T5: second software renderer test — run city_bisect2.html?gpucheck=1 under
X11/--use-gl=gl (Mesa/llvmpipe path) vs --use-angle=swiftshader (baseline), compare
the __GPUCHECK blocks (whole-zone corr/ratio, per-step ratios, renderer string)."""
import json, time, sys, threading, subprocess, os
from playwright.sync_api import sync_playwright

ROOT = "/tmp/my-project/work/city_slice_wt"
PORT = 8143
ZIP = "/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip"
OUT = "/tmp/my-project/work/TDKR-Game/extraction/re/session55/s55_t5_gpu2.json"

def serve():
    subprocess.run([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT, capture_output=True)
threading.Thread(target=serve, daemon=True).start()
time.sleep(1.0)

VARIANTS = [
    ("x11_gl", ["--use-gl=gl", "--no-sandbox"]),
    ("x11_swiftshader", ["--use-gl=angle", "--use-angle=swiftshader", "--no-sandbox"]),
]
res = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, args=VARIANTS[0][1])
    ctx = browser.new_context(viewport={"width": 1024, "height": 768})
    page = ctx.new_page()
    page.goto("data:text/html,<canvas id=c></canvas><script>const gl=document.getElementById('c').getContext('webgl');window.R=gl?gl.getParameter(gl.RENDERER):'NULL';</script>")
    print("probe under x11_gl:", page.evaluate("window.R"))
    browser.close()
    for name, args in VARIANTS:
        browser = pw.chromium.launch(headless=False, args=args)
        ctx = browser.new_context(viewport={"width": 1024, "height": 768})
        page = ctx.new_page()
        cerr = []
        page.on("pageerror", lambda e, c=cerr: c.append(str(e)[:120]))
        url = f"http://localhost:{PORT}/playable/city_bisect2.html?gpucheck=1"
        page.goto(url, timeout=60000, wait_until="load")
        time.sleep(1.5)
        page.set_input_files("input[type=file]", ZIP)
        gpu = None
        for i in range(150):
            time.sleep(2)
            try:
                gpu = page.evaluate("() => window.__GPUCHECK || null")
            except Exception:
                gpu = None
            if gpu and gpu.get("done"):
                break
        res[name] = {"gpucheck": gpu, "page_errors": cerr[:6],
                     "elapsed_s": round(2 * i, 1)}
        # keep only the summary fields to keep the receipt small
        if gpu:
            keep = {k: v for k, v in gpu.items() if k in ("renderer", "corr", "ratio", "steps", "wholeZone", "unitAudit", "wronglm", "corrVsRef", "done") or not isinstance(v, (list, dict))}
            res[name]["summary"] = keep
        ctx.close()
        browser.close()
        print(name, "->", json.dumps(res[name]["summary"] if gpu else None)[:400])

json.dump(res, open(OUT, "w"), indent=1)
print("->", OUT)
