// _ZNK23CComponentBuiltinSkyBox3NewEv @ 003cebd8

void _ZNK23CComponentBuiltinSkyBox3NewEv(void)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = (int *)_Znwj(0x10);
  iVar3 = *(int *)(DAT_003cec18 + 0x3cebfc);
  iVar2 = DAT_003cec14 + 0x3cec00;
  *(undefined1 *)(piVar1 + 2) = 0;
  *piVar1 = iVar2;
  piVar1[1] = iVar3 + 0xc;
  piVar1[3] = 0;
  return;
}

