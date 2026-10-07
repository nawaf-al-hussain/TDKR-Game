// _ZN22CCustomSkyBoxSceneNode27onRegisterSceneNodeInternalEPKv @ 00452af4

undefined4 _ZN22CCustomSkyBoxSceneNode27onRegisterSceneNodeInternalEPKv(int param_1)

{
  bool bVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  int iVar8;
  int *piVar9;
  undefined4 *puVar10;
  int *local_40;
  undefined1 auStack_3c [4];
  int *local_38;
  undefined4 *local_34;
  undefined4 *local_30;
  undefined4 local_2c;
  undefined4 *puVar11;
  
  local_34 = (undefined4 *)0x0;
  local_30 = (undefined4 *)0x0;
  local_2c = 0;
  _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
            (*(undefined4 *)(param_1 + 0x108),0x6d656164,&local_34);
  puVar4 = local_30;
  puVar10 = local_34;
  if (local_34 != local_30) {
    do {
      while( true ) {
        puVar11 = puVar10 + 1;
        piVar9 = (int *)*puVar10;
        puVar10 = puVar11;
        if (((piVar9[0x3d] & 0x18U) == 0x18) && ((*(uint *)(piVar9[0x34] + 0xf4) & 0x18) == 0x18))
        break;
LAB_00452b40:
        puVar2 = local_34;
        puVar3 = local_30;
        if (puVar4 == puVar11) goto joined_r0x00452c54;
      }
      (**(code **)(*piVar9 + 0x118))(&local_40,piVar9);
      iVar5 = (**(code **)(*local_40 + 0x10))();
      if (local_40 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      if (iVar5 < 1) goto LAB_00452b40;
      iVar7 = 0;
      do {
        (**(code **)(*piVar9 + 0x118))(&local_38,piVar9);
        iVar8 = iVar7 + 1;
        (**(code **)(*local_38 + 0x18))(auStack_3c,local_38,iVar7);
        if (local_38 != (int *)0x0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        }
        piVar6 = *(int **)(*(int *)(param_1 + 0xe8) + 0x2c);
        (**(code **)(*piVar6 + 8))(piVar6,piVar9,0,auStack_3c,iVar8,2,0,0x7fffffff);
        _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(auStack_3c);
        iVar7 = iVar8;
      } while (iVar5 != iVar8);
      puVar2 = local_34;
      puVar3 = local_30;
    } while (puVar4 != puVar11);
joined_r0x00452c54:
    while (puVar4 = local_30, bVar1 = puVar2 != local_30, local_30 = puVar3, bVar1) {
      puVar10 = puVar2 + 1;
      piVar9 = (int *)*puVar2;
      puVar2 = puVar10;
      local_30 = puVar4;
      if (piVar9 != (int *)0x0) {
        local_30 = puVar3;
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                  ((int)piVar9 + *(int *)(*piVar9 + -0x10));
        puVar3 = local_30;
        local_30 = puVar4;
      }
    }
  }
  if (local_34 != (undefined4 *)0x0) {
    free(local_34);
  }
  return 0;
}

