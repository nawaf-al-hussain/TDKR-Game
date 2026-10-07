// _ZN11Application10UpdateGiftEv @ 003f20c0

int * _ZN11Application10UpdateGiftEv(int param_1)

{
  int *piVar1;
  int *piVar2;
  undefined4 uVar3;
  int iVar4;
  int *piVar5;
  int *piVar6;
  int iVar7;
  
  piVar1 = (int *)_ZN12gxStateStack12CurrentStateEv(**(int **)(DAT_003f22cc + 0x3f20d0) + 4);
  piVar2 = (int *)(**(code **)(*piVar1 + 8))(piVar1,2);
  if (piVar2 == (int *)0x0) {
    piVar2 = (int *)(**(code **)(*piVar1 + 8))(piVar1,4);
    if (piVar2 == (int *)0x0) {
      return (int *)0x0;
    }
  }
  else if ((*(uint *)(*(int *)(DAT_003f22d0 + 0x3f2108) + 0x4c8) & 0x8000) != 0) {
    return piVar2;
  }
  piVar1 = *(int **)(DAT_003f22d4 + 0x3f211c);
  iVar4 = *piVar1;
  if (((iVar4 != 0) &&
      (piVar5 = *(int **)(iVar4 + 0x1c),
      (*(int *)(iVar4 + 0x20) - (int)piVar5 >> 2) * -0x55555555 != 0)) &&
     (*(char *)((int)&__DT_SYMTAB[0x1f1].st_size + param_1 + 1) == '\0')) {
    iVar4 = _ZN6CLevel8GetLevelEv();
    piVar2 = (int *)0x0;
    if (iVar4 != 0) {
      _ZN6CLevel8GetLevelEv();
      iVar4 = _ZNK6CLevel18GetPlayerInventoryEv();
      piVar2 = (int *)0x0;
      if (iVar4 != 0) {
        if (*piVar5 == 0) {
          _ZN6CLevel8GetLevelEv();
          uVar3 = _ZNK6CLevel18GetPlayerInventoryEv();
          _ZN10CInventory18AddWayneTechPointsEibb(uVar3,piVar5[1],1,0);
        }
        else if (*piVar5 == 1) {
          if (0 < piVar5[1]) {
            iVar4 = 0;
            do {
              _ZN6CLevel8GetLevelEv();
              iVar4 = iVar4 + 1;
              _ZNK6CLevel18GetPlayerInventoryEv();
              _ZN10CInventory17IncreaseCharLevelEv();
            } while (iVar4 < piVar5[1]);
          }
          _ZN11Application11GetInstanceEv();
          _ZN11Application19SaveInventoryInFileEPKc_constprop_2509();
        }
        showAlert(DAT_003f22d8 + 0x3f21b0,piVar5[2],DAT_003f22dc + 0x3f21b4,0,10,0);
        iVar4 = *piVar1;
        piVar1 = *(int **)(iVar4 + 0x1c);
        piVar2 = *(int **)(iVar4 + 0x20);
        if (piVar1 != piVar2) {
          piVar5 = piVar1 + 3;
          if ((piVar2 != piVar5) &&
             (iVar7 = ((int)piVar2 - (int)piVar5 >> 2) * -0x55555555, piVar6 = piVar5, 0 < iVar7)) {
            do {
              piVar2 = piVar5 + 2;
              piVar5[-3] = piVar1[3];
              piVar5[-2] = piVar1[4];
              piVar5 = piVar5 + 3;
              _ZNSs6assignERKSs(piVar1 + 2,piVar2);
              iVar7 = iVar7 + -1;
              piVar1 = piVar6;
              piVar6 = piVar6 + 3;
            } while (iVar7 != 0);
            piVar2 = *(int **)(iVar4 + 0x20);
          }
          *(int **)(iVar4 + 0x20) = piVar2 + -3;
          iVar4 = piVar2[-1] + -0xc;
          if (iVar4 != DAT_00aaef68 + 0xaaef48) {
            _ZNSs4_Rep10_M_disposeERKSaIcE_part_14(iVar4,&stack0xfffffff4);
          }
          return piVar2 + -1;
        }
      }
    }
  }
  return piVar2;
}


