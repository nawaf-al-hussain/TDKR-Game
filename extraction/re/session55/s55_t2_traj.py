#!/usr/bin/env python3
"""s55 T2(b)+(c): capture live ?s5=1 (decoded) and ?s5=1&s5legacy=1 (placeholder control)
trajectories; compute speed-over-time and altitude-lost-per-metre; compare with the
engine-implied analytic model (speed = f5 + (f6-f5)*(2/pi)*|pitch|, sink = f0 + (f1-f0)*(2/pi)*|pitch|)."""
import json, time, math
from playwright.sync_api import sync_playwright

BASE = "https://nawaf-al-hussain.github.io/TDKR-Game/playable/integration_lazy.html"
ZIP = "/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip"
OUT = "/tmp/my-project/work/TDKR-Game/extraction/re/session55/s55_t2_traj.json"

def capture(url, label):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--enable-unsafe-swiftshader"])
        page = browser.new_page()
        page.goto(url, timeout=45000, wait_until="load")
        time.sleep(1)
        page.set_input_files("input[type=file]", ZIP)
        for _ in range(120):
            time.sleep(1)
            try:
                done = page.evaluate("() => !!(window.__GATE && window.__GATE.soup)")
            except Exception:
                done = False
            if done:
                break
        time.sleep(12)
        st = page.evaluate("() => ({ s5: window.__GATE && window.__GATE.s5, params: window.__S5P || null })")
        browser.close()
    print(label, "s5:", json.dumps(st.get("s5", {}))[:300])
    return st

dec = capture(BASE + "?s5=1", "decoded")
leg = capture(BASE + "?s5=1&s5legacy=1", "legacy")

def measures(st):
    s5 = (st or {}).get("s5") or {}
    traj = s5.get("traj") or []
    if len(traj) < 3:
        return {"traj_n": len(traj), "s5": s5}
    # glide phase: from first sample after grapple (use all samples; the traj is glide-dominated)
    xs = [p["x"] for p in traj]; ys = [p["y"] for p in traj]; ts = [p["t"] for p in traj]
    zs = [p["z"] for p in traj]; vzs = [p.get("vz") for p in traj]
    # horizontal speed between consecutive samples (units: x,y in world units, t ms)
    sp = []
    for i in range(1, len(traj)):
        dt = (ts[i] - ts[i - 1]) / 1000.0
        if dt > 0:
            d = math.hypot(xs[i] - xs[i - 1], ys[i] - ys[i - 1])
            sp.append(d / dt)
    # altitude per metre over the whole glide window
    dz = zs[0] - zs[-1]
    dh = math.hypot(xs[-1] - xs[0], ys[-1] - ys[0])
    return {
        "traj_n": len(traj), "span_ms": ts[-1] - ts[0],
        "mean_h_speed": round(sum(sp) / len(sp), 3) if sp else None,
        "h_speed_first_last": [round(sp[0], 2), round(sp[-1], 2)] if len(sp) > 1 else None,
        "alt_lost": round(dz, 2), "horiz_dist": round(dh, 2),
        "alt_per_m": round(dz / dh, 3) if dh > 0 else None,
        "vz_mean": round(sum(v for v in vzs if v is not None) / max(1, len([v for v in vzs if v is not None])), 3),
        "landed": s5.get("landed"), "landMs": s5.get("landMs"),
        "glideClipActive": s5.get("glideClipActive"),
        "traj": traj,
    }

md, ml = measures(dec), measures(leg)
# engine-implied at staged pitch0 = -45 deg (no upgrade): speed = 1 + 5*(2/pi)*sin? — pitch_rad = 45*pi/180
pr = math.radians(45)
eng_speed = 1 + 5 * (2 / math.pi) * pr
eng_sink = 4 + 12 * (2 / math.pi) * pr
eng_apm = eng_sink / eng_speed
res = {
    "decoded": md, "legacy": ml,
    "engine_implied": {"pitch0_deg": -45, "pitch_rad": pr,
                       "speed": round(eng_speed, 3), "sink": round(eng_sink, 3),
                       "alt_per_m": round(eng_apm, 3),
                       "model": "RefreshForcesGlide: speed=f5+(f6-f5)*(2/pi)|p|; sink=f0+(f1-f0)*(2/pi)|p|"},
    "delta_control": {
        "speed_dec_vs_leg": (md.get("mean_h_speed"), ml.get("mean_h_speed")),
        "apm_dec_vs_leg": (md.get("alt_per_m"), ml.get("alt_per_m")),
        "moved": (md.get("mean_h_speed") != ml.get("mean_h_speed")) or (md.get("alt_per_m") != ml.get("alt_per_m")),
    },
    "clip_lengths_ms": {"_057_glide_idle": 2167, "_065_glide_idle_to_run": 667,
                        "_089_grapnel_pull": 1899, "_088_grapnel_shoot": 432,
                        "slice_landing_excerpt_ms": 450},
}
json.dump(res, open(OUT, "w"), indent=1)
print("\nengine-implied: speed %g sink %g alt/m %g" % (eng_speed, eng_sink, eng_apm))
print("decoded:", {k: v for k, v in md.items() if k != "traj"})
print("legacy :", {k: v for k, v in ml.items() if k != "traj"})
print("control moved:", res["delta_control"]["moved"])
print("->", OUT)
