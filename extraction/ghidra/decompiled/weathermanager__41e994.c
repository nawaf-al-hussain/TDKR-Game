// _ZN15CWeatherManager22LoadGlobalIlluminationEP13CMemoryStream @ 0041e994

void _ZN15CWeatherManager22LoadGlobalIlluminationEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 *puVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  int *local_14;
  
  local_14 = (int *)_Znwj(0x74);
  iVar4 = *(int *)(DAT_0041eb1c + 0x41e9c8) + 0xc;
  iVar2 = DAT_0041eb18 + 0x41e9e8;
  *local_14 = DAT_0041eb18 + 0x41e9cc;
  local_14[3] = 0;
  local_14[4] = 0;
  local_14[5] = 0;
  local_14[6] = 0;
  local_14[7] = 0;
  local_14[8] = 0;
  local_14[9] = 0;
  local_14[0x10] = 0;
  local_14[10] = 0;
  local_14[0x11] = 0;
  local_14[0xb] = 0;
  local_14[0x12] = 0;
  local_14[0xd] = iVar4;
  local_14[0x13] = 0;
  local_14[0xe] = iVar4;
  local_14[0x18] = 0;
  local_14[0xf] = iVar4;
  local_14[0x19] = 0;
  local_14[0x14] = iVar4;
  local_14[0x1a] = 0;
  local_14[0x17] = 0;
  local_14[0x1b] = 0;
  local_14[0x1c] = iVar2;
  _ZN27CTemplateGlobalIllumination4LoadEP13CMemoryStream(local_14,param_2);
  iVar2 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                    (local_14 + 0xd,DAT_0041eb20 + 0x41ea50);
  if (((iVar2 != 0) && (*(int **)(param_1 + 0x44) != (int *)0x0)) &&
     ((**(code **)(**(int **)(param_1 + 0x44) + 0x84))(), *(int *)(param_1 + 0x44) != 0)) {
    piVar3 = *(int **)(*(int *)(DAT_0041eb24 + 0x41ea88) + 0x180);
    if (piVar3 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                ((int)piVar3 + *(int *)(*piVar3 + -0x10) + 4);
    }
    (**(code **)(*piVar3 + 0x68))(piVar3,param_1 + 0x44);
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar3 + *(int *)(*piVar3 + -0x10));
    if (*(int *)(param_1 + 0x44) != 0) {
      *(undefined1 *)(param_1 + 0x28) = 1;
    }
  }
  puVar1 = *(undefined4 **)(param_1 + 0x10);
  if (puVar1 == *(undefined4 **)(param_1 + 0x14)) {
    _ZNSt6vectorIP27CTemplateGlobalIlluminationSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
              (param_1 + 0xc,puVar1,&local_14);
  }
  else {
    iVar2 = 0;
    if (puVar1 != (undefined4 *)0x0) {
      *puVar1 = local_14;
      iVar2 = *(int *)(param_1 + 0x10);
    }
    *(int *)(param_1 + 0x10) = iVar2 + 4;
  }
  return;
}


