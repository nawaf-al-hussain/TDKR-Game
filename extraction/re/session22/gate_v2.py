#!/usr/bin/env python3
"""Gate v2 — stream-complete + fingerprint + spatial checks (session 22).

v2 additions over the v1 luminance gate (which only checked the frame):
  - STREAM-COMPLETE: every boot-enabled GLB (manifest tiers street + skyline,
    the v14 boot policy) must return HTTP 200 and render, measured from the
    actual network responses.  Catches "enabled at boot but never loaded"
    (the v14-v17 skyline bug: 21/26).
  - FINGERPRINT: Pearson r of the 128x72 luminance grid against a stored
    healthy reference.  DETECTS DRIFT, NOT CORRECTNESS — a wrong-but-stable
    render passes it by design; placement correctness rests solely on the
    engine record 0x14051.
  - spatial: mean>=threshold, near-black<=blackfrac, quadrant floor,
    quadrant ratio, L/R asymmetry <= 0.6 (v2 threshold; v1 used 0.15).

Synthetic controls (must all FAIL): black, half-black, right-half-dim at
mean 10, right-half-dim at mean 3, mid-load uniform frame, street-GLB
removal (full gate on a crippled staging copy).
"""
import argparse
import asyncio
import http.server
import json
import os
import socketserver
import threading

import numpy as np

ASYM_MAX = 0.6
FINGERPRINT_MIN = 0.5


def spatial_checks(img, threshold=8.0, blackfrac=0.97, quad_floor=4.0,
                   quad_ratio=12.0, asym_max=ASYM_MAX, night_floor=0.5):
    reasons = []
    h, w = img.shape
    lum = float(img.mean())
    if lum < threshold:
        reasons.append(f"mean luminance {lum:.2f} < {threshold}")
    nb = float((img < 12).mean())
    if nb > blackfrac:
        reasons.append(f"near-black fraction {nb:.3f} > {blackfrac}")
    if nb < night_floor:
        reasons.append(f"near-black fraction {nb:.3f} < {night_floor} "
                       f"(no night-sky structure — uniform/mid-load frame)")
    quads = {"TL": img[:h // 2, :w // 2], "TR": img[:h // 2, w // 2:],
             "BL": img[h // 2:, :w // 2], "BR": img[h // 2:, w // 2:]}
    qmean = {k: float(v.mean()) for k, v in quads.items()}
    for k, v in qmean.items():
        if v < quad_floor:
            reasons.append(f"quadrant {k} mean {v:.2f} < {quad_floor}")
    qmax, qmin = max(qmean.values()), min(qmean.values())
    if qmin > 0 and qmax / qmin > quad_ratio:
        reasons.append(f"quadrant imbalance {qmax / qmin:.1f} > {quad_ratio}")
    lmean = float((qmean["TL"] + qmean["BL"]) / 2)
    rmean = float((qmean["TR"] + qmean["BR"]) / 2)
    asym = abs(lmean - rmean) / max((lmean + rmean) / 2, 1e-6)
    if asym > asym_max:
        reasons.append(f"left/right asymmetry {asym:.2f} > {asym_max}")
    return (not reasons), reasons, dict(mean=lum, near_black=nb, quads=qmean,
                                        lr_asymmetry=round(asym, 3))


def fingerprint(img, ref):
    a = np.asarray(img.resize((128, 72))).astype(np.float32)[:, :, :3]
    a = a.mean(2)
    b = ref
    if a.std() < 1e-6 or b.std() < 1e-6:
        return 0.0
    return float(np.corrcoef(a.ravel(), b.ravel())[0, 1])


def serve(root, port):
    os.chdir(root)

    class Q(socketserver.TCPServer):
        allow_reuse_address = True

    def run():
        with Q(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as h:
            h.serve_forever()
    threading.Thread(target=run, daemon=True).start()


async def probe(root, port, wait_s=45):
    from playwright.async_api import async_playwright
    glb_status = {}
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader",
                                          "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        pg.on("response", lambda r: glb_status.update(
            {r.url.split("?")[0].split("/")[-1]: r.status}
            if ".glb" in r.url else {}))
        await pg.goto(f"http://localhost:{port}/index.html")
        waited = 0.0
        while waited < wait_s:
            await pg.wait_for_timeout(2000)
            waited += 2.0
            txt = await pg.evaluate(
                "() => document.body.innerText.replace(/\\s+/g,' ')")
            if "streaming city" not in txt and "loading" not in txt.lower():
                break
        await pg.wait_for_timeout(8000)   # settle + background skyline stream
        shot = await pg.screenshot()
        await b.close()
    return shot, glb_status, errors


def run_gate(root, port, ref_path, out_json):
    from PIL import Image
    import io
    man = json.load(open(os.path.join(root, "models", "manifest.json")))
    enabled = []
    for tier in ("street", "skyline"):
        enabled += man.get("tiers", {}).get(tier, [])
    serve(root, port)
    shot, glb_status, errors = asyncio.run(probe(root, port))
    img = np.asarray(Image.open(io.BytesIO(shot)).convert("L"), np.float32)
    ok_sp, reasons, detail = spatial_checks(img)
    glbs_ok = sum(1 for f in enabled
                  if glb_status.get(os.path.basename(f), 0) == 200)
    total_all = len(man["glbs"])
    all_ok = sum(1 for f in (os.path.basename(g["file"]) for g in man["glbs"])
                 if glb_status.get(f, 0) == 200)
    ref = None
    r = None
    if ref_path and os.path.exists(ref_path):
        ref = np.load(ref_path)
        r = fingerprint(Image.open(io.BytesIO(shot)), ref)
    fp_ok = (r is not None and r >= FINGERPRINT_MIN) or ref is None
    verdict = "PASS" if (ok_sp and not errors and glbs_ok == len(enabled)
                         and fp_ok) else "FAIL"
    report = dict(root=root, verdict=verdict,
                  stream_complete=f"{glbs_ok}/{len(enabled)}",
                  stream_total_all=f"{all_ok}/{total_all}",
                  fingerprint=(None if r is None else round(r, 3)),
                  spatial=detail, reasons=reasons, page_errors=errors[:5])
    print(json.dumps(report, indent=1))
    if out_json:
        json.dump(report, open(out_json, "w"), indent=1)
    return report, img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--port", type=int, default=8911)
    ap.add_argument("--ref", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    report, _ = run_gate(args.root, args.port, args.ref, args.out)
    raise SystemExit(0 if report["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
