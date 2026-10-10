#!/usr/bin/env python3
"""Session 16 — visual verification of the v16 street tier (+40 bindings).
Serves work/ghpages_site locally, fixed cameras, screenshots to work/valout16.
"""
import asyncio
import http.server
import os
import socketserver
import threading

from playwright.async_api import async_playwright

ROOT = "/home/z/my-project/work/ghpages_site"
OUT = "/home/z/my-project/work/valout16"
PORT = 8899

os.chdir(ROOT)
os.makedirs(OUT, exist_ok=True)


class Q(socketserver.TCPServer):
    allow_reuse_address = True


def serve():
    handler = http.server.SimpleHTTPRequestHandler
    with Q(("127.0.0.1", PORT), handler) as httpd:
        httpd.serve_forever()


threading.Thread(target=serve, daemon=True).start()

SHOTS = [
    ("overview", 28000, [-2600, 2100, 2900, -500, 0, 900]),
    ("street_close_north", 22000, [-500, 420, 1500, -720, 10, -780]),
    ("street_park", 18000, [-300, 300, 400, -720, 10, -300]),
    ("street_low_angle", 16000, [-900, 60, -300, -700, 20, -700]),
]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader",
                                          "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        console = []
        pg.on("console", lambda m: console.append(m.text[:200])
              if m.type in ("error", "warning") else None)
        await pg.goto(f"http://localhost:{PORT}/index.html")
        await pg.wait_for_timeout(28000)
        status = await pg.evaluate("() => document.body.innerText.slice(0, 400)")
        print("STATUS:", status.replace("\n", " | ")[:300])
        for name, wait, cam in SHOTS:
            await pg.evaluate(f"""() => {{
                const v = window.__v;
                if (v && v.camera) {{
                    v.camera.position.set({cam[0]}, {cam[1]}, {cam[2]});
                    v.controls && v.controls.target.set({cam[3]}, {cam[4]},
                                                        {cam[5]});
                    v.controls && v.controls.update();
                }}
            }}""")
            await pg.wait_for_timeout(wait)
            await pg.screenshot(path=os.path.join(OUT, f"shot_{name}.png"))
            print(f"shot_{name}.png done")
        if errors:
            print("page errors:", errors[:6])
        if console:
            print("console:", console[:8])
        await b.close()

asyncio.run(main())
