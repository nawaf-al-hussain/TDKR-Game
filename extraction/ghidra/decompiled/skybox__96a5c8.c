// _ZNK6glitch5scene16CSkyBoxSceneNode5cloneEv @ 0096a5c8

int * _ZNK6glitch5scene16CSkyBoxSceneNode5cloneEv(int *param_1,int param_2)

{
  bool bVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  undefined4 uVar5;
  int *local_34;
  int *local_30;
  int *local_2c;
  int *local_28;
  int *local_24;
  int *local_20;
  int local_1c [2];
  
  uVar5 = *(undefined4 *)(*(int *)(param_2 + 0xe8) + 0x10);
  local_34 = (int *)0x0;
  local_30 = (int *)0x0;
  local_2c = (int *)0x0;
  local_28 = (int *)0x0;
  local_24 = (int *)0x0;
  local_20 = (int *)0x0;
  piVar2 = (int *)_Znwj(0x150);
  _ZN6glitch5scene16CSkyBoxSceneNodeC1EPNS_5video12IVideoDriverERKN5boost13intrusive_ptrINS2_8ITextureEEESA_SA_SA_SA_SA_i_constprop_1157
            (piVar2,uVar5,&local_34,&local_30,&local_2c,&local_28,&local_24,&local_20,
             *(undefined4 *)(param_2 + 0xe4));
  if (local_20 != (int *)0x0) {
    piVar4 = local_20 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_20 + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_24 != (int *)0x0) {
    piVar4 = local_24 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_24 + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_28 != (int *)0x0) {
    piVar4 = local_28 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_28 + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_2c != (int *)0x0) {
    piVar4 = local_2c + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_2c + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_30 != (int *)0x0) {
    piVar4 = local_30 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_30 + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_34 != (int *)0x0) {
    piVar4 = local_34 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3;
    DataMemoryBarrier(0xf);
    if (iVar3 == 0) {
      (**(code **)(*local_34 + 4))();
    }
    else if (iVar3 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  *param_1 = (int)piVar2;
  if (piVar2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar2 + *(int *)(*piVar2 + -0x10) + 4);
  }
  _ZN6glitch5scene10ISceneNode12cloneMembersEPKS1_(piVar2,param_2);
  local_1c[0] = *(int *)(param_2 + 0x124);
  if (local_1c[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar3 = piVar2[0x49];
  piVar2[0x49] = local_1c[0];
  local_1c[0] = iVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_1c);
  local_1c[0] = *(int *)(param_2 + 0x128);
  if (local_1c[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar3 = piVar2[0x4a];
  piVar2[0x4a] = local_1c[0];
  local_1c[0] = iVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_1c);
  local_1c[0] = *(int *)(param_2 + 300);
  if (local_1c[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar3 = piVar2[0x4b];
  piVar2[0x4b] = local_1c[0];
  local_1c[0] = iVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_1c);
  local_1c[0] = *(int *)(param_2 + 0x130);
  if (local_1c[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar3 = piVar2[0x4c];
  piVar2[0x4c] = local_1c[0];
  local_1c[0] = iVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_1c);
  local_1c[0] = *(int *)(param_2 + 0x134);
  if (local_1c[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar3 = piVar2[0x4d];
  piVar2[0x4d] = local_1c[0];
  local_1c[0] = iVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_1c);
  local_1c[0] = *(int *)(param_2 + 0x138);
  if (local_1c[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar3 = piVar2[0x4e];
  piVar2[0x4e] = local_1c[0];
  local_1c[0] = iVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_1c);
  return param_1;
}

