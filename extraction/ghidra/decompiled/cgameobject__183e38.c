// _ZN21AIControl_WeaponStash18GetAvailableInZoneEPSt6vectorIP11CGameObjectSaIS2_EEfS2_ @ 00183e38

void _ZN21AIControl_WeaponStash18GetAvailableInZoneEPSt6vectorIP11CGameObjectSaIS2_EEfS2_
               (int param_1,undefined4 *param_2,float param_3,int *param_4)

{
  undefined8 uVar1;
  float *pfVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  
  iVar4 = *param_4;
  param_2[1] = *param_2;
  pfVar2 = (float *)(**(code **)(iVar4 + 0x18))(param_4);
  fVar8 = *pfVar2;
  uVar1 = *(undefined8 *)(pfVar2 + 1);
  for (iVar4 = *(int *)(param_1 + 0xc); param_1 + 4 != iVar4;
      iVar4 = _ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(iVar4)) {
    iVar3 = (**(code **)(**(int **)(iVar4 + 0x10) + 0x54))();
    if ((iVar3 != 0) && (*(int *)(iVar4 + 0x14) == 0)) {
      pfVar2 = (float *)(**(code **)(**(int **)(iVar4 + 0x10) + 0x18))();
      fVar6 = (float)uVar1 - pfVar2[1];
      fVar7 = (float)((ulonglong)uVar1 >> 0x20) - pfVar2[2];
      if ((fVar8 - *pfVar2) * (fVar8 - *pfVar2) + fVar6 * fVar6 + fVar7 * fVar7 < param_3 * param_3)
      {
        puVar5 = (undefined4 *)param_2[1];
        if (puVar5 == (undefined4 *)param_2[2]) {
          _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                    (param_2,puVar5,iVar4 + 0x10);
        }
        else {
          iVar3 = 0;
          if (puVar5 != (undefined4 *)0x0) {
            *puVar5 = *(undefined4 *)(iVar4 + 0x10);
            iVar3 = param_2[1];
          }
          param_2[1] = iVar3 + 4;
        }
      }
    }
  }
  return;
}

