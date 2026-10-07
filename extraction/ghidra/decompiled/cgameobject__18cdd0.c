// _ZN13CAIController13NoiseRegisterEP11CGameObjectRKN6glitch4core8vector3dIfEEffi @ 0018cdd0

void _ZN13CAIController13NoiseRegisterEP11CGameObjectRKN6glitch4core8vector3dIfEEffi
               (int param_1,int *param_2,undefined4 *param_3,undefined4 param_4,undefined4 param_5,
               undefined4 param_6)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  int iVar7;
  int iVar8;
  int local_64 [2];
  int local_5c [2];
  int local_54 [2];
  int local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  
  if (*(char *)((int)param_2 + 0xed) != '\0') {
    iVar2 = _ZNSt3mapIi8SUpgradeSt4lessIiESaISt4pairIKiS0_EEEixERS4_
                      (*(int *)(DAT_0018d0b4 + 0x18cff8) + 4);
    param_4 = *(undefined4 *)(iVar2 + 0xc);
  }
  uVar4 = *param_3;
  iVar7 = param_1 + 4;
  uVar6 = param_3[1];
  iVar8 = param_1 + 8;
  uVar5 = param_3[2];
  iVar1 = (**(code **)(*param_2 + 0x14))(param_2);
  iVar2 = *(int *)(param_1 + 0xc);
  iVar3 = iVar8;
  while (iVar2 != 0) {
    if (*(int *)(iVar2 + 0x10) < iVar1) {
      iVar2 = *(int *)(iVar2 + 0xc);
    }
    else {
      iVar2 = *(int *)(iVar2 + 8);
      iVar3 = iVar2;
    }
  }
  if ((iVar8 != iVar3) && (*(int *)(iVar3 + 0x10) <= iVar1)) goto LAB_0018cf58;
  local_48 = 0;
  local_44 = 0;
  local_40 = 0;
  local_3c = 0;
  local_38 = 0;
  local_34 = 0;
  local_30 = 0;
  local_2c = 0;
  local_4c = iVar1;
  if (iVar8 == iVar3) {
    if ((*(int *)(param_1 + 0x18) == 0) ||
       (iVar2 = *(int *)(param_1 + 0x14), iVar1 <= *(int *)(iVar2 + 0x10))) {
      _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_3370
                (local_64,iVar7,&local_4c);
      iVar3 = local_64[0];
      goto LAB_0018cf58;
    }
LAB_0018d03c:
    iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3314
                      (iVar7,0,iVar2,&local_4c);
  }
  else {
    if (iVar1 < *(int *)(iVar3 + 0x10)) {
      iVar2 = iVar3;
      if (*(int *)(param_1 + 0x10) != iVar3) {
        iVar2 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar3);
        if (iVar1 <= *(int *)(iVar2 + 0x10)) {
          _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_3370
                    (local_5c,iVar7,&local_4c);
          iVar3 = local_5c[0];
          goto LAB_0018cf58;
        }
        if (*(int *)(iVar2 + 0xc) != 0) {
          iVar2 = _Znwj(0x34);
          if (iVar2 != -0x10) {
            *(undefined4 *)(iVar2 + 0x18) = local_44;
            *(undefined4 *)(iVar2 + 0x1c) = local_40;
            *(undefined4 *)(iVar2 + 0x20) = local_3c;
            *(undefined4 *)(iVar2 + 0x24) = local_38;
            *(undefined4 *)(iVar2 + 0x28) = local_34;
            *(undefined4 *)(iVar2 + 0x30) = local_2c;
            *(int *)(iVar2 + 0x10) = local_4c;
            *(undefined4 *)(iVar2 + 0x14) = local_48;
            *(undefined4 *)(iVar2 + 0x2c) = local_30;
          }
          _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(1,iVar2,iVar3,iVar8);
          *(int *)(param_1 + 0x18) = *(int *)(param_1 + 0x18) + 1;
          iVar3 = iVar2;
          goto LAB_0018cf58;
        }
        goto LAB_0018d03c;
      }
    }
    else {
      if (iVar1 <= *(int *)(iVar3 + 0x10)) goto LAB_0018cf58;
      if (*(int *)(param_1 + 0x14) == iVar3) {
        iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3314
                          (iVar7,0,iVar3,&local_4c);
        goto LAB_0018cf58;
      }
      iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3);
      if (*(int *)(iVar2 + 0x10) <= iVar1) {
        _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_3370
                  (local_54,iVar7,&local_4c);
        iVar3 = local_54[0];
        goto LAB_0018cf58;
      }
      if (*(int *)(iVar3 + 0xc) == 0) {
        iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3314
                          (iVar7,0,iVar3,&local_4c);
        goto LAB_0018cf58;
      }
    }
    iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CAIController10NoiseEventEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3314
                      (iVar7,iVar2,iVar2,&local_4c);
  }
LAB_0018cf58:
  *(int **)(iVar3 + 0x14) = param_2;
  *(undefined4 *)(iVar3 + 0x1c) = uVar6;
  *(undefined4 *)(iVar3 + 0x18) = uVar4;
  *(undefined4 *)(iVar3 + 0x20) = uVar5;
  *(undefined4 *)(iVar3 + 0x24) = param_4;
  *(undefined4 *)(iVar3 + 0x28) = param_5;
  *(undefined4 *)(iVar3 + 0x2c) = param_6;
  *(undefined4 *)(iVar3 + 0x30) = 0;
  return;
}

