
import json, re, zipfile
import numpy as np
z = zipfile.ZipFile("/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip")
gla = z.read("com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla")
pat = re.compile(rb"GetDistFromMC\s*\(\s*[\w.\[\]\"]+\s*\)\s*(<|>|<=|>=|==)\s*([0-9]+\.?[0-9]*)")
ctxs = []
for mt in pat.finditer(gla):
    pos = mt.start()
    pre = gla[max(0, pos-80):pos]
    if pre.rstrip().endswith(b"--"):
        continue
    ctxs.append({"rel": mt.group(1).decode(), "thr": float(mt.group(2)),
                 "ctx": gla[pos-30:mt.end()+10].decode("latin1", "replace")})
print("comparison sites with literal threshold:", len(ctxs))
thrs = np.array([c["thr"] for c in ctxs]) if ctxs else np.array([0.0])
pcts = np.percentile(thrs, [5, 25, 50, 75, 95]).round(2)
print("threshold pcts:", pcts)
print("unique:", sorted(set(thrs.tolist()))[:24])
V = json.load(open("/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json"))
halves = np.array([t["half"] for t in V if t.get("half")])
rh = np.hypot(halves[:, 0], halves[:, 1])
print("trigger rxy pcts:", np.percentile(rh, [50, 75, 90, 99]).round(2),
      "hz p50:", round(float(np.percentile(halves[:, 2], 50)), 2))
res = {"sites_with_threshold": len(ctxs),
       "threshold_pcts": pcts.tolist(),
       "unique_thresholds": sorted(set(thrs.tolist())),
       "trig_rxy_p50": round(float(np.percentile(rh, 50)), 2),
       "trig_rxy_p90": round(float(np.percentile(rh, 90)), 2),
       "trig_hz_p50": round(float(np.percentile(halves[:, 2], 50)), 2),
       "samples": ctxs[:12]}
s38 = json.load(open("/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t3_perobject.json"))
res["s38_rerun_verbatim"] = {k: s38[k] for k in ["n_real_pairs", "real_inside_rate", "null_inside_rate",
       "real_dn_median", "null_dn_median", "rank_median", "n_pairs_S", "n_pairs_L"]}
res["enum_status"] = {
    "walk_dump": "truncated s26_eng dump repaired: 14,000 records GothamCity (of ~14,917)",
    "id_space_mismatch": "walk ids = load-order 1..14000; script callee ids = game object ids; overlap 0",
    "positions": "not captured by the s26 walk summary; rerun with TObjectData TRS capture required",
    "verdict": "LNObject enumeration NOT achieved this session; per-object test stays n=14-19",
    "volume_model": "unvalidated, engine-derived only (per-object link still open)"}
json.dump(res, open("/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t3_results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("samples",)}, indent=1)[:1400])
