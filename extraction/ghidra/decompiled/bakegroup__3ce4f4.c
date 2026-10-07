// _ZNK24CComponentBeastBakeGroup5CloneEv @ 003ce4f4

int * _ZNK24CComponentBeastBakeGroup5CloneEv
                (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  undefined4 extraout_r2;
  int iVar2;
  
  piVar1 = (int *)_Znwj(0x14);
  iVar2 = DAT_003ce544 + 0x3ce51c;
  *piVar1 = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (piVar1 + 1,param_1 + 4,extraout_r2,iVar2,param_4);
  piVar1[2] = *(int *)(param_1 + 8);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (piVar1 + 3,param_1 + 0xc);
  piVar1[4] = *(int *)(param_1 + 0x10);
  return piVar1;
}


