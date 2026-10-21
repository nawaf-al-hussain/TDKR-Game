# T1 — MC_MAX_DISTANCE: MECHANISM FULLY SOLVED; NO RUNTIME VALUE EXISTS (estimate RETRACTED)

## What was found this session

1. THE FILL MECHANISM (the thing s42 could not find) — it does not fill, it is save-driven:
   - `CLuaScriptManager::ResetLuaGlobalVars(lua_State*)` @0x14b478 (664 B, NEW decode):
     lua_settop(L,0) -> lua_getfield(L,-10002,'_G') -> lua_next walk of _G, key skip-list
     via libc strcmp against the ten stdlib names (os/math/debug/coroutine/string/table/
     io/_VERSION/package/_G — the odd fragments 'g','utine','ng','e','SION','age' in the
     pool are GCC tail-merging of these same names) -> for keys found in the this+0x44
     registry vector (8-byte {name*,bool,bool}, length header at name-0xc) with BOTH bools
     set: lua_pushnil @0xa499c4 (IDENTIFIED by disasm: pushes nil tag) + lua_setfield ->
     it REMOVES registry globals, it does not fill them.
   - The real value path: `0x1495b4(this, reader, resetFlag)` — its only caller is the
     save/load static 0x3f36c8 (5 save-cluster callers: 0x3e2540/0x3e2db8/0x3e3108/
     0x3f29f4 x2). 0x1495b4: lua_getfield(GLOBALS,'_G') then `0x14b2dc` = a Lua TABLE
     DESERIALIZER: loop{ tag=ReadByte; key=ReadString; subtag -> bool@0xa49c4c /
     number@0xa499dc / string@0xa49a80 / nested-table(recurse) } each lua_settable(L,-3)
     DIRECTLY INTO _G — names AND values come from the serialized stream (a save game),
     never from code. This is why no static xref names MC_MAX_DISTANCE.
   - All 21 GlobalVarAddToLocalTable callers accounted: 14 in RegisterScriptGlobalVariables
     (the ~10 game tables incl. MC_MAX_DISTANCE, bool=false) + 7 in 0x149a5c/0x149f9c/
     0x14a8bc which register ONLY the ten stdlib names as protected tables.
2. SCRIPT-SIDE TRUTH (replaces s42's '1210 reads'):
   game_config.gla = 51-member GLA container (gol.bin, eventParameters.xml, locations.bin,
   per-level .lvc + .edge + .nm + .index). Line-classified comment-aware scan:
   - .lvc level scripts: 144 ACTIVE reads = 102 ARITHMETIC (5*MC_MAX_DISTANCE etc.) + 42
     argument passes; 57 commented out.
   - gol.bin (object templates): 753 ACTIVE = 47 arithmetic + 706 argument; 256 commented.
   - ACTIVE WRITES: NONE anywhere (regex gap closed: `MC_MAX_DISTANCE\s*=[^=]` on
     comment-stripped active lines = 0 in all 51 members).
   - eventParameters.xml / locations.bin / hosts.txt: 0 MC_ hits.
3. NO SHIPPED SOURCE FOR A VALUE: 'MC_MAX_DISTANCE' occurs in exactly one file of the
   entire 1.8 GB extracted tree — game_config.gla Lua source. The APK ships no save /
   profile / config containing it (APK = launcher UI + libKRHP.so only). The serialized
   _G snapshot travels only in save files created at runtime.
4. THE VM CANNOT RAISE THE ARITHMETIC ERROR (decisive): stock Lua 5.1 rodata contains
   'attempt to perform arithmetic' / 'attempt to index' / 'attempt to call' /
   'attempt to concatenate'. In shipped libKRHP.so ALL FOUR ARE ABSENT ('attempt to
   compare' IS present, x2; __index/__newindex/__metatable present). Gameloft patched
   the VM error paths out — wrong-type arithmetic/index/call/concat degrade SILENTLY
   instead of raising. Therefore `5 * MC_MAX_DISTANCE` on the never-replaced empty table
   does NOT error in the shipped engine; numeric consumers (lua_tonumber side) see 0.
5. VERDICT: MC_MAX_DISTANCE has NO runtime numeric value in the shipped build. The
   engine is engineered so it never needs one: empty table global + error-path-patched
   VM + save-snapshot as the only (optional) value channel. The s42 estimate '40..3000'
   is RETRACTED — there is no evidence any number exists. The 10.0 shim placeholder
   stays FLAGGED-ONLY: the engine-accurate shim model is a table-sentinel that coerces
   to 0 in arithmetic, NOT 10.0 (which over-states engine behaviour). The 42 active
   argument-pass sites + 149 arithmetic sites run with the sentinel; sound/event radii
   that use it evaluate to 0-by-conversion in the shipped build.

## Two independent signals
- Signal A (mechanism): complete call-graph decode — every registry writer/reader
  identified; the only name->value channel is the save-stream deserializer (save-only).
- Signal B (data): full-tree name scan — zero shipped occurrences outside Lua source;
  plus VM string probe proving the error path the value would need to avoid is absent.

Artifacts: s43_t1_disasm_rlgv.py, s43_t1_resolve_rlgv.py, s43_t1_caller_chain.py,
s43_t1_api_ident.py, s43_t1_walkup.py, s43_t1_regblocks.py, s43_t1_gla_scan.py,
s43_t1_active_reads.py, s43_t1_meta_assign.py (all under /home/z/my-project/scripts/,
synced to extraction/re/session43/).
