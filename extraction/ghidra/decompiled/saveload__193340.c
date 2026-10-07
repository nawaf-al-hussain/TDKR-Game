// _ZN13CQuestManager14SaveLoad_LocalEP13CMemoryStream @ 00193340

/* WARNING: Removing unreachable block (ram,0x001922ec) */
/* WARNING: Removing unreachable block (ram,0x00192304) */
/* WARNING: Removing unreachable block (ram,0x00192318) */
/* WARNING: Removing unreachable block (ram,0x00192320) */
/* WARNING: Removing unreachable block (ram,0x00192324) */
/* WARNING: Removing unreachable block (ram,0x00192328) */
/* WARNING: Removing unreachable block (ram,0x00192338) */
/* WARNING: Removing unreachable block (ram,0x0019232c) */
/* WARNING: Removing unreachable block (ram,0x0019248c) */
/* WARNING: Removing unreachable block (ram,0x00192494) */
/* WARNING: Removing unreachable block (ram,0x00192344) */
/* WARNING: Removing unreachable block (ram,0x001921b0) */
/* WARNING: Removing unreachable block (ram,0x00192220) */
/* WARNING: Removing unreachable block (ram,0x00192228) */
/* WARNING: Removing unreachable block (ram,0x00192254) */
/* WARNING: Removing unreachable block (ram,0x00192258) */
/* WARNING: Removing unreachable block (ram,0x0019225c) */
/* WARNING: Removing unreachable block (ram,0x00192260) */
/* WARNING: Removing unreachable block (ram,0x00192264) */
/* WARNING: Removing unreachable block (ram,0x00192268) */
/* WARNING: Removing unreachable block (ram,0x001923d4) */
/* WARNING: Removing unreachable block (ram,0x001923ec) */
/* WARNING: Removing unreachable block (ram,0x00192400) */
/* WARNING: Removing unreachable block (ram,0x00192408) */
/* WARNING: Removing unreachable block (ram,0x0019240c) */
/* WARNING: Removing unreachable block (ram,0x00192420) */
/* WARNING: Removing unreachable block (ram,0x00192414) */
/* WARNING: Removing unreachable block (ram,0x00192458) */
/* WARNING: Removing unreachable block (ram,0x00192410) */
/* WARNING: Removing unreachable block (ram,0x00192460) */
/* WARNING: Removing unreachable block (ram,0x00192478) */
/* WARNING: Removing unreachable block (ram,0x0019242c) */
/* WARNING: Removing unreachable block (ram,0x0019235c) */
/* WARNING: Removing unreachable block (ram,0x00192374) */
/* WARNING: Removing unreachable block (ram,0x00192388) */
/* WARNING: Removing unreachable block (ram,0x00192390) */
/* WARNING: Removing unreachable block (ram,0x00192394) */
/* WARNING: Removing unreachable block (ram,0x001923a8) */
/* WARNING: Removing unreachable block (ram,0x0019239c) */
/* WARNING: Removing unreachable block (ram,0x00192444) */
/* WARNING: Removing unreachable block (ram,0x00192398) */
/* WARNING: Removing unreachable block (ram,0x0019244c) */
/* WARNING: Removing unreachable block (ram,0x001923b4) */
/* WARNING: Removing unreachable block (ram,0x001922c4) */

void _ZN13CQuestManager14SaveLoad_LocalEP13CMemoryStream(undefined4 *param_1,undefined4 param_2)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  void *pvVar4;
  uint uVar5;
  uint uVar6;
  float *pfVar7;
  void *__src;
  undefined4 *puVar8;
  undefined4 *puVar9;
  int *piVar10;
  uint *puVar11;
  undefined4 *puVar12;
  int *piVar13;
  int *piVar14;
  undefined2 *__src_00;
  short *psVar15;
  int iVar16;
  undefined4 *puVar17;
  int iVar18;
  size_t sVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  uint *local_30;
  int local_2c;
  undefined4 *puStack_28;
  
  piVar10 = (int *)param_1[0x1c];
  piVar13 = (int *)param_1[0x1b];
  param_1[9] = param_1[8];
  while (piVar14 = piVar13, piVar13 != piVar10) {
    while (piVar13 = piVar14 + 1, *piVar14 != 0) {
      _ZdlPv();
      *piVar14 = 0;
      piVar10 = (int *)param_1[0x1c];
      piVar14 = piVar13;
      if (piVar13 == piVar10) goto LAB_0019338c;
    }
  }
LAB_0019338c:
  param_1[0x1c] = param_1[0x1b];
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  param_1[0x3e] = uVar2;
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  param_1[0x3c] = uVar2;
  iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar3) {
    iVar16 = 0;
    do {
      while( true ) {
        uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
        __src_00 = (undefined2 *)param_1[9];
        if (__src_00 != (undefined2 *)param_1[10]) break;
        puVar11 = (uint *)((int)__src_00 - param_1[8] >> 1);
        if (puVar11 == (uint *)0x0) {
          local_2c = 2;
          local_30 = (uint *)0x0;
        }
        else {
          local_30 = (uint *)((int)puVar11 * 2);
          if (local_30 < puVar11) {
            local_2c = -2;
          }
          else {
            puVar11 = local_30;
            if (&DAT_7fffffff <= local_30) {
              puVar11 = (uint *)&DAT_7fffffff;
            }
            local_2c = (int)puVar11 << 1;
          }
        }
        pvVar4 = (void *)_Znwj(local_2c);
        __src = (void *)param_1[8];
        iVar18 = (int)__src_00 - (int)__src >> 1;
        if ((int)pvVar4 + (int)local_30 != 0) {
          *(undefined2 *)((int)pvVar4 + (int)local_30) = uVar1;
        }
        if (iVar18 == 0) {
          sVar19 = 0;
        }
        else {
          sVar19 = iVar18 << 1;
          memmove(pvVar4,__src,sVar19);
        }
        puVar11 = (uint *)((int)pvVar4 + sVar19 + 2);
        iVar18 = param_1[9] - (int)__src_00 >> 1;
        sVar19 = 0;
        if (iVar18 != 0) {
          sVar19 = iVar18 << 1;
          local_30 = puVar11;
          memmove(puVar11,__src_00,sVar19);
          puVar11 = local_30;
        }
        if (param_1[8] != 0) {
          _ZdlPv();
        }
        iVar16 = iVar16 + 1;
        param_1[8] = pvVar4;
        param_1[9] = (int)puVar11 + sVar19;
        param_1[10] = (int)pvVar4 + local_2c;
        if (iVar16 == iVar3) goto LAB_001934c0;
      }
      iVar16 = iVar16 + 1;
      if (__src_00 != (undefined2 *)0x0) {
        *__src_00 = uVar1;
      }
      param_1[9] = __src_00 + 1;
    } while (iVar16 != iVar3);
  }
LAB_001934c0:
  iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar3) {
    iVar16 = 0;
    do {
      uVar5 = _ZN13CMemoryStream7ReadIntEv(param_2);
      uVar6 = _ZN13CMemoryStream7ReadIntEv(param_2);
      puVar11 = (uint *)_ZN13CMemoryStream9ReadFloatEv(param_2);
      piVar10 = (int *)param_1[0x1b];
      do {
        if ((int *)param_1[0x1c] == piVar10) {
          local_30 = puVar11;
          puVar11 = (uint *)_Znwj(0xc);
          puVar17 = (undefined4 *)param_1[0x1c];
          *puVar11 = (uint)local_30;
          puVar9 = (undefined4 *)param_1[0x1d];
          puVar11[2] = uVar5;
          puVar11[1] = uVar6;
          if (puVar17 == puVar9) {
            uVar5 = (int)puVar17 - param_1[0x1b] >> 2;
            if (uVar5 == 0) {
              local_2c = 4;
            }
            else {
              uVar6 = uVar5 * 2;
              if (uVar6 < uVar5) {
                local_2c = -4;
              }
              else {
                if (0x3ffffffe < uVar6) {
                  uVar6 = 0x3fffffff;
                }
                local_2c = uVar6 << 2;
              }
            }
            local_30 = puVar11;
            pvVar4 = (void *)_Znwj(local_2c);
            if ((void *)((int)pvVar4 + uVar5 * 4) != (void *)0x0) {
              *(uint **)((int)pvVar4 + uVar5 * 4) = local_30;
            }
            iVar18 = (int)puVar17 - (int)param_1[0x1b] >> 2;
            sVar19 = 0;
            if (iVar18 != 0) {
              sVar19 = iVar18 << 2;
              memmove(pvVar4,(void *)param_1[0x1b],sVar19);
            }
            puVar11 = (uint *)((int)pvVar4 + sVar19 + 4);
            iVar18 = param_1[0x1c] - (int)puVar17 >> 2;
            sVar19 = 0;
            if (iVar18 != 0) {
              sVar19 = iVar18 << 2;
              local_30 = puVar11;
              memmove(puVar11,puVar17,sVar19);
              puVar11 = local_30;
            }
            if (param_1[0x1b] != 0) {
              _ZdlPv();
            }
            param_1[0x1b] = pvVar4;
            param_1[0x1c] = (int)puVar11 + sVar19;
            param_1[0x1d] = (int)pvVar4 + local_2c;
          }
          else {
            iVar18 = 0;
            if (puVar17 != (undefined4 *)0x0) {
              *puVar17 = puVar11;
              iVar18 = param_1[0x1c];
            }
            param_1[0x1c] = iVar18 + 4;
          }
          break;
        }
        iVar18 = *piVar10;
        piVar10 = piVar10 + 1;
      } while (uVar5 != *(uint *)(iVar18 + 8));
      iVar16 = iVar16 + 1;
    } while (iVar16 != iVar3);
  }
  _ZN13CMemoryStream8ReadBoolERb(param_2,param_1 + 0x40);
  if (*(char *)(param_1 + 0x40) == '\0') {
    if (param_1[0x3e] == -1) {
      return;
    }
    _ZN13CQuestManager14SetQuestStatusEiib(param_1,param_1[0x3e],9,1);
    if (*(char *)(param_1 + 0x40) != '\0') {
      _ZN13CQuestManager17UpdateSideMissionEf(param_1,0);
    }
    if ((*(char *)(param_1 + 0xc) != '\0') &&
       (piVar10 = (int *)_ZNK11CGameObject12GetComponentEi(param_1[0xb],0x5863bd59),
       piVar10 != (int *)0x0)) {
      (**(code **)(*piVar10 + 0x1c))(piVar10,0);
    }
    if (*(char *)(param_1 + 0x1f) == '\0') {
      return;
    }
    if (*(char *)(param_1 + 0x1a) != '\0') {
      return;
    }
    local_2c = 0;
    puStack_28 = (undefined4 *)0x0;
    iVar3 = _ZN6CLevel8GetLevelEv();
    pfVar7 = (float *)(**(code **)(**(int **)(iVar3 + 0xec) + 0x18))();
    fVar21 = *pfVar7;
    iVar3 = _ZN6CLevel8GetLevelEv();
    iVar3 = (**(code **)(**(int **)(iVar3 + 0xec) + 0x18))();
    puVar9 = (undefined4 *)param_1[0xe];
    puVar12 = (undefined4 *)param_1[0xd];
    fVar22 = *(float *)(iVar3 + 4);
    puVar17 = puStack_28;
LAB_001955cc:
    do {
      puVar8 = puVar12;
      if (puVar12 == puVar9) {
LAB_00195680:
        iVar3 = (int)puVar17 - local_2c >> 2;
        if (iVar3 != 0) {
          iVar3 = _Z6randomi(iVar3);
          iVar3 = *(int *)(local_2c + iVar3 * 4);
          *(undefined1 *)(param_1 + 0x1a) = 1;
          *param_1 = 0;
          uVar2 = *(undefined4 *)(iVar3 + 0x18);
          param_1[0x1e] = iVar3;
          _ZN13CQuestManager14SetQuestStatusEiib(param_1,uVar2,1,1);
          uVar2 = _ZN11Application11GetInstanceEv();
          _ZN11Application31SendTrackingEventMissionStartedEiii
                    (uVar2,*(undefined4 *)(param_1[0x1e] + 0x18),0,0);
        }
        if (local_2c != 0) {
          _ZdlPv();
        }
        return;
      }
      while( true ) {
        puVar12 = puVar8 + 1;
        local_30 = (uint *)*puVar8;
        *(undefined1 *)((int)local_30 + 0x25) = 0;
        fVar20 = fVar22 - (float)local_30[0xb];
        fVar20 = (fVar21 - (float)local_30[10]) * (fVar21 - (float)local_30[10]) + fVar20 * fVar20;
        if ((*(char *)((int)local_30 + 0x27) != '\0') &&
           ((float)local_30[8] * (float)local_30[8] < fVar20)) {
          *(undefined1 *)((int)local_30 + 0x27) = 0;
        }
        if (((((char)local_30[9] == '\0') || (*(char *)((int)local_30 + 0x26) != '\0')) ||
            (*(char *)((int)local_30 + 0x27) != '\0')) ||
           ((float)local_30[8] * (float)local_30[8] <= fVar20)) goto LAB_001955cc;
        *(undefined1 *)((int)local_30 + 0x25) = 1;
        if (puVar17 == (undefined4 *)0x0) break;
        puVar8 = (undefined4 *)0x0;
        if (puVar17 != (undefined4 *)0x0) {
          *puVar17 = local_30;
          puVar9 = (undefined4 *)param_1[0xe];
          puVar8 = puStack_28;
        }
        puVar17 = puVar8 + 1;
        puVar8 = puVar12;
        puStack_28 = puVar17;
        if (puVar12 == puVar9) goto LAB_00195680;
      }
      _ZNSt6vectorIP7HotSpotSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                (&local_2c,0,&local_30);
      puVar9 = (undefined4 *)param_1[0xe];
      puVar17 = puStack_28;
    } while( true );
  }
  if (*(char *)(param_1 + 0x3d) == '\0') {
    _ZN13CQuestManager23GenerateNextSideMissionEv(param_1);
    *(undefined1 *)(param_1 + 0x3d) = 1;
  }
  else {
    iVar3 = param_1[0x3e];
    if (iVar3 != -1) goto code_r0x001920e4;
    _ZN13CQuestManager23GenerateNextSideMissionEv(param_1);
  }
  iVar3 = param_1[0x3e];
  if (iVar3 == -1) {
    return;
  }
code_r0x001920e4:
  puVar9 = (undefined4 *)param_1[2];
  iVar16 = param_1[3] - (int)puVar9 >> 2;
  if (iVar16 == 0) {
LAB_00192148:
    psVar15 = (short *)_ZN13CQuestManager12InsertInListEii(param_1,iVar3,0xffffffff);
    if (psVar15 == (short *)0x0) {
      return;
    }
  }
  else {
    psVar15 = (short *)*puVar9;
    if (iVar3 != *psVar15) {
      iVar18 = 0;
      do {
        iVar18 = iVar18 + 1;
        if (iVar18 == iVar16) goto LAB_00192148;
        psVar15 = (short *)puVar9[iVar18];
      } while (iVar3 != *psVar15);
    }
  }
  piVar10 = (int *)_ZN13CZonesManager10FindObjectEit
                             (**(undefined4 **)(DAT_00192498 + 0x192174),
                              *(undefined4 *)(psVar15 + 2),1);
  if ((piVar10 != (int *)0x0) &&
     (iVar16 = _ZNK11CGameObject12GetComponentEi(piVar10,0x55a6393b), iVar16 != 0)) {
    if (*(int *)(iVar16 + 0x10) == 0) {
      iVar16 = -1;
    }
    else {
      iVar16 = *(int *)(*(int *)(iVar16 + 0x10) + 4);
    }
    if (iVar3 == iVar16) {
      (**(code **)(*piVar10 + 0x50))(piVar10,1);
    }
  }
  uVar5 = (uint)*(byte *)(psVar15 + 4);
  if (uVar5 != 1) {
    param_1[uVar5 + 0x2b] = param_1[uVar5 + 0x2b] + -1;
    param_1[0x2c] = param_1[0x2c] + 1;
    *(undefined1 *)(psVar15 + 4) = 1;
  }
  return;
}


