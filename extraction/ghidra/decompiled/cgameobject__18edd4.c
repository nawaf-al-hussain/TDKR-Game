// _ZN13CAIController22IntersectsWithStunAreaEP11CGameObject @ 0018edd4

undefined4 _ZN13CAIController22IntersectsWithStunAreaEP11CGameObject(int param_1,int *param_2)

{
  float *pfVar1;
  float fVar2;
  float fVar3;
  int iVar4;
  int iVar5;
  float *pfVar6;
  float fVar7;
  
  iVar4 = *(int *)(param_1 + 0x17c);
  if (0 < iVar4) {
    iVar5 = 0;
    do {
      while( true ) {
        pfVar6 = *(float **)(*(int *)(param_1 + 0x178) + iVar5 * 4);
        if ((0.0 < pfVar6[7]) && (pfVar6[8] <= 0.0)) break;
        iVar5 = iVar5 + 1;
        if (iVar4 <= iVar5) {
          return 0;
        }
      }
      pfVar1 = (float *)(**(code **)(*param_2 + 0x18))(param_2);
      iVar4 = (**(code **)(*param_2 + 0x18))(param_2);
      fVar2 = (float)_ZNK11CGameObject9GetHeightEv(param_2);
      fVar7 = *(float *)(iVar4 + 8);
      fVar3 = (float)_ZNK11CGameObject9GetRadiusEv(param_2);
      if ((pfVar1[2] <= pfVar6[2] + pfVar6[4]) &&
         ((pfVar6[2] <= fVar2 + fVar7 &&
          ((*pfVar6 - *pfVar1) * (*pfVar6 - *pfVar1) +
           (pfVar6[1] - pfVar1[1]) * (pfVar6[1] - pfVar1[1]) <=
           (fVar3 + pfVar6[3]) * (fVar3 + pfVar6[3]))))) {
        return *(undefined4 *)(*(int *)(param_1 + 0x178) + iVar5 * 4);
      }
      iVar4 = *(int *)(param_1 + 0x17c);
      iVar5 = iVar5 + 1;
    } while (iVar5 < iVar4);
  }
  return 0;
}

