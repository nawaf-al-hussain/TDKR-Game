// _ZN11ShopManager23AllCharUpgradesUnlockedEv @ 001eff98

undefined4 _ZN11ShopManager23AllCharUpgradesUnlockedEv(int param_1)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  int *piVar5;
  uint uVar6;
  uint uVar7;
  undefined4 local_68;
  int local_64;
  int local_60;
  undefined4 local_5c;
  int local_58;
  int local_54;
  undefined4 local_50;
  undefined1 auStack_4c [37];
  char local_27;
  int local_24;
  int local_20;
  
  uVar7 = 0;
  local_64 = 0;
  local_60 = 0;
  local_5c = 0;
  _ZNK11ShopManager16GetCategoryItemsEjRSt6vectorIiSaIiEE_part_2185_constprop_3242
            (param_1,2,&local_64);
  iVar1 = local_64;
  if ((uint)(local_60 - local_64) >> 2 != 0) {
    piVar5 = (int *)(DAT_001f0128 + 0x1effe4);
    iVar3 = local_60;
    do {
      uVar2 = *(uint *)(iVar1 + uVar7 * 4);
      uVar6 = 0;
      local_58 = 0;
      local_54 = 0;
      local_50 = 0;
      if (uVar2 < 0x12) {
        _ZNK11ShopManager17GetItemPropertiesEjRSt6vectorIiSaIiEE_part_2881_constprop_3382
                  (param_1,uVar2,&local_58);
        if ((uint)(local_54 - local_58) >> 2 != 0) {
          do {
            uVar2 = *(uint *)(local_58 + uVar6 * 4);
            iVar1 = uVar6 * 4;
            if ((0x51 < uVar2) ||
               (iVar3 = *(int *)(*(int *)(param_1 + 0x38) + uVar2 * 4), iVar3 == 0)) {
              iVar3 = param_1 + 0x6c;
            }
            uVar6 = uVar6 + 1;
            _ZN29CComponentNewShopItemPropertyC1ERKS_(auStack_4c,iVar3);
            local_68 = *(undefined4 *)(local_58 + iVar1);
            iVar1 = _ZNSt3mapIi8SUpgradeSt4lessIiESaISt4pairIKiS0_EEEixERS4_(*piVar5 + 4,&local_68);
            if (((int)*(short *)(iVar1 + 2) != ~((local_20 - local_24 >> 2) * 0x11111111)) &&
               (local_27 != '\0')) {
              _ZN29CComponentNewShopItemPropertyD2Ev(auStack_4c);
              if (local_58 != 0) {
                _ZdlPv(local_58);
              }
              uVar4 = 0;
              iVar1 = local_64;
              goto LAB_001f00c0;
            }
            _ZN29CComponentNewShopItemPropertyD2Ev(auStack_4c);
          } while (uVar6 < (uint)(local_54 - local_58 >> 2));
        }
        iVar3 = local_60;
        iVar1 = local_64;
        if (local_58 != 0) {
          _ZdlPv();
          iVar3 = local_60;
          iVar1 = local_64;
        }
      }
      uVar7 = uVar7 + 1;
    } while (uVar7 < (uint)(iVar3 - iVar1 >> 2));
  }
  uVar4 = 1;
LAB_001f00c0:
  if (iVar1 != 0) {
    _ZdlPv();
  }
  return uVar4;
}

