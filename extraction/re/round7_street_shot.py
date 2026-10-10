#!/usr/bin/env python3
"""Round-7 ask 4 + outstanding gates.

1. STREET-LEVEL BUILDING SHOTS from the LIVE v17 viewer (near-field, not
   top-down): pick large +40 building segments from the round-6 feature
   bank, place the camera at street level (z ~ 2-4 u) ~30-50 u away,
   target the block at mid-height, screenshot.
2. HEADLESS NETWORK-LOG GATE: log every response + failed request during
   the load; ANY 4xx/5xx (or failed request) = FAIL.  The URL crawl gate
   only sees static references; this sees what the running viewer
   actually fetches.

Outputs: extraction/previews/round7_street_*.png
         extraction/re/round7_netlog.json (+ stdout verdict)
"""
import asyncio
import json
import sys

sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from playwright.async_api import async_playwright  # noqa

RE = "/home/z/my-project/repo/extraction/re"
PREV = "/home/z/my-project/repo/extraction/previews"
URL = "https://nawaf-al-hussain.github.io/TDKR-Game/"

# building families from the +40 fine-family labels
BLD = {"building_residential", "building_landmark_misc",
       "building_footprint", "building_office"}


def pick_blocks():
    bank = json.load(open(f"{RE}/round6_geom_features.json"))
    B = bank["GothamCity"]
    n = len(B["m40"])
    cands = []
    for i in range(n):
        if B["fam40"][i] not in BLD:
            continue
        size = B["features"]["size_xy"][i]
        if size < 30:
            continue
        cands.append((B["centroid_xy"][i], size, B["fam40"][i],
                      B["features"]["zext"][i]))
    # spread: greedy pick with >=250u separation, largest first
    cands.sort(key=lambda c: -c[1])
    picked = []
    for c, size, fam, zext in cands:
        if all((c[0] - p[0][0]) ** 2 + (c[1] - p[0][1]) ** 2 > 250 ** 2
               for p in picked):
            picked.append((c, size, fam, zext))
        if len(picked) == 3:
            break
    return picked


async def main():
    blocks = pick_blocks()
    print("picked blocks:", [(tuple(map(int, c)), round(s, 1), f)
                             for c, s, f, z in blocks])
    net = dict(responses=[], failed=[], bad=[])
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader",
                                          "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})

        async def on_resp(r):
            net["responses"].append(dict(url=r.url, status=r.status))
            if r.status >= 400:
                net["bad"].append(dict(url=r.url,
                                                   status=r.status))

        pg.on("response", lambda r: asyncio.ensure_future(on_resp(r)))
        pg.on("requestfailed", lambda r: net["failed"].append(
            dict(url=r.url, err=str(r.failure)[:120])))
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        await pg.goto(URL, wait_until="load", timeout=90000)
        # wait for the city stream to finish (overlay shows 'streaming city')
        waited = 0
        for i in range(30):
            streaming = await pg.evaluate(
                "() => document.body.innerText.includes('streaming city')")
            if not streaming:
                break
            waited += 5
            await pg.wait_for_timeout(5000)
        print(f"streaming cleared after ~{waited}s")
        await pg.wait_for_timeout(4000)

        for k, (c, size, fam, zext) in enumerate(blocks):
            cx, cy = float(c[0]), float(c[1])
            # GLB is y-up: viewer (x, y, z) = world (x, z, -y).
            # street-level camera ~5u up, target at the block mid-height
            hmid = min(20.0, max(8.0, float(zext) * 0.35))
            await pg.evaluate(f"""() => {{
                const v = window.__v;
                v.controls.target.set({cx}, {hmid}, {-cy});
                v.camera.position.set({cx + 42.0}, 5.0, {-cy + 48.0});
                v.controls.update();
            }}""")
            await pg.wait_for_timeout(3500)
            out = f"{PREV}/round7_street_block{k}.png"
            await pg.screenshot(path=out)
            print(f"saved {out} (block world ({cx:.0f},{cy:.0f}), {fam}, "
                  f"size~{size:.0f}u, target h={hmid:.0f})")

        await b.close()

    bad = net["bad"] + net["failed"]
    net["n_responses"] = len(net["responses"])
    net["page_errors"] = errors[:8]
    net["verdict"] = "FAIL" if bad else "PASS"
    json.dump(net, open(f"{RE}/round7_netlog.json", "w"), indent=1)
    print(f"\nNETWORK GATE: {net['verdict']}  "
          f"({len(net['responses'])} responses, {len(net['failed'])} failed "
          f"requests, {len(net['bad'])} 4xx/5xx)")
    for r in bad[:10]:
        print("   ", r)
    if errors:
        print("page errors:", errors[:4])


if __name__ == "__main__":
    asyncio.run(main())
