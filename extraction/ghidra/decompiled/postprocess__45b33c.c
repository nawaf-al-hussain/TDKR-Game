// _ZN32CPostProcessEffect_CC_RadialBlur5ApplyEv @ 0045b33c

undefined4 _ZN32CPostProcessEffect_CC_RadialBlur5ApplyEv(int param_1)

{
  int iVar1;
  int iVar2;
  float *pfVar3;
  float fVar4;
  
  iVar1 = *(int *)(param_1 + 0x34);
  if ((uint)*(ushort *)(param_1 + 0x4a) < (uint)*(ushort *)(*(int *)(iVar1 + 4) + 0xe)) {
    iVar2 = *(int *)(*(int *)(iVar1 + 4) + 0x20) + (uint)*(ushort *)(param_1 + 0x4a) * 0x10;
    if (iVar2 == 0) {
      return 0;
    }
    if ((*(char *)(iVar2 + 9) == '\x05') && (*(short *)(iVar2 + 0xc) != 0)) {
      fVar4 = *(float *)(*(int *)(*(int *)(*(int *)(param_1 + 0x38) + 8) + 0x10) + 0x54);
      pfVar3 = (float *)(iVar1 + 0x30 + *(int *)(iVar2 + 4));
      if (*pfVar3 != fVar4) {
        *(undefined4 *)(iVar1 + 0x14) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0x18) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0xc) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0x10) = 0xffffffff;
      }
      *pfVar3 = fVar4;
      return 1;
    }
  }
  return 0;
}


