// _ZN19CActorBaseComponent8SaveLoadEP13CMemoryStream @ 0039c87c

void _ZN19CActorBaseComponent8SaveLoadEP13CMemoryStream(int *param_1,int *param_2)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  char cVar4;
  char cVar5;
  uint uVar6;
  uint uVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  uint uVar12;
  int iVar13;
  int local_2c [2];
  
  iVar13 = param_2[3];
  iVar8 = *param_2;
  *(bool *)((int)param_1 + 0xd) = *(char *)(iVar8 + iVar13) != '\0';
  param_2[3] = iVar13 + 1;
  param_1[5] = (int)*(char *)(iVar8 + iVar13 + 1) << 0x18;
  param_2[3] = iVar13 + 2;
  param_1[5] = param_1[5] | (uint)*(byte *)(iVar8 + iVar13 + 2) << 0x10;
  param_2[3] = iVar13 + 3;
  param_1[5] = param_1[5] | (uint)*(byte *)(iVar8 + iVar13 + 3) << 8;
  param_2[3] = iVar13 + 4;
  param_1[5] = param_1[5] | (uint)*(byte *)(iVar8 + iVar13 + 4);
  param_2[3] = iVar13 + 5;
  *(bool *)((int)param_1 + 0x36d) = *(char *)(iVar8 + iVar13 + 5) != '\0';
  param_2[3] = iVar13 + 6;
  _ZN13CMemoryStream4ReadERf(param_2,local_2c);
  param_1[0x57] = local_2c[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_2c);
  param_1[0x58] = local_2c[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_2c);
  iVar8 = *(int *)(param_1[1] + 0xb0);
  param_1[0x59] = local_2c[0];
  if (iVar8 == 0) {
    iVar8 = param_1[0xb5];
    uVar7 = 0;
    if ((uint)(param_1[0xb6] - iVar8) >> 2 != 0) {
      do {
        _ZN7CWeapon8SaveLoadEP13CMemoryStream(*(undefined4 *)(iVar8 + uVar7 * 4),param_2);
        iVar8 = param_1[0xb5];
        uVar7 = uVar7 + 1;
      } while (uVar7 < (uint)(param_1[0xb6] - iVar8 >> 2));
    }
  }
  else {
    iVar13 = param_2[3];
    iVar8 = *param_2;
    *(bool *)(param_1 + 0x11c) = *(char *)(iVar8 + iVar13) != '\0';
    param_2[3] = iVar13 + 1;
    *(bool *)((int)param_1 + 0x471) = *(char *)(iVar8 + iVar13 + 1) != '\0';
    param_2[3] = iVar13 + 2;
    *(bool *)((int)param_1 + 0x472) = *(char *)(iVar8 + iVar13 + 2) != '\0';
    param_2[3] = iVar13 + 3;
    cVar4 = *(char *)(iVar8 + iVar13 + 3);
    param_2[3] = iVar13 + 4;
    bVar1 = *(byte *)(iVar8 + iVar13 + 4);
    param_2[3] = iVar13 + 5;
    bVar2 = *(byte *)(iVar8 + iVar13 + 5);
    param_2[3] = iVar13 + 6;
    bVar3 = *(byte *)(iVar8 + iVar13 + 6);
    param_2[3] = iVar13 + 7;
    uVar7 = (uint)bVar3 | (int)cVar4 << 0x18 | (uint)bVar1 << 0x10 | (uint)bVar2 << 8;
    if (0 < (int)uVar7) {
      iVar8 = _ZN13CZonesManager10FindObjectEit
                        (**(undefined4 **)(DAT_0039ccc4 + 0x39ca10),uVar7,0x11);
      param_1[0x118] = iVar8;
    }
    _ZN13CMemoryStream4ReadERf(param_2,local_2c);
    param_1[0x119] = local_2c[0];
    _ZN13CMemoryStream4ReadERf(param_2,local_2c);
    param_1[0x11a] = local_2c[0];
    _ZN13CMemoryStream4ReadERf(param_2,local_2c);
    iVar9 = param_2[3];
    iVar13 = *param_2;
    param_1[0x11b] = local_2c[0];
    iVar10 = iVar9 + 5;
    iVar8 = param_1[0xb5];
    param_1[0x136] = (int)*(char *)(iVar13 + iVar9) << 0x18;
    param_2[3] = iVar9 + 1;
    iVar11 = param_1[0xb6];
    param_1[0x136] = param_1[0x136] | (uint)*(byte *)(iVar13 + iVar9 + 1) << 0x10;
    param_2[3] = iVar9 + 2;
    param_1[0x136] = param_1[0x136] | (uint)*(byte *)(iVar13 + iVar9 + 2) << 8;
    param_2[3] = iVar9 + 3;
    param_1[0x136] = param_1[0x136] | (uint)*(byte *)(iVar13 + iVar9 + 3);
    param_2[3] = iVar9 + 4;
    *(bool *)((int)param_1 + 0x4de) = *(char *)(iVar13 + iVar9 + 4) != '\0';
    param_2[3] = iVar10;
    if ((uint)(iVar11 - iVar8) >> 2 != 0) {
      uVar7 = 0;
      while( true ) {
        iVar11 = param_1[1];
        cVar4 = *(char *)(iVar13 + iVar10);
        param_2[3] = iVar10 + 1;
        cVar5 = *(char *)(iVar13 + iVar10 + 1);
        iVar9 = uVar7 * 4;
        param_2[3] = iVar10 + 2;
        iVar11 = *(int *)(iVar11 + 0xb0);
        bVar1 = *(byte *)(iVar13 + iVar10 + 2);
        param_2[3] = iVar10 + 3;
        bVar2 = *(byte *)(iVar13 + iVar10 + 3);
        param_2[3] = iVar10 + 4;
        bVar3 = *(byte *)(iVar13 + iVar10 + 4);
        iVar8 = *(int *)(iVar8 + uVar7 * 4);
        param_2[3] = iVar10 + 5;
        uVar12 = (uint)bVar3 | (int)cVar5 << 0x18 | (uint)bVar1 << 0x10 | (uint)bVar2 << 8;
        uVar6 = _ZN10CInventory12GetItemCountEi
                          (*(undefined4 *)(iVar11 + 0x5bc),*(undefined4 *)(iVar8 + 0x2c));
        if ((uVar12 == 0xffffffff) || ((cVar4 != '\0' && ((int)uVar6 < (int)uVar12)))) {
          iVar8 = param_1[0xb5];
        }
        else {
          iVar8 = param_1[0xb5];
          uVar12 = uVar6;
        }
        uVar7 = uVar7 + 1;
        _ZN15PlayerComponent13SetWeaponAmmoEii
                  (*(undefined4 *)(param_1[1] + 0xb0),
                   *(undefined4 *)(*(int *)(iVar8 + iVar9) + 0x2c),uVar12);
        iVar8 = param_1[0xb5];
        if ((uint)(param_1[0xb6] - iVar8 >> 2) <= uVar7) break;
        iVar13 = *param_2;
        iVar10 = param_2[3];
      }
    }
    iVar8 = _ZN19CActorBaseComponent9GetWeaponEii(param_1,8,param_1[0x136]);
    if (iVar8 != 0) {
      _ZN11CHUDDisplay11OnSetWeaponEibb
                (**(undefined4 **)(DAT_0039ccc8 + 0x39cbec),*(undefined4 *)(iVar8 + 0x2c),1,1);
    }
  }
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xe2);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xe8);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xee);
  iVar8 = param_1[1];
  if (*(int *)(iVar8 + 0x10c) == 0) {
    if (*(char *)(iVar8 + 0xed) != '\0') {
      param_1[5] = 0;
      iVar8 = 0;
      goto LAB_0039cc34;
    }
  }
  else if (*(int *)(iVar8 + 0xb0) != 0) {
    *(int *)(*(int *)(iVar8 + 0xb0) + 0x4bc) = *(int *)(iVar8 + 0x10c);
  }
  iVar8 = param_1[5];
LAB_0039cc34:
  (**(code **)(*param_1 + 0x34))(param_1,iVar8);
  _ZNSt8_Rb_treeIiSt4pairIKiP13CollSpaceBaseESt10_Select1stIS4_ESt4lessIiESaIS4_EE8_M_eraseEPSt13_Rb_tree_nodeIS4_E
            (param_1 + 0x3f,param_1[0x41]);
  param_1[0x42] = (int)(param_1 + 0x40);
  param_1[0x41] = 0;
  param_1[0x43] = (int)(param_1 + 0x40);
  param_1[0x44] = 0;
  return;
}


