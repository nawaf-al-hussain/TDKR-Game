// _Z29SetGlobalIlluminationScriptedP9lua_State @ 0016f258

undefined4
_Z29SetGlobalIlluminationScriptedP9lua_State
          (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  uint in_fpscr;
  float fVar4;
  
  uVar1 = lua_tointeger(param_1,1,param_3,param_4,param_4);
  uVar2 = lua_tointeger(param_1,2);
  iVar3 = _ZN6CLevel8GetLevelEv();
  fVar4 = (float)VectorSignedToFloat(uVar2,(byte)(in_fpscr >> 0x16) & 3);
  _ZN15CWeatherManager15SetIlluminationEiff(*(undefined4 *)(iVar3 + 0xa98),uVar1,0,fVar4 + 1.0);
  return 0;
}


