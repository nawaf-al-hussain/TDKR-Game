// _ZN5CPool11FreeElementEP11CGameObject @ 0015695c

void _ZN5CPool11FreeElementEP11CGameObject(int param_1,int param_2)

{
  uint uVar1;
  uint uVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  
  uVar2 = *(uint *)(param_1 + 4);
  if (uVar2 == 0) {
    return;
  }
  piVar3 = *(int **)(param_1 + 0xc);
  if (*piVar3 == param_2) {
    uVar1 = 0;
  }
  else {
    uVar1 = 0;
    piVar4 = piVar3;
    do {
      uVar1 = uVar1 + 1;
      if (uVar1 == uVar2) break;
      piVar4 = piVar4 + 1;
    } while (*piVar4 != param_2);
  }
  uVar2 = uVar2 - 1;
  *(uint *)(param_1 + 4) = uVar2;
  if (uVar1 < uVar2) {
    iVar5 = piVar3[uVar2];
    piVar3[uVar2] = piVar3[uVar1];
    *(int *)(*(int *)(param_1 + 0xc) + uVar1 * 4) = iVar5;
    piVar3 = *(int **)(param_1 + 0xc);
  }
  iVar5 = _ZNK11CGameObject12GetComponentEi(piVar3[uVar2],0x154bb0);
  if (iVar5 == 0) {
    return;
  }
  _ZN14CPoolComponent10InvalidateEv();
  return;
}

