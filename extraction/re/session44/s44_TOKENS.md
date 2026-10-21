# s44 token streams — DERIVED DATA, NOT IN REPO (removed session 45)

The loose-TRS validation (s44 T5) consumed per-zone Lua token streams. The two
gz blobs (s44_tokens_island{1,2}.json.gz, 60.1 MB + 8.3 MB) were committed in
s44 and are REMOVED from HEAD in session 45; they inflated the incremental
bundle to 19 MB. Regenerate in ~6 s per zone:

    python3 extraction/re/session26/lvc_pure.py <zone>.lvc --tokens
    # writes <zone>.lvc.puretoks.json  (the --tokens flag takes no filename)
    gzip -n -9 -c <zone>.lvc.puretoks.json > s44_tokens_<zone>.json.gz

Generator provenance: island2 regenerated 2026-10-21 and gunzip-content
compared byte-identical to the s44 stream (sha256 e12422abaf9bea489314bafc
6165f3f078bad0a4cf360b1ad411f1373c6ae988). island1 not regenerated this
session (identical producer path; s44 stream sha256 79d44f754433319f6da309ba
72bd29618506cae9dca6d510cc26c54da5bfb442 kept in download/bundles_s44).
Sources: /tmp/my-project/work/data/GothamCity{,_Island2}.lvc (user release
v1.1.6b). Bundle backup: download/bundles_s44/main_s44_inc.bundle still
contains the s44 blobs for recovery.
