// _Z21CVehicle_EnableLightsP11CGameObjecti @ 001789e0

void _Z21CVehicle_EnableLightsP11CGameObjecti(int param_1,undefined4 param_2)

{
  int iVar1;
  
  if ((*(int *)(param_1 + 0xc0) == 0) || (1 < *(int *)(*(int *)(param_1 + 0xc0) + 0x2c) - 1U)) {
    iVar1 = _ZNK11CGameObject12GetSceneNodeEv();
    if (iVar1 != 0) {
      _ZN13VehicleLights11_SetVisibleEPN6glitch5scene10ISceneNodeEib(iVar1,param_2,1);
      return;
    }
  }
  return;
}

