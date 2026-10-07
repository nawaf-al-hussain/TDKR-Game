// _ZN6glitch7collada23CAnimatorBlenderSampler19setAnimationClipIDsERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEEPKii @ 00773b44

void _ZN6glitch7collada23CAnimatorBlenderSampler19setAnimationClipIDsERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEEPKii
               (int param_1,undefined4 *param_2,undefined4 *param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  int *piVar3;
  undefined4 uVar4;
  code *pcVar5;
  int iVar6;
  int iVar7;
  int *piVar8;
  undefined4 uVar9;
  int *piVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  
  if (param_4 < 1) {
    iVar6 = 0;
  }
  else {
    iVar6 = 0;
    do {
      iVar7 = iVar6 * 4;
      puVar2 = (undefined4 *)(**(code **)(*(int *)*param_2 + 0x10))((int *)*param_2,*param_3);
      piVar8 = *(int **)(param_1 + 0x24);
      uVar4 = *puVar2;
      uVar9 = puVar2[1];
      piVar3 = (int *)(**(code **)(**(int **)(piVar8[0x10] + iVar6 * 4) + 0x44))();
      piVar10 = *(int **)(piVar8[0x10] + iVar6 * 4);
      fVar11 = *(float *)(*piVar3 + 0x10);
      fVar12 = *(float *)(*piVar3 + 0x14);
      (**(code **)(*piVar10 + 0xa4))(piVar10,uVar4);
      puVar2 = (undefined4 *)(**(code **)(**(int **)(piVar8[0x10] + iVar6 * 4) + 0x44))();
      (**(code **)(*(int *)*puVar2 + 0x14))((int *)*puVar2,uVar9);
      iVar1 = iVar6 * 4;
      iVar6 = iVar6 + 1;
      piVar3 = (int *)(**(code **)(**(int **)(piVar8[0x10] + iVar1) + 0x44))();
      pcVar5 = *(code **)(*piVar8 + 0x44);
      piVar8[0x16] = (int)((float)piVar8[0x16] +
                          ((*(float *)(*piVar3 + 0x14) - *(float *)(*piVar3 + 0x10)) -
                          (fVar12 - fVar11)) * *(float *)(piVar8[10] + iVar7));
      puVar2 = (undefined4 *)(*pcVar5)(piVar8);
      fVar12 = (float)piVar8[0x16];
      piVar3 = (int *)*puVar2;
      fVar14 = (float)piVar3[5];
      fVar13 = (float)piVar3[1];
      (**(code **)(*piVar3 + 0x54))(piVar3,0,fVar12,0);
      fVar11 = 0.0;
      if (fVar14 == 0.0) {
        pcVar5 = *(code **)(*piVar3 + 0x10);
      }
      else {
        fVar11 = (fVar12 * fVar13) / fVar14;
        pcVar5 = *(code **)(*piVar3 + 0x10);
      }
      (*pcVar5)(piVar3,fVar11);
      param_3 = param_3 + 1;
    } while (iVar6 != param_4);
    iVar6 = param_4;
    if (3 < param_4) goto LAB_00773cd8;
  }
  do {
    iVar7 = iVar6 + 1;
    _ZN6glitch7collada37CSceneNodeAnimatorSynchronizedBlender9setWeightEif
              (*(undefined4 *)(param_1 + 0x24),iVar6,0);
    iVar6 = iVar7;
  } while (iVar7 < 4);
LAB_00773cd8:
  *(int *)(param_1 + 0x28) = param_4;
  return;
}


