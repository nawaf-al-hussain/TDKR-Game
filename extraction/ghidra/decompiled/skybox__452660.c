// _ZN22CCustomSkyBoxSceneNodeD2Ev @ 00452660

int * _ZN22CCustomSkyBoxSceneNodeD2Ev(int *param_1,int *param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  
  iVar3 = *param_2;
  piVar2 = (int *)param_1[0x42];
  *param_1 = iVar3;
  iVar1 = *(int *)(iVar3 + -0x10);
  iVar4 = *piVar2;
  *(int *)((int)param_1 + *(int *)(iVar3 + -0xc)) = param_2[4];
  *(int *)((int)param_1 + iVar1) = param_2[5];
  (**(code **)(iVar4 + 0x84))(piVar2);
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
  _ZN6glitch5scene10ISceneNodeD2Ev(param_1,param_2 + 1);
  return param_1;
}

