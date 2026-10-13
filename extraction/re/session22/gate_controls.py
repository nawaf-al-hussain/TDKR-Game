#!/usr/bin/env python3
"""Synthetic controls for gate v2 spatial checks + fingerprint reference.

Controls (all must FAIL): black frame, half-black (top), right-half-dim at
mean 10, right-half-dim at mean 3, mid-load uniform frame (mean ~12.8).
Plus: capture staged/live screenshots, compute the fingerprint r between
them, and run the street-GLB-removal control through the full gate.
"""
import asyncio
import io
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/scripts")
from gate_v2 import spatial_checks, probe, serve, run_gate  # noqa

OUT = "/home/z/my-project/work"


def synth():
    H, W = 720, 1280
    results = {}

    def check(name, img):
        ok, reasons, detail = spatial_checks(img)
        results[name] = dict(ok=ok, mean=round(detail["mean"], 2),
                             asym=detail["lr_asymmetry"],
                             reasons=reasons[:2])
        print(f"  {name:34s} -> {'FAIL' if not ok else 'PASS!!'} "
              f"(mean {detail['mean']:.2f}, asym {detail['lr_asymmetry']:.2f})"
              f"  {reasons[:2]}")

    black = np.zeros((H, W), np.float32)
    check("black", black)

    half = np.zeros((H, W), np.float32)
    half[:H // 2] = 0.5
    check("half-black (top)", half)

    # right-half-dim tuned to overall mean 10
    for target in (10.0, 3.0):
        lo = 0.5
        hi = 2 * target - lo
        img = np.zeros((H, W), np.float32)
        img[:, :W // 2] = hi
        img[:, W // 2:] = lo
        check(f"right-half-dim @ mean {target:.0f}", img)

    uniform = np.full((H, W), 12.8, np.float32)
    check("mid-load uniform (mean 12.8)", uniform)

    json.dump(results, open(f"{OUT}/gate_controls.json", "w"), indent=1)


async def shots():
    shots = {}
    for name, root in (("staged", "/home/z/my-project/work/staging/staged_fixed"),
                       ("live", "/home/z/my-project/work/staging/staged_live")):
        serve(root, 8921 if name == "staged" else 8922)
        shot, glb, errs = await probe(root, 8921 if name == "staged" else 8922)
        shots[name] = np.asarray(Image.open(io.BytesIO(shot)).convert("L"),
                                 np.float32)
    np.save(f"{OUT}/ref_staged_128x72.npy",
            np.asarray(Image.fromarray(shots["staged"].astype(np.uint8))
                       .resize((128, 72)), np.float32))
    a = np.asarray(Image.fromarray(shots["staged"].astype(np.uint8))
                   .resize((128, 72)), np.float32)
    b = np.asarray(Image.fromarray(shots["live"].astype(np.uint8))
                   .resize((128, 72)), np.float32)
    r = float(np.corrcoef(a.ravel(), b.ravel())[0, 1])
    print(f"fingerprint r(staged, live) = {r:.3f}")
    json.dump(dict(staged_live_r=r), open(f"{OUT}/fingerprint.json", "w"))
    Image.fromarray(shots["staged"].astype(np.uint8)).save(
        f"{OUT}/shot_staged_fixed.png")
    Image.fromarray(shots["live"].astype(np.uint8)).save(
        f"{OUT}/shot_v17_live.png")


def glb_removal():
    root = "/home/z/my-project/work/staging/staged_noglb"
    os.system(f"rm -rf {root} && cp -r /home/z/my-project/work/staging/staged_fixed {root}")
    victim = None
    man = json.load(open(os.path.join(root, "models", "manifest.json")))
    for g in man["glbs"]:
        if g.get("tier") == "street":
            victim = g["file"]
            break
    os.remove(os.path.join(root, victim))
    print(f"street-GLB removal control: removed {victim}")
    report, _ = run_gate(root, 8923, None, f"{OUT}/gate_noglb.json")
    print(f"  -> verdict {report['verdict']} "
          f"(stream {report['stream_complete']})")


if __name__ == "__main__":
    print("-- synthetic spatial controls")
    synth()
    print("-- screenshots + fingerprint")
    asyncio.run(shots())
    print("-- street-GLB removal (full gate)")
    glb_removal()
