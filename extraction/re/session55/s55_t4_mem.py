#!/usr/bin/env python3
"""s55 T4: memory breakdown — poolchunk mode with CDP metrics + renderer RSS sampling.
Attribution: RSS vs JS-heap(CDP) => native/GPU/client copies; plus empty-page baseline
for the chromium/swiftshader floor."""
import json, time, subprocess, sys, threading
from playwright.sync_api import sync_playwright

PORT = 8141
ROOT = "/tmp/s54_smoke"
ZIP = "/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip"
OUT = "/tmp/my-project/work/TDKR-Game/extraction/re/session55/s55_t4_mem.json"

def serve():
    subprocess.run([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT, capture_output=True)
threading.Thread(target=serve, daemon=True).start()
time.sleep(1.0)

def rss_mb(pid):
    try:
        s = open(f"/proc/{pid}/status").read()
        for line in s.splitlines():
            if line.startswith("VmRSS"):
                return int(line.split()[1]) / 1024.0
    except Exception:
        return None
    return None

results = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--enable-unsafe-swiftshader"])
    for label, url, with_zip in [
        ("empty_three", f"http://localhost:{PORT}/playable/walktest.html", False),
        ("poolchunk", f"http://localhost:{PORT}/playable/integration_lazy.html?poolchunk=1", True),
    ]:
        ctx = browser.new_context()
        page = ctx.new_page()
        proc = page.context.browser  # need renderer pid: use CDP
        cdp = ctx.new_cdp_session(page)
        cdp.send("Performance.enable")
        samples = []
        t0 = time.time()
        page.goto(url, timeout=45000, wait_until="load")
        if with_zip:
            time.sleep(1)
            page.set_input_files("input[type=file]", ZIP)
        for i in range(40):
            time.sleep(2)
            try:
                m = cdp.send("Performance.getMetrics")["metrics"]
                md = {x["name"]: x["value"] for x in m}
            except Exception:
                md = {}
            # renderer process: find via ps children of the browser (approx: max RSS child)
            rss = None
            try:
                out = subprocess.run(["pgrep", "-f", "type=renderer"], capture_output=True, text=True).stdout.split()
                rss = max((rss_mb(int(p)) or 0) for p in out) if out else None
            except Exception:
                pass
            samples.append({"t": round(time.time() - t0, 1),
                            "jsHeapMB": round(md.get("JSHeapUsedSize", 0) / 1048576, 1),
                            "jsHeapTotalMB": round(md.get("JSHeapTotalSize", 0) / 1048576, 1),
                            "rssMB": round(rss, 1) if rss else None})
        gate = page.evaluate("() => { const g = window.__GATE || {}; return {"
                             "soup: g.soup || null, routes: g.routes ? {run: g.routes.run, agree: g.routes.agree} : null}; }")
        # peak renderer RSS across the window
        peak_rss = max((s["rssMB"] or 0) for s in samples)
        peak_js = max(s["jsHeapMB"] for s in samples)
        first_img = next((s["t"] for s in samples if s["rssMB"] and s["rssMB"] > (results.get("empty_three", {}).get("peak_rss", 100))), None)
        results[label] = {"samples": samples[::2], "peak_rss": peak_rss, "peak_js": peak_js,
                          "native_residual": round(peak_rss - peak_js, 1), "gate": gate}
        ctx.close()
    browser.close()

json.dump(results, open(OUT, "w"), indent=1)
for k, r in results.items():
    print(f"{k:12s} peak_rss={r['peak_rss']} MB peak_js={r['peak_js']} MB native={r['native_residual']} MB")
print("poolchunk gate:", json.dumps(results["poolchunk"]["gate"]))
print("->", OUT)
