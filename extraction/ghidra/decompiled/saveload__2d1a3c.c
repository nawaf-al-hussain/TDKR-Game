// _ZN13CZonesManager8SaveLoadEP13CMemoryStream @ 002d1a3c

void _ZN13CZonesManager8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  undefined4 *puVar5;
  uint uVar6;
  undefined4 *puVar7;
  int iVar8;
  short local_44;
  undefined1 auStack_42 [2];
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined1 local_24;
  undefined1 local_23;
  
  _ZN22GameObjectCacheManager11ResetStatusEv(*(undefined4 *)(param_1 + 0x68));
  _ZN13CMemoryStream4ReadERi(param_2,&local_40);
  _ZN13CMemoryStream4ReadERi(param_2,&local_3c);
  if ((-1 < local_3c) &&
     (iVar4 = *(int *)(param_1 + 0x80), (uint)(*(int *)(param_1 + 0x84) - iVar4) >> 2 != 0)) {
    uVar6 = 0;
    do {
      iVar1 = uVar6 * 4;
      iVar2 = uVar6 * 4;
      uVar6 = uVar6 + 1;
      iVar1 = (**(code **)(**(int **)(iVar4 + iVar1) + 0x14))();
      iVar4 = *(int *)(param_1 + 0x80);
      if (iVar1 == local_3c) {
        *(undefined4 *)(param_1 + 0x6c) = *(undefined4 *)(iVar4 + iVar2);
        break;
      }
    } while (uVar6 < (uint)(*(int *)(param_1 + 0x84) - iVar4 >> 2));
  }
  iVar4 = *(int *)(param_1 + 0x4c);
  if (local_40 != iVar4) {
    if (local_40 < 0) {
      piVar3 = *(int **)(param_1 + 0x44);
      local_38 = iVar4;
      if (piVar3 == *(int **)(param_1 + 0x48)) {
        _ZNSt6vectorIiSaIiEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPiS1_EERKi
                  (param_1 + 0x40,piVar3,&local_38);
        *(int *)(param_1 + 0x4c) = local_40;
      }
      else {
        if (piVar3 != (int *)0x0) {
          *piVar3 = iVar4;
        }
        *(int *)(param_1 + 0x4c) = local_40;
        *(int **)(param_1 + 0x44) = piVar3 + 1;
      }
    }
    else {
      iVar1 = *(int *)(param_1 + 0x24);
      iVar8 = param_1 + 0x20;
      iVar4 = iVar1;
      iVar2 = iVar8;
      while (iVar4 != 0) {
        if (*(int *)(iVar4 + 0x10) < local_40) {
          iVar4 = *(int *)(iVar4 + 0xc);
        }
        else {
          iVar4 = *(int *)(iVar4 + 8);
          iVar2 = iVar4;
        }
      }
      iVar4 = iVar8;
      if ((iVar8 != iVar2) && (iVar4 = iVar2, local_40 < *(int *)(iVar2 + 0x10))) {
        iVar4 = iVar8;
      }
      iVar2 = iVar8;
      if (iVar8 != iVar4) {
        while (iVar1 != 0) {
          if (*(int *)(iVar1 + 0x10) < local_40) {
            iVar1 = *(int *)(iVar1 + 0xc);
          }
          else {
            iVar2 = iVar1;
            iVar1 = *(int *)(iVar1 + 8);
          }
        }
        if ((iVar8 == iVar2) || (local_40 < *(int *)(iVar2 + 0x10))) {
          local_34 = local_40;
          local_30 = 0xffffffff;
          local_2c = 0xffffffff;
          local_28 = 0xffffffff;
          local_24 = 0;
          local_23 = 0;
          iVar2 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
                            (param_1 + 0x1c,iVar2,&local_34);
        }
        if (*(char *)(iVar2 + 0x20) != '\0') {
          local_38 = *(int *)(param_1 + 0x4c);
          if (local_38 != -1) {
            piVar3 = *(int **)(param_1 + 0x44);
            if (piVar3 == *(int **)(param_1 + 0x48)) {
              _ZNSt6vectorIiSaIiEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPiS1_EERKi
                        (param_1 + 0x40,piVar3,&local_38);
            }
            else {
              if (piVar3 != (int *)0x0) {
                *piVar3 = local_38;
              }
              *(int **)(param_1 + 0x44) = piVar3 + 1;
            }
          }
          piVar3 = *(int **)(param_1 + 0x38);
          *(int *)(param_1 + 0x4c) = local_40;
          local_38 = local_40;
          if (piVar3 == *(int **)(param_1 + 0x3c)) {
            _ZNSt6vectorIiSaIiEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPiS1_EERKi
                      (param_1 + 0x34,piVar3,&local_38);
          }
          else {
            if (piVar3 != (int *)0x0) {
              *piVar3 = local_40;
            }
            *(int **)(param_1 + 0x38) = piVar3 + 1;
          }
        }
      }
    }
  }
  uVar6 = 0;
  *(undefined1 *)(*(int *)(param_1 + 100) + 0x20) = 0;
  _ZN13CZonesManager24HandleZoneUnloadRequestsEv(param_1);
  _ZN13CZonesManager22HandleZoneLoadRequestsEb(param_1,0);
  _ZN13CZonesManager20RefreshAllActorsPoolEv(param_1);
  *(undefined1 *)(*(int *)(param_1 + 100) + 0x20) = 1;
  _ZN13CMemoryStream4ReadERt(param_2,&local_44);
  do {
    if (local_44 == 0) {
      puVar7 = *(undefined4 **)(DAT_002d1dcc + 0x2d1cd8);
      _ZN13CMemoryStream4ReadERt(param_2,auStack_42);
      for (piVar3 = (int *)*puVar7; piVar3 != (int *)puVar7[1]; piVar3 = piVar3 + 1) {
        _ZN13CMemoryStream4ReadERb(param_2,*piVar3 + 8);
      }
      return;
    }
    iVar4 = _ZN13CMemoryStream7ReadIntEv(param_2);
    puVar5 = *(undefined4 **)(param_1 + 0x84);
    puVar7 = *(undefined4 **)(param_1 + 0x80);
    if (uVar6 < (uint)((int)puVar5 - (int)puVar7 >> 2)) {
      iVar2 = (**(code **)(*(int *)puVar7[uVar6] + 0x14))();
      if (iVar2 != iVar4) {
        puVar5 = *(undefined4 **)(param_1 + 0x84);
        puVar7 = *(undefined4 **)(param_1 + 0x80);
        goto LAB_002d1c98;
      }
      piVar3 = *(int **)(*(int *)(param_1 + 0x80) + uVar6 * 4);
LAB_002d1d2c:
      if (piVar3 == (int *)0x0) goto LAB_002d1ca4;
      uVar6 = uVar6 + 1;
      _ZN13CMemoryStream17ReadBlockStartIntEv(param_2);
      (**(code **)(*piVar3 + 0x94))(piVar3,param_2);
      _ZN13CMemoryStream15ReadBlockEndIntEv(param_2);
    }
    else {
LAB_002d1c98:
      while (puVar7 != puVar5) {
        iVar2 = (**(code **)(*(int *)*puVar7 + 0x14))();
        if (iVar4 == iVar2) {
          piVar3 = (int *)*puVar7;
          goto LAB_002d1d2c;
        }
        puVar7 = puVar7 + 1;
        puVar5 = *(undefined4 **)(param_1 + 0x84);
      }
LAB_002d1ca4:
      _ZN13CMemoryStream12SkipBlockIntEv(param_2);
    }
    local_44 = local_44 + -1;
  } while( true );
}


