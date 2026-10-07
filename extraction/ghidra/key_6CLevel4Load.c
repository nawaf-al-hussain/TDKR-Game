// _ZN6CLevel4LoadEP13CMemoryStream @ 004036c8

undefined4 _ZN6CLevel4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int iVar7;
  undefined4 *puVar8;
  undefined1 local_29;
  undefined1 auStack_28 [4];
  int local_24;
  int local_20;
  undefined4 local_1c;
  
  _ZN13CMemoryStream4ReadERi(param_2,auStack_28);
  iVar7 = DAT_004039f8;
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x2c);
  iVar7 = iVar7 + 0x403704;
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x58);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x30);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x34);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x38);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x3c);
  iVar4 = *(int *)(param_1 + 0xa98);
  _ZN13CMemoryStream4ReadERb(param_2,iVar4 + 4);
  _ZN13CMemoryStream4ReadERb(param_2,iVar4 + 0x28);
  _ZN13CMemoryStream4ReadERi(param_2,iVar4 + 8);
  if (*(char *)(iVar4 + 4) != '\0') {
    *(undefined4 *)(iVar4 + 0x58) = *(undefined4 *)(*(int *)(iVar4 + 0xc) + *(int *)(iVar4 + 8) * 4)
    ;
  }
  _ZN15VoxSoundManager19LoadVoxManagerStateEP13CMemoryStream
            (**(undefined4 **)(iVar7 + DAT_004039fc),param_2);
  _ZN17CLuaScriptManager8SaveLoadEP13CMemoryStreamb
            (**(undefined4 **)(iVar7 + DAT_00403a00),param_2,*(undefined1 *)(param_1 + 0x45));
  puVar8 = *(undefined4 **)(iVar7 + DAT_00403a04);
  _ZN13CZonesManager8SaveLoadEP13CMemoryStream(*puVar8,param_2);
  _ZN16CMonorailManager8SaveLoadEP13CMemoryStream(**(undefined4 **)(iVar7 + DAT_00403a08),param_2);
  (**(code **)(**(int **)(param_1 + 0xec) + 0x94))(*(int **)(param_1 + 0xec),param_2);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x5c);
  _ZN13CMemoryStream4ReadERN6glitch4core8vector3dIfEE(param_2,param_1 + 0x48);
  _ZN11CSlowMotion8SaveLoadEP13CMemoryStream(*(undefined4 *)(param_1 + 0xa64),param_2);
  _ZN11CSlowMotion8SaveLoadEP13CMemoryStream(*(undefined4 *)(param_1 + 0xa68),param_2);
  _ZN13CMemoryStream4ReadERi(param_2,&local_24);
  if (0 < local_24) {
    iVar4 = 0;
    do {
      _ZN13CMemoryStream4ReadERi(param_2,&local_20);
      iVar4 = iVar4 + 1;
      _ZN13CMemoryStream4ReadERi(param_2,&local_1c);
      if (-1 < local_20) {
        uVar1 = _ZN13CZonesManager10FindObjectEit(*puVar8,local_20,0xffff);
        _ZN6CLevel12AddObjectiveEP11CGameObjecti(param_1,uVar1,local_1c);
      }
    } while (iVar4 < local_24);
  }
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x29);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x68);
  if (-1 < *(int *)(param_1 + 0x68)) {
    *(int *)(param_1 + 100) = *(int *)(param_1 + 0x68);
    *(undefined4 *)(param_1 + 0x68) = 0xffffffff;
    _ZN6CLevel17RunSwfIntroScriptEv(param_1);
  }
  _ZN13CQuestManager14SaveLoad_LocalEP13CMemoryStream
            (**(undefined4 **)(iVar7 + DAT_00403a0c),param_2);
  piVar5 = *(int **)(param_1 + 0x988);
  _ZN13CMemoryStream4ReadERb(param_2,piVar5 + 2);
  _ZN13CMemoryStream4ReadERb(param_2,(int)piVar5 + 9);
  _ZN13CMemoryStream4ReadERb(param_2,(int)piVar5 + 10);
  _ZN13CMemoryStream4ReadERb(param_2,(int)piVar5 + 0xb);
  _ZN13CMemoryStream4ReadERb(param_2,&local_29);
  piVar2 = (int *)(**(code **)(*piVar5 + 0x18))(piVar5);
  (**(code **)(*piVar2 + 0x88))(piVar2,local_29);
  _ZN13CMemoryStream4ReadERb(param_2,&local_29);
  piVar2 = (int *)(**(code **)(*piVar5 + 0x1c))(piVar5);
  (**(code **)(*piVar2 + 0x88))(piVar2,local_29);
  _ZN11CHUDDisplay8SaveLoadEP13CMemoryStream(*(undefined4 *)(DAT_00403a10 + 0x403960),param_2);
  uVar1 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
  _ZN19cAchievementManager14LoadStatisticsEP13CMemoryStream(uVar1,param_2);
  iVar4 = *(int *)(*(int *)(DAT_00403a14 + 0x403978) + 0x178);
  if (iVar4 != 0) {
    iVar3 = *(int *)(iVar4 + 8);
    iVar6 = 0;
    do {
      piVar2 = *(int **)(iVar3 + iVar6);
      iVar6 = iVar6 + 4;
      if (piVar2 != (int *)0x0) {
        (**(code **)(*piVar2 + 0x34))(piVar2,param_2);
        iVar3 = *(int *)(iVar4 + 8);
      }
    } while (iVar6 != 0x30);
    if (*(char *)(*(undefined4 **)(iVar3 + 0x10) + 0x12) == '\0') {
      (**(code **)**(undefined4 **)(iVar3 + 0x10))();
    }
  }
  _ZN15CTrafficControl8SaveLoadEP13CMemoryStream(**(undefined4 **)(iVar7 + DAT_00403a18),param_2);
  return 1;
}

