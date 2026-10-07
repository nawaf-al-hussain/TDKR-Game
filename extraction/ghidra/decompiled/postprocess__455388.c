// _ZN18CPostProcessEffect6RenderEi @ 00455388

void _ZN18CPostProcessEffect6RenderEi(int *param_1,int param_2)

{
  bool bVar1;
  int *__ptr;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  code *pcVar7;
  int *piVar8;
  int *piVar9;
  byte bVar10;
  uint uVar11;
  int local_50;
  int *local_4c;
  int *local_48;
  int local_44;
  int local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 uStack_34;
  int local_30 [5];
  char *local_1c;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  iVar4 = *(int *)(param_1[0xe] + 0x14);
  piVar8 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
  if (((param_2 < *(int *)(param_1[0xe] + 0x18) - iVar4 >> 2) && (-1 < param_2)) &&
     (iVar2 = *(int *)(iVar4 + param_2 * 4), iVar2 != 0)) {
    (**(code **)(*piVar8 + 0x18))(piVar8);
    iVar4 = param_1[0xd];
    uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(iVar4 + 4),DAT_00455660 + 0x455400,0);
    local_50 = *(int *)(iVar2 + 4);
    if (local_50 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_50 + 4);
    }
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (iVar4,uVar3,0,&local_50);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_50);
    (**(code **)(*param_1 + 0x2c))(param_1);
    local_4c = (int *)0x0;
    _ZN6glitch5video12IVideoDriver11setMaterialERKN5boost13intrusive_ptrINS0_9CMaterialEEERKNS3_IKNS0_27CMaterialVertexAttributeMapEEE
              (piVar8,param_1 + 0xd);
    piVar9 = local_4c;
    if (local_4c != (int *)0x0) {
      DataMemoryBarrier(0xf);
      do {
        iVar4 = *local_4c;
        bVar1 = (bool)hasExclusiveAccess(local_4c);
      } while (!bVar1);
      *local_4c = iVar4 + -1;
      DataMemoryBarrier(0xf);
      if (iVar4 + -1 == 0) {
        _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(local_4c);
        free(piVar9);
      }
    }
    local_38 = *(undefined4 *)(iVar2 + 0x18);
    uStack_34 = *(undefined4 *)(iVar2 + 0x1c);
    iVar2 = *(int *)(piVar8[0x48] + -4);
    local_40 = *(int *)(iVar2 + 0x1c) - *(int *)(iVar2 + 0x14);
    local_3c = *(int *)(iVar2 + 0x20) - *(int *)(iVar2 + 0x18);
    _ZN19CPostProcessManager18UpdateVertexBufferERKN6glitch4core11dimension2dIiEES5_S5__constprop_2530
              (param_1[0xe],&local_38,&local_40);
    piVar9 = *(int **)(param_1[0xe] + 0x54);
    uVar11 = (piVar8[2] & 0x1fffffU) >> 0x14;
    piVar8[2] = piVar8[2] & 0xffefffff;
    *(byte *)((int)piVar8 + 0x291) = (byte)uVar11 | *(byte *)((int)piVar8 + 0x291);
    local_48 = piVar9;
    if (piVar9 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar9);
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar9);
    }
    local_30[2] = 4;
    local_30[4] = 4;
    local_1c = "ivdi3";
    local_30[0] = 0;
    local_30[1] = 0;
    local_30[3] = 0;
    local_44 = 0;
    (**(code **)(*piVar8 + 0x3c))(piVar8,&local_48,local_30,0,&local_44);
    if (local_44 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_30[0] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    __ptr = local_48;
    if (local_48 != (int *)0x0) {
      DataMemoryBarrier(0xf);
      do {
        iVar2 = *local_48;
        bVar1 = (bool)hasExclusiveAccess(local_48);
      } while (!bVar1);
      *local_48 = iVar2 + -1;
      DataMemoryBarrier(0xf);
      if (iVar2 + -1 == 0) {
        _ZN6glitch5video14CVertexStreamsD1Ev(local_48);
        free(__ptr);
      }
    }
    if (piVar9 != (int *)0x0) {
      DataMemoryBarrier(0xf);
      do {
        iVar2 = *piVar9;
        bVar1 = (bool)hasExclusiveAccess(piVar9);
      } while (!bVar1);
      *piVar9 = iVar2 + -1;
      DataMemoryBarrier(0xf);
      if (iVar2 + -1 == 0) {
        _ZN6glitch5video14CVertexStreamsD1Ev(piVar9);
        free(piVar9);
      }
    }
    uVar5 = piVar8[2];
    bVar10 = *(byte *)((int)piVar8 + 0x291);
    if (uVar11 == 0) {
      uVar6 = uVar5 & 0xffefffff;
    }
    else {
      uVar6 = uVar5 | 0x100000;
    }
    piVar8[2] = uVar6;
    if (uVar11 != (uVar5 & 0x1fffff) >> 0x14) {
      bVar10 = bVar10 | 1;
    }
    pcVar7 = *(code **)(*piVar8 + 0x1c);
    *(byte *)((int)piVar8 + 0x291) = bVar10;
    (*pcVar7)(piVar8);
  }
  return;
}


