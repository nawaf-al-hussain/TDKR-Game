// _ZN19CPostProcessManager24BuildColorGradingTextureEv @ 00458e18

void _ZN19CPostProcessManager24BuildColorGradingTextureEv(int param_1)

{
  undefined2 uVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  float fVar5;
  float fVar6;
  code *pcVar7;
  int iVar8;
  int iVar9;
  undefined4 uVar10;
  int *piVar11;
  int local_2c;
  int local_28;
  int local_24 [2];
  
  iVar9 = *(int *)(param_1 + 0x38);
  uVar2 = (**(code **)(**(int **)(*(int *)(param_1 + 8) + 0x20) + 0x38))();
  uVar3 = (**(code **)(**(int **)(*(int *)(param_1 + 8) + iVar9 * 4) + 0x38))();
  if ((uVar3 & uVar2) != 0) {
    iVar8 = *(int *)(*(int *)(param_1 + 8) + 0x20);
    uVar10 = *(undefined4 *)(*(int *)(*(int *)(DAT_004590c8 + 0x458e80) + 0x10) + 0x154);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar8 + 0x50),0);
    _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar8 + 0x50),0);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar8 + 0x54),0);
    _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar8 + 0x54),0);
    _ZN6CLevel8GetLevelEv();
    iVar9 = _ZNK6CLevel18GetPlayerComponentEv();
    if ((*(int *)(iVar9 + 0x3fc) == 0) ||
       ((*(uint *)(*(int *)(iVar9 + 0x3fc) + 0xf4) & 0x18) != 0x18)) {
      uVar1 = *(undefined2 *)(param_1 + 100);
      local_2c = *(int *)(*(int *)(*(int *)(param_1 + 0x14) + 0xc) + 4);
      if (local_2c != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_2c + 4);
      }
      _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
                (uVar10,uVar1,0,&local_2c);
      _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_2c);
    }
    else {
      _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
                (uVar10,*(undefined2 *)(param_1 + 100),0,param_1 + 4);
    }
    iVar9 = DAT_004590cc;
    piVar11 = *(int **)(*(int *)(param_1 + 8) + 4);
    iVar4 = _ZN6CLevel8GetLevelEv();
    fVar5 = (float)_ZNK11CGameObject9GetHealthEv(*(undefined4 *)(iVar4 + 0xec));
    fVar5 = (20.0 - fVar5) * DAT_004590c0 + 1.0;
    fVar6 = (float)_ZN11CHUDDisplay12GetHurtAlphaEv(*(undefined4 *)(iVar9 + 0x458f34));
    if (fVar5 < 1.0 - fVar6) {
      fVar5 = (float)_ZN11CHUDDisplay12GetHurtAlphaEv(*(undefined4 *)(iVar9 + 0x458f34));
      fVar5 = 1.0 - fVar5;
    }
    iVar9 = _ZN6CLevel8GetLevelEv();
    fVar6 = DAT_004590c4;
    if ((*(char *)(iVar9 + 0xa50) == '\0') && (*(char *)(DAT_004590d0 + 0x45905c) == '\0')) {
      if (fVar5 < DAT_004590c4) {
        fVar5 = DAT_004590c4;
      }
      if (1.0 < fVar5) {
        fVar5 = 1.0;
      }
      fVar6 = fVar5;
      if (fVar5 < DAT_004590c4) {
        fVar6 = DAT_004590c4;
      }
    }
    if ((*(float *)(param_1 + 0x5c) != fVar6) ||
       (*(float *)(iVar8 + 0x4c) != *(float *)(param_1 + 0x60))) {
      local_28 = *(int *)(iVar8 + 0x50);
      *(float *)(param_1 + 0x60) = *(float *)(iVar8 + 0x4c);
      iVar9 = *piVar11;
      *(float *)(param_1 + 0x5c) = fVar6;
      pcVar7 = *(code **)(iVar9 + 0x3c);
      if (local_28 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_28 + 4);
      }
      local_24[0] = *(int *)(iVar8 + 0x54);
      if (local_24[0] != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_24[0] + 4);
      }
      (*pcVar7)(piVar11,&local_28,local_24,*(undefined4 *)(iVar8 + 0x4c),fVar6);
      _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(local_24);
      _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_28);
      (**(code **)(*piVar11 + 0x20))(piVar11,3,0xffffffff);
      (**(code **)(*piVar11 + 0x24))(piVar11,3);
      (**(code **)(*piVar11 + 0x28))(piVar11,3);
    }
  }
  return;
}

