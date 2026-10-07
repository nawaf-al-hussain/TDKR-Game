// _Z23ResetGlobalIlluminationP9lua_State @ 0016f2ac

undefined4
_Z23ResetGlobalIlluminationP9lua_State
          (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  
  lua_tointeger(param_1,1,param_3,param_4,param_4);
  iVar1 = _ZN6CLevel8GetLevelEv();
  *(undefined1 *)(*(int *)(iVar1 + 0xa98) + 4) = 0;
  return 0;
}


