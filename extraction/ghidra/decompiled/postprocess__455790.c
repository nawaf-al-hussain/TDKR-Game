// _ZN18CPostProcessEffect4SaveEP13CMemoryStream @ 00455790

void _ZN18CPostProcessEffect4SaveEP13CMemoryStream
               (int param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  
  _ZN13CMemoryStream8WriteIntEi(param_2,*(undefined1 *)(param_1 + 0x30),param_3,param_4,param_4);
  _ZN13CMemoryStream8WriteIntEi(param_2,*(undefined4 *)(param_1 + 0x40));
  uVar2 = *(undefined4 *)(param_1 + 0x44);
  iVar1 = _ZN13CMemoryStream13AssureAddSizeEi(param_2,4);
  if (iVar1 == 0) {
    return;
  }
  iVar1 = param_2[3];
  *(char *)(*param_2 + iVar1) = (char)((uint)uVar2 >> 0x18);
  iVar3 = iVar1 + 4;
  *(char *)(*param_2 + iVar1 + 1) = (char)((uint)uVar2 >> 0x10);
  *(char *)(*param_2 + iVar1 + 2) = (char)((uint)uVar2 >> 8);
  *(char *)(*param_2 + iVar1 + 3) = (char)uVar2;
  param_2[3] = iVar3;
  if (param_2[2] < iVar3) {
    param_2[2] = iVar3;
  }
  return;
}


