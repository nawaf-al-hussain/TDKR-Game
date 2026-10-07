// _ZNK19CComponentLevelInit3NewEv @ 002114a0

int * _ZNK19CComponentLevelInit3NewEv(void)

{
  int *__s;
  int iVar1;
  
  __s = (int *)_Znwj(0xa4);
  memset(__s,0,0xa4);
  iVar1 = *(int *)(DAT_00211500 + 0x2114d4) + 0xc;
  *__s = DAT_002114fc + 0x2114d8;
  __s[1] = iVar1;
  __s[2] = iVar1;
  __s[3] = iVar1;
  __s[4] = iVar1;
  __s[5] = iVar1;
  __s[6] = iVar1;
  __s[8] = iVar1;
  __s[0xd] = iVar1;
  return __s;
}


