// _ZN18CBaseControlScheme8SaveLoadEP13CMemoryStream @ 003fb2dc

void _ZN18CBaseControlScheme8SaveLoadEP13CMemoryStream(int *param_1,undefined4 param_2)

{
  int *piVar1;
  undefined1 local_11 [5];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 2);
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 9);
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 10);
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 0xb);
  _ZN13CMemoryStream4ReadERb(param_2,local_11);
  piVar1 = (int *)(**(code **)(*param_1 + 0x18))(param_1);
  (**(code **)(*piVar1 + 0x88))(piVar1,local_11[0]);
  _ZN13CMemoryStream4ReadERb(param_2,local_11);
  piVar1 = (int *)(**(code **)(*param_1 + 0x1c))(param_1);
  (**(code **)(*piVar1 + 0x88))(piVar1,local_11[0]);
  return;
}


