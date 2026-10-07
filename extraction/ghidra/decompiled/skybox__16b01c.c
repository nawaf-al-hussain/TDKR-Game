// _Z18SetSkyboxAnimationP9lua_State @ 0016b01c

undefined4 _Z18SetSkyboxAnimationP9lua_State(undefined4 param_1)

{
  undefined4 uVar1;
  int local_14 [2];
  
  lua_tointeger(param_1,1);
  uVar1 = lua_tolstring(param_1,2,0);
  _ZN6glitch5scene10ISceneNode20getSceneNodeFromTypeENS0_17E_SCENE_NODE_TYPEE
            (local_14,*(undefined4 *)(**(int **)(DAT_0016b090 + 0x16b054) + 4),0x5f796b73);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(local_14);
  if (local_14[0] != 0) {
    _ZN22CCustomSkyBoxSceneNode19PlaySkyboxAnimationEPKc(local_14[0],uVar1);
  }
  return 0;
}

