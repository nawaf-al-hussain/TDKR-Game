// _Z11ApplyDamageP11CGameObjectS0_iRKN6glitch4core8vector3dIfEEfffff @ 0018dbf8

void _Z11ApplyDamageP11CGameObjectS0_iRKN6glitch4core8vector3dIfEEfffff
               (int *param_1,int param_2,undefined4 param_3,float *param_4,undefined4 param_5,
               float param_6,float param_7,float param_8,float param_9)

{
  float *pfVar1;
  float fVar2;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  float local_40 [3];
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  int local_24;
  
  pfVar1 = (float *)(**(code **)(*param_1 + 0x18))();
  fVar2 = (*pfVar1 - *param_4) * (*pfVar1 - *param_4) +
          (pfVar1[1] - param_4[1]) * (pfVar1[1] - param_4[1]) +
          (pfVar1[2] - param_4[2]) * (pfVar1[2] - param_4[2]);
  if (fVar2 < param_6 * param_6) {
    param_7 = (param_6 - SQRT(fVar2)) * param_7;
    if (param_7 < 0.0) {
      param_7 = DAT_0018dd30;
    }
    fVar2 = 1.0;
    if (param_7 <= 1.0) {
      fVar2 = param_7;
    }
    param_8 = param_8 + fVar2 * (param_9 - param_8);
    if ((param_2 != 0) && (*(int *)(param_2 + 0xbc) != 0)) {
      param_8 = (float)_ZN15CNpcAIComponent16NPCComputeDamageEf(*(int *)(param_2 + 0xbc),param_8);
    }
    local_40[1] = 9.80909e-45;
    local_34 = 0;
    local_30 = 0;
    local_2c = 0;
    local_28 = 0;
    local_40[0] = param_8;
    local_40[2] = (float)param_3;
    local_24 = param_2;
    (**(code **)(*param_1 + 0xac))(param_1,local_40);
    local_4c = 0;
    local_48 = 0;
    local_44 = 0;
    (**(code **)(*param_1 + 0xb0))(param_1,&local_4c);
  }
  return;
}

