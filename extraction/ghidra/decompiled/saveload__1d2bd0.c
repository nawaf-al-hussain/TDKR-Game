// _ZN15CTrafficSpawner8SaveLoadEP13CMemoryStream @ 001d2bd0

void _ZN15CTrafficSpawner8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined4 *puVar8;
  int local_3c;
  int local_38;
  undefined4 local_34;
  int local_30 [3];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x18);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x1c);
  iVar6 = 0;
  _ZN13CMemoryStream4ReadERi(param_2,&local_3c);
  iVar7 = param_1 + 0x24;
  _ZNSt8_Rb_treeIiSt4pairIKiP15CTrafficSettingESt10_Select1stIS4_ESt4lessIiESaIS4_EE8_M_eraseEPSt13_Rb_tree_nodeIS4_E
            (param_1 + 0x20,*(undefined4 *)(param_1 + 0x28));
  *(int *)(param_1 + 0x2c) = iVar7;
  *(undefined4 *)(param_1 + 0x28) = 0;
  *(int *)(param_1 + 0x30) = iVar7;
  *(undefined4 *)(param_1 + 0x34) = 0;
  if (0 < local_3c) {
    puVar8 = *(undefined4 **)(DAT_001d2d0c + 0x1d2c54);
    do {
      _ZN13CMemoryStream4ReadERi(param_2,&local_38);
      _ZN13CMemoryStream4ReadERi(param_2,&local_34);
      iVar1 = local_38;
      iVar2 = _ZN13CZonesManager10FindObjectEit(*puVar8,local_34,1);
      if (iVar2 != 0) {
        iVar5 = *(int *)(param_1 + 0x28);
        iVar3 = iVar7;
        while (iVar5 != 0) {
          if (*(int *)(iVar5 + 0x10) < iVar1) {
            iVar5 = *(int *)(iVar5 + 0xc);
          }
          else {
            iVar5 = *(int *)(iVar5 + 8);
            iVar3 = iVar5;
          }
        }
        if ((iVar7 == iVar3) || (iVar1 < *(int *)(iVar3 + 0x10))) {
          local_30[0] = iVar1;
          local_30[1] = 0;
          iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiP15CTrafficSettingESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_3325
                            (param_1 + 0x20,iVar3,local_30);
        }
        uVar4 = _ZNK11CGameObject12GetComponentEi(iVar2,0x3189e053);
        *(undefined4 *)(iVar3 + 0x14) = uVar4;
      }
      iVar6 = iVar6 + 1;
    } while (iVar6 < local_3c);
  }
  return;
}


