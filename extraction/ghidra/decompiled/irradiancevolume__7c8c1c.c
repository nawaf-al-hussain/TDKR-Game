// _ZN6glitch10irradiance17CIrradianceVolumeC1ENS_4core8aabbox3dIfEEffibb @ 007c8c1c

int * _ZN6glitch10irradiance17CIrradianceVolumeC1ENS_4core8aabbox3dIfEEffibb
                (int *param_1,float *param_2,float param_3,int param_4,int param_5,char param_6,
                char param_7)

{
  uint uVar1;
  int iVar2;
  void *pvVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  undefined4 *puVar7;
  void *pvVar8;
  undefined4 *puVar9;
  size_t sVar10;
  int iVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  
  iVar11 = 0;
  param_1[6] = (int)*param_2;
  param_1[7] = (int)param_2[1];
  fVar18 = 1.0 / param_3;
  param_1[8] = (int)param_2[2];
  param_1[9] = (int)param_2[3];
  param_1[10] = (int)param_2[4];
  param_1[0xb] = (int)param_2[5];
  fVar14 = param_2[3];
  fVar12 = param_2[4];
  fVar13 = param_2[1];
  fVar17 = *param_2;
  fVar15 = param_2[5];
  fVar16 = param_2[2];
  param_1[0xc] = (int)param_3;
  param_1[0x12] = param_4;
  *(char *)(param_1 + 0x13) = param_6;
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[0xd] = param_5;
  *(char *)((int)param_1 + 0x4d) = param_7;
  iVar4 = (int)(fVar18 * (fVar14 - fVar17)) + 1;
  param_1[0xe] = iVar4;
  iVar2 = (int)(fVar18 * (fVar12 - fVar13)) + 1;
  param_1[0xf] = iVar2;
  iVar5 = (int)(fVar18 * (fVar15 - fVar16)) + 1;
  param_1[0x10] = iVar5;
  iVar5 = iVar2 * iVar4 * iVar5;
  param_1[0x11] = iVar5;
  if ((param_6 != '\0') && (0 < param_5)) {
    while( true ) {
      pvVar3 = (void *)_Znaj(iVar5 * 0x84);
      if (iVar5 != 0) {
        iVar2 = 0;
        pvVar8 = pvVar3;
        do {
          iVar2 = iVar2 + 1;
          memset(pvVar8,0,0x84);
          pvVar8 = (void *)((int)pvVar8 + 0x84);
        } while (iVar5 != iVar2);
      }
      puVar7 = (undefined4 *)param_1[1];
      if (puVar7 == (undefined4 *)param_1[2]) {
        uVar1 = (int)puVar7 - *param_1 >> 2;
        if (uVar1 == 0) {
          iVar2 = 4;
        }
        else {
          uVar6 = uVar1 * 2;
          if (uVar6 < uVar1) {
            iVar2 = -4;
          }
          else {
            if (0x3ffffffe < uVar6) {
              uVar6 = 0x3fffffff;
            }
            iVar2 = uVar6 << 2;
          }
        }
        pvVar8 = (void *)_Znwj(iVar2);
        if ((void *)((int)pvVar8 + uVar1 * 4) != (void *)0x0) {
          *(void **)((int)pvVar8 + uVar1 * 4) = pvVar3;
        }
        iVar4 = (int)puVar7 - *param_1 >> 2;
        sVar10 = 0;
        if (iVar4 != 0) {
          sVar10 = iVar4 << 2;
          memmove(pvVar8,(void *)*param_1,sVar10);
        }
        pvVar3 = (void *)((int)pvVar8 + sVar10 + 4);
        iVar4 = param_1[1] - (int)puVar7 >> 2;
        sVar10 = 0;
        if (iVar4 != 0) {
          sVar10 = iVar4 << 2;
          memmove(pvVar3,puVar7,sVar10);
        }
        if (*param_1 != 0) {
          _ZdlPv();
        }
        *param_1 = (int)pvVar8;
        param_1[1] = (int)pvVar3 + sVar10;
        param_1[2] = (int)pvVar8 + iVar2;
      }
      else {
        iVar2 = 0;
        if (puVar7 != (undefined4 *)0x0) {
          *puVar7 = pvVar3;
          iVar2 = param_1[1];
        }
        param_1[1] = iVar2 + 4;
      }
      param_5 = param_1[0xd];
      iVar11 = iVar11 + 1;
      if (param_5 <= iVar11) break;
      iVar5 = param_1[0x11];
    }
  }
  if ((param_7 != '\0') && (0 < param_5)) {
    iVar2 = 0;
    do {
      iVar4 = param_1[0x11];
      puVar7 = (undefined4 *)_Znaj(iVar4 * 0x24);
      if (iVar4 != 0) {
        iVar5 = 0;
        puVar9 = puVar7;
        do {
          iVar5 = iVar5 + 1;
          *puVar9 = 0;
          puVar9[1] = 0;
          puVar9[2] = 0;
          puVar9[3] = 0;
          puVar9[4] = 0;
          puVar9[5] = 0;
          puVar9[6] = 0;
          puVar9[7] = 0;
          puVar9[8] = 0;
          puVar9 = puVar9 + 9;
        } while (iVar4 != iVar5);
      }
      puVar9 = (undefined4 *)param_1[4];
      if (puVar9 == (undefined4 *)param_1[5]) {
        uVar1 = (int)puVar9 - param_1[3] >> 2;
        if (uVar1 == 0) {
          iVar4 = 4;
        }
        else {
          uVar6 = uVar1 * 2;
          if (uVar6 < uVar1) {
            iVar4 = -4;
          }
          else {
            if (0x3ffffffe < uVar6) {
              uVar6 = 0x3fffffff;
            }
            iVar4 = uVar6 << 2;
          }
        }
        pvVar3 = (void *)_Znwj(iVar4);
        if ((void *)((int)pvVar3 + uVar1 * 4) != (void *)0x0) {
          *(undefined4 **)((int)pvVar3 + uVar1 * 4) = puVar7;
        }
        iVar5 = (int)puVar9 - param_1[3] >> 2;
        sVar10 = 0;
        if (iVar5 != 0) {
          sVar10 = iVar5 << 2;
          memmove(pvVar3,(void *)param_1[3],sVar10);
        }
        pvVar8 = (void *)((int)pvVar3 + sVar10 + 4);
        iVar5 = param_1[4] - (int)puVar9 >> 2;
        sVar10 = 0;
        if (iVar5 != 0) {
          sVar10 = iVar5 << 2;
          memmove(pvVar8,puVar9,sVar10);
        }
        if (param_1[3] != 0) {
          _ZdlPv();
        }
        param_1[3] = (int)pvVar3;
        param_1[4] = (int)pvVar8 + sVar10;
        param_1[5] = (int)pvVar3 + iVar4;
      }
      else {
        iVar4 = 0;
        if (puVar9 != (undefined4 *)0x0) {
          *puVar9 = puVar7;
          iVar4 = param_1[4];
        }
        param_1[4] = iVar4 + 4;
      }
      iVar2 = iVar2 + 1;
    } while (iVar2 < param_1[0xd]);
  }
  return param_1;
}


