// _ZN22CCustomSkyBoxSceneNodeC2EPKci @ 00451c20

int * _ZN22CCustomSkyBoxSceneNodeC2EPKci
                (int *param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 *puVar1;
  void *pvVar2;
  int *piVar3;
  undefined4 *puVar4;
  int *piVar5;
  undefined4 *puVar6;
  code *pcVar7;
  void *pvVar8;
  int iVar9;
  int iVar10;
  int *local_78;
  int *local_74;
  int local_70;
  undefined4 local_6c;
  int *local_68;
  int *local_64;
  undefined1 auStack_60 [4];
  undefined1 auStack_5c [4];
  undefined1 auStack_58 [4];
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 *local_3c;
  undefined4 *local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  local_54 = 0;
  local_50 = 0;
  local_4c = 0;
  local_30 = 0;
  local_2c = 0;
  local_28 = 0;
  local_24 = 0x3f800000;
  local_48 = 0x3f800000;
  local_44 = 0x3f800000;
  local_40 = 0x3f800000;
  _ZN6glitch5scene10ISceneNodeC2EiRKNS_4core8vector3dIfEERKNS2_10quaternionES6_
            (param_1,param_2 + 1,param_4,&local_54,&local_30,&local_48);
  iVar9 = *param_2;
  iVar10 = *(int *)(iVar9 + -0xc);
  *param_1 = iVar9;
  iVar9 = *(int *)(iVar9 + -0x10);
  *(int *)((int)param_1 + iVar10) = param_2[4];
  *(int *)((int)param_1 + iVar9) = param_2[5];
  param_1[0x42] = 0;
  param_1[0x43] = 0;
  _ZN6glitch5scene10ISceneNode19setAutomaticCullingEPKvNS0_14E_CULLING_TYPEE(param_1,0,0);
  _Z21ConstructColladaScenePKc(&local_78,param_3);
  piVar5 = local_78;
  if (local_78 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)local_78 + *(int *)(*local_78 + -0x10) + 4);
  }
  piVar3 = (int *)param_1[0x42];
  param_1[0x42] = (int)piVar5;
  if (piVar3 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar3 + *(int *)(*piVar3 + -0x10));
  }
  if (local_78 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)local_78 + *(int *)(*local_78 + -0x10));
  }
  puVar4 = *(undefined4 **)(DAT_00452110 + 0x451d34);
  if (*(int *)*puVar4 == 1) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (&local_70,param_3);
    iVar9 = local_70;
    iVar10 = *(int *)(local_70 + -0xc);
    if (iVar10 != 0) {
      pvVar8 = (void *)(DAT_00452124 + 0x4520dc);
      do {
        iVar10 = iVar10 + -1;
        pvVar2 = memchr(pvVar8,(int)*(char *)(iVar9 + iVar10),1);
        if (pvVar2 != (void *)0x0) goto LAB_00451f8c;
      } while (iVar10 != 0);
    }
    iVar10 = -1;
LAB_00451f8c:
    _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6substrEjj_constprop_2491
              (auStack_5c,&local_70,0,iVar10);
    if (*(int *)*puVar4 == 1) {
      iVar9 = (int)&DAT_00452110 + DAT_00452128;
    }
    else {
      iVar9 = DAT_00452118 + 0x451fbc;
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_58,auStack_5c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (auStack_58,iVar9);
    iVar9 = *(int *)(local_70 + -0xc);
    if (iVar9 != 0) {
      pvVar8 = (void *)(DAT_00452120 + 0x4520a4);
      iVar10 = iVar9;
      do {
        iVar10 = iVar10 + -1;
        pvVar2 = memchr(pvVar8,(int)*(char *)(local_70 + iVar10),1);
        if (pvVar2 != (void *)0x0) goto LAB_00451fe4;
      } while (iVar10 != 0);
    }
    iVar10 = -1;
LAB_00451fe4:
    _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6substrEjj_constprop_2491
              (auStack_60,&local_70,iVar10,iVar9);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (&local_6c,auStack_58);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendERKS7_
              (&local_6c,auStack_60);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_60);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_58);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_5c);
    _ZN6glitch7collada16CColladaDatabase17constructAnimatorEPKcPNS0_15CColladaFactoryE
              (&local_64,local_6c,DAT_0045211c + 0x45203c);
    piVar5 = local_64;
    if ((local_64 != (int *)0x0) &&
       (_ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                  ((int)local_64 + *(int *)(*local_64 + -0xc) + 4), local_64 != (int *)0x0)) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_64 + *(int *)(*local_64 + -0xc));
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (&local_6c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (&local_70);
    if (piVar5 == (int *)0x0) goto LAB_00451d40;
  }
  else {
LAB_00451d40:
    _ZN6glitch7collada16CColladaDatabase17constructAnimatorEPKcPNS0_15CColladaFactoryE
              (&local_68,param_3,DAT_00452114 + 0x451d54);
    piVar5 = local_68;
    if (local_68 == (int *)0x0) goto LAB_00451dac;
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)local_68 + *(int *)(*local_68 + -0xc) + 4);
    if (local_68 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_68 + *(int *)(*local_68 + -0xc));
    }
    if (piVar5 == (int *)0x0) goto LAB_00451dac;
  }
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
            ((int)piVar5 + *(int *)(*piVar5 + -0xc) + 4);
LAB_00451dac:
  piVar3 = (int *)param_1[0x43];
  param_1[0x43] = (int)piVar5;
  if (piVar3 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar3 + *(int *)(*piVar3 + -0xc));
  }
  if (piVar5 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar5 + *(int *)(*piVar5 + -0xc));
  }
  if ((int *)param_1[0x43] != (int *)0x0) {
    puVar4 = (undefined4 *)(**(code **)(*(int *)param_1[0x43] + 0x44))();
    piVar5 = (int *)*puVar4;
    if (piVar5 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                ((int)piVar5 + *(int *)(*piVar5 + -0xc) + 4);
      (**(code **)(*piVar5 + 0x44))(piVar5,1);
    }
    (**(code **)(*(int *)param_1[0x42] + 0x98))();
    piVar3 = (int *)param_1[0x42];
    local_74 = (int *)param_1[0x43];
    pcVar7 = *(code **)(*piVar3 + 0x90);
    if (local_74 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                ((int)local_74 + *(int *)(*local_74 + -0xc) + 4);
    }
    (*pcVar7)(piVar3,&local_74);
    if (local_74 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_74 + *(int *)(*local_74 + -0xc));
    }
    if (piVar5 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar5 + *(int *)(*piVar5 + -0xc));
    }
  }
  local_3c = (undefined4 *)0x0;
  local_38 = (undefined4 *)0x0;
  local_34 = 0;
  _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
            (param_1[0x42],0x6d656164,&local_3c);
  puVar1 = local_38;
  for (puVar4 = local_3c; puVar4 != puVar1; puVar4 = puVar4 + 1) {
    (**(code **)(*(int *)*puVar4 + 0xbc))((int *)*puVar4,0,0);
  }
  _ZN6glitch5scene10ISceneNode8addChildERKN5boost13intrusive_ptrIS1_EE(param_1,param_1 + 0x42);
  puVar1 = local_38;
  param_1[0x44] = 0;
  puVar4 = local_3c;
  while (puVar4 != puVar1) {
    puVar6 = puVar4 + 1;
    piVar5 = (int *)*puVar4;
    puVar4 = puVar6;
    if (piVar5 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar5 + *(int *)(*piVar5 + -0x10));
    }
  }
  if (local_3c != (undefined4 *)0x0) {
    free(local_3c);
  }
  return param_1;
}

