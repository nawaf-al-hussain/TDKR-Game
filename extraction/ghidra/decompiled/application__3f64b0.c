// _ZN11Application10DrawStringEPKciiiRKN6glitch5video6SColorES6_ @ 003f64b0

void _ZN11Application10DrawStringEPKciiiRKN6glitch5video6SColorES6_
               (int param_1,undefined4 param_2,int param_3,int param_4,uint param_5,
               undefined4 param_6,undefined4 *param_7)

{
  int *piVar1;
  int extraout_r1;
  int iVar2;
  int iVar3;
  bool bVar4;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  
  piVar1 = *(int **)((int)&__DT_SYMTAB[0x1e9].st_name + param_1);
  (**(code **)(*piVar1 + 0x20))(&local_30,piVar1,param_2);
  if ((param_5 & 0x20) != 0) {
    param_4 = param_4 - local_2c;
  }
  iVar2 = extraout_r1;
  if ((param_5 & 0x10) != 0) {
    iVar2 = local_2c - (local_2c >> 0x1f);
    param_4 = param_4 - local_2c / 2;
  }
  if ((param_5 & 2) != 0) {
    param_3 = param_3 - local_30;
  }
  bVar4 = (param_5 & 1) != 0;
  if (bVar4) {
    iVar2 = local_30 - (local_30 >> 0x1f);
  }
  local_1c = param_4 + local_2c;
  iVar3 = DAT_003f6588 + 0x3f652c;
  if (bVar4) {
    param_3 = param_3 - (iVar2 >> 1);
  }
  local_20 = param_3 + local_30;
  local_28 = param_3;
  local_24 = param_4;
  _Z6strcpyPwPKc(iVar3,param_2);
  piVar1 = *(int **)((int)&__DT_SYMTAB[0x1e9].st_name + param_1);
  (**(code **)(*piVar1 + 0xc))(piVar1,iVar3,&local_28,*param_7,0,0,0);
  return;
}


