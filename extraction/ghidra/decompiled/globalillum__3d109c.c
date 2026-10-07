// _ZNK26CComponentLevelGlobalIllum5CloneEv @ 003d109c

int * _ZNK26CComponentLevelGlobalIllum5CloneEv(int param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  
  piVar1 = (int *)_Znwj(0x24);
  iVar7 = DAT_003d10fc + 0x3d10c8;
  piVar1[1] = *(int *)(param_1 + 4);
  piVar1[2] = *(int *)(param_1 + 8);
  iVar2 = *(int *)(param_1 + 0x10);
  iVar3 = *(int *)(param_1 + 0x14);
  iVar4 = *(int *)(param_1 + 0x18);
  iVar5 = *(int *)(param_1 + 0x1c);
  iVar6 = *(int *)(param_1 + 0xc);
  *piVar1 = iVar7;
  piVar1[4] = iVar2;
  piVar1[5] = iVar3;
  piVar1[6] = iVar4;
  piVar1[7] = iVar5;
  piVar1[3] = iVar6;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (piVar1 + 8,param_1 + 0x20);
  return piVar1;
}


