// _ZN5CZone8SaveLoadEP13CMemoryStream @ 002c80f8

undefined4 _ZN5CZone8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int *piVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  undefined4 *puVar6;
  uint uVar7;
  int *piVar8;
  char local_41;
  short local_40 [2];
  short local_3c [2];
  int local_38;
  undefined4 local_34;
  int local_30;
  int local_2c [2];
  
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x154);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x15c);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x17c);
  _ZN13CMemoryStream4ReadERs(param_2,local_40);
  if (0 < local_40[0]) {
    uVar5 = 0;
    do {
      _ZN13CMemoryStream4ReadERi(param_2,&local_30);
      puVar6 = *(undefined4 **)(*(int *)(param_1 + 0x1b8) + (short)uVar5 * 4);
      iVar1 = (**(code **)*puVar6)(puVar6);
      if (iVar1 == local_30) {
        _ZN13CMemoryStream14ReadBlockStartEv(param_2);
        uVar5 = uVar5 + 1 & 0xffff;
        _ZN13CMemoryStream4ReadERb(param_2,puVar6 + 0x19);
        _ZN13CMemoryStream12ReadBlockEndEv(param_2);
      }
      else {
        iVar4 = *(int *)(param_1 + 0x1b8);
        iVar1 = *(int *)(param_1 + 0x1bc) - iVar4 >> 2;
        uVar7 = iVar1 - 1;
        if ((int)uVar7 < 0) {
LAB_002c8484:
          iVar1 = local_30;
          if (-1 < local_30) {
            uVar3 = _ZN6CLevel8GetLevelEv();
            iVar1 = _ZN6CLevel17QuickFindWaypointEi(uVar3,iVar1);
            if (iVar1 != 0) goto LAB_002c81e0;
          }
          _ZN13CMemoryStream9SkipBlockEv(param_2);
        }
        else {
          iVar1 = (iVar1 + 0x3fffffff) * 4;
          while (iVar4 = (**(code **)**(undefined4 **)(iVar4 + iVar1))(), iVar4 != local_30) {
            uVar7 = uVar7 - 1;
            iVar1 = iVar1 + -4;
            if ((int)uVar7 < 0) goto LAB_002c8484;
            iVar4 = *(int *)(param_1 + 0x1b8);
          }
          uVar5 = uVar7 & 0xffff;
          iVar1 = *(int *)(*(int *)(param_1 + 0x1b8) + iVar1);
          if (iVar1 == 0) goto LAB_002c8484;
LAB_002c81e0:
          _ZN13CMemoryStream14ReadBlockStartEv(param_2);
          _ZN13CMemoryStream4ReadERb(param_2,iVar1 + 100);
          _ZN13CMemoryStream12ReadBlockEndEv(param_2);
        }
      }
      local_40[0] = local_40[0] + -1;
    } while (0 < local_40[0]);
  }
  _ZN13CMemoryStream4ReadERs(param_2,local_3c);
  if (0 < local_3c[0]) {
    uVar5 = 0;
    piVar8 = (int *)(DAT_002c84b4 + 0x2c824c);
    puVar6 = (undefined4 *)(DAT_002c84b8 + 0x2c8254);
    do {
      _ZN13CMemoryStream4ReadERi(param_2,&local_38);
      local_41 = '\0';
      _ZN13CMemoryStream4ReadERb(param_2,&local_41);
      if (local_41 == '\0') {
        iVar1 = (int)(short)uVar5;
        if (*(int *)(*(int *)(param_1 + 0x138) + 0x10) <= iVar1) {
          iVar1 = 0;
          uVar5 = 0;
        }
        if (local_38 - 3000000U < 1000000) {
          local_2c[0] = *(int *)(DAT_002c84bc + 0x2c82c0) + 0xc;
          _ZN13CMemoryStream4ReadERi(param_2,&local_34);
          _ZN13CMemoryStream4ReadERi(param_2,&local_30);
          _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                    (param_2,local_2c);
          piVar2 = (int *)_ZN22GameObjectCacheManager11GetSaveLoadEiiiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                                    (*(undefined4 *)(*piVar8 + 0x68),local_38,local_30,local_34,
                                     local_2c);
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                    (local_2c);
          iVar1 = (**(code **)(*piVar2 + 0x14))(piVar2);
          if (iVar1 == local_38) {
LAB_002c83f8:
            _ZN13CMemoryStream14ReadBlockStartEv(param_2);
            uVar5 = uVar5 + 1 & 0xffff;
            (**(code **)(*piVar2 + 0x94))(piVar2,param_2);
            _ZN13CMemoryStream12ReadBlockEndEv(param_2);
            goto LAB_002c83ac;
          }
        }
        else {
          piVar2 = *(int **)(*(int *)(*(int *)(param_1 + 0x138) + 0xc) + iVar1 * 4);
          iVar1 = (**(code **)(*piVar2 + 0x14))(piVar2);
          if (iVar1 == local_38) goto LAB_002c83f8;
        }
        iVar1 = *(int *)(param_1 + 0x138);
        uVar7 = *(int *)(iVar1 + 0x10) - 1;
        if ((int)uVar7 < 0) {
LAB_002c8450:
          piVar2 = (int *)_ZN13CZonesManager10FindObjectEit(*puVar6,local_38,0xffff);
          if (piVar2 == (int *)0x0) {
            _ZN13CMemoryStream9SkipBlockEv(param_2);
            goto LAB_002c83ac;
          }
          _ZN13CMemoryStream14ReadBlockStartEv();
          _ZN11CGameObject7SetZoneEP5CZoneb(piVar2,param_1,0);
        }
        else {
          iVar4 = uVar7 * 4;
          while (iVar1 = (**(code **)(**(int **)(*(int *)(iVar1 + 0xc) + iVar4) + 0x14))(),
                iVar1 != local_38) {
            uVar7 = uVar7 - 1;
            iVar4 = iVar4 + -4;
            if (uVar7 == 0xffffffff) goto LAB_002c8450;
            iVar1 = *(int *)(param_1 + 0x138);
          }
          uVar5 = uVar7 & 0xffff;
          piVar2 = *(int **)(*(int *)(*(int *)(param_1 + 0x138) + 0xc) + iVar4);
          if (piVar2 == (int *)0x0) goto LAB_002c8450;
          _ZN13CMemoryStream14ReadBlockStartEv(param_2);
        }
        (**(code **)(*piVar2 + 0x94))(piVar2,param_2);
        _ZN13CMemoryStream12ReadBlockEndEv(param_2);
      }
LAB_002c83ac:
      local_3c[0] = local_3c[0] + -1;
    } while (0 < local_3c[0]);
  }
  return 1;
}


