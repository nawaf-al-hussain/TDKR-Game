// _ZNK6glitch7collada20CAnimationDictionary18getAnimationClipIDEPKc @ 0076d6d8

int _ZNK6glitch7collada20CAnimationDictionary18getAnimationClipIDEPKc(int *param_1)

{
  int iVar1;
  
  iVar1 = (**(code **)(*param_1 + 8))();
  if (iVar1 == -1) {
    iVar1 = 0;
  }
  else {
    iVar1 = param_1[9] + iVar1 * 8;
  }
  return iVar1;
}


