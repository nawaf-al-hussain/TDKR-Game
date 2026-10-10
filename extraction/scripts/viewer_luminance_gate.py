#!/usr/bin/env python3
"""Headless luminance gate — a black render must not reach gh-pages.

Round-4 process rule: the v16 deploy shipped with the aux LUT/fog textures
missing; HTTP smoke checks passed 57/57 while the viewer rendered
whole-screen black (the LUT post pass nulls out).  This gate serves the
staged site locally, loads the real viewer in headless Chromium, waits for
the street tier to stream, screenshots the DEFAULT view, and fails when
any of the following trip (round-5 additions in caps):
  - mean luminance below --threshold (0-255)
  - NEAR-BLACK PIXEL FRACTION above --blackfrac (a night sky is ~0.85;
    a dead WebGL context is ~1.0)
  - ANY QUADRANT's mean luminance below --quad-floor (half a black frame
    cannot pass on mean luminance alone)
  - QUADRANT IMBALANCE max/min above --quad-ratio (dark-half renders)

Negative controls (round-5): staging copies with the LUT / fog texture
removed must FAIL this gate; see round5_gate_negative_controls.py.

Usage:
  python3 viewer_luminance_gate.py [--root DIR] [--port N]
      [--threshold 8] [--wait 30]
Exit 0 = luminance OK and no page errors; 1 = gate failed.
"""
import argparse
import asyncio
import http.server
import json
import os
import socketserver
import threading

from playwright.async_api import async_playwright


def spatial_checks(img, threshold, blackfrac, quad_floor, quad_ratio,
                   asym_max=0.15):
    """Return (ok, reasons, detail).  img: 2D float luminance 0-255.
    Calibrated on the healthy v17 default view: mean 12.79, near-black
    (<12) fraction 0.846, quadrant means 8.94-16.66 (ratio 1.86),
    left/right asymmetry ~0.03 (default camera looks down a street axis).
    asym_max is default-view-specific by design (the gate always shoots
    the default view); it catches half-dim renders that keep their means."""
    reasons = []
    h, w = img.shape
    lum = float(img.mean())
    if lum < threshold:
        reasons.append(f"mean luminance {lum:.2f} < {threshold}")
    nb = float((img < 12).mean())
    if nb > blackfrac:
        reasons.append(f"near-black fraction {nb:.3f} > {blackfrac}")
    quads = {"TL": img[:h // 2, :w // 2], "TR": img[:h // 2, w // 2:],
             "BL": img[h // 2:, :w // 2], "BR": img[h // 2:, w // 2:]}
    qmean = {k: float(v.mean()) for k, v in quads.items()}
    for k, v in qmean.items():
        if v < quad_floor:
            reasons.append(f"quadrant {k} mean {v:.2f} < {quad_floor} "
                           f"(partial black frame)")
    qmax, qmin = max(qmean.values()), min(qmean.values())
    if qmin > 0 and qmax / qmin > quad_ratio:
        reasons.append(f"quadrant imbalance {qmax / qmin:.1f} > "
                       f"{quad_ratio} (half-dark frame)")
    lmean = float((qmean["TL"] + qmean["BL"]) / 2)
    rmean = float((qmean["TR"] + qmean["BR"]) / 2)
    asym = abs(lmean - rmean) / max((lmean + rmean) / 2, 1e-6)
    if asym > asym_max:
        reasons.append(f"left/right asymmetry {asym:.2f} > {asym_max} "
                       f"(half-dim render)")
    return (not reasons), reasons, dict(mean=lum, near_black=nb, quads=qmean,
                                        lr_asymmetry=round(asym, 3))


async def run(root, port, threshold, wait_s, shot_path):
    os.chdir(root)

    class Q(socketserver.TCPServer):
        allow_reuse_address = True

    def serve():
        with Q(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as h:
            h.serve_forever()

    threading.Thread(target=serve, daemon=True).start()

    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader",
                                          "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        await pg.goto(f"http://localhost:{port}/index.html")
        # wait until the streaming indicator is done (or timeout)
        deadline = wait_s
        waited = 0.0
        while waited < deadline:
            await pg.wait_for_timeout(2000)
            waited += 2.0
            txt = await pg.evaluate(
                "() => document.body.innerText.replace(/\\s+/g,' ')")
            if "streaming city" not in txt and "loading" not in txt.lower():
                break
        await pg.wait_for_timeout(4000)   # settle + first frames
        status = await pg.evaluate("() => document.body.innerText.slice(0, 300)")
        await pg.screenshot(path=shot_path)
        await b.close()

    from PIL import Image
    import numpy as np
    img = np.asarray(Image.open(shot_path).convert("L"), np.float32)
    lum = float(img.mean())
    print(f"STATUS: {status[:160]}")
    print(f"mean luminance: {lum:.2f} / 255   (threshold {threshold})")
    return lum, errors, img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/z/my-project/work/ghpages_site")
    ap.add_argument("--port", type=int, default=8907)
    ap.add_argument("--threshold", type=float, default=8.0,
                    help="fail when mean luminance (0-255) is below this "
                         "(calibrated: healthy night grade ~12.8, black "
                         "render <3)")
    ap.add_argument("--blackfrac", type=float, default=0.97,
                    help="fail when the fraction of near-black (<12) pixels "
                         "exceeds this (healthy ~0.846, dead context ~1.0)")
    ap.add_argument("--quad-floor", type=float, default=4.0,
                    help="fail when any image quadrant's mean is below this")
    ap.add_argument("--quad-ratio", type=float, default=12.0,
                    help="fail when max/min quadrant mean exceeds this")
    ap.add_argument("--wait", type=float, default=30.0)
    ap.add_argument("--shot", default="/home/z/my-project/work/lum_gate.png")
    args = ap.parse_args()

    lum, errors, img = asyncio.run(run(args.root, args.port, args.threshold,
                                       args.wait, args.shot))
    ok, reasons, detail = spatial_checks(img, args.threshold, args.blackfrac,
                                         args.quad_floor, args.quad_ratio)
    if errors:
        print(f"page errors ({len(errors)}): {errors[:3]}")
    print(f"spatial: mean {detail['mean']:.2f}, near-black "
          f"{detail['near_black']:.3f}, L/R asym {detail['lr_asymmetry']:.2f}, "
          f"quadrants "
          + " ".join(f"{k}={v:.2f}" for k, v in detail['quads'].items()))
    for r in reasons:
        print(f"  SPATIAL FAIL: {r}")
    verdict = "PASS" if ok and not errors else "FAIL"
    print("LUMINANCE GATE", verdict)
    json.dump(dict(mean_luminance=lum, threshold=args.threshold,
                   spatial=detail, reasons=reasons, page_errors=errors[:5],
                   verdict=verdict),
              open(os.path.join(os.path.dirname(args.shot) or ".",
                                "lum_gate_report.json"), "w"), indent=1)
    if not ok or errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
