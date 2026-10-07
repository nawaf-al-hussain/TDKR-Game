// _ZNK24CComponentBeastBakeGroup3NewEv @ 003ce4b0

void _ZNK24CComponentBeastBakeGroup3NewEv(void)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = (int *)_Znwj(0x14);
  iVar2 = DAT_003ce4ec + 0x3ce4d8;
  iVar3 = *(int *)(DAT_003ce4f0 + 0x3ce4d4) + 0xc;
  piVar1[2] = 0;
  piVar1[4] = 0;
  *piVar1 = iVar2;
  piVar1[1] = iVar3;
  piVar1[3] = iVar3;
  return;
}


