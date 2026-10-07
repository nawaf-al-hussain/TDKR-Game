// _ZN13CAIController16NoiseGetLevelSumEPfPP11CGameObjectPN6glitch4core8vector3dIfEES7_ @ 0018d234

void _ZN13CAIController16NoiseGetLevelSumEPfPP11CGameObjectPN6glitch4core8vector3dIfEES7_
               (int param_1,float *param_2,undefined4 *param_3,undefined4 *param_4,float *param_5)

{
  float fVar1;
  undefined4 uVar2;
  int iVar3;
  float fVar4;
  float fVar5;
  float local_34;
  float local_30;
  float local_2c;
  
  *param_2 = 0.0;
  *param_3 = 0;
  fVar5 = 0.0;
  *param_4 = 0;
  param_4[1] = 0;
  param_4[2] = 0;
  for (iVar3 = *(int *)(param_1 + 0x10); param_1 + 8 != iVar3;
      iVar3 = _ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(iVar3)) {
    local_34 = *param_5 - *(float *)(iVar3 + 0x18);
    local_30 = param_5[1] - *(float *)(iVar3 + 0x1c);
    local_2c = param_5[2] - *(float *)(iVar3 + 0x20);
    fVar1 = (float)_ZNK6glitch4core8vector3dIfE9getLengthEv(&local_34);
    fVar4 = *(float *)(iVar3 + 0x28);
    fVar1 = fVar1 * *(float *)(param_1 + 0x1c);
    if (fVar1 <= fVar4) {
      if (*(int *)(iVar3 + 0x2c) == 1) {
        fVar4 = ((fVar4 - fVar1) * *(float *)(iVar3 + 0x24)) / fVar4;
      }
      else {
        fVar4 = *(float *)(iVar3 + 0x24);
      }
      *param_2 = *param_2 + fVar4;
      if (fVar5 < fVar4) {
        uVar2 = *(undefined4 *)(iVar3 + 0x18);
        *param_3 = *(undefined4 *)(iVar3 + 0x14);
        *param_4 = uVar2;
        param_4[1] = *(undefined4 *)(iVar3 + 0x1c);
        param_4[2] = *(undefined4 *)(iVar3 + 0x20);
        fVar5 = fVar4;
      }
    }
  }
  return;
}

