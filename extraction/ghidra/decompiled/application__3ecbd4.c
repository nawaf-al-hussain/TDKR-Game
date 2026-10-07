// _ZN11Application18UnloadLevelStringsEv @ 003ecbd4

void _ZN11Application18UnloadLevelStringsEv(int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  
  puVar1 = *(undefined4 **)((int)&__DT_SYMTAB[0x1df].st_value + param_1);
  if (puVar1 == (undefined4 *)0x0) {
    return;
  }
  if (puVar1[2] != 0) {
    _ZdaPv();
    puVar1[2] = 0;
  }
  if (puVar1[3] != 0) {
    _ZdaPv();
    puVar1[3] = 0;
  }
  iVar2 = puVar1[5];
  iVar3 = puVar1[6];
  if ((uint)(iVar3 - iVar2) >> 2 != 0) {
    uVar4 = 0;
    do {
      if (*(int *)(iVar2 + uVar4 * 4) != 0) {
        _ZdlPv();
        *(undefined4 *)(puVar1[5] + uVar4 * 4) = 0;
        iVar2 = puVar1[5];
        iVar3 = puVar1[6];
      }
      uVar4 = uVar4 + 1;
    } while (uVar4 < (uint)(iVar3 - iVar2 >> 2));
  }
  puVar1[6] = iVar2;
  *puVar1 = 0xffffffff;
  return;
}


