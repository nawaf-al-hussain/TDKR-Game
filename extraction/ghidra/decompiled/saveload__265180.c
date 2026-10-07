// _ZN10CInventory14SaveLoadGlobalEP13CMemoryStream @ 00265180

void _ZN10CInventory14SaveLoadGlobalEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 uVar5;
  int *piVar6;
  int *piVar7;
  uint uVar8;
  int *piVar9;
  int iVar10;
  int iVar11;
  int *piVar12;
  int iVar13;
  int iVar14;
  int *piVar15;
  int *piVar16;
  int local_48;
  int *local_44;
  undefined1 local_39;
  undefined4 local_38;
  int local_34;
  int local_30;
  int local_2c [2];
  
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x60);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 100);
  iVar14 = 0;
  iVar11 = param_1;
  iVar13 = param_1;
  do {
    _ZN13CMemoryStream4ReadERi(param_2,&local_38);
    iVar1 = iVar14 * 0x10;
    uVar3 = _ZN11CEncryption9DecodeIntEib(local_38,0);
    iVar10 = 0;
    iVar4 = _Z6randomi(0x10);
    *(int *)(iVar11 + 0x1c8) = iVar4;
    do {
      while (iVar4 != iVar10) {
        uVar5 = _Z6randomi(0xa98ac7);
        uVar5 = _ZN11CEncryption9EncodeIntEib(uVar5,1);
        iVar4 = iVar10 * 4;
        iVar10 = iVar10 + 1;
        *(undefined4 *)(iVar13 + iVar4 + 0x88) = uVar5;
        iVar4 = *(int *)(iVar11 + 0x1c8);
        if (iVar10 == 0x10) goto LAB_00265248;
      }
      uVar5 = _ZN11CEncryption9EncodeIntEib(uVar3,1);
      iVar4 = iVar1 + iVar10;
      iVar10 = iVar10 + 1;
      *(undefined4 *)(param_1 + (iVar4 + 0x22) * 4) = uVar5;
      iVar4 = *(int *)(iVar11 + 0x1c8);
    } while (iVar10 != 0x10);
LAB_00265248:
    iVar14 = iVar14 + 1;
    iVar13 = iVar13 + 0x40;
    uVar3 = _ZN11CEncryption9DecodeIntEib(*(undefined4 *)(param_1 + (iVar1 + iVar4 + 0x22) * 4));
    uVar3 = _ZN11CEncryption9EncodeIntEib(uVar3,0);
    *(undefined4 *)(iVar11 + 0x74) = uVar3;
    iVar11 = iVar11 + 4;
  } while (iVar14 != 5);
  iVar11 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar11) {
    iVar14 = 0;
    iVar13 = param_1 + 4;
    do {
      _ZN13CMemoryStream4ReadERi(param_2,&local_34);
      _ZN13CMemoryStream4ReadERb(param_2,&local_39);
      _ZN13CMemoryStream4ReadERi(param_2,local_2c);
      _ZN13CMemoryStream4ReadERi(param_2,&local_30);
      _ZN10CInventory7AddItemE9eItemTypeiibbb(param_1,local_30,local_34,0,0,local_39,0);
      iVar1 = iVar13;
      iVar4 = *(int *)(param_1 + 8);
      while (iVar4 != 0) {
        if (*(int *)(iVar4 + 0x10) < local_34) {
          iVar4 = *(int *)(iVar4 + 0xc);
        }
        else {
          iVar1 = iVar4;
          iVar4 = *(int *)(iVar4 + 8);
        }
      }
      iVar4 = iVar13;
      if ((iVar13 != iVar1) && (iVar4 = iVar1, local_34 < *(int *)(iVar1 + 0x10))) {
        iVar4 = iVar13;
      }
      if (iVar13 == iVar4) {
        _ZN10CInventory7AddItemE9eItemTypeiibbb(param_1,local_30,local_34,local_2c[0],0,0,0);
      }
      else {
        *(int *)(iVar4 + 0x14) = local_2c[0];
      }
      iVar14 = iVar14 + 1;
    } while (iVar14 != iVar11);
  }
  *(undefined4 *)(param_1 + 0x58) = *(undefined4 *)(param_1 + 0x54);
  iVar11 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar11) {
    iVar13 = 0;
    do {
      while( true ) {
        local_2c[0] = _ZN13CMemoryStream7ReadIntEv(param_2);
        piVar7 = *(int **)(param_1 + 0x58);
        if (piVar7 != *(int **)(param_1 + 0x5c)) break;
        iVar13 = iVar13 + 1;
        _ZNSt6vectorIiSaIiEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPiS1_EERKi
                  (param_1 + 0x54,piVar7,local_2c);
        if (iVar13 == iVar11) goto LAB_002653d0;
      }
      iVar13 = iVar13 + 1;
      if (piVar7 != (int *)0x0) {
        *piVar7 = local_2c[0];
      }
      *(int **)(param_1 + 0x58) = piVar7 + 1;
    } while (iVar13 != iVar11);
  }
LAB_002653d0:
  iVar11 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar11) {
    iVar13 = 0;
    do {
      while( true ) {
        _ZN13CMemoryStream4ReadERj(param_2,&local_30);
        _ZN13CMemoryStream4ReadERi(param_2,local_2c);
        iVar1 = local_2c[0];
        iVar14 = local_30;
        piVar6 = *(int **)(param_1 + 0x4c);
        for (piVar7 = *(int **)(param_1 + 0x48); piVar7 != piVar6; piVar7 = piVar7 + 2) {
          if ((local_30 == *piVar7) && (local_2c[0] == piVar7[1])) goto LAB_00265458;
        }
        piVar12 = *(int **)(param_1 + 0x50);
        if (piVar12 == piVar6) break;
        if (piVar6 != (int *)0x0) {
          *piVar6 = local_30;
          piVar6[1] = local_2c[0];
        }
        *(int **)(param_1 + 0x4c) = piVar6 + 2;
LAB_00265458:
        iVar13 = iVar13 + 1;
        if (iVar13 == iVar11) goto LAB_00265464;
      }
      uVar2 = (int)piVar7 - (int)*(int **)(param_1 + 0x48) >> 3;
      if (uVar2 == 0) {
        local_48 = 8;
      }
      else {
        uVar8 = uVar2 * 2;
        if (uVar8 < uVar2) {
          local_48 = -8;
        }
        else {
          if (0x1ffffffe < uVar8) {
            uVar8 = 0x1fffffff;
          }
          local_48 = uVar8 << 3;
        }
      }
      piVar7 = (int *)_Znwj(local_48);
      piVar16 = *(int **)(param_1 + 0x48);
      piVar6 = *(int **)(param_1 + 0x4c);
      if (piVar7 + uVar2 * 2 != (int *)0x0) {
        (piVar7 + uVar2 * 2)[1] = iVar1;
        piVar7[uVar2 * 2] = iVar14;
      }
      local_44 = piVar7 + 2;
      piVar9 = piVar7;
      piVar15 = piVar16;
      if (piVar12 != piVar16) {
        do {
          if (piVar9 != (int *)0x0) {
            iVar14 = piVar15[1];
            *piVar9 = *piVar15;
            piVar9[1] = iVar14;
          }
          piVar15 = piVar15 + 2;
          piVar9 = piVar9 + 2;
        } while (piVar12 != piVar15);
        local_44 = (int *)((int)piVar7 + ((int)piVar12 - (int)(piVar16 + 2) & 0xfffffff8U) + 0x10);
      }
      piVar9 = local_44;
      piVar15 = piVar12;
      if (piVar12 != piVar6) {
        do {
          if (piVar9 != (int *)0x0) {
            iVar14 = piVar15[1];
            *piVar9 = *piVar15;
            piVar9[1] = iVar14;
          }
          piVar15 = piVar15 + 2;
          piVar9 = piVar9 + 2;
        } while (piVar6 != piVar15);
        local_44 = (int *)((int)local_44 + ((int)piVar6 - (int)(piVar12 + 2) & 0xfffffff8U) + 8);
      }
      if (piVar16 != (int *)0x0) {
        _ZdlPv(piVar16);
      }
      iVar13 = iVar13 + 1;
      *(int **)(param_1 + 0x48) = piVar7;
      *(int *)(param_1 + 0x50) = (int)piVar7 + local_48;
      *(int **)(param_1 + 0x4c) = local_44;
    } while (iVar13 != iVar11);
  }
LAB_00265464:
  iVar11 = _ZN6CLevel8GetLevelEv();
  _ZN19CActorBaseComponent19SetInventoryWeaponsEv(*(undefined4 *)(*(int *)(iVar11 + 0xec) + 0xb8));
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x65);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x68);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x6c);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x70);
  _ZN15UpgradesManager18LoadUpgradesStatusEP13CMemoryStream
            (**(undefined4 **)(DAT_00265660 + 0x2654b4),param_2);
  _ZN11ShopManager15UnlockShopItemsEv(**(undefined4 **)(DAT_00265664 + 0x2654c4));
  _ZN11CHUDDisplay18RefreshGadgetWheelEv(**(undefined4 **)(DAT_00265668 + 0x2654d4));
  return;
}


