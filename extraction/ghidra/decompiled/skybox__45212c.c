// _ZN22CCustomSkyBoxSceneNodeC1EPKci @ 0045212c

int * _ZN22CCustomSkyBoxSceneNodeC1EPKci(int *param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 *puVar1;
  void *pvVar2;
  int *piVar3;
  undefined4 *puVar4;
  int *piVar5;
  undefined4 *puVar6;
  int iVar7;
  code *pcVar8;
  int iVar9;
  void *pvVar10;
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
  
  iVar9 = DAT_0045263c;
  iVar7 = DAT_00452638;
  param_1[0x47] = 0;
  param_1[0x45] = iVar7 + 0x452158;
  param_1[0x46] = iVar7 + 0x452178;
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
            (param_1,iVar9 + 0x452158,param_3,&local_54,&local_30,&local_48);
  iVar7 = DAT_00452640;
  param_1[0x42] = 0;
  *param_1 = iVar7 + 0x4521d8;
  param_1[0x45] = iVar7 + 0x452304;
  param_1[0x46] = iVar7 + 0x452324;
  param_1[0x43] = 0;
  _ZN6glitch5scene10ISceneNode19setAutomaticCullingEPKvNS0_14E_CULLING_TYPEE(param_1,0,0);
  _Z21ConstructColladaScenePKc(&local_78,param_2);
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
  puVar4 = *(undefined4 **)(DAT_00452644 + 0x45225c);
  if (*(int *)*puVar4 == 1) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (&local_70,param_2);
    iVar7 = local_70;
    iVar9 = *(int *)(local_70 + -0xc);
    if (iVar9 != 0) {
      pvVar10 = (void *)(DAT_00452658 + 0x452604);
      do {
        iVar9 = iVar9 + -1;
        pvVar2 = memchr(pvVar10,(int)*(char *)(iVar7 + iVar9),1);
        if (pvVar2 != (void *)0x0) goto LAB_004524b4;
      } while (iVar9 != 0);
    }
    iVar9 = -1;
LAB_004524b4:
    _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6substrEjj_constprop_2491
              (auStack_5c,&local_70,0,iVar9);
    if (*(int *)*puVar4 == 1) {
      iVar7 = (int)&DAT_00452638 + DAT_0045265c;
    }
    else {
      iVar7 = DAT_0045264c + 0x4524e4;
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_58,auStack_5c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (auStack_58,iVar7);
    iVar7 = *(int *)(local_70 + -0xc);
    if (iVar7 != 0) {
      pvVar10 = (void *)(DAT_00452654 + 0x4525cc);
      iVar9 = iVar7;
      do {
        iVar9 = iVar9 + -1;
        pvVar2 = memchr(pvVar10,(int)*(char *)(local_70 + iVar9),1);
        if (pvVar2 != (void *)0x0) goto LAB_0045250c;
      } while (iVar9 != 0);
    }
    iVar9 = -1;
LAB_0045250c:
    _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6substrEjj_constprop_2491
              (auStack_60,&local_70,iVar9,iVar7);
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
              (&local_64,local_6c,DAT_00452650 + 0x452564);
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
    if (piVar5 == (int *)0x0) goto LAB_00452268;
  }
  else {
LAB_00452268:
    _ZN6glitch7collada16CColladaDatabase17constructAnimatorEPKcPNS0_15CColladaFactoryE
              (&local_68,param_2,DAT_00452648 + 0x45227c);
    piVar5 = local_68;
    if (local_68 == (int *)0x0) goto LAB_004522d4;
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)local_68 + *(int *)(*local_68 + -0xc) + 4);
    if (local_68 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_68 + *(int *)(*local_68 + -0xc));
    }
    if (piVar5 == (int *)0x0) goto LAB_004522d4;
  }
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
            ((int)piVar5 + *(int *)(*piVar5 + -0xc) + 4);
LAB_004522d4:
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
    pcVar8 = *(code **)(*piVar3 + 0x90);
    if (local_74 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                ((int)local_74 + *(int *)(*local_74 + -0xc) + 4);
    }
    (*pcVar8)(piVar3,&local_74);
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

