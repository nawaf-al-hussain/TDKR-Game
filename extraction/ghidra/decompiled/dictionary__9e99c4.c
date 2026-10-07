// inflateSetDictionary @ 009e99c4

undefined4 inflateSetDictionary(int param_1,void *param_2,uint param_3)

{
  void *__dest;
  undefined4 uVar1;
  int *piVar2;
  int *piVar3;
  int iVar4;
  uint uVar5;
  size_t sVar6;
  uint __n;
  
  if ((param_1 == 0) || (piVar3 = *(int **)(param_1 + 0x1c), piVar3 == (int *)0x0)) {
    return 0xfffffffe;
  }
  if (piVar3[2] == 0) {
    piVar2 = piVar3;
    if (*piVar3 != 10) goto LAB_009e9a00;
  }
  else if (*piVar3 != 10) {
    return 0xfffffffe;
  }
  uVar1 = adler32(0,0,0);
  iVar4 = adler32(uVar1,param_2,param_3);
  if (piVar3[6] != iVar4) {
    return 0xfffffffd;
  }
  piVar2 = *(int **)(param_1 + 0x1c);
LAB_009e9a00:
  __dest = (void *)piVar2[0xd];
  iVar4 = *(int *)(param_1 + 0x10);
  if (__dest == (void *)0x0) {
    __dest = (void *)(**(code **)(param_1 + 0x20))
                               (*(undefined4 *)(param_1 + 0x28),1 << (piVar2[9] & 0xffU),1);
    piVar2[0xd] = (int)__dest;
    if (__dest == (void *)0x0) {
      *piVar3 = 0x1c;
      return 0xfffffffc;
    }
    uVar5 = iVar4 - *(int *)(param_1 + 0x10);
  }
  else {
    uVar5 = 0;
  }
  sVar6 = piVar2[10];
  if (sVar6 == 0) {
    piVar2[0xc] = 0;
    sVar6 = 1 << (piVar2[9] & 0xffU);
    piVar2[0xb] = 0;
    piVar2[10] = sVar6;
  }
  if (uVar5 < sVar6) {
    __n = sVar6 - piVar2[0xc];
    if (uVar5 <= __n) {
      __n = uVar5;
    }
    memcpy((void *)((int)__dest + piVar2[0xc]),(void *)(*(int *)(param_1 + 0xc) - uVar5),__n);
    sVar6 = uVar5 - __n;
    if (sVar6 == 0) {
      iVar4 = piVar2[0xc];
      piVar2[0xc] = __n + iVar4;
      if (__n + iVar4 == piVar2[10]) {
        piVar2[0xc] = 0;
      }
      if ((uint)piVar2[0xb] < (uint)piVar2[10]) {
        piVar2[0xb] = __n + piVar2[0xb];
      }
    }
    else {
      memcpy((void *)piVar2[0xd],(void *)(*(int *)(param_1 + 0xc) - sVar6),sVar6);
      piVar2[0xc] = sVar6;
      piVar2[0xb] = piVar2[10];
    }
  }
  else {
    memcpy(__dest,(void *)(*(int *)(param_1 + 0xc) - sVar6),sVar6);
    piVar2[0xc] = 0;
    piVar2[0xb] = piVar2[10];
  }
  sVar6 = piVar3[10];
  if (param_3 <= sVar6) {
    memcpy((void *)(piVar3[0xd] + (sVar6 - param_3)),param_2,param_3);
    piVar3[0xb] = param_3;
    piVar3[3] = 1;
    return 0;
  }
  memcpy((void *)piVar3[0xd],(void *)((int)param_2 + (param_3 - sVar6)),sVar6);
  piVar3[0xb] = piVar3[10];
  piVar3[3] = 1;
  return 0;
}


