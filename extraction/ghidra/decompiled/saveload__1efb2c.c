// _ZN11ShopManager14SaveLoadGlobalEP13CMemoryStream @ 001efb2c

void _ZN11ShopManager14SaveLoadGlobalEP13CMemoryStream(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  undefined1 local_25;
  int local_24;
  
  uVar4 = 0;
  local_24 = 0;
  _ZN13CMemoryStream4ReadERj(param_2);
  iVar1 = *(int *)(param_1 + 0x44);
  if (local_24 == *(int *)(param_1 + 0x48) - iVar1 >> 1) {
    if (local_24 != 0) {
      do {
        _ZN13CMemoryStream4ReadERt(param_2,iVar1 + uVar4 * 2);
        iVar1 = *(int *)(param_1 + 0x44);
        uVar4 = uVar4 + 1;
      } while (uVar4 < (uint)(*(int *)(param_1 + 0x48) - iVar1 >> 1));
    }
  }
  else {
    *(int *)(param_2 + 0xc) = *(int *)(param_2 + 0xc) + local_24 * 2;
  }
  iVar2 = *(int *)(param_1 + 0x38);
  iVar1 = *(int *)(param_1 + 0x3c);
  if ((uint)(iVar1 - iVar2) >> 2 != 0) {
    uVar4 = 0;
    do {
      iVar6 = *(int *)(iVar2 + uVar4 * 4);
      if ((*(int *)(iVar6 + 0x2c) - *(int *)(iVar6 + 0x28) >> 2) * 0x11111111 != 0) {
        iVar1 = 0;
        uVar5 = 0;
        do {
          _ZN13CMemoryStream4ReadERb(param_2,&local_25);
          iVar2 = *(int *)(iVar6 + 0x28);
          iVar3 = *(int *)(iVar6 + 0x2c);
          uVar5 = uVar5 + 1;
          *(undefined1 *)(iVar2 + iVar1) = local_25;
          iVar1 = iVar1 + 0x3c;
        } while (uVar5 < (uint)((iVar3 - iVar2 >> 2) * -0x11111111));
        iVar1 = *(int *)(param_1 + 0x3c);
        iVar2 = *(int *)(param_1 + 0x38);
      }
      uVar4 = uVar4 + 1;
    } while (uVar4 < (uint)(iVar1 - iVar2 >> 2));
  }
  _ZN13CMemoryStream4ReadERh(param_2,param_1 + 0xc4);
  return;
}


