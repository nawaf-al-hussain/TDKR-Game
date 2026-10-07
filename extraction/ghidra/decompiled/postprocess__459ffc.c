// _ZN31CPostProcessEffect_DepthOfField5ApplyEv @ 00459ffc

void _ZN31CPostProcessEffect_DepthOfField5ApplyEv(int param_1)

{
  float *pfVar1;
  undefined4 uVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  bool bVar6;
  float extraout_s15;
  float fVar7;
  float fVar8;
  float fVar9;
  undefined4 local_44;
  undefined4 local_40;
  int *local_3c;
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  
  piVar4 = (int *)(DAT_0045a268 + 0x45a018);
  local_44 = (**(code **)(**(int **)(*piVar4 + 0xe4) + 0x134))();
  local_40 = (**(code **)(**(int **)(*piVar4 + 0xe4) + 0x138))(*(int **)(*piVar4 + 0xe4));
  _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv(&local_38,*(undefined4 *)(*piVar4 + 0xe4));
  bVar6 = *(int *)(param_1 + 0x1c) == -1;
  fVar7 = extraout_s15;
  if (bVar6) {
    fVar7 = *(float *)(param_1 + 0x20);
  }
  *(undefined4 *)(param_1 + 0x50) = *(undefined4 *)(param_1 + 0x58);
  *(undefined4 *)(param_1 + 0x4c) = *(undefined4 *)(param_1 + 0x28);
  *(undefined4 *)(param_1 + 0x54) = *(undefined4 *)(param_1 + 0x24);
  if (!bVar6) {
    piVar4 = (int *)_ZN13CZonesManager9FindActorEi(**(undefined4 **)(DAT_0045a26c + 0x45a08c));
    fVar7 = DAT_0045a260;
    fVar8 = DAT_0045a260;
    fVar9 = DAT_0045a260;
    if (piVar4 != (int *)0x0) {
      pfVar1 = (float *)(**(code **)(*piVar4 + 0x18))();
      piVar3 = (int *)piVar4[0x43];
      fVar9 = *pfVar1;
      fVar7 = pfVar1[1];
      fVar8 = pfVar1[2];
      if (piVar3 != (int *)0x0) {
        pfVar1 = (float *)(**(code **)(*piVar3 + 0x18))(piVar3);
        fVar9 = *pfVar1;
        fVar7 = pfVar1[1];
        fVar8 = pfVar1[2];
      }
      if ((*(int *)(*(int *)(param_1 + 0x18) + -0xc) != 0) &&
         (iVar5 = _ZNK11CGameObject12GetSceneNodeEv(piVar4), iVar5 != 0)) {
        uVar2 = _ZNK11CGameObject12GetSceneNodeEv(piVar4);
        _ZN6glitch5scene10ISceneNode20getSceneNodeFromNameEPKc
                  (&local_3c,uVar2,*(undefined4 *)(param_1 + 0x18));
        if (local_3c != (int *)0x0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                    ((int)local_3c + *(int *)(*local_3c + -0x10));
          _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv(&local_2c,local_3c);
          fVar7 = local_28;
          fVar8 = local_24;
          fVar9 = local_2c;
        }
      }
    }
    fVar7 = SQRT((fVar9 - local_38) * (fVar9 - local_38) + (fVar7 - local_34) * (fVar7 - local_34) +
                 (fVar8 - local_30) * (fVar8 - local_30));
  }
  fVar8 = DAT_0045a260;
  *(float *)(param_1 + 0x50) = fVar7 + fVar7;
  fVar7 = (fVar7 + fVar7 + -4.0) * DAT_0045a264;
  if (1.0 < fVar7) {
    fVar7 = 1.0;
  }
  if (fVar7 < 0.0) {
    fVar7 = fVar8;
  }
  *(float *)(param_1 + 0x54) = 1.0 - fVar7;
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x5c),0,param_1 + 0x4c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x60),0,param_1 + 0x54);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x5e),0,param_1 + 0x50);
  iVar5 = *(int *)(param_1 + 0x34);
  uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar5 + 4),DAT_0045a270 + 0x45a1a4,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (iVar5,uVar2,0,&local_44);
  iVar5 = *(int *)(param_1 + 0x34);
  uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar5 + 4),DAT_0045a274 + 0x45a1d0,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (iVar5,uVar2,0,&local_40);
  return;
}


