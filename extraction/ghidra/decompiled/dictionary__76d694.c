// _ZNK6glitch7collada20CAnimationDictionary12getClipIndexEPKc @ 0076d694

int _ZNK6glitch7collada20CAnimationDictionary12getClipIndexEPKc(int param_1)

{
  int iVar1;
  
  iVar1 = _ZNK6glitch7collada20CAnimationDictionary7getClipEPKc();
  if (iVar1 != 0) {
    return (iVar1 - *(int *)(*(int *)(param_1 + 0x1c) + 0xc) >> 2) * -0x55555555;
  }
  return -1;
}


