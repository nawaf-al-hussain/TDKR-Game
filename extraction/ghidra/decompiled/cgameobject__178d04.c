// _Z22CAI_CallReinforcementsP11CGameObjectiS0_f @ 00178d04

void _Z22CAI_CallReinforcementsP11CGameObjectiS0_f
               (int *param_1,undefined4 param_2,int *param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  int *piVar6;
  float fVar7;
  undefined4 *local_2c;
  undefined4 *local_28;
  undefined4 local_24;
  
  if ((param_1 != (int *)0x0) && (param_3 != (int *)0x0 && param_1[0x2f] != 0)) {
    local_2c = (undefined4 *)0x0;
    local_28 = (undefined4 *)0x0;
    local_24 = 0;
    iVar1 = _ZN15CNpcAIComponent7IsEnemyEv();
    if (iVar1 == 0) {
      uVar2 = _ZN6CLevel8GetLevelEv();
      _ZN6CLevel16GetActorsInRangeEPSt6vectorIP11CGameObjectSaIS2_EEifbi
                (uVar2,&local_2c,param_2,param_4,1,0xffffffff);
      puVar4 = local_2c;
    }
    else {
      _ZN13CAIController17GetEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEifi_constprop_3254
                (*(undefined4 *)(DAT_00178ea8 + 0x178ea4),&local_2c,param_2,param_4);
      puVar4 = local_2c;
    }
LAB_00178d7c:
    puVar5 = puVar4;
    if (puVar4 != local_28) {
      while( true ) {
        puVar4 = puVar5 + 1;
        iVar1 = (**(code **)(*(int *)*puVar5 + 0x14))();
        iVar3 = (**(code **)(*param_1 + 0x14))(param_1);
        if (iVar1 == iVar3) break;
        iVar1 = (**(code **)(*(int *)*puVar5 + 0x14))();
        iVar3 = (**(code **)(*param_3 + 0x14))(param_3);
        if (iVar1 == iVar3) break;
        piVar6 = (int *)*puVar5;
        if (((piVar6[0x2f] == 0) || (*(int *)(piVar6[0x2f] + 0x44) != 2)) ||
           (iVar1 = _ZN11CGameObject11IsAttackingEPS_b(piVar6,0,0), iVar1 != 0)) break;
        iVar1 = (**(code **)(*param_1 + 0x18))(param_1);
        fVar7 = *(float *)(iVar1 + 8);
        iVar1 = (**(code **)(*piVar6 + 0x18))(piVar6);
        if (3.0 < ABS(fVar7 - *(float *)(iVar1 + 8))) break;
        _ZN19CAwarenessComponent16SetCurrentTargetEP11CGameObject(piVar6[0x2b],param_3);
        _ZN15CNpcAIComponent15StartCatchEnemyEv(piVar6[0x2f]);
        puVar5 = puVar4;
        if (puVar4 == local_28) goto LAB_00178e70;
      }
      goto LAB_00178d7c;
    }
LAB_00178e70:
    if (local_2c != (undefined4 *)0x0) {
      _ZdlPv();
    }
  }
  return;
}

