// _ZN15AIControl_Alarm10UnregisterEP11CGameObjecti @ 0018395c

void _ZN15AIControl_Alarm10UnregisterEP11CGameObjecti(int param_1,uint param_2,int param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar1 = param_1 + 4;
  iVar3 = *(int *)(param_1 + 8);
  iVar2 = iVar1;
  while (iVar3 != 0) {
    if (*(uint *)(iVar3 + 0x10) < param_2) {
      iVar3 = *(int *)(iVar3 + 0xc);
    }
    else {
      iVar3 = *(int *)(iVar3 + 8);
      iVar2 = iVar3;
    }
  }
  iVar3 = iVar1;
  if ((iVar1 != iVar2) && (iVar3 = iVar2, param_2 < *(uint *)(iVar2 + 0x10))) {
    iVar3 = iVar1;
  }
  if ((iVar1 != iVar3) && (*(int *)(iVar3 + 0x14) == param_3)) {
    *(undefined4 *)(iVar3 + 0x14) = 0;
  }
  return;
}

