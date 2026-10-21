# T2 — walker adopted by the playable pages: soup parsed FROM THE USER'S FILES (byte-verified), gates + negative controls PASS

## The soup is no longer shipped

- playables/lvc.js (+ lvc_readseq_s30.json 15 KB, lvc_gol_templates.json 85 KB)
  joined the page assets; the collision soup is built at runtime from the
  USER'S zip: game_config.gla -> glaSlice -> GothamCity.lvc -> parseLvc
  (census mode, NEW optional 4th arg) -> CCollisionComponent (0x2DB4AB62 =
  766542306; 794 components) triangles + C_BASE (1362553) TRS -> full euler
  transform -> TCS1 buffer.
- **Digest parity: PASS** — the JS rebuild from the user's zip is byte-identical
  to the Python export: 137,893 tris / 794 objects / 5,418,337 B, whole-file
  sha256 00ce7970e45adc854ac7cae6d0f97797b602342d101e1ecb5eb1c2c01016beb8
  (trirec-only 59016471964a90a218466dc5ffac4c1277235859e928255794061f624e7241b6).
  gc_collision.bin is no longer fetched by any page (branch commit 13f4706).

## Bug found and fixed on the way

- **lvc.js read floats LITTLE-endian; the lvc format is BIG-endian**
  (lvc_pure 'f' = '>f'). Latent since s26 (floats are rare in the tested record
  paths); exposed by the collision export (C_BASE TRS). Fixed in the canonical
  extraction/re/session26/lvc.js and shipped to the branch.

## Gates (headless Chromium, user release zip)

- walktest.html: gate.pass = 0 console errors + .nm self-check (30824v/31647c)
  + soup digest + 24/24 verdict agreement + 24/24 distance agreement (<0.25 m)
  + structured route-map pixel stats (meanRGB 19.53/24.69/33.96, stdR 23.04).
  Wall ~7 s (soup build included).
- Negative control 1 (?corrupt=1): corrupt the FIRST navmesh vertex before the
  parse -> self-check FAIL -> gate aborts with failReason nm_self_check_failed,
  pass=false. (First attempt corrupted a mid-file vertex and hung the grid
  loop on huge spans — both grid builders now skip non-finite/absurd spans;
  the corruption is caught, not survived.)
- Negative control 2 (?corrupt=2): shift route-0's start cell center +50 m
  after the self-check -> route 0 verdict changes (no_navmesh vs stuck_wall),
  agreement 23/24 -> gate.pass=false BY DETECTION (agreement drop), not by flag.

## Playable page adoption (?userfiles=1)

- index.html (the r25 first-playable page) gains a walker mode: on zip pick it
  parses navmesh + soup from game_config.gla and drives the capsule with
  nm_ground (navmesh surface) + blocked (soup walls, step-ignore 0.55);
  patch.json fallback retained for the default mode.
- Verified in-browser: after driving the capsule, its base z (P.z-0.9 =
  0.229) equals nm_ground at its x,y (0.229) to 3 decimals.

## Honest scope note

- The playable city visualization still comes from the converted GLB tier +
  patch.json markers; only the capsule's GROUND/WALLS moved to user files.
  Rendering the city itself from user files is the T1 option-(a) work
  (2-session estimate stands).
- The 24-route gate covers the harness's same_region subset (reference
  headline 15/40 across 40 routes; the browser subset agrees 24/24 on its 24).

Artifacts: s45_t2_soup.js (node verifier), s45_t2_digest.py (canonical
digests), s45_t2_soup_digest.json; branch gh-pages-staged-s44 commits 13f4706
+ the index adoption commit.
