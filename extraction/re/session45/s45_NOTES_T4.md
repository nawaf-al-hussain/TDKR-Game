# T4 — MC_MAX_DISTANCE second (runtime) signal PASS; shim -> 40.0; fengari vs Lua 5.1 parity holds

## Runtime (name, value) — s45_t4_microreg.py

Micro-emulation of the REAL registration block under Unicorn (ARM mode — the
s42 full-function run still dies at an un-stubbed callee pc=0xb000; the s45
variant with an invalid-insn recovery hook corrupts LR and was abandoned):
- entry 0x14722c, SP+4 -> fake CLuaScriptManager, +0x50 -> fake lua_State,
  r8 = 0xb30948 (s44's undisturbed name-pool pointer), stubbed callees.
- The engine executes, at runtime: **lua_pushnumber(40.0)** (r1 = 0x42200000
  via movt #0x4220 @0x147234) then **lua_setfield(_G(-10002),
  'MC_MAX_DISTANCE')** @0x14725c — one write, ZERO later overwrites inside the
  block. Second signal alongside the s44 static decode; siblings confirmed in
  the same pattern family (12.0f = NPC_SOUND_RUN @0x1471f0 etc.).
- Overwrite check: the only writer of the _G name in the block is this
  registration; the s44 static reachability stands (SetGlobal/save-stream
  deserializer never receive 'MC_MAX_DISTANCE'; 1210 reads, 0 writes).

## Shim + parity rerun

- fengari shim (s36_t6_fengari_log.cjs): MC_MAX_DISTANCE 10.0 -> **40.0**.
- Lua 5.1 shim (s36_t6_lua51.py, lupa): 10.0 -> **40.0**.
- Rerun on the available OnEnter script set (s34_t4_scripts.json: 34 scripts —
  the committed s36 comparison ran 10; s40's separate 100-script run used a
  different runner/set): **34/34 IDENTICAL** call traces fengari vs real Lua
  5.1 (call counts + argument values), status 'dead' everywhere (coroutine
  ends), 0 DIFF. The constant change is behavior-neutral for the parity set,
  as expected — the shim now carries the engine-verified value.

Artifacts: s45_t4_microreg.py, s45_t4_fengari_log.cjs (100-cap variant),
s45_t4_fengari_logs.json, s45_t4_lua51_logs.json.
