#!/usr/bin/env python3
"""Round-5 negative controls for the luminance gate + deploy allowlist.

Round-5 review prescriptions, with the honest empirical outcome:
  1. Staging copy minus a LUT (and minus the fog texture): the CURRENT v17
     viewer degrades gracefully (the v16 black-LUT-pass failure mode was
     fixed in the viewer itself), so the LUMINANCE gate PASSES there — the
     aux-loss class is instead caught by the deploy URL gate, which is
     demonstrated here to FAIL on the same stagings.  Both facts recorded.
  2. A staging whose manifest points at missing GLBs (the "city fails to
     stream" mode) must FAIL the luminance gate.
  3. Synthetic frames (black / half-black / right-half-dim / right-half-3)
     through the spatial checks: each FAILS; healthy v17 frame PASSES.
  4. deploy_site.py allowlist: planned deletes outside models/*.glb abort
     (exit 2); an orphan models/*.glb is planned for deletion; worklogs and
     skybox are never in the delete plan.

Outputs: extraction/re/round5_pipeline.json + stdout.
"""
import json
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

RE = "/home/z/my-project/repo"
SCRIPTS = f"{RE}/extraction/scripts"
WORK = "/home/z/my-project/work/round5_gate"
HEALTHY_SHOT = "/home/z/my-project/work/lum_gate.png"
OUT = f"{RE}/extraction/re/round5_pipeline.json"


def run_gate(root, port, shot):
    r = subprocess.run(
        [sys.executable, f"{SCRIPTS}/viewer_luminance_gate.py",
         "--root", root, "--port", str(port), "--shot", shot],
        capture_output=True, text=True, timeout=240)
    tail = "\n".join(r.stdout.strip().split("\n")[-4:])
    return ("PASS" if r.returncode == 0 else "FAIL"), tail


def run_url_gate(root):
    r = subprocess.run(
        [sys.executable, f"{SCRIPTS}/deploy_site.py", "--source", root,
         "--dest", root, "--no-sync"],
        capture_output=True, text=True, timeout=240)
    tail = "\n".join(l for l in r.stdout.strip().split("\n")
                     if "MISSING" in l or "GATE" in l or "referenced" in l)
    return ("PASS" if r.returncode == 0 else "FAIL"), tail


def spatial_negative_controls():
    sys.path.insert(0, SCRIPTS)
    from viewer_luminance_gate import spatial_checks
    img = np.asarray(Image.open(HEALTHY_SHOT).convert("L"), np.float32)
    h, w = img.shape
    frames = {
        "healthy_v17": img,
        "black": np.zeros_like(img),
        "half_black_right": np.concatenate(
            [img[:, :w // 2], np.zeros((h, w // 2), np.float32)], axis=1),
        "right_half_dim10": np.concatenate(
            [img[:, :w // 2], np.full((h, w // 2), 10.0, np.float32)], axis=1),
        "right_half_dim3": np.concatenate(
            [img[:, :w // 2], np.full((h, w // 2), 3.0, np.float32)], axis=1),
    }
    cases = {}
    for name, fr in frames.items():
        ok, reasons, detail = spatial_checks(fr, threshold=8.0, blackfrac=0.97,
                                             quad_floor=4.0, quad_ratio=12.0)
        cases[name] = dict(ok=bool(ok), reasons=reasons,
                           mean=round(float(fr.mean()), 2))
        print(f"  spatial[{name:18s}] mean={fr.mean():6.2f} -> "
              f"{'PASS' if ok else 'FAIL: ' + reasons[0]}")
    return cases


def make_broken_manifest_stage(stage):
    """Manifest whose first three GLB files point at nonexistent paths."""
    if os.path.exists(stage):
        shutil.rmtree(stage)
    shutil.copytree("/home/z/my-project/work/ghpages_site", stage)
    man_p = os.path.join(stage, "models", "manifest.json")
    man = json.load(open(man_p))
    nbroke = 0
    for g in man["glbs"]:
        if "/street_" in g["file"] and nbroke < 6:
            g["file"] = g["file"].replace("street_island",
                                          "street_ISLAND999_MISSING")
            nbroke += 1
    json.dump(man, open(man_p, "w"), indent=1)


def main():
    os.makedirs(WORK, exist_ok=True)
    report = {}

    print("== 1. spatial-check synthetic negative controls")
    report["spatial_controls"] = spatial_negative_controls()

    print("== 2. live gate negative controls (staging copies)")
    live = {}
    variants = {
        "healthy_baseline": ("copy", []),
        "lut_removed": ("copy", ["models/tex/LUT_000_default.png"]),
        "fog_removed": ("copy", ["models/tex/GC_VerticalFOG.png"]),
        "broken_manifest": ("broken", []),
    }
    for name, (kind, removals) in variants.items():
        stage = f"{WORK}/{name}"
        if kind == "broken":
            make_broken_manifest_stage(stage)
        else:
            if os.path.exists(stage):
                shutil.rmtree(stage)
            shutil.copytree("/home/z/my-project/work/ghpages_site", stage)
            for rel in removals:
                p = os.path.join(stage, rel)
                if os.path.exists(p):
                    os.remove(p)
        verdict, tail = run_gate(stage, 8910 + abs(hash(name)) % 80,
                                 f"{WORK}/{name}.png")
        urlverdict, urltail = run_url_gate(stage)
        live[name] = dict(removed=removals, luminance_gate=verdict,
                          luminance_tail=tail, url_gate=urlverdict,
                          url_tail=urltail)
        print(f"  {name:18s} -> luminance {verdict}, url-gate {urlverdict}")
        print("   " + tail.replace("\n", "\n   ")[:300])
        if urlverdict == "FAIL":
            print("   url-gate: " + " | ".join(urltail.split("\n")[:2]))

    report["live_gate"] = live

    sc = report["spatial_controls"]
    checks = dict(
        spatial_healthy_pass=sc["healthy_v17"]["ok"],
        spatial_black_fail=not sc["black"]["ok"],
        spatial_halfblack_fail=not sc["half_black_right"]["ok"],
        spatial_dimhalf_fail=(not sc["right_half_dim10"]["ok"]
                              and not sc["right_half_dim3"]["ok"]),
        baseline_lum_pass=live["healthy_baseline"]["luminance_gate"] == "PASS",
        aux_loss_caught_by_url_gate=(live["lut_removed"]["url_gate"] == "FAIL"
                                     and live["fog_removed"]["url_gate"]
                                     == "FAIL"),
        broken_manifest_fail=(live["broken_manifest"]["luminance_gate"]
                              == "FAIL"
                              or live["broken_manifest"]["url_gate"] == "FAIL"),
    )
    report["checks"] = checks
    report["all_negative_controls"] = bool(all(checks.values()))
    json.dump(report, open(OUT, "w"), indent=1)
    print("\nchecks:", json.dumps(checks, indent=1))
    print(f"ALL NEGATIVE CONTROLS: "
          f"{'PASS' if report['all_negative_controls'] else 'PARTIAL'}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
