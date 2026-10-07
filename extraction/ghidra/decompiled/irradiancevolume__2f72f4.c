// _ZThn52_N25CTemplateIrradianceVolumeD1Ev @ 002f72f4

int * _ZThn52_N25CTemplateIrradianceVolumeD1Ev(int *param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = param_1 + -0xd;
  iVar3 = DAT_002f7350 + 0x2f7328;
  iVar2 = DAT_002f7354 + 0x2f7330;
  *piVar1 = DAT_002f734c + 0x2f7324;
  param_1[3] = iVar3;
  *param_1 = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 1);
  *param_1 = iVar3;
  *piVar1 = iVar3;
  return piVar1;
}


