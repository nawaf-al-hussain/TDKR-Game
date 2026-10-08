// _ZN18CGameObjectManager30GetComponentTemplateFromObjectEii @ 0037850c

undefined4
_ZN18CGameObjectManager30GetComponentTemplateFromObjectEii(int param_1,int param_2,int param_3)

{
  int *piVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int local_14 [2];
  
  iVar3 = param_1 + 4;
  iVar5 = *(int *)(param_1 + 8);
  iVar4 = iVar3;
  while (iVar5 != 0) {
    if (*(int *)(iVar5 + 0x10) < param_2) {
      iVar5 = *(int *)(iVar5 + 0xc);
    }
    else {
      iVar5 = *(int *)(iVar5 + 8);
      iVar4 = iVar5;
    }
  }
  iVar5 = iVar3;
  if ((iVar3 != iVar4) && (iVar5 = iVar4, param_2 < *(int *)(iVar4 + 0x10))) {
    iVar5 = iVar3;
  }
  if (iVar3 == iVar5) {
LAB_0037859c:
    uVar2 = 0;
  }
  else {
    local_14[0] = param_2;
    piVar1 = (int *)_ZNSt3mapIiSt6vectorIN18CGameObjectManager11TObjectDataESaIS2_EESt4lessIiESaISt4pairIKiS4_EEEixERS8_
                              (param_1,local_14);
    iVar5 = *piVar1;
    do {
      iVar4 = iVar5;
      if (piVar1[1] == iVar4) goto LAB_0037859c;
      iVar5 = iVar4 + 0xc;
    } while (*(int *)(iVar4 + 8) != param_3);
    uVar2 = *(undefined4 *)(iVar4 + 4);
  }
  return uVar2;
}


