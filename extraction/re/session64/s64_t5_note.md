# SESSION 64 — T5: disk & asset hygiene INVENTORY (report only; nothing deleted without user decision)

## Current disk state
Rootfs 9.9 GB: **881 MB used, 8.5 GB free (10%)** - healthy. NOTE: this is a NEW
rootfs (the session-63 100%-full environment was replaced by an environment migration;
the old /home/z mirrors - incl. the 3.1 GB TDKR_assets mirror - are gone with it;
/home/z/my-project/download is now 86 MB of deliverable mirrors).

## Large directories / files (du, /tmp/my-project)
| path | size | what | proposal |
|---|---|---|---|
| work/s26_eng_Military_records.json | 2.9 GB | s26 intermediate analysis dump (Military gla token records) | REGENERABLE (session26 generator scripts present in the repo) - propose delete |
| work/s26_eng_Military_toks.json | 2.6 GB | s26 token dump, same family | REGENERABLE - propose delete |
| work/obb_extract/ | 1.8 GB | extracted OBB tree | keep (pipeline inputs) or regenerate from the zip on demand |
| work/apk_obb/ | 1.8 GB | second extraction tree | propose consolidate with obb_extract |
| work/TDKR_data/ | 1.8 GB | extracted game data | keep (page/analysis inputs) |
| work/TDKR_assets/ | 988 MB | converted assets | keep (GLB/tex pipeline outputs) |
| work/TDKR_zip.zip | 854 MB | **byte-IDENTICAL duplicate** of TDKR_v1.1.6b_APK_OBB.zip (cmp-verified this session) | SAFE DELETE (854 MB) |
| work/TDKR_v1.1.6b_APK_OBB.zip | 854 MB | canonical user release zip (v1.1.6b) | KEEP (ground truth; also in raw/) |
| work/TDKR-Game/ | 573 MB | the repo (code + extraction notes; game data excluded by policy) | KEEP |
| work/l_gothamcity/ + l_gothamcity.gla | 463 MB | city level extraction + archive | keep (soup/census inputs) |
| raw/TDKR_v1.1.6b_APK_OBB.zip | 854 MB | second copy of the canonical zip | keep (referenced by every gate harness) |
| raw/com.gameloft.android.AMAZ.GloftKRAS/ | small | APK package dir | keep |

## Rules respected
- Nothing deleted this session. Game data and sole copies untouched.
- The repo stays clean of game-derived data: the largest tracked artifacts are text
  JSONs/notes; every session commit re-runs the >5 MB staging audit (clean in s64).

## If the user wants space back (in order of safety)
1. work/TDKR_zip.zip (854 MB) - verified duplicate, zero risk.
2. work/s26_eng_Military_records.json + s26_eng_Military_toks.json (5.5 GB) -
   regenerable via extraction/re/session26 generators; conclusions already recorded in
   the repo notes.
3. work/apk_obb/ vs work/obb_extract/ (1.8 GB overlap) - needs a per-file diff first.
