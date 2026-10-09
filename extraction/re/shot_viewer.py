#!/usr/bin/env python3
"""Headless screenshots of the TDKR viewer at several camera positions."""
import asyncio
import sys
from playwright.async_api import async_playwright

async def shot(url, out, wait_ms=14000, cam=None, tier=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        pg.on("console", lambda m: errors.append(m.text[:150]) if m.type == "error" else None)
        await pg.goto(url)
        await pg.wait_for_timeout(wait_ms)
        if cam:
            await pg.evaluate(f"""() => {{
                const v = window.__v;
                if (v && v.camera) {{
                    v.camera.position.set({cam[0]}, {cam[1]}, {cam[2]});
                    v.controls && v.controls.target.set({cam[3]}, {cam[4]}, {cam[5]});
                    v.controls && v.controls.update();
                }}
            }}""")
            await pg.wait_for_timeout(2500)
        await pg.screenshot(path=out)
        print(f"{out}: errors={errors[:4]}")
        await b.close()

if __name__ == "__main__":
    url = "http://localhost:8899/index.html"
    # wait for load complete then default view
    asyncio.run(shot(url, "/home/z/my-project/work/shot_default.png", wait_ms=45000))
