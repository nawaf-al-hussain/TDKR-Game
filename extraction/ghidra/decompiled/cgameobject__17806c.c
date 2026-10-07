// _Z14CGetDistFromMCP15CGameObjectBase @ 0017806c

void _Z14CGetDistFromMCP15CGameObjectBase(int *param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined1 auStack_1c [16];
  
  iVar1 = _ZN6CLevel8GetLevelEv();
  iVar1 = *(int *)(iVar1 + 0xec);
  uVar2 = (**(code **)(*param_1 + 0xc))(param_1);
  _ZN19CActorBaseComponent16GetActorPositionEv(auStack_1c,*(undefined4 *)(iVar1 + 0xb8));
  _ZNK6glitch4core8vector3dIfE15getDistanceFromERKS2_(uVar2,auStack_1c);
  return;
}

