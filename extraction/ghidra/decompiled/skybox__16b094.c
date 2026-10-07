// _Z14SetSkyboxLightP9lua_State @ 0016b094

undefined4 _Z14SetSkyboxLightP9lua_State(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 local_14 [2];
  
  uVar1 = lua_tointeger(param_1,1);
  uVar1 = _ZN13CZonesManager10FindObjectEit(**(undefined4 **)(DAT_0016b118 + 0x16b0b4),uVar1,0xffff)
  ;
  _ZN6glitch5scene10ISceneNode20getSceneNodeFromTypeENS0_17E_SCENE_NODE_TYPEE
            (local_14,*(undefined4 *)(**(int **)(DAT_0016b11c + 0x16b0d0) + 4),0x5f796b73);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(local_14);
  iVar2 = _ZNK11CGameObject12GetComponentEi(uVar1,0x4ab8a7cd);
  if (iVar2 != 0) {
    _ZN22CCustomSkyBoxSceneNode14SetSkyboxLightEP20CSmartLightComponent(local_14[0]);
  }
  return 0;
}

