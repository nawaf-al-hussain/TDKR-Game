// _ZN20CPortalVisibilityMgr8SaveLoadEP13CMemoryStream @ 002c56ac

void _ZN20CPortalVisibilityMgr8SaveLoadEP13CMemoryStream(undefined4 *param_1,undefined4 param_2)

{
  int *piVar1;
  undefined1 auStack_12 [2];
  
  _ZN13CMemoryStream4ReadERt(param_2,auStack_12);
  for (piVar1 = (int *)*param_1; (int *)param_1[1] != piVar1; piVar1 = piVar1 + 1) {
    _ZN13CMemoryStream4ReadERb(param_2,*piVar1 + 8);
  }
  return;
}


