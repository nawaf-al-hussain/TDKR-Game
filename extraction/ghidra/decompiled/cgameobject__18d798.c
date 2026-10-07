// _ZN13CAIController19Decor_NoiseGetEventEPiPP11CGameObjectPN6glitch4core8vector3dIfEES7_ @ 0018d798

void _ZN13CAIController19Decor_NoiseGetEventEPiPP11CGameObjectPN6glitch4core8vector3dIfEES7_
               (int param_1,undefined4 *param_2,undefined4 *param_3,float *param_4,float *param_5)

{
  int iVar1;
  undefined4 uVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  
  *param_2 = 0;
  *param_3 = 0;
  iVar1 = *(int *)(param_1 + 0x2c);
  fVar9 = -1.0;
  *param_4 = 0.0;
  param_4[1] = 0.0;
  param_4[2] = 0.0;
  while (param_1 + 0x24 != iVar1) {
    fVar3 = *(float *)(iVar1 + 0x18);
    fVar8 = *param_5 - fVar3;
    fVar4 = *(float *)(iVar1 + 0x1c);
    fVar5 = *(float *)(iVar1 + 0x20);
    fVar6 = param_5[1] - fVar4;
    fVar7 = param_5[2] - fVar5;
    if ((fVar8 * fVar8 + fVar6 * fVar6 + fVar7 * fVar7 <= *(float *)(iVar1 + 0x28)) &&
       ((fVar6 = *(float *)(iVar1 + 0x2c), fVar9 < 0.0 || (fVar6 < fVar9)))) {
      uVar2 = *(undefined4 *)(iVar1 + 0x14);
      *param_2 = *(undefined4 *)(iVar1 + 0x24);
      *param_3 = uVar2;
      *param_4 = fVar3;
      param_4[1] = fVar4;
      param_4[2] = fVar5;
      fVar9 = fVar6;
    }
    iVar1 = _ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base();
  }
  return;
}

