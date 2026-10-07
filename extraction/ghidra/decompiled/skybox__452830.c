// _ZN22CCustomSkyBoxSceneNodeD0Ev @ 00452830

int * _ZN22CCustomSkyBoxSceneNodeD0Ev(int *param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  
  iVar3 = DAT_00452908;
  *param_1 = DAT_00452908 + 0x452858;
  iVar1 = *(int *)param_1[0x42];
  param_1[0x45] = iVar3 + 0x452984;
  param_1[0x46] = iVar3 + 0x4529a4;
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
  _ZN6glitch5scene10ISceneNodeD2Ev(param_1,DAT_0045290c + 0x4528d8);
  iVar3 = DAT_00452914 + 0x4528f8;
  param_1[0x45] = DAT_00452910 + 0x4528f8;
  param_1[0x46] = iVar3;
  _ZdlPv(param_1);
  return param_1;
}

