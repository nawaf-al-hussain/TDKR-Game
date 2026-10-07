// _ZN6glitch5scene16CSkyBoxSceneNodeD1Ev @ 0099adb4

int * _ZN6glitch5scene16CSkyBoxSceneNodeD1Ev(int *param_1)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  
  iVar3 = DAT_0099aec4;
  piVar4 = (int *)param_1[0x4f];
  iVar2 = DAT_0099aec4 + 0x99af0c;
  *param_1 = DAT_0099aec4 + 0x99ade0;
  param_1[0x51] = iVar2;
  param_1[0x52] = iVar3 + 0x99af2c;
  if (piVar4 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3 + -1;
    DataMemoryBarrier(0xf);
    if (iVar3 + -1 == 0) {
      _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(piVar4);
      _Z10GlitchFreePv(piVar4);
    }
  }
  piVar4 = param_1 + 0x4f;
  do {
    piVar4 = piVar4 + -1;
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar4);
  } while (param_1 + 0x49 != piVar4);
  piVar4 = (int *)param_1[0x48];
  if (piVar4 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *piVar4;
      bVar1 = (bool)hasExclusiveAccess(piVar4);
    } while (!bVar1);
    *piVar4 = iVar3 + -1;
    DataMemoryBarrier(0xf);
    if (iVar3 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(piVar4);
      _Z10GlitchFreePv(piVar4);
    }
  }
  _ZN6glitch5scene10ISceneNodeD2Ev(param_1,DAT_0099aec8 + 0x99ae74);
  iVar3 = DAT_0099aed0 + 0x99ae94;
  param_1[0x51] = DAT_0099aecc + 0x99ae94;
  param_1[0x52] = iVar3;
  return param_1;
}

