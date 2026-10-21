# T1 — MC_MAX_DISTANCE: VALUE EXISTS AND IS ENGINE-REGISTERED = 40.0f; VM NOT PATCHED; s42 estimate lower bound was exactly right; s43 table-sentinel model REFUTED

## The decisive chain (all static, symbolized libKRHP.so, .symtab present)

1. THE VM IS NOT PATCHED (s43's void probe replaced by real evidence):
   - The error strings ARE present: "attempt to %s a %s value" @0xbb2154,
     "perform arithmetic on" @0xbb217c, "concatenate" @0xbb2170, both
     "attempt to compare ..." forms @0xbb2194/0xbb21b8, full luaT_eventname
     pointer array @0xbcdcac-0xbcdcec (stock 5.1 order), luaT_typenames
     array @0xbcdc2c, parser strings ("unexpected symbol" @0xbb2be4 etc.),
     positive controls (stack overflow x3, C stack overflow, PANIC:...,
     Lua 5.1 x2). s43 searched CONTIGUOUS phrases ("attempt to perform
     arithmetic") that stock Lua 5.1 NEVER contains — its absence proved
     nothing. (My own first xref scan also missed the real references: the
     idiom is `ldr rX,[pc,#imm]` (pool word = PC-RELATIVE OFFSET) + `add rX, pc, rX`,
     not absolute pool words.)
   - luaG_typeerror @0xa53fa0, luaG_aritherror @0xa54088, luaG_ordererror
     @0xa54114, luaG_runerror @0xa54208, luaD_throw — ALL INTACT.
     luaG_aritherror: number -> ok; string -> luaO_str2d @0xa5caf0; else
     luaG_typeerror(L, operand, "perform arithmetic on") @0xa540f4.
   - The VM's Arith (lvm.c static) @0xa690a8 disassembled completely: both
     operands tonumber -> f32 arithmetic (vadd/vsub/vmul/vdiv.f32, fmod via
     vdiv+VMLS, pow helper @0xa71190; LUA_NUMBER = FLOAT); else metatable
     lookup (table tag 5 / userdata tag 7 paths); NO metamethod ->
     0xa69358 `bl luaG_typeerror` with "perform arithmetic on". A TABLE
     operand RAISES the standard error. `attempt to compare` handling intact
     (typenames + same-type/two-type format split @0xa54114).

2. THE VALUE EXISTS: RegisterScriptGlobalVariables @0x146db0 registers
   MC_MAX_DISTANCE AS A NUMBER:
     0x147230 mov r1,#0 ; 0x147234 movt r1,#0x4220   -> f32 0x42200000 = 40.0
     0x147240 bl lua_pushnumber (0xa499dc)
     0x147254 add r6, pc, r6 -> 0xb30948 "MC_MAX_DISTANCE" (r6 not rewritten
             between 0x147254 and 0x147438 — verified)
     0x147424 mov r2, r6 ; 0x147438 bl lua_setfield(_G/-10002)
     0x147448 bl GlobalVarAddToLocalTable(this, "MC_MAX_DISTANCE", false)
   Numeric registration family (same immediate idiom, direct disasm):
     NPC_SOUND_WALK_DISTANCE = 8.0f, NPC_SOUND_RUN_DISTANCE = 12.0f,
     MC_SOUND_DISTANCE = 40.0f, MC_MAX_DISTANCE = 40.0f.
   The TABLE registrations (lua_createtable -> setfield) at 0x14770c-0x147724
   are ActorSFXState and the other state containers — s42/s43 misattributed
   MC_MAX_DISTANCE to that group ("setfield site @0x147724" actually
   registers ActorSFXState; s43's mechanism story was built on that).
   ResetLuaGlobalVars @0x14b478 (pushnil removal) = level-UNLOAD cleanup;
   the number is re-registered on manager init. The save-stream deserializer
   remains an OPTIONAL override channel — irrelevant now.

3. RUNTIME BEHAVIOUR: `5 * MC_MAX_DISTANCE` = 200.0 (f32 vmul.f32). NO error,
   NO silent degradation, NO table sentinel. All 102 arithmetic uses evaluate
   with 40.0.

4. REACHABILITY (s44_t1_reach.py, 102/102 uses found, matching s43's count):
   The .lvc "scripts" are streams of LENGTH-PREFIXED PER-HANDLER mini-chunks
   (`function ObjNNNNNN_OnReach(...)...end` each preceded by its byte-length
   prefix). Every one of the 102 arithmetic uses sits INSIDE a handler
   function (OnReach / OnEnter / Failed / Always / ...); 0 at true chunk
   top level (my scanner's initial 14 "TOPLEVEL" were artifacts of the
   length-prefix structure — verified by manual context dumps around
   GothamCity.lvc:50059). Consequence: chunks COMPILE clean; the arithmetic
   evaluates when each handler FIRES, with 40.0 — the game works as designed.

## Verdict (replaces all prior T1 verdicts)

- TRUE VALUE: MC_MAX_DISTANCE = 40.0 (engine-registered constant).
- 5 * MC_MAX_DISTANCE = 200.0; no error; the 102 uses are live.
- s42 estimate "40..3000": RETRACTED as an estimate — its lower bound 40 was
  exactly right (drawn from MC_SOUND_DISTANCE, the correct neighbour).
- s43 "no runtime value exists / empty-table sentinel / VM patched /
  degrades silently": REFUTED on all four points.
- Shim: MC_MAX_DISTANCE = 40.0 is now EVIDENCE-BACKED; the 10.0 flagged
  placeholder should be replaced by 40.0 (no flag needed).
- Dynamic VM drive under Unicorn: attempted (lua_newstate @0xa61120 found —
  engine-confirmed via its caller @0x146bb4; JUMP_SLOT GOT patching +
  Python allocator built) but blocked by the custom state-layout quirks of
  this GLITCH Lua build (LG/lua_State split at +0xcc, custom allocf/ud
  field placement). The brief's fallback — disassemble
  luaV_arith-equivalent (the Arith static) / luaG_aritherror and show what
  a table operand does — was executed instead and is decisive.

## Two independent signals

- Signal A: complete disassembly of the error chain (Arith @0xa690a8 ->
  luaG_typeerror @0xa53fa0 -> luaG_runerror @0xa54208 -> luaD_throw) with
  the exact "perform arithmetic on" string wired via the ldr-pool+add-pc
  idiom @0xa69348-0xa69358.
- Signal B: the registration site itself (pushnumber 40.0f -> setfield with
  the resolved "MC_MAX_DISTANCE" string) inside the numeric family whose
  other members s42 already decoded and whose script-side usage pattern
  (0 writes, 0 field accesses, 899 numeric argument uses) requires a number.

Artifacts: s44_t1_xrefs.py, s44_t1_xrefs.json, s44_t1_luasyms.json,
s44_t1_luaregion_syms.json, s44_t1_disasm_ldebug.py, s44_t1_reach.py,
s44_t1_reach.json, s44_t1_regtable.json, s44_t1_lua_drive.py,
s44_t1_drive_result.json, s44_t1_plt.json.
