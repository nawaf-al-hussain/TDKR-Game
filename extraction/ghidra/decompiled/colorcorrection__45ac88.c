// _ZN34CPostProcessEffect_ColorCorrection6UpdateEf @ 0045ac88

void _ZN34CPostProcessEffect_ColorCorrection6UpdateEf(int *param_1,float param_2)

{
  int iVar1;
  code *pcVar2;
  float fVar3;
  
  iVar1 = param_1[0x10];
  if (iVar1 == 1) {
    if (((float)param_1[3] < DAT_0045ae44) || (DAT_0045ae48 < (float)param_1[3])) {
      pcVar2 = *(code **)(*param_1 + 0x18);
      param_1[0x11] = (int)((float)param_1[0x11] + param_2);
      (*pcVar2)(param_1);
      if ((float)param_1[0x11] < (float)param_1[3]) {
        return;
      }
    }
    param_1[0x10] = 3;
    param_1[0x11] = 0;
    *(char *)(param_1 + 0xc) = (char)param_1[0x16];
  }
  else if (iVar1 == 2) {
    fVar3 = (float)param_1[1];
    if ((fVar3 < DAT_0045ae44) || (DAT_0045ae48 < fVar3)) {
      if ((float)param_1[0x11] < fVar3) {
        param_1[0x11] = (int)(param_2 + (float)param_1[0x11]);
      }
      else {
        param_1[0x10] = 1;
        param_1[0x11] = 0;
      }
    }
    else {
      iVar1 = param_1[0x15];
      if (iVar1 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
      }
      param_1[0x14] = iVar1;
      _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
      iVar1 = param_1[0xe];
      param_1[0x13] = 0;
      param_1[0x11] = 0;
      param_1[0x10] = 3;
      *(undefined4 *)(iVar1 + 0x5c) = 0xbf800000;
      *(undefined4 *)(iVar1 + 0x60) = 0xbf800000;
    }
  }
  else if (iVar1 == 0) {
    if (((float)param_1[2] < DAT_0045ae44) || (DAT_0045ae48 < (float)param_1[2])) {
      pcVar2 = *(code **)(*param_1 + 0x14);
      param_1[0x11] = (int)((float)param_1[0x11] + param_2);
      (*pcVar2)(param_1);
      if ((float)param_1[0x11] < (float)param_1[2]) {
        return;
      }
    }
    param_1[0x10] = 2;
    param_1[0x11] = 0;
  }
  return;
}


