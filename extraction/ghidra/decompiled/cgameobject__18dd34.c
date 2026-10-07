// _ZN13CAIController12SplashDamageEP11CGameObjectRKN6glitch4core8vector3dIfEES1_ffffib @ 0018dd34

void _ZN13CAIController12SplashDamageEP11CGameObjectRKN6glitch4core8vector3dIfEES1_ffffib
               (int param_1,int *param_2,float *param_3,int *param_4,float param_5,float param_6,
               float param_7,float param_8,int param_9,char param_10)

{
  float *pfVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  undefined4 local_84;
  undefined4 local_80;
  undefined4 local_7c;
  undefined4 local_78;
  float local_74;
  float local_70;
  float local_6c;
  float local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  float local_58;
  float local_54;
  float local_50;
  int *local_4c;
  
  fVar7 = DAT_0018e0e0;
  if (param_5 < param_6) {
    fVar7 = 1.0 / (param_6 - param_5);
  }
  if (param_2 == (int *)0x0) {
LAB_0018e098:
    local_84 = 0xffffffff;
  }
  else if (param_2[0x2e] == 0) {
    local_84 = 0xffffffff;
  }
  else {
    iVar3 = *(int *)(param_2[0x2e] + 0x2e0);
    if (iVar3 == 0) goto LAB_0018e098;
    local_84 = *(undefined4 *)(iVar3 + 0x30);
  }
  if (param_4 != (int *)0x0) {
    if ((param_4 == param_2) && (param_10 == '\0')) {
      _ZN6CLevel8GetLevelEv();
      goto LAB_0018defc;
    }
    pfVar1 = (float *)(**(code **)(*param_4 + 0x18))(param_4);
    fVar5 = (*pfVar1 - *param_3) * (*pfVar1 - *param_3) +
            (pfVar1[1] - param_3[1]) * (pfVar1[1] - param_3[1]) +
            (pfVar1[2] - param_3[2]) * (pfVar1[2] - param_3[2]);
    if (fVar5 < param_6 * param_6) {
      fVar5 = (param_6 - SQRT(fVar5)) * fVar7;
      if (fVar5 < 0.0) {
        fVar5 = DAT_0018e0e0;
      }
      fVar6 = 1.0;
      if (fVar5 <= 1.0) {
        fVar6 = fVar5;
      }
      fVar5 = param_7 + fVar6 * (param_8 - param_7);
      if ((param_2 != (int *)0x0) && (param_2[0x2f] != 0)) {
        fVar5 = (float)_ZN15CNpcAIComponent16NPCComputeDamageEf(param_2[0x2f],fVar5);
      }
      local_60 = local_84;
      local_64 = 7;
      local_58 = 0.0;
      local_5c = 0;
      local_54 = 0.0;
      local_50 = 0.0;
      local_68 = fVar5;
      local_4c = param_2;
      (**(code **)(*param_4 + 0xac))(param_4,&local_68);
      local_80 = 0;
      local_7c = 0;
      local_78 = 0;
      (**(code **)(*param_4 + 0xb0))(param_4,&local_80);
    }
  }
  iVar3 = _ZN6CLevel8GetLevelEv();
  if ((param_2 == (int *)0x0 && param_4 != *(int **)(iVar3 + 0xec)) && (param_10 != '\0')) {
    _Z11ApplyDamageP11CGameObjectS0_iRKN6glitch4core8vector3dIfEEfffff
              (*(int **)(iVar3 + 0xec),0,local_84,param_3,param_5,param_6,fVar7,param_7,param_8);
  }
LAB_0018defc:
  fVar5 = DAT_0018e0e0;
  iVar3 = *(int *)(param_1 + 0xb8);
  while (param_1 + 0xb0 != iVar3) {
    piVar4 = *(int **)(iVar3 + 0x10);
    iVar3 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3);
    iVar2 = (**(code **)(*piVar4 + 0x54))(piVar4);
    if (((((iVar2 != 0) && (iVar2 = _ZNK11CGameObject13IsInStateTypeEib(piVar4,0x100,0), iVar2 == 0)
          ) && (piVar4 != param_4)) &&
        ((param_9 == -1 || (iVar2 = _ZN11CGameObject13GetAIBehaviorEv(piVar4), iVar2 == param_9))))
       && ((param_10 != '\0' || (param_2 != piVar4)))) {
      pfVar1 = (float *)(**(code **)(*piVar4 + 0x18))(piVar4);
      fVar6 = (*pfVar1 - *param_3) * (*pfVar1 - *param_3) +
              (pfVar1[1] - param_3[1]) * (pfVar1[1] - param_3[1]) +
              (pfVar1[2] - param_3[2]) * (pfVar1[2] - param_3[2]);
      if (fVar6 < param_6 * param_6) {
        fVar6 = (param_6 - SQRT(fVar6)) * fVar7;
        if (fVar6 < 0.0) {
          fVar6 = fVar5;
        }
        if (1.0 < fVar6) {
          fVar6 = 1.0;
        }
        fVar6 = param_7 + fVar6 * (param_8 - param_7);
        if ((param_2 != (int *)0x0) && (param_2[0x2f] != 0)) {
          fVar6 = (float)_ZN15CNpcAIComponent16NPCComputeDamageEf(param_2[0x2f],fVar6);
        }
        local_58 = fVar5;
        local_54 = fVar5;
        local_50 = fVar5;
        local_60 = local_84;
        local_64 = 7;
        local_5c = 0;
        local_68 = fVar6;
        local_4c = param_2;
        (**(code **)(*piVar4 + 0xac))(piVar4,&local_68);
        local_74 = fVar5;
        local_70 = fVar5;
        local_6c = fVar5;
        (**(code **)(*piVar4 + 0xb0))(piVar4,&local_74);
      }
    }
  }
  return;
}

