// _ZN13CAIController19Decor_NoiseRegisterEP11CGameObjectRKN6glitch4core8vector3dIfEEif @ 0018d364

void _ZN13CAIController19Decor_NoiseRegisterEP11CGameObjectRKN6glitch4core8vector3dIfEEif
               (int param_1,int *param_2,undefined4 *param_3,undefined4 param_4,float param_5)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  int iVar7;
  int iVar8;
  int local_68 [2];
  int local_60 [2];
  int local_58 [2];
  int local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  
  uVar6 = *param_3;
  iVar7 = param_1 + 0x24;
  uVar5 = param_3[1];
  uVar4 = param_3[2];
  iVar1 = (**(code **)(*param_2 + 0x14))(param_2);
  iVar8 = *(int *)(param_1 + 0x28);
  iVar3 = iVar7;
  while (iVar8 != 0) {
    if (*(int *)(iVar8 + 0x10) < iVar1) {
      iVar8 = *(int *)(iVar8 + 0xc);
    }
    else {
      iVar8 = *(int *)(iVar8 + 8);
      iVar3 = iVar8;
    }
  }
  if ((iVar7 != iVar3) && (*(int *)(iVar3 + 0x10) <= iVar1)) goto LAB_0018d4e8;
  local_4c = 0;
  iVar8 = param_1 + 0x20;
  local_48 = 0;
  local_44 = 0;
  local_40 = 0;
  local_3c = 0;
  local_38 = 0;
  local_34 = 0;
  local_50 = iVar1;
  if (iVar7 == iVar3) {
    if ((*(int *)(param_1 + 0x34) == 0) ||
       (iVar2 = *(int *)(param_1 + 0x30), iVar1 <= *(int *)(iVar2 + 0x10))) {
      _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_3356
                (local_68,iVar8,&local_50);
      iVar3 = local_68[0];
      goto LAB_0018d4e8;
    }
LAB_0018d5a4:
    iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3316
                      (iVar8,0,iVar2,&local_50);
  }
  else {
    if (iVar1 < *(int *)(iVar3 + 0x10)) {
      iVar2 = iVar3;
      if (*(int *)(param_1 + 0x2c) != iVar3) {
        iVar2 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar3);
        if (iVar1 <= *(int *)(iVar2 + 0x10)) {
          _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_3356
                    (local_60,iVar8,&local_50);
          iVar3 = local_60[0];
          goto LAB_0018d4e8;
        }
        if (*(int *)(iVar2 + 0xc) != 0) {
          iVar8 = _Znwj(0x30);
          if (iVar8 != -0x10) {
            *(undefined4 *)(iVar8 + 0x18) = local_48;
            *(undefined4 *)(iVar8 + 0x1c) = local_44;
            *(undefined4 *)(iVar8 + 0x20) = local_40;
            *(undefined4 *)(iVar8 + 0x28) = local_38;
            *(undefined4 *)(iVar8 + 0x2c) = local_34;
            *(int *)(iVar8 + 0x10) = local_50;
            *(undefined4 *)(iVar8 + 0x14) = local_4c;
            *(undefined4 *)(iVar8 + 0x24) = local_3c;
          }
          _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(1,iVar8,iVar3,iVar7);
          *(int *)(param_1 + 0x34) = *(int *)(param_1 + 0x34) + 1;
          iVar3 = iVar8;
          goto LAB_0018d4e8;
        }
        goto LAB_0018d5a4;
      }
    }
    else {
      if (iVar1 <= *(int *)(iVar3 + 0x10)) goto LAB_0018d4e8;
      if (*(int *)(param_1 + 0x30) == iVar3) {
        iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3316
                          (iVar8,0,iVar3,&local_50);
        goto LAB_0018d4e8;
      }
      iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3);
      if (*(int *)(iVar2 + 0x10) <= iVar1) {
        _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_3356
                  (local_58,iVar8,&local_50);
        iVar3 = local_58[0];
        goto LAB_0018d4e8;
      }
      if (*(int *)(iVar3 + 0xc) == 0) {
        iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3316
                          (iVar8,0,iVar3,&local_50);
        goto LAB_0018d4e8;
      }
    }
    iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController16Decor_NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3316
                      (iVar8,iVar2,iVar2,&local_50);
  }
LAB_0018d4e8:
  *(int **)(iVar3 + 0x14) = param_2;
  *(undefined4 *)(iVar3 + 0x18) = uVar6;
  *(float *)(iVar3 + 0x28) = param_5 * param_5;
  *(undefined4 *)(iVar3 + 0x1c) = uVar5;
  *(undefined4 *)(iVar3 + 0x20) = uVar4;
  *(undefined4 *)(iVar3 + 0x24) = param_4;
  *(undefined4 *)(iVar3 + 0x2c) = 0;
  return;
}

