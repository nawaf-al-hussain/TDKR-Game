// _ZN13CAIController11AddStunAreaEN6glitch4core8vector3dIfEEffP11CGameObjectffRKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEE @ 0018eca4

void _ZN13CAIController11AddStunAreaEN6glitch4core8vector3dIfEEffP11CGameObjectffRKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEE
               (int param_1,undefined4 *param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,undefined4 param_6,undefined4 param_7,undefined4 param_8)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 uVar4;
  int *piVar5;
  undefined4 *puVar6;
  
  if (0 < *(int *)(param_1 + 0x17c)) {
    iVar3 = -1;
    iVar1 = 0;
    piVar5 = *(int **)(param_1 + 0x178);
    do {
      if (*(float *)(*piVar5 + 0x1c) <= 0.0) {
        iVar3 = iVar1;
      }
      iVar1 = iVar1 + 1;
      piVar5 = piVar5 + 1;
    } while (iVar1 != *(int *)(param_1 + 0x17c));
    if (iVar3 != -1) {
      puVar6 = (undefined4 *)(*(int **)(param_1 + 0x178))[iVar3];
      uVar4 = param_2[1];
      uVar2 = param_2[2];
      *puVar6 = *param_2;
      puVar6[1] = uVar4;
      puVar6[2] = uVar2;
      puVar6[4] = param_4;
      puVar6[3] = param_3;
      puVar6[5] = param_5;
      puVar6[7] = param_6;
      puVar6[8] = param_7;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                (puVar6 + 6,param_8);
      return;
    }
  }
  return;
}

