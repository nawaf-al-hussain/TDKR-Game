// _ZNK26CComponentLevelGlobalIllum3NewEv @ 003d1024

void _ZNK26CComponentLevelGlobalIllum3NewEv(void)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = (int *)_Znwj(0x24);
  iVar2 = *(int *)(DAT_003d1098 + 0x3d104c);
  iVar3 = DAT_003d1094 + 0x3d104c;
  piVar1[3] = 0;
  piVar1[4] = 0;
  piVar1[5] = 0;
  piVar1[6] = 0;
  piVar1[7] = 0;
  piVar1[8] = 0;
  piVar1[1] = 0;
  *piVar1 = iVar3;
  piVar1[2] = 0;
  piVar1[3] = 0;
  piVar1[4] = 0;
  piVar1[5] = 0;
  piVar1[6] = 0;
  piVar1[7] = 0;
  piVar1[8] = iVar2 + 0xc;
  return;
}


