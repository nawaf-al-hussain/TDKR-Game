// _Z14ChangeLightMapP9lua_State @ 00177a28

undefined4
_Z14ChangeLightMapP9lua_State
          (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = lua_tolstring(param_1,1,0,param_4,param_4);
  uVar2 = lua_tolstring(param_1,2,0);
  _ZN13CZonesManager14ChangeLightMapEPKcS1_(**(undefined4 **)(DAT_00177a70 + 0x177a60),uVar1,uVar2);
  return 0;
}


