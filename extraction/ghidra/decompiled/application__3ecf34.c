// _ZN11Application17GetStringFromNameEPKc @ 003ecf34

int _ZN11Application17GetStringFromNameEPKc(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  undefined4 unaff_r4;
  undefined4 unaff_r5;
  int iVar5;
  
  iVar1 = _ZN8CStrings17GetStringFromNameEPKc
                    (*(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_value + param_1));
  if (iVar1 != 0) {
    return iVar1;
  }
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + param_1);
  iVar3 = *(int *)(iVar2 + 0x18);
  iVar1 = iVar3 - *(int *)(iVar2 + 0x14) >> 2;
  if (iVar1 != 0) {
    uVar4 = 0;
    iVar5 = DAT_0033b72c + 0x33b6c8;
    do {
      _Z13CharToUnicodePtPKc(iVar5,param_2,iVar3,iVar1,unaff_r4,unaff_r5);
      iVar1 = uVar4 * 4;
      iVar3 = uVar4 * 4;
      uVar4 = uVar4 + 1;
      iVar3 = _Z6strcmpPKtS0_(*(undefined4 *)(*(int *)(iVar2 + 0x14) + iVar3),iVar5);
      if (iVar3 == 0) {
        return *(int *)(iVar2 + 8) + *(int *)(*(int *)(iVar2 + 0xc) + iVar1) * 2;
      }
      iVar3 = *(int *)(iVar2 + 0x18);
      iVar1 = iVar3 - *(int *)(iVar2 + 0x14);
    } while (uVar4 < (uint)(iVar1 >> 2));
    return 0;
  }
  return 0;
}


