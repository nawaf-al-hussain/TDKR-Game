// _ZN6glitch5scene16CSkyBoxSceneNode14renderInternalEPv @ 0096a0f0

void _ZN6glitch5scene16CSkyBoxSceneNode14renderInternalEPv(int param_1)

{
  bool bVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  float *pfVar5;
  int iVar6;
  int iVar7;
  int *piVar8;
  int *piVar9;
  int iVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  int *local_bc;
  int *local_b8;
  int *local_b4;
  int *local_b0;
  float local_ac;
  float local_a8;
  float local_a4;
  undefined4 local_a0;
  undefined4 local_9c;
  int local_98;
  undefined4 local_94;
  undefined4 local_90;
  undefined4 local_8c;
  int local_88;
  int local_84;
  int *local_80;
  int *local_7c;
  int local_78;
  int local_74;
  int local_70;
  undefined4 local_6c;
  undefined1 auStack_68 [48];
  int local_38;
  int local_34;
  int local_30;
  
  piVar9 = *(int **)(*(int *)(param_1 + 0xe8) + 0x10);
  piVar8 = *(int **)(*(int *)(param_1 + 0xe8) + 0xe4);
  if (piVar8 == (int *)0x0 || piVar9 == (int *)0x0) {
    return;
  }
  piVar2 = (int *)(**(code **)(*piVar8 + 0x168))(piVar8);
  if (piVar2 == (int *)0x0) {
    _ZN6glitch4core8CMatrix4IfEC2ERKS2_NS2_12eConstructorE_constprop_1050(auStack_68,param_1 + 0x10)
    ;
    local_38 = piVar8[0x10];
    local_34 = piVar8[0x11];
    local_30 = piVar8[0x12];
    _ZN6glitch5video12IVideoDriver12setTransformENS0_22E_TRANSFORMATION_STATEERKNS_4core8CMatrix4IfEEj
              (piVar9,2,auStack_68,0);
    iVar10 = 0;
    iVar3 = 4;
    iVar6 = 0;
    do {
      iVar7 = iVar3;
      iVar3 = param_1 + (iVar10 + 0x48) * 4;
      local_b4 = piVar2;
      iVar4 = _ZNK6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12getParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRSE_
                        (*(undefined4 *)(iVar3 + 4),*(undefined2 *)(param_1 + 0x140),0,&local_b4);
      if (iVar4 == 0) {
LAB_0096a308:
        iVar3 = iVar7 + 4;
        if (local_b4 != (int *)0x0) {
          piVar8 = local_b4 + 1;
          DataMemoryBarrier(0xf);
          do {
            iVar6 = *piVar8 + -1;
            bVar1 = (bool)hasExclusiveAccess(piVar8);
          } while (!bVar1);
          *piVar8 = iVar6;
          DataMemoryBarrier(0xf);
          if (iVar6 == 0) {
            (**(code **)(*local_b4 + 4))();
          }
          else if (iVar6 == 1) {
            _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
          }
        }
      }
      else {
        if (local_b4 == (int *)0x0) {
          iVar3 = iVar7;
        }
        iVar3 = iVar3 + 4;
        if (local_b4 != (int *)0x0) {
          local_bc = *(int **)(param_1 + 0x13c);
          if (local_bc != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
          }
          _ZN6glitch5video12IVideoDriver11setMaterialERKN5boost13intrusive_ptrINS0_9CMaterialEEERKNS3_IKNS0_27CMaterialVertexAttributeMapEEE
                    (piVar9,iVar3,&local_bc);
          piVar8 = local_bc;
          if (local_bc != (int *)0x0) {
            DataMemoryBarrier(0xf);
            do {
              iVar3 = *local_bc;
              bVar1 = (bool)hasExclusiveAccess(local_bc);
            } while (!bVar1);
            *local_bc = iVar3 + -1;
            DataMemoryBarrier(0xf);
            if (iVar3 + -1 == 0) {
              _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(local_bc);
              _Z10GlitchFreePv(piVar8);
            }
          }
          local_b8 = *(int **)(param_1 + 0x120);
          if (local_b8 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
          }
          local_78 = iVar7 - iVar6;
          local_6c = 0x500ff;
          local_b0 = piVar2;
          local_80 = piVar2;
          local_7c = piVar2;
          local_74 = iVar6;
          local_70 = iVar7;
          (**(code **)(*piVar9 + 0x3c))(piVar9,&local_b8,&local_80,0,&local_b0);
          if (local_b0 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
          }
          if (local_80 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
          }
          piVar8 = local_b8;
          if (local_b8 != (int *)0x0) {
            DataMemoryBarrier(0xf);
            do {
              iVar3 = *local_b8;
              bVar1 = (bool)hasExclusiveAccess(local_b8);
            } while (!bVar1);
            *local_b8 = iVar3 + -1;
            DataMemoryBarrier(0xf);
            if (iVar3 + -1 == 0) {
              _ZN6glitch5video14CVertexStreamsD1Ev(local_b8);
              _Z10GlitchFreePv(piVar8);
            }
          }
          goto LAB_0096a308;
        }
      }
      iVar10 = iVar10 + 1;
      iVar6 = iVar7;
      if (iVar3 == 0x1c) {
        return;
      }
    } while( true );
  }
  pfVar5 = (float *)(**(code **)(*piVar8 + 0x124))(piVar8);
  local_ac = *pfVar5 - (float)piVar8[0x10];
  local_a8 = pfVar5[1] - (float)piVar8[0x11];
  local_a4 = pfVar5[2] - (float)piVar8[0x12];
  _ZN6glitch4core8vector3dIfE9normalizeEv(&local_ac);
  fVar13 = ABS(local_ac);
  fVar12 = ABS(local_a8);
  fVar11 = ABS(local_a4);
  if (fVar12 <= fVar13) {
    if (fVar11 <= fVar13) {
      if (0.0 < local_ac) {
        iVar3 = 0;
      }
      else {
        iVar3 = 2;
      }
      goto LAB_0096a3fc;
    }
    if (fVar13 <= fVar12) goto LAB_0096a3c0;
LAB_0096a4f0:
    if (fVar12 <= fVar11) {
      if (0.0 < local_a4) {
        iVar3 = 1;
      }
      else {
        iVar3 = 3;
      }
      goto LAB_0096a3fc;
    }
  }
  else {
LAB_0096a3c0:
    if (fVar11 <= fVar12) {
      if (0.0 < local_a8) {
        iVar3 = 4;
      }
      else {
        iVar3 = 5;
      }
      goto LAB_0096a3fc;
    }
    if (fVar13 <= fVar11) goto LAB_0096a4f0;
  }
  iVar3 = 0;
LAB_0096a3fc:
  local_b4 = (int *)0x0;
  iVar3 = _ZNK6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12getParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRSE_
                    (*(undefined4 *)(param_1 + iVar3 * 4 + 0x124),*(undefined2 *)(param_1 + 0x140),0
                     ,&local_b4);
  if (iVar3 != 0) {
    if (local_b4 == (int *)0x0) {
      return;
    }
    local_88 = local_b4[7];
    local_84 = local_b4[8];
    local_9c = 0;
    local_94 = *(undefined4 *)(*(int *)(piVar9[0x48] + -4) + 0x10);
    local_a0 = 0xffffffff;
    local_98 = *(int *)(*(int *)(piVar9[0x48] + -4) + 0xc) + -1;
    local_90 = 0;
    local_8c = 0;
    _ZN6glitch5video9C2DDriver11draw2DImageEPNS0_12IVideoDriverERKN5boost13intrusive_ptrINS0_8ITextureEEERKNS_4core4rectIiEESE_PSD_PKNS0_6SColorEb
              (piVar9,&local_b4,&local_a0,&local_90,0,0,0);
  }
  if (local_b4 != (int *)0x0) {
    piVar8 = local_b4 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_b4 + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  return;
}

