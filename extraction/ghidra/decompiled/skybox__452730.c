// _ZN22CCustomSkyBoxSceneNodeD1Ev @ 00452730

int * _ZN22CCustomSkyBoxSceneNodeD1Ev(int *param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  
  iVar3 = DAT_00452800;
  *param_1 = DAT_00452800 + 0x452758;
  iVar1 = *(int *)param_1[0x42];
  param_1[0x45] = iVar3 + 0x452884;
  param_1[0x46] = iVar3 + 0x4528a4;
  (**(code **)(iVar1 + 0x84))();
  piVar2 = (int *)param_1[0x42];
  param_1[0x42] = 0;
  if (piVar2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar2 + *(int *)(*piVar2 + -0x10));
  }
  piVar2 = (int *)param_1[0x43];
  if (piVar2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar2 + *(int *)(*piVar2 + -0xc));
  }
  piVar2 = (int *)param_1[0x42];
  if (piVar2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar2 + *(int *)(*piVar2 + -0x10));
  }
  _ZN6glitch5scene10ISceneNodeD2Ev(param_1,DAT_00452804 + 0x4527d8);
  iVar3 = DAT_0045280c + 0x4527f8;
  param_1[0x45] = DAT_00452808 + 0x4527f8;
  param_1[0x46] = iVar3;
  return param_1;
}

