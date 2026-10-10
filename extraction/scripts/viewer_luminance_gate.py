#!/usr/bin/env python3
"""Headless luminance gate — a black render must not reach gh-pages.

Round-4 process rule: the v16 deploy shipped with the aux LUT/fog textures
missing; HTTP smoke checks passed 57/57 while the viewer rendered
whole-screen black (the LUT post pass nulls out).  This gate serves the
staged site locally, loads the real viewer in headless Chromium, waits for
the street tier to stream, screenshots the DEFAULT view, and fails when
mean luminance falls below --threshold (0-255).

Usage:
  python3 viewer_luminance_gate.py [--root DIR] [--port N]
      [--threshold 18] [--wait 30]
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
    return lum, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/z/my-project/work/ghpages_site")
    ap.add_argument("--port", type=int, default=8907)
    ap.add_argument("--threshold", type=float, default=8.0,
                    help="fail when mean luminance (0-255) is below this (calibrated: healthy night grade ~12.8, black-render failure mode <3)")
    ap.add_argument("--wait", type=float, default=30.0)
    ap.add_argument("--shot", default="/home/z/my-project/work/lum_gate.png")
    args = ap.parse_args()

    lum, errors = asyncio.run(run(args.root, args.port, args.threshold,
                                  args.wait, args.shot))
    ok = lum >= args.threshold
    if errors:
        print(f"page errors ({len(errors)}): {errors[:3]}")
    print("LUMINANCE GATE", "PASS" if ok and not errors else "FAIL")
    json.dump(dict(mean_luminance=lum, threshold=args.threshold,
                   page_errors=errors[:5]),
              open(os.path.join(os.path.dirname(args.shot) or ".",
                                "lum_gate_report.json"), "w"), indent=1)
    if not ok or errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
