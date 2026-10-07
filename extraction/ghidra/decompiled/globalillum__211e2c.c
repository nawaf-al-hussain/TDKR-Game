// _ZNK25CComponentBaseGlobalIllum3NewEv @ 00211e2c

int * _ZNK25CComponentBaseGlobalIllum3NewEv(void)

{
  int *__s;
  int iVar1;
  
  __s = (int *)_Znwj(0x70);
  memset(__s,0,0x70);
  iVar1 = *(int *)(DAT_00211e80 + 0x211e60) + 0xc;
  *__s = DAT_00211e7c + 0x211e64;
  __s[0xd] = iVar1;
  __s[0xe] = iVar1;
  __s[0xf] = iVar1;
  __s[0x14] = iVar1;
  return __s;
}


