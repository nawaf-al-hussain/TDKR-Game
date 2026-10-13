#!/usr/bin/env python3
"""T2/T4 — A/B renders from the staged site (v19).

Views: default (viewer boot camera), block0 (SW road anchor), plaza
(crossing segment).  Each in two chain modes:
  default URL          -> v17 UVs (unchanged default)
  ?chain=engine        -> engine UVs (TEXCOORD_2/3 + GL_REPEAT)
Camera driven via the window.__v debug hook (viewer y-up: game (x,y,z) ->
viewer (x, z, -y)).
"""
import asyncio
import http.server
import json
import os
import socketserver
import sys
import threading

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/z/my-project/work/staged_wt"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/z/my-project/work"
PORT = 8923

VIEWS = {
    "block0": dict(target=(-568.6, 2.0, 1098.5), r=120.0),
    "plaza": dict(target=(-23.9, 2.0, 0.1), r=116.0),
}


def serve(root, port):
    os.chdir(root)

    class Q(socketserver.TCPServer):
        allow_reuse_address = True

    def run():
        with Q(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as h:
            h.serve_forever()
    threading.Thread(target=run, daemon=True).start()


async def shot(pg, url, name, wait_stream=True):
    await pg.goto(url)
    if wait_stream:
        waited = 0.0
        while waited < 60:
            await pg.wait_for_timeout(2000)
            waited += 2.0
            txt = await pg.evaluate(
                "() => document.body.innerText.replace(/\\s+/g,' ')")
            if "streaming city" not in txt and "loading" not in txt.lower():
                break
    await pg.wait_for_timeout(9000)  # settle + skyline stream
    await pg.screenshot(path=f"{OUT}/{name}.png")
    print("saved", name)


async def main():
    from playwright.async_api import async_playwright
    serve(ROOT, PORT)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader",
                                          "--enable-unsafe-swiftshader"])
        base = f"http://localhost:{PORT}/index.html"
        # 1. default view, both chains
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        await shot(pg, base, "ab_default_v17chain")
        await shot(pg, base + "?chain=engine", "ab_default_engine")

        # 2. block0 / plaza, both chains (camera via __v hook)
        for vname, vw in VIEWS.items():
            tx, ty, tz = vw["target"]
            r = vw["r"]
            for chain, suffix in (("", "v17chain"), ("?chain=engine", "engine")):
                url = base + chain
                await pg.goto(url)
                waited = 0.0
                while waited < 60:
                    await pg.wait_for_timeout(2000)
                    waited += 2.0
                    txt = await pg.evaluate(
                        "() => document.body.innerText.replace(/\\s+/g,' ')")
                    if "streaming city" not in txt and \
                       "loading" not in txt.lower():
                        break
                await pg.wait_for_timeout(4000)
                await pg.evaluate(
                    f"""() => {{
                      const v = window.__v;
                      v.controls.target.set({tx}, {ty}, {tz});
                      v.camera.position.set({tx + 1.05 * r:.1f},
                                            {ty + 0.62 * r:.1f},
                                            {tz + 1.05 * r:.1f});
                      v.controls.update();
                    }}""")
                await pg.wait_for_timeout(4000)
                await pg.screenshot(path=f"{OUT}/ab_{vname}_{suffix}.png")
                print(f"saved ab_{vname}_{suffix}")
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
