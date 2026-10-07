// _ZN11Application10DrawStringEPKtiii @ 003f674c

void _ZN11Application10DrawStringEPKtiii
               (int param_1,undefined4 param_2,int param_3,int param_4,uint param_5)

{
  int *piVar1;
  int extraout_r2;
  int iVar2;
  bool bVar3;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  
  iVar2 = DAT_003f6828 + 0x3f676c;
  _Z6strcpyPwPKt(iVar2);
  piVar1 = *(int **)((int)&__DT_SYMTAB[0x1e9].st_name + param_1);
  (**(code **)(*piVar1 + 0x1c))(&local_30,piVar1,iVar2);
  if ((param_5 & 0x20) != 0) {
    param_4 = param_4 - local_2c;
  }
  iVar2 = extraout_r2;
  if ((param_5 & 0x10) != 0) {
    iVar2 = local_2c - (local_2c >> 0x1f);
    param_4 = param_4 - local_2c / 2;
  }
  if ((param_5 & 2) != 0) {
    param_3 = param_3 - local_30;
  }
  bVar3 = (param_5 & 1) != 0;
  if (bVar3) {
    iVar2 = local_30 - (local_30 >> 0x1f);
  }
  local_1c = local_2c + param_4;
  if (bVar3) {
    param_3 = param_3 - (iVar2 >> 1);
  }
  piVar1 = *(int **)((int)&__DT_SYMTAB[0x1e9].st_name + param_1);
  local_20 = local_30 + param_3;
  local_28 = param_3;
  local_24 = param_4;
  (**(code **)(*piVar1 + 0xc))(piVar1,DAT_003f682c + 0x3f67c8,&local_28,0xff00ff00,0,0,0);
  return;
}


