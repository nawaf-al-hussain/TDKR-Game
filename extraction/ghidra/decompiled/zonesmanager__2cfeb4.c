// _ZN13CZonesManager20RefreshAllActorsPoolEv @ 002cfeb4

void _ZN13CZonesManager20RefreshAllActorsPoolEv(int param_1)

{
  uint uVar1;
  undefined8 uVar2;
  float *pfVar3;
  int iVar4;
  int iVar5;
  undefined8 *puVar6;
  int iVar7;
  int iVar8;
  void *__dest;
  int *piVar9;
  float *pfVar10;
  uint uVar11;
  int *piVar12;
  int *piVar13;
  undefined4 *__src;
  int iVar14;
  int *piVar15;
  int *piVar16;
  int *piVar17;
  int *piVar18;
  void *__dest_00;
  size_t sVar19;
  int iVar20;
  int iVar21;
  float fVar22;
  float fVar23;
  float *local_4c;
  int local_48;
  int *local_44;
  int local_40;
  
  piVar16 = *(int **)(param_1 + 0x80);
  iVar20 = 0;
  local_44 = (int *)0x0;
  piVar9 = (int *)(DAT_002d0288 + 0x2cfee4);
  local_40 = 0;
  *(undefined4 *)(param_1 + 0x58) = *(undefined4 *)(param_1 + 0x54);
  do {
    piVar17 = piVar16;
    if (*(int **)(param_1 + 0x84) == piVar16) {
LAB_002cff94:
      if (local_44 != (int *)0x0) {
        _ZN11CGameObject7SetZoneEP5CZoneb(local_44,local_40,0);
      }
      piVar9 = (int *)(DAT_002d028c + 0x2cffbc);
      iVar4 = *piVar9;
      *piVar9 = iVar4 + 1;
      if (iVar20 <= iVar4 + 1) {
        *piVar9 = 0;
      }
      return;
    }
    while( true ) {
      piVar16 = piVar17 + 1;
      iVar4 = (**(code **)(*(int *)*piVar17 + 0x54))();
      if (iVar4 == 0) break;
      iVar4 = *(int *)(*(int *)(*piVar17 + 0x134) + 8);
      iVar21 = *(int *)(iVar4 + 0x10);
      if (iVar21 < 1) break;
      iVar14 = 0;
      do {
        piVar15 = *(int **)(*(int *)(iVar4 + 0xc) + iVar14 * 4);
        iVar5 = (**(code **)(*piVar15 + 0x54))(piVar15);
        if (iVar5 != 0) {
          if (*(char *)(*piVar17 + 0x1e4) != '\0') {
            __src = *(undefined4 **)(param_1 + 0x58);
            if (__src == *(undefined4 **)(param_1 + 0x5c)) {
              uVar1 = (int)__src - *(int *)(param_1 + 0x54) >> 2;
              if (uVar1 == 0) {
                local_4c = (float *)0x4;
              }
              else {
                uVar11 = uVar1 * 2;
                if (uVar11 < uVar1) {
                  local_4c = (float *)0xfffffffc;
                }
                else {
                  if (0x3ffffffe < uVar11) {
                    uVar11 = 0x3fffffff;
                  }
                  local_4c = (float *)(uVar11 << 2);
                }
              }
              __dest = (void *)_Znwj(local_4c);
              if ((void *)((int)__dest + uVar1 * 4) != (void *)0x0) {
                *(int **)((int)__dest + uVar1 * 4) = piVar15;
              }
              iVar5 = (int)__src - (int)*(void **)(param_1 + 0x54) >> 2;
              sVar19 = 0;
              if (iVar5 != 0) {
                sVar19 = iVar5 << 2;
                memmove(__dest,*(void **)(param_1 + 0x54),sVar19);
              }
              __dest_00 = (void *)((int)__dest + sVar19 + 4);
              iVar5 = *(int *)(param_1 + 0x58) - (int)__src >> 2;
              sVar19 = 0;
              if (iVar5 != 0) {
                sVar19 = iVar5 << 2;
                memmove(__dest_00,__src,sVar19);
              }
              if (*(int *)(param_1 + 0x54) != 0) {
                _ZdlPv();
              }
              *(void **)(param_1 + 0x54) = __dest;
              *(size_t *)(param_1 + 0x58) = (int)__dest_00 + sVar19;
              *(int *)(param_1 + 0x5c) = (int)__dest + (int)local_4c;
            }
            else {
              iVar5 = 0;
              if (__src != (undefined4 *)0x0) {
                *__src = piVar15;
                iVar5 = *(int *)(param_1 + 0x58);
              }
              *(int *)(param_1 + 0x58) = iVar5 + 4;
            }
          }
          if (*piVar9 == iVar20) {
            local_4c = (float *)0x0;
            local_48 = 0;
            puVar6 = (undefined8 *)(**(code **)(*piVar15 + 0x18))(piVar15);
            fVar23 = *(float *)(puVar6 + 1);
            uVar2 = *puVar6;
            iVar7 = (**(code **)(*piVar15 + 0xa0))(piVar15);
            piVar18 = *(int **)(param_1 + 0x80);
            pfVar3 = local_4c;
            iVar5 = local_48;
LAB_002d0024:
            local_48 = iVar5;
            local_4c = pfVar3;
            piVar12 = piVar18;
            if (piVar18 != *(int **)(param_1 + 0x84)) {
              while( true ) {
                piVar18 = piVar12 + 1;
                iVar8 = (**(code **)(*(int *)*piVar12 + 0x54))();
                pfVar3 = local_4c;
                iVar5 = local_48;
                if (iVar8 == 0) break;
                iVar8 = *piVar12;
                piVar12 = *(int **)(iVar8 + 0x184);
                do {
                  if (*(int **)(iVar8 + 0x188) == piVar12) goto LAB_002d0024;
                  piVar13 = piVar12 + 1;
                  pfVar10 = (float *)*piVar12;
                  fVar22 = (float)uVar2;
                  piVar12 = piVar13;
                } while (((((fVar22 < *pfVar10) || (pfVar10[3] < fVar22)) ||
                          (fVar22 = (float)((ulonglong)uVar2 >> 0x20), fVar22 < pfVar10[1])) ||
                         ((pfVar10[4] < fVar22 || (fVar23 + 0.5 < pfVar10[2])))) ||
                        (pfVar10[5] < fVar23 + 0.5));
                pfVar3 = pfVar10;
                iVar5 = iVar8;
                if (((local_4c == (float *)0x0) || ((int)local_4c[6] < (int)pfVar10[6])) ||
                   (pfVar3 = local_4c, iVar5 = local_48, pfVar10[6] != local_4c[6])) break;
                if (iVar7 == iVar8) {
                  local_48 = iVar7;
                  local_4c = pfVar10;
                }
                piVar12 = piVar18;
                if (piVar18 == *(int **)(param_1 + 0x84)) goto LAB_002d010c;
              }
              goto LAB_002d0024;
            }
LAB_002d010c:
            if ((local_48 != 0) &&
               (iVar5 = (**(code **)(*piVar15 + 0xa0))(piVar15), local_48 != iVar5)) {
              local_44 = piVar15;
              local_40 = local_48;
            }
          }
          iVar20 = iVar20 + 1;
        }
        iVar14 = iVar14 + 1;
      } while (iVar14 != iVar21);
      piVar17 = piVar16;
      if (*(int **)(param_1 + 0x84) == piVar16) goto LAB_002cff94;
    }
  } while( true );
}


