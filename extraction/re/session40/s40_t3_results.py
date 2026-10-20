#!/usr/bin/env python3
"""S40 T3 results: constant-value evidence table (static, 5th-pass)."""
import json
res = {
 "method": [
  "Thumb-2 LDR-literal xref scanner (39,427 pool targets mapped, validated against"
  " the two known PVRTCDecompress call sites)",
  "exhaustive word-scan for each constant-name string address in the image",
  "name-pointer table walk (backward from the FACE_ cluster)",
  "script-side definition scan over game_config.gla template Lua"
 ],
 "constants": {
  "FACE_BATMAN":   {"value": "Batman", "src": "engine registry @0xc0b028 (vaddr), pairs FACE_* -> actor-name strings"},
  "FACE_HOSTAGE":  {"value": "Hostage", "src": "engine registry @0xc0b050"},
  "FACE_MERCENARY":{"value": "Mercenary", "src": "engine registry @0xc0b038"},
  "FACE_NONE":     {"value": None, "src": "engine registry @0xc0b018 (NULL value ptr)"},
  "FACE_MC":       {"value": "Batman", "src": "engine registry @0xc0b020"},
  "UNDERGROUND":   {"value": "unresolved", "src": "string @0xb3fbe2, zero pointer refs; likely raw string compare (zone name), not a numeric constant"},
  "MC_MAX_DISTANCE": {"value": "NEVER REGISTERED", "src": "FIFTH independent negative: string @0xb30948 exists but ZERO pool words and ZERO code refs; no registrant to hook; assumed 10.0 remains a shim placeholder, engine value unknowable statically"},
  "CAMERA_SHAKE_BOMB": {"value": "NEVER REGISTERED", "src": "string @0xb3089c, zero pool words / zero code refs"},
  "ZONE": {"value": "script-local boolean", "src": "36 script-side 'ZONE = true/false' definitions in game_config.gla"},
  "ACTIVE/DISABLED/ENABLED/KILLED/NUMBERED/MIHAI/INNN.../TRIGERR...": {
      "value": "not engine strings, no script defs found in game_config.gla",
      "src": "likely defined in level Lua chunks (per-level .lvc scripts) or dead names"}
 },
 "runtime_hook": {
  "status": "BLOCKED (unchanged from s39)",
  "blocker": "Lua glue is Thumb (s39); the FACE_ registry table has ZERO code"
            " xrefs to its entries (referenced via computed addresses), so there"
            " is no static registrant site to emulate; generic lua_setglobal"
            " hooking would need the Thumb-aware interpreter walk = next session"
 },
 "table_size": 28
}
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_t3_consts.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:800])
