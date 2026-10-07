// _ZN13CQuestManager14SaveLoadGlobalEP13CMemoryStream @ 00193014

void _ZN13CQuestManager14SaveLoadGlobalEP13CMemoryStream
               (int param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  uint uVar1;
  short sVar2;
  char cVar3;
  int iVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  undefined4 *puVar8;
  uint uVar9;
  int *piVar10;
  short *psVar11;
  int iVar12;
  
  iVar7 = 100;
LAB_00193030:
  iVar12 = iVar7;
  iVar4 = _ZN13CMemoryStream7ReadIntEv(param_2);
  iVar5 = _ZN13CMemoryStream7ReadIntEv(param_2);
  cVar3 = _ZN13CMemoryStream8ReadCharEv(param_2);
  iVar7 = iVar5;
  if (0 < iVar5) {
    iVar7 = iVar4;
  }
  if ((0 < iVar7) && (**(char **)(DAT_00193240 + 0x193068) == '\0')) {
    puVar8 = *(undefined4 **)(param_1 + 8);
    uVar1 = *(int *)(param_1 + 0xc) - (int)puVar8 >> 2;
    iVar7 = 0;
    if (uVar1 == 0) goto LAB_001930dc;
    psVar11 = (short *)*puVar8;
    uVar9 = 0;
    sVar2 = *psVar11;
    while (iVar4 != sVar2) {
      uVar9 = uVar9 + 1;
      if (uVar9 == uVar1) {
        if (100 < uVar9) goto joined_r0x001931a8;
        psVar11 = (short *)*puVar8;
        iVar7 = 4;
        if (*psVar11 != -1) goto LAB_001930d4;
        goto LAB_001930f0;
      }
      psVar11 = (short *)puVar8[uVar9];
      sVar2 = *psVar11;
    }
    goto LAB_00193118;
  }
  goto joined_r0x001931a8;
LAB_001930dc:
  while( true ) {
    psVar11 = *(short **)((int)puVar8 + iVar7);
    iVar7 = iVar7 + 4;
    if (*psVar11 == -1) break;
LAB_001930d4:
    if (iVar7 == 400) goto joined_r0x001931a8;
  }
LAB_001930f0:
  *(int *)(psVar11 + 2) = iVar5;
  *psVar11 = (short)iVar4;
  iVar7 = param_1 + (*(byte *)(psVar11 + 4) + 0x2a) * 4;
  *(int *)(iVar7 + 4) = *(int *)(iVar7 + 4) + 1;
  if (psVar11 != (short *)0x0) {
LAB_00193118:
    *(char *)(psVar11 + 4) = cVar3;
    if ((((cVar3 == '\a') &&
         (piVar6 = (int *)_ZN13CZonesManager10FindObjectEit
                                    (**(undefined4 **)(DAT_00193244 + 0x19313c),
                                     *(undefined4 *)(psVar11 + 2),1,
                                     *(undefined4 **)(DAT_00193244 + 0x19313c),param_4),
         piVar6 != (int *)0x0)) && (iVar7 = (**(code **)(*piVar6 + 0x54))(), iVar7 != 0)) &&
       (iVar7 = _ZNK11CGameObject12GetComponentEi(piVar6,0x55a6393b), iVar7 != 0)) {
      if (*(int *)(iVar7 + 0x10) == 0) {
        iVar7 = -1;
      }
      else {
        iVar7 = *(int *)(*(int *)(iVar7 + 0x10) + 4);
      }
      if (*psVar11 == iVar7) {
        (**(code **)(*piVar6 + 0x50))(piVar6,0);
      }
    }
  }
joined_r0x001931a8:
  iVar7 = iVar12 + -1;
  if (iVar7 == 0) {
    memset((void *)(param_1 + 0xac),iVar12 + -1,0x34);
    piVar6 = *(int **)(param_1 + 0xc);
    for (piVar10 = *(int **)(param_1 + 8); piVar6 != piVar10; piVar10 = piVar10 + 1) {
      iVar7 = param_1 + (*(byte *)(*piVar10 + 8) + 0x2a) * 4;
      *(int *)(iVar7 + 4) = *(int *)(iVar7 + 4) + 1;
    }
    _ZN13CQuestManager16SaveLoadHotSpotsEP13CMemoryStream(param_1,param_2);
    piVar6 = (int *)_ZNK11CGameObject12GetComponentEi(*(undefined4 *)(param_1 + 0x2c),0x5863bd59);
    _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x30);
    (**(code **)(*piVar6 + 0x38))(piVar6,param_2);
    memcpy((void *)(param_1 + 4),(void *)(*param_2 + param_2[3]),4);
    param_2[3] = param_2[3] + 4;
    return;
  }
  goto LAB_00193030;
}


