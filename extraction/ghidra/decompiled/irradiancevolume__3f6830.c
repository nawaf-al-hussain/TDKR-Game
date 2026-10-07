// _ZN11Application30CreateIrradianceVolumeFilePathESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi @ 003f6830

undefined4
_ZN11Application30CreateIrradianceVolumeFilePathESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi
          (undefined4 param_1,uint *param_2,undefined4 param_3)

{
  char *__s;
  undefined4 uVar1;
  uint uVar2;
  void *__src;
  int iVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  size_t __n;
  void *__dest;
  bool bVar8;
  undefined1 auStack_30 [4];
  undefined1 auStack_2c [4];
  undefined1 auStack_28 [4];
  undefined1 auStack_24 [4];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_30);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (auStack_30,DAT_003f6ac8 + 0x3f685c);
  __s = (char *)_ZN6glitch4core18allocProcessBufferEi(0x11);
  snprintf(__s,0x10,(char *)(DAT_003f6acc + 0x3f6878),param_3);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (auStack_2c,__s);
  if (__s != (char *)0x0) {
    _ZN6glitch4core20releaseProcessBufferEPv(__s);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_28,auStack_30);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendERKS7_
            (auStack_28,auStack_2c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_24,auStack_28);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (auStack_24,DAT_003f6ad0 + 0x3f68cc);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (param_2,auStack_24);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_24);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_28);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_2c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_30);
  uVar4 = *param_2;
  uVar2 = *(uint *)(uVar4 - 0xc);
  if (uVar2 != 0) {
    iVar3 = uVar2 - 1;
    iVar6 = iVar3;
    do {
      if (*(char *)(uVar4 + iVar6) == '/') goto LAB_003f6950;
      bVar8 = iVar6 != 0;
      iVar6 = iVar6 + -1;
    } while (bVar8);
    iVar6 = -1;
LAB_003f6950:
    do {
      if (*(char *)(uVar4 + iVar3) == '\\') goto LAB_003f695c;
      bVar8 = iVar3 != 0;
      iVar3 = iVar3 + -1;
    } while (bVar8);
    iVar3 = -1;
LAB_003f695c:
    if (iVar3 < iVar6) {
      iVar3 = iVar6;
    }
    if (-1 < iVar3) {
      uVar7 = iVar3 + 1;
      if (uVar2 < uVar7) {
        _ZSt20__throw_out_of_rangePKc(DAT_003f6adc + 0x3f6abc);
      }
      else if (3 < 0x3ffffffc - uVar2) {
        uVar5 = DAT_003f6ad4 + 0x3f699c;
        if (((uVar5 < uVar4) || (uVar4 + uVar2 < uVar5)) || (0 < *(int *)(uVar4 - 4))) {
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
                    (param_2,uVar7,0,4);
          memcpy((void *)(*param_2 + uVar7),(void *)(DAT_003f6ad8 + 0x3f69e4),4);
        }
        else {
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
                    (param_2,uVar7,0,4);
          uVar2 = *param_2;
          __src = (void *)(uVar2 + (uVar5 - uVar4));
          __dest = (void *)(uVar2 + uVar7);
          if (__dest < (void *)((int)__src + 4)) {
            if (__src < __dest) {
              __n = (int)__dest - (int)__src;
              if (__n == 1) {
                *(undefined1 *)(uVar2 + uVar7) = *(undefined1 *)(uVar2 + (uVar5 - uVar4));
                memcpy((void *)((int)__dest + 1),(void *)((int)__dest + 4),3);
              }
              else {
                memcpy(__dest,__src,__n);
                if (4 - __n == 1) {
                  *(undefined1 *)((int)__dest + __n) = *(undefined1 *)((int)__dest + 4);
                }
                else {
                  memcpy((void *)((int)__dest + __n),(void *)((int)__dest + 4),4 - __n);
                }
              }
            }
            else {
              memcpy(__dest,(void *)((int)__src + 4),4);
            }
          }
          else {
            memcpy(__dest,__src,4);
          }
        }
        goto LAB_003f6910;
      }
      uVar1 = _ZSt20__throw_length_errorPKc((int)&DAT_003f6ac8 + DAT_003f6ae0);
      return uVar1;
    }
  }
LAB_003f6910:
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1,param_2);
  return param_1;
}


