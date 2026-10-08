// _ZN5CZone20LoadIrradianceVolumeEP13CMemoryStream @ 002c95dc

void _ZN5CZone20LoadIrradianceVolumeEP13CMemoryStream(undefined4 param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined1 *puVar3;
  char *__s;
  void *pvVar4;
  int *piVar5;
  uint uVar6;
  undefined1 *puVar7;
  uint uVar8;
  int iVar9;
  undefined1 *puVar10;
  size_t __n;
  void *pvVar11;
  void *local_7c;
  undefined1 *local_78;
  undefined1 *local_74;
  int local_70;
  undefined1 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined1 local_40;
  undefined1 local_3f;
  undefined1 local_3e;
  int local_3c;
  undefined1 *local_38;
  undefined1 local_34;
  undefined1 local_33;
  undefined1 local_32;
  undefined1 local_31;
  int local_30;
  undefined1 local_2c;
  undefined4 local_28;
  undefined1 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  
  puVar7 = *(undefined1 **)(DAT_002c9c98 + 0x2c95fc);
  local_38 = puVar7 + 0xc;
  local_70 = DAT_002c9c9c + 0x2c960c;
  local_3c = DAT_002c9c9c + 0x2c9628;
  local_64 = 0;
  local_30 = DAT_002c9c9c + 0x2c9644;
  local_60 = 0;
  local_5c = 0;
  local_58 = 0;
  local_54 = 0;
  local_50 = 0;
  local_4c = 0;
  local_48 = 0;
  local_44 = 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_6c = iVar2 != 0;
  local_68 = _ZN13CMemoryStream7ReadIntEv(param_2);
  local_64 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_60 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_5c = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_58 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_54 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_50 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_4c = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_48 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_44 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_40 = iVar2 != 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_3f = iVar2 != 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_3e = iVar2 != 0;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_38);
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_34 = iVar2 != 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_33 = iVar2 != 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_32 = iVar2 != 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_31 = iVar2 != 0;
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_2c = iVar2 != 0;
  local_28 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  iVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  local_24 = iVar2 != 0;
  local_20 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_1c = _ZN13CMemoryStream9ReadFloatEv(param_2);
  iVar2 = *(int *)(**(int **)(DAT_002c9ca0 + 0x2c97b8) + 0x10);
  iVar9 = *(int *)(iVar2 + 0x29c);
  if (iVar9 == 0) {
    _ZNK6glitch5video12IVideoDriver28instantiateIrradianceManagerEv(iVar2);
    iVar9 = *(int *)(iVar2 + 0x29c);
  }
  _ZN6CLevel8GetLevelEv();
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (&local_78,*(undefined4 *)(DAT_002c9ca4 + 0x2c97e0));
  iVar2 = *(int *)(local_78 + -0xc);
  if (iVar2 == 0x3ffffffc) {
                    /* WARNING: Subroutine does not return */
    _ZSt20__throw_length_errorPKc(DAT_002c9cec + 0x2c9c8c);
  }
  uVar6 = *(uint *)(local_78 + -8);
  uVar8 = iVar2 + 1;
  if ((uVar6 < uVar8) || (0 < *(int *)(local_78 + -4))) {
    puVar10 = (undefined1 *)(DAT_002c9ca8 + 0x2c9818);
    if ((puVar10 < local_78) || (puVar3 = local_78 + iVar2, puVar3 < puVar10)) {
      if ((uVar8 == uVar6) && (*(int *)(local_78 + -4) < 1)) {
        puVar3 = local_78 + iVar2;
        puVar10 = (undefined1 *)(DAT_002c9cd8 + 0x2c9c18);
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_78,uVar8);
        puVar10 = (undefined1 *)(DAT_002c9cac + 0x2c9844);
        puVar3 = local_78 + *(int *)(local_78 + -0xc);
      }
    }
    else {
      iVar2 = (int)puVar10 - (int)local_78;
      if ((uVar8 == uVar6) && (*(int *)(local_78 + -4) < 1)) {
        puVar10 = local_78 + iVar2;
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_78,uVar8);
        puVar10 = local_78 + iVar2;
        puVar3 = local_78 + *(int *)(local_78 + -0xc);
      }
    }
  }
  else {
    puVar3 = local_78 + iVar2;
    puVar10 = (undefined1 *)(DAT_002c9cd4 + 0x2c9b90);
  }
  uVar1 = local_68;
  *puVar3 = *puVar10;
  if (local_78 + -0xc != puVar7) {
    *(uint *)(local_78 + -0xc) = uVar8;
    *(undefined4 *)(local_78 + -4) = 0;
    local_78[uVar8] = 0;
  }
  __s = (char *)_ZN6glitch4core18allocProcessBufferEi(0x11);
  snprintf(__s,0x10,(char *)(DAT_002c9cb0 + 0x2c9888),uVar1);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1896
            (&local_74,__s);
  if (__s != (char *)0x0) {
    _ZN6glitch4core20releaseProcessBufferEPv(__s);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (&local_7c,&local_78);
  __n = *(size_t *)(local_74 + -0xc);
  if (__n != 0) {
    iVar2 = *(int *)((int)local_7c + -0xc);
    uVar6 = iVar2 + __n;
    if ((*(uint *)((int)local_7c + -8) < uVar6) || (0 < *(int *)((int)local_7c + -4))) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                (&local_7c,uVar6);
      iVar2 = *(int *)((int)local_7c + -0xc);
    }
    if (__n == 1) {
      *(undefined1 *)((int)local_7c + iVar2) = *local_74;
    }
    else {
      memcpy((void *)((int)local_7c + iVar2),local_74,__n);
    }
    if ((undefined1 *)((int)local_7c + -0xc) != puVar7) {
      *(uint *)((int)local_7c + -0xc) = uVar6;
      *(undefined4 *)((int)local_7c + -4) = 0;
      *(undefined1 *)((int)local_7c + uVar6) = 0;
    }
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_74);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_78);
  if (*(char *)(iVar9 + 0x28) != '\0') {
    iVar2 = *(int *)((int)local_7c + -0xc);
    if (0x3ffffffcU - iVar2 < 4) {
                    /* WARNING: Subroutine does not return */
      _ZSt20__throw_length_errorPKc((int)&DAT_002c9c98 + DAT_002c9cf0);
    }
    uVar6 = *(uint *)((int)local_7c + -8);
    uVar8 = iVar2 + 4;
    if ((uVar6 < uVar8) || (0 < *(int *)((int)local_7c + -4))) {
      pvVar11 = (void *)(DAT_002c9cc4 + 0x2c9ae0);
      if ((pvVar11 < local_7c) || (pvVar4 = (void *)((int)local_7c + iVar2), pvVar4 < pvVar11)) {
        if ((uVar8 == uVar6) && (*(int *)((int)local_7c + -4) < 1)) {
          pvVar4 = (void *)((int)local_7c + iVar2);
          pvVar11 = (void *)(DAT_002c9ce4 + 0x2c9c74);
        }
        else {
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                    (&local_7c,uVar8);
          pvVar11 = (void *)(DAT_002c9cc8 + 0x2c9b0c);
          pvVar4 = (void *)((int)local_7c + *(int *)((int)local_7c + -0xc));
        }
      }
      else {
        iVar2 = (int)pvVar11 - (int)local_7c;
        if ((uVar8 == uVar6) && (*(int *)((int)local_7c + -4) < 1)) {
          pvVar11 = (void *)((int)local_7c + iVar2);
        }
        else {
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                    (&local_7c,uVar8);
          pvVar4 = (void *)((int)local_7c + *(int *)((int)local_7c + -0xc));
          pvVar11 = (void *)((int)local_7c + iVar2);
        }
      }
    }
    else {
      pvVar4 = (void *)((int)local_7c + iVar2);
      pvVar11 = (void *)(DAT_002c9ce0 + 0x2c9c44);
    }
    memcpy(pvVar4,pvVar11,4);
    if ((undefined1 *)((int)local_7c + -0xc) != puVar7) {
      *(uint *)((int)local_7c + -0xc) = uVar8;
      *(undefined4 *)((int)local_7c + -4) = 0;
      *(undefined1 *)((int)local_7c + uVar8) = 0;
    }
  }
  iVar2 = *(int *)((int)local_7c + -0xc);
  if (0x3ffffffcU - iVar2 < 4) {
                    /* WARNING: Subroutine does not return */
    _ZSt20__throw_length_errorPKc(DAT_002c9ce8 + 0x2c9c80);
  }
  uVar6 = *(uint *)((int)local_7c + -8);
  uVar8 = iVar2 + 4;
  if ((uVar6 < uVar8) || (0 < *(int *)((int)local_7c + -4))) {
    pvVar11 = (void *)(DAT_002c9cb4 + 0x2c9984);
    if ((pvVar11 < local_7c) || (pvVar4 = (void *)((int)local_7c + iVar2), pvVar4 < pvVar11)) {
      if ((uVar8 == uVar6) && (*(int *)((int)local_7c + -4) < 1)) {
        pvVar4 = (void *)((int)local_7c + iVar2);
        pvVar11 = (void *)(DAT_002c9cdc + 0x2c9c34);
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_7c,uVar8);
        pvVar11 = (void *)(DAT_002c9ccc + 0x2c9b6c);
        pvVar4 = (void *)((int)local_7c + *(int *)((int)local_7c + -0xc));
      }
    }
    else {
      iVar2 = (int)pvVar11 - (int)local_7c;
      if ((uVar8 != uVar6) || (0 < *(int *)((int)local_7c + -4))) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_7c,uVar8);
        pvVar4 = (void *)((int)local_7c + *(int *)((int)local_7c + -0xc));
      }
      pvVar11 = (void *)((int)local_7c + iVar2);
    }
  }
  else {
    pvVar4 = (void *)((int)local_7c + iVar2);
    pvVar11 = (void *)(DAT_002c9cd0 + 0x2c9b80);
  }
  memcpy(pvVar4,pvVar11,4);
  if ((undefined1 *)((int)local_7c + -0xc) != puVar7) {
    *(uint *)((int)local_7c + -0xc) = uVar8;
    *(undefined4 *)((int)local_7c + -4) = 0;
    *(undefined1 *)((int)local_7c + uVar8) = 0;
  }
  piVar5 = (int *)_Z9GetDevicev();
  iVar2 = (**(code **)(**(int **)(*piVar5 + 0x28) + 0x48))(*(int **)(*piVar5 + 0x28),local_7c);
  if (iVar2 != 0) {
    _ZN6glitch10irradiance18CIrradianceManager4loadEPKc(iVar9,local_7c);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_7c);
  local_70 = DAT_002c9cb8 + 0x2c9a38;
  local_30 = DAT_002c9cbc + 0x2c9a3c;
  local_3c = DAT_002c9cc0 + 0x2c9a44;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_38);
  return;
}


