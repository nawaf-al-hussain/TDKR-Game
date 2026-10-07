// _ZN11Application7_UpdateEf @ 003f13a8

void _ZN11Application7_UpdateEf(int param_1,float param_2)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  float *pfVar6;
  undefined4 uVar7;
  int iVar8;
  undefined4 uVar9;
  int iVar10;
  int extraout_r2;
  int iVar11;
  uint uVar12;
  undefined4 *puVar13;
  int *piVar14;
  undefined4 uVar15;
  bool bVar16;
  uint in_fpscr;
  float fVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  double dVar21;
  double dVar22;
  double dVar23;
  undefined8 uVar24;
  float local_6c;
  float local_68;
  float local_64;
  
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (iVar1 != 0) {
    uVar2 = _ZN6CLevel8GetLevelEv();
    _ZN6CLevel15ResetDebugLinesEb(uVar2,0);
  }
  _ZN9CControls12CheckActionsEv();
  iVar1 = *(int *)(DAT_003f1828 + 0x3f13e4);
  if (0 < iVar1) {
    iVar11 = 0;
    iVar3 = *(int *)(DAT_003f182c + 0x3f1400);
    iVar10 = 0;
    do {
      iVar8 = *(int *)(iVar3 + iVar11);
      if (iVar8 < -1) {
        *(undefined4 *)(iVar3 + iVar11) = 0xffffffff;
      }
      else if (iVar8 != -1) {
        *(int *)(iVar3 + iVar11) = iVar8 + (int)param_2;
      }
      iVar10 = iVar10 + 1;
      iVar11 = iVar11 + 8;
    } while (iVar10 < iVar1);
  }
  for (puVar13 = *(undefined4 **)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
      (undefined4 *)((int)&__DT_SYMTAB[0x1de].st_value + param_1) != puVar13;
      puVar13 = (undefined4 *)*puVar13) {
    (**(code **)(*(int *)puVar13[2] + 8))((int *)puVar13[2],param_2);
  }
  iVar1 = _ZN11Application11GetInstanceEv();
  uVar15 = *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  uVar2 = _ZNK6glitch5video12IVideoDriver22getTextureBindingCountEi(uVar15,0);
  uVar4 = _ZNK6glitch5video12IVideoDriver16getDrawCallCountEi(uVar15,0);
  uVar5 = _ZNK6glitch5video12IVideoDriver18getDrawCall2DCountEi(uVar15,0);
  iVar1 = _ZN6CLevel8GetLevelEv();
  if ((iVar1 == 0) || (iVar1 = _ZN6CLevel8GetLevelEv(), *(int *)(iVar1 + 0xa98) == 0)) {
    uVar7 = _ZNK6glitch5video12IVideoDriver6getFPSEi(uVar15,0);
    uVar15 = _ZNK6glitch5video12IVideoDriver22getPrimitiveCountDrawnEji(uVar15,0,0);
    sprintf((char *)(DAT_003f184c + 0x3f16ec),(char *)(DAT_003f1848 + 0x3f16d8),uVar7,uVar15,uVar2,
            uVar4,uVar5);
  }
  else {
    _ZN6CLevel8GetLevelEv();
    if (*(char *)(DAT_003f1830 + 0x3f14d4) == '\0') {
      _ZN6CLevel8GetLevelEv();
      if (*(char *)(DAT_003f1850 + 0x3f1704) == '\0') {
        uVar2 = _ZNK6glitch5video12IVideoDriver6getFPSEi(uVar15);
        sprintf((char *)(DAT_003f1864 + 0x3f17dc),(char *)(DAT_003f1860 + 0x3f17d0),uVar2);
      }
      else {
        uVar7 = _ZNK6glitch5video12IVideoDriver6getFPSEi(uVar15,0);
        piVar14 = (int *)(DAT_003f1854 + 0x3f1728);
        uVar24 = _ZNK6glitch5video12IVideoDriver22getPrimitiveCountDrawnEji(uVar15,0,0);
        uVar12 = (uint)uVar24;
        iVar1 = _ZN6CLevel8GetLevelEv(uVar12,(int)((ulonglong)uVar24 >> 0x20),uVar12 * 0x10624dd3);
        uVar15 = *(undefined4 *)(iVar1 + 0x990);
        iVar1 = _ZN6CLevel8GetLevelEv();
        iVar3 = *piVar14;
        uVar9 = *(undefined4 *)(iVar1 + 0x98c);
        if (iVar3 == 0) {
          iVar3 = _Znwj(0x80);
          _ZN15CEffectsManagerC2Ev();
          *piVar14 = iVar3;
        }
        sprintf((char *)(DAT_003f1858 + 0x3f1794),(char *)(DAT_003f185c + 0x3f179c),uVar7,
                uVar12 / 1000,uVar2,uVar4,uVar5,uVar15,uVar9,
                *(undefined4 *)(*(int *)(iVar3 + 0x7c) + 4));
      }
    }
    else {
      piVar14 = *(int **)(DAT_003f1834 + 0x3f14e8);
      iVar1 = *piVar14;
      dVar18 = DAT_003f1820;
      dVar19 = DAT_003f1820;
      dVar20 = DAT_003f1820;
      dVar21 = DAT_003f1820;
      dVar22 = DAT_003f1820;
      dVar23 = DAT_003f1820;
      if ((iVar1 != 0) && (iVar1 = *(int *)(iVar1 + 0x10), iVar1 != 0)) {
        _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
                  (&local_6c,*(undefined4 *)(iVar1 + 0x1b8));
        pfVar6 = (float *)(**(code **)(**(int **)(*(int *)(*piVar14 + 0x10) + 0x1b8) + 0x124))();
        dVar18 = (double)pfVar6[2];
        dVar19 = (double)local_6c;
        dVar20 = (double)local_64;
        dVar21 = (double)local_68;
        dVar22 = (double)*pfVar6;
        dVar23 = (double)pfVar6[1];
      }
      uVar7 = _ZNK6glitch5video12IVideoDriver6getFPSEi(uVar15,0);
      piVar14 = (int *)(DAT_003f1838 + 0x3f1570);
      uVar24 = _ZNK6glitch5video12IVideoDriver22getPrimitiveCountDrawnEji(uVar15,0,0);
      uVar12 = (uint)uVar24;
      iVar1 = _ZN6CLevel8GetLevelEv(uVar12,(int)((ulonglong)uVar24 >> 0x20),uVar12 * 0x10624dd3);
      uVar15 = *(undefined4 *)(iVar1 + 0x990);
      iVar1 = _ZN6CLevel8GetLevelEv();
      iVar3 = *piVar14;
      uVar9 = *(undefined4 *)(iVar1 + 0x98c);
      if (iVar3 == 0) {
        iVar3 = _Znwj(0x80);
        _ZN15CEffectsManagerC2Ev();
        *piVar14 = iVar3;
      }
      sprintf((char *)(DAT_003f183c + 0x3f15dc),(char *)(DAT_003f1840 + 0x3f15e8),uVar7,
              uVar12 / 1000,uVar2,uVar4,uVar5,uVar15,uVar9,
              *(undefined4 *)(*(int *)(iVar3 + 0x7c) + 4),dVar19,dVar21,dVar20,dVar22,dVar23,dVar18)
      ;
    }
  }
  iVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
  if (iVar1 != 0) {
    uVar12 = *(uint *)(DAT_003f1844 + 0x3f1618);
    bVar16 = (uVar12 & 0x80) != 0;
    iVar1 = extraout_r2;
    if (bVar16) {
      iVar1 = param_1 + 0x11c00;
    }
    if (bVar16) {
      *(float *)(iVar1 + 0x32c) = param_2 + *(float *)(iVar1 + 0x32c);
    }
    bVar16 = (uVar12 & 0x10) != 0;
    if (bVar16) {
      iVar1 = param_1 + 0x11c00;
    }
    if (bVar16) {
      *(float *)(iVar1 + 0x34c) = param_2 + *(float *)(iVar1 + 0x34c);
    }
    bVar16 = (uVar12 & 0x20) != 0;
    if (bVar16) {
      iVar1 = param_1 + 0x11c00;
    }
    if (bVar16) {
      *(float *)(iVar1 + 0x360) = param_2 + *(float *)(iVar1 + 0x360);
    }
    bVar16 = (uVar12 & 0x40) != 0;
    if (bVar16) {
      uVar12 = param_1 + 0x11c00;
    }
    if (bVar16) {
      *(float *)(uVar12 + 0x374) = param_2 + *(float *)(uVar12 + 0x374);
    }
    fVar17 = (float)VectorUnsignedToFloat
                              (*(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1),
                               (byte)(in_fpscr >> 0x16) & 3);
    uVar2 = VectorFloatToUnsigned(param_2 + fVar17,3);
    *(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1) = uVar2;
    uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
    _ZN4glot15TrackingManager6UpdateEi(uVar2,(int)param_2);
  }
  return;
}


