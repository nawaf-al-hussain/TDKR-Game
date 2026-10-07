// _ZN11Application10GetVersionEPt @ 003f2390

void _ZN11Application10GetVersionEPt(short *param_1)

{
  char cVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  short sVar5;
  char *pcVar6;
  
  iVar4 = DAT_003f2418;
  pcVar6 = (char *)(DAT_003f2410 + 0x3f23a8);
  puVar3 = *(undefined4 **)(DAT_003f2414 + 0x3f23b4);
  *param_1 = (short)**(undefined4 **)(DAT_003f240c + 0x3f23a0) + 0x30;
  cVar1 = *pcVar6;
  uVar2 = **(undefined4 **)(iVar4 + 0x3f23c4);
  param_1[4] = (short)*puVar3 + 0x30;
  if (cVar1 != ' ') {
    iVar4 = 0xc;
    sVar5 = (short)cVar1;
  }
  else {
    iVar4 = 10;
    sVar5 = 0x20;
  }
  param_1[1] = 0x2e;
  if (cVar1 != ' ') {
    param_1[5] = sVar5;
  }
  param_1[3] = 0x2e;
  param_1[2] = (short)uVar2 + 0x30;
  *(undefined2 *)((int)param_1 + iVar4) = 0;
  return;
}


