// _ZN5CZone14ChangeLightMapEPKcS1_ @ 002c9208

void _ZN5CZone14ChangeLightMapEPKcS1_(int param_1,undefined4 param_2,undefined4 param_3)

{
  bool bVar1;
  int *piVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int *local_38;
  int *local_34;
  int *local_30;
  int *local_2c [2];
  
  if (*(int *)(param_1 + 0x198) != 0) {
    piVar3 = (int *)_Z9GetDevicev();
    _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
              (&local_38,*(undefined4 *)(*(int *)(*piVar3 + 8) + 0x14c),param_2,0);
    piVar3 = (int *)_Z9GetDevicev();
    _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
              (&local_34,*(undefined4 *)(*(int *)(*piVar3 + 8) + 0x14c),param_3,0);
    iVar4 = (**(code **)(**(int **)(param_1 + 0x198) + 0x10))();
    if (0 < iVar4) {
      iVar8 = 0;
      iVar6 = DAT_002c95d0 + 0x2c9298;
      iVar9 = DAT_002c95d4 + 0x2c92a8;
      iVar7 = DAT_002c95d8 + 0x2c92ac;
      piVar3 = (int *)0x0;
      while( true ) {
        local_30 = (int *)0x0;
        (**(code **)(**(int **)(param_1 + 0x198) + 0x18))(local_2c,*(int **)(param_1 + 0x198),iVar8)
        ;
        piVar2 = local_2c[0];
        if (local_2c[0] != (int *)0x0) {
          DataMemoryBarrier(0xf);
          do {
            bVar1 = (bool)hasExclusiveAccess(local_2c[0]);
          } while (!bVar1);
          *local_2c[0] = *local_2c[0] + 1;
          DataMemoryBarrier(0xf);
        }
        if (piVar3 != (int *)0x0) {
          if (*piVar3 == 2) {
            _ZNK6glitch5video9CMaterial23removeFromRootSceneNodeEv(piVar3);
          }
          DataMemoryBarrier(0xf);
          do {
            iVar5 = *piVar3;
            bVar1 = (bool)hasExclusiveAccess(piVar3);
          } while (!bVar1);
          *piVar3 = iVar5 + -1;
          DataMemoryBarrier(0xf);
          if (iVar5 + -1 == 0) {
            _ZN6glitch5video9CMaterialD1Ev(piVar3);
            _Z10GlitchFreePv(piVar3);
          }
        }
        piVar3 = local_2c[0];
        if (local_2c[0] != (int *)0x0) {
          if (*local_2c[0] == 2) {
            _ZNK6glitch5video9CMaterial23removeFromRootSceneNodeEv(local_2c[0]);
          }
          DataMemoryBarrier(0xf);
          do {
            iVar5 = *piVar3;
            bVar1 = (bool)hasExclusiveAccess(piVar3);
          } while (!bVar1);
          *piVar3 = iVar5 + -1;
          DataMemoryBarrier(0xf);
          if (iVar5 + -1 == 0) {
            _ZN6glitch5video9CMaterialD1Ev(piVar3);
            _Z10GlitchFreePv(piVar3);
          }
        }
        iVar5 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(piVar2[1],iVar9,0);
        if ((((iVar5 != 0xffff) ||
             (iVar5 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(piVar2[1],iVar6,0),
             iVar5 != 0xffff)) ||
            (iVar5 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(piVar2[1],iVar7,0),
            iVar5 != 0xffff)) &&
           (_ZNK6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12getParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRSE_
                      (piVar2,iVar5,0,&local_30), local_30 == local_38)) {
          _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
                    (piVar2,iVar5,0,&local_34);
        }
        if (local_30 != (int *)0x0) {
          piVar3 = local_30 + 1;
          DataMemoryBarrier(0xf);
          do {
            iVar5 = *piVar3 + -1;
            bVar1 = (bool)hasExclusiveAccess(piVar3);
          } while (!bVar1);
          *piVar3 = iVar5;
          DataMemoryBarrier(0xf);
          if (iVar5 == 0) {
            (**(code **)(*local_30 + 4))();
          }
          else if (iVar5 == 1) {
            _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
          }
        }
        if (iVar4 == iVar8 + 1) break;
        iVar8 = iVar8 + 1;
        piVar3 = piVar2;
      }
      if (*piVar2 == 2) {
        _ZNK6glitch5video9CMaterial23removeFromRootSceneNodeEv(piVar2);
      }
      DataMemoryBarrier(0xf);
      do {
        iVar4 = *piVar2;
        bVar1 = (bool)hasExclusiveAccess(piVar2);
      } while (!bVar1);
      *piVar2 = iVar4 + -1;
      DataMemoryBarrier(0xf);
      if (iVar4 + -1 == 0) {
        _ZN6glitch5video9CMaterialD1Ev(piVar2);
        _Z10GlitchFreePv(piVar2);
      }
    }
    if (local_34 != (int *)0x0) {
      piVar3 = local_34 + 1;
      DataMemoryBarrier(0xf);
      do {
        iVar4 = *piVar3 + -1;
        bVar1 = (bool)hasExclusiveAccess(piVar3);
      } while (!bVar1);
      *piVar3 = iVar4;
      DataMemoryBarrier(0xf);
      if (iVar4 == 0) {
        (**(code **)(*local_34 + 4))();
      }
      else if (iVar4 == 1) {
        _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
      }
    }
    if (local_38 != (int *)0x0) {
      piVar3 = local_38 + 1;
      DataMemoryBarrier(0xf);
      do {
        iVar4 = *piVar3 + -1;
        bVar1 = (bool)hasExclusiveAccess(piVar3);
      } while (!bVar1);
      *piVar3 = iVar4;
      DataMemoryBarrier(0xf);
      if (iVar4 == 0) {
        (**(code **)(*local_38 + 4))();
      }
      else if (iVar4 == 1) {
        _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
      }
    }
  }
  return;
}

