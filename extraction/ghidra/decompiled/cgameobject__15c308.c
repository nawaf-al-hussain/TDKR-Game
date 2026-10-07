// _Z28DoGetClosestWaypointDistanceP15CGameObjectBaseP15CWayPointObjectRfb @ 0015c308

int * _Z28DoGetClosestWaypointDistanceP15CGameObjectBaseP15CWayPointObjectRfb
                (int *param_1,int *param_2,float *param_3,int param_4)

{
  int *piVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  float fVar4;
  void *pvVar5;
  float *pfVar6;
  float *pfVar7;
  void *pvVar8;
  int iVar9;
  int *piVar10;
  int *piVar11;
  int iVar12;
  int *piVar13;
  uint uVar14;
  uint uVar15;
  size_t sVar16;
  int *local_54 [2];
  int local_4c;
  int *local_48;
  int *local_44;
  int *local_40;
  int *local_3c;
  int local_38;
  int *local_34;
  int *local_30;
  float local_2c;
  float local_28;
  float local_24;
  
  if (param_2 != (int *)0x0) {
    local_54[0] = param_2;
    uVar2 = (**(code **)(*param_2 + 0xc))(param_2);
    uVar3 = (**(code **)(*param_1 + 0xc))(param_1);
    fVar4 = (float)_ZNK6glitch4core8vector3dIfE15getDistanceFromERKS2_(uVar2,uVar3);
    *param_3 = fVar4;
    param_2 = local_54[0];
    if (param_4 != 0) {
      local_44 = (int *)0x0;
      local_40 = (int *)0x0;
      local_3c = (int *)0x0;
      local_38 = 0;
      local_34 = (int *)0x0;
      local_30 = (int *)0x0;
      _ZNSt6vectorIP15CWayPointObjectSaIS1_EE9push_backERKS1__part_2244(&local_38,local_54);
LAB_0015c38c:
      if ((uint)((int)local_34 - local_38) >> 2 != 0) {
        local_34 = local_34 + -1;
        local_4c = *local_34;
        if (local_40 == local_3c) {
          _ZNSt6vectorIP15CWayPointObjectSaIS1_EE9push_backERKS1__part_2244(&local_44,&local_4c);
        }
        else {
          if (local_40 != (int *)0x0) {
            *local_40 = local_4c;
          }
          local_40 = local_40 + 1;
        }
        uVar14 = 0;
        uVar15 = *(int *)(local_4c + 0x58) - *(int *)(local_4c + 0x54) >> 2;
        if (uVar15 == 0) goto LAB_0015c63c;
LAB_0015c3ec:
        iVar9 = local_4c;
        if (0x3fffffff < uVar15) {
LAB_0015c738:
                    /* WARNING: Subroutine does not return */
          _ZSt17__throw_bad_allocv();
        }
        pvVar5 = (void *)_Znwj(uVar15 << 2);
        pvVar8 = *(void **)(iVar9 + 0x54);
        iVar9 = *(int *)(iVar9 + 0x58) - (int)pvVar8 >> 2;
        if (iVar9 != 0) {
          sVar16 = iVar9 << 2;
          memmove(pvVar5,pvVar8,sVar16);
          goto LAB_0015c41c;
        }
        do {
          sVar16 = 0;
LAB_0015c41c:
          if (pvVar5 != (void *)0x0) {
            _ZdlPv(pvVar5);
          }
          iVar9 = local_4c;
          if ((uint)((int)sVar16 >> 2) <= uVar14) goto LAB_0015c38c;
          uVar15 = *(int *)(local_4c + 0x58) - *(int *)(local_4c + 0x54) >> 2;
          if (uVar15 == 0) {
            pvVar5 = (void *)0x0;
LAB_0015c484:
            sVar16 = 0;
          }
          else {
            if (0x3fffffff < uVar15) goto LAB_0015c738;
            pvVar5 = (void *)_Znwj(uVar15 << 2);
            pvVar8 = *(void **)(iVar9 + 0x54);
            iVar9 = *(int *)(iVar9 + 0x58) - (int)pvVar8 >> 2;
            if (iVar9 == 0) goto LAB_0015c484;
            sVar16 = iVar9 << 2;
            memmove(pvVar5,pvVar8,sVar16);
          }
          if ((uint)((int)sVar16 >> 2) <= uVar14) {
                    /* WARNING: Subroutine does not return */
            _ZSt20__throw_out_of_rangePKc((int)&DAT_0015c748 + DAT_0015c748);
          }
          local_48 = *(int **)((int)pvVar5 + uVar14 * 4);
          if (pvVar5 != (void *)0x0) {
            _ZdlPv(pvVar5);
          }
          iVar12 = (int)local_40 - (int)local_44;
          iVar9 = iVar12 >> 4;
          piVar11 = local_44;
          if (0 < iVar9) {
            piVar13 = local_44;
            if ((int *)*local_44 != local_48) {
              if (local_48 == (int *)local_44[1]) {
                piVar13 = local_44 + 1;
              }
              else if (local_48 == (int *)local_44[2]) {
                piVar13 = local_44 + 2;
              }
              else {
                piVar10 = local_44;
                if (local_48 == (int *)local_44[3]) {
                  piVar13 = local_44 + 3;
                }
                else {
                  do {
                    iVar9 = iVar9 + -1;
                    piVar11 = piVar10 + 4;
                    if (iVar9 == 0) {
                      iVar12 = (int)local_40 - (int)piVar11;
                      goto LAB_0015c564;
                    }
                    piVar13 = piVar11;
                  } while (((((int *)piVar10[4] != local_48) &&
                            (piVar13 = piVar10 + 5, (int *)piVar10[5] != local_48)) &&
                           (piVar13 = piVar10 + 6, (int *)piVar10[6] != local_48)) &&
                          (piVar1 = piVar10 + 7, piVar13 = piVar10 + 7, piVar10 = piVar11,
                          (int *)*piVar1 != local_48));
                }
              }
            }
            goto joined_r0x0015c6ac;
          }
LAB_0015c564:
          iVar12 = iVar12 >> 2;
          if (iVar12 == 2) {
LAB_0015c700:
            piVar13 = piVar11;
            if ((int *)*piVar11 != local_48) {
              piVar11 = piVar11 + 1;
LAB_0015c584:
              piVar13 = piVar11;
              if ((int *)*piVar11 != local_48) {
                piVar13 = local_40;
              }
            }
          }
          else if (iVar12 == 3) {
            piVar13 = piVar11;
            if ((int *)*piVar11 != local_48) {
              piVar11 = piVar11 + 1;
              goto LAB_0015c700;
            }
          }
          else {
            piVar13 = local_40;
            if (iVar12 == 1) goto LAB_0015c584;
          }
joined_r0x0015c6ac:
          if (local_40 == piVar13) {
            if (local_34 == local_30) {
              _ZNSt6vectorIP15CWayPointObjectSaIS1_EE9push_backERKS1__part_2244(&local_38,&local_48)
              ;
            }
            else {
              if (local_34 != (int *)0x0) {
                *local_34 = (int)local_48;
              }
              local_34 = local_34 + 1;
            }
          }
          uVar14 = uVar14 + 1;
          pfVar6 = (float *)(**(code **)(*local_48 + 0xc))();
          pfVar7 = (float *)(**(code **)(*param_1 + 0xc))(param_1);
          local_2c = *pfVar6 - *pfVar7;
          local_28 = pfVar6[1] - pfVar7[1];
          local_24 = pfVar6[2] - pfVar7[2];
          fVar4 = (float)_ZNK6glitch4core8vector3dIfE9getLengthEv(&local_2c);
          iVar9 = *(int *)(local_4c + 0x54);
          iVar12 = *(int *)(local_4c + 0x58);
          if (fVar4 < *param_3) {
            *param_3 = fVar4;
            local_54[0] = local_48;
          }
          uVar15 = iVar12 - iVar9 >> 2;
          if (uVar15 != 0) goto LAB_0015c3ec;
LAB_0015c63c:
          pvVar5 = (void *)0x0;
        } while( true );
      }
      if (local_38 != 0) {
        _ZdlPv();
      }
      param_2 = local_54[0];
      if (local_44 != (int *)0x0) {
        _ZdlPv();
        param_2 = local_54[0];
      }
    }
  }
  return param_2;
}

