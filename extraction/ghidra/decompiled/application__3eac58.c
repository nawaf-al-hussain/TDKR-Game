// _ZN11Application11GetInstanceEv @ 003eac58

int _ZN11Application11GetInstanceEv(void)

{
  int *piVar1;
  int iVar2;
  
  piVar1 = (int *)(DAT_003eac98 + 0x3eac68);
  iVar2 = *piVar1;
  if (iVar2 != 0) {
    return iVar2;
  }
  iVar2 = _Znwj(0x12030);
  _ZN11ApplicationC1Ev();
  *piVar1 = iVar2;
  return iVar2;
}


