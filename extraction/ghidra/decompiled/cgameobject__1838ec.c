// _ZN15AIControl_Alarm8RegisterEP11CGameObjecti @ 001838ec

undefined4
_ZN15AIControl_Alarm8RegisterEP11CGameObjecti(int param_1,uint param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  
  iVar1 = param_1 + 4;
  iVar4 = *(int *)(param_1 + 8);
  iVar3 = iVar1;
  while (iVar4 != 0) {
    if (*(uint *)(iVar4 + 0x10) < param_2) {
      iVar4 = *(int *)(iVar4 + 0xc);
    }
    else {
      iVar4 = *(int *)(iVar4 + 8);
      iVar3 = iVar4;
    }
  }
  iVar4 = iVar1;
  if ((iVar1 != iVar3) && (iVar4 = iVar3, param_2 < *(uint *)(iVar3 + 0x10))) {
    iVar4 = iVar1;
  }
  if ((iVar1 == iVar4) || (*(int *)(iVar4 + 0x14) != 0)) {
    uVar2 = 0;
  }
  else {
    *(undefined4 *)(iVar4 + 0x14) = param_3;
    uVar2 = 1;
  }
  return uVar2;
}

