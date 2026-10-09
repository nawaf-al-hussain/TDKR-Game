#!/usr/bin/env python3
"""Review test 6 — fixed-camera screenshots above the street-tier bbox,
skyline tier ON vs OFF, plus a wide overview. Serves gh-pages locally."""
import asyncio
import http.server
import os
import socketserver
import threading

from playwright.async_api import async_playwright

ROOT = "/home/z/my-project/work/TDKR-Game/gh-pages"
OUT = "/home/z/my-project/work/valout"
PORT = 8899

os.chdir(ROOT)


class Q(socketserver.TCPServer):
    allow_reuse_address = True


def serve():
    handler = http.server.SimpleHTTPRequestHandler
    with Q(("127.0.0.1", PORT), handler) as httpd:
        httpd.serve_forever()


threading.Thread(target=serve, daemon=True).start()

# camera above the street-tier bbox (street island1 center ~ (-717, -780)
# game XY -> glTF (x, z, -y): glTF pos = (-717, h, 780); look at city center
SHOTS = [
    # name, wait, cam[px,py,pz, tx,ty,tz], skyline toggle
    ("overview_default", 30000, [-2600, 2100, 2900, -500, 0, 900], None),
    ("street_close_skyline_on", 30000,
     [-500, 420, 1500, -720, 10, -780], None),
    ("street_close_skyline_off", 26000,
     [-500, 420, 1500, -720, 10, -780], "off"),
    ("skyline_from_above", 26000, [-1100, 900, 640, -1100, 0, -1250], None),
]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader",
                                          "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        await pg.goto(f"http://localhost:{PORT}/index.html")
        await pg.wait_for_timeout(30000)
        for name, wait, cam, sky in SHOTS:
            if sky == "off":
                # toggle skyline tier off via its button
                await pg.evaluate("""() => {
                    const btns=[...document.querySelectorAll('.tier-btn')];
                    const b=btns.find(x=>x.textContent.includes('Skyline'));
                    if (b) b.click();
                }""")
                await pg.wait_for_timeout(3000)
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
        await b.close()

asyncio.run(main())
