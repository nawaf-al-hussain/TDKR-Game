// _Z11SetFogColorP9lua_State @ 00166568

undefined4 _Z11SetFogColorP9lua_State(undefined4 param_1)

{
  undefined1 uVar1;
  undefined1 uVar2;
  undefined1 uVar3;
  undefined1 uVar4;
  int iVar5;
  undefined1 local_1c;
  undefined1 local_1b;
  undefined1 local_1a;
  undefined1 local_19;
  
  uVar1 = lua_tointeger(param_1,1);
  uVar2 = lua_tointeger(param_1,2);
  uVar3 = lua_tointeger(param_1,3);
  uVar4 = lua_tointeger(param_1,4);
  lua_tointeger(param_1,5);
  iVar5 = _ZN6CLevel8GetLevelEv();
  local_1c = uVar1;
  local_1b = uVar2;
  local_1a = uVar3;
  local_19 = uVar4;
  _ZN15CWeatherManager11SetFogColorERKN6glitch5video6SColorE
            (*(undefined4 *)(iVar5 + 0xa98),&local_1c);
  return 0;
}

