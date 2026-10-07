// _ZN19CPostProcessManager18UpdateVertexBufferERKN6glitch4core11dimension2dIiEES5_S5_ @ 0045859c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _ZN19CPostProcessManager18UpdateVertexBufferERKN6glitch4core11dimension2dIiEES5_S5_
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  byte bVar3;
  int iVar4;
  uint in_fpscr;
  undefined4 uVar5;
  undefined4 uVar6;
  
  iVar4 = *(int *)(param_1 + 0x58);
  if (iVar4 == 0) {
    iVar1 = 0;
  }
  else {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar4 + 4);
    iVar1 = *(int *)(param_1 + 0x58);
  }
  puVar2 = (undefined4 *)
           _ZNK6glitch5video7IBuffer11mapInternalEjjjj(iVar1,1,0,*(undefined4 *)(iVar1 + 0x14),0);
  uVar5 = VectorSignedToFloat(*param_4,(byte)(in_fpscr >> 0x16) & 3);
  uVar6 = VectorSignedToFloat(param_4[1],(byte)(in_fpscr >> 0x16) & 3);
  puVar2[2] = 0;
  *puVar2 = uVar5;
  puVar2[8] = 0;
  puVar2[7] = uVar5;
  puVar2[9] = 0;
  puVar2[1] = uVar6;
  puVar2[0xb] = 0;
  puVar2[0xf] = uVar6;
  puVar2[0xd] = 0;
  puVar2[0x15] = 0;
  puVar2[0x16] = 0;
  puVar2[0x17] = 0;
  puVar2[0x18] = 0;
  puVar2[0x19] = 0;
  puVar2[0x1a] = 0;
  puVar2[0x1b] = 0;
  puVar2[0xe] = 0;
  puVar2[0x10] = 0;
  puVar2[0x11] = 0;
  puVar2[3] = 0x3f800000;
  puVar2[4] = 0x3f800000;
  puVar2[5] = 0x3f800000;
  puVar2[6] = 0x3f800000;
  puVar2[10] = 0x3f800000;
  puVar2[0xc] = 0x3f800000;
  puVar2[0x12] = 0x3f800000;
  puVar2[0x13] = 0;
  puVar2[0x14] = 0x3f800000;
  if (iVar4 == 0) {
    if (puVar2 != (undefined4 *)0x0) {
      if ((DAT_00000023 & 0x1f) < 2) {
        if ((DAT_00000022 & 0x10) == 0) {
          if (((DAT_00000022 & 4) != 0) && (DAT_00000023 >> 5 != 0)) {
            bVar3 = DAT_00000022 & 0x20;
            if ((DAT_00000022 & 0x20) != 0) {
              bVar3 = 4;
            }
            (**(code **)(iRam00000000 + 0x20))
                      (0,_DAT_00000018,_DAT_0000001c,_DAT_00000010,bVar3,DAT_00000022 & 0x10);
            DAT_00000022 = DAT_00000022 & 0xdf;
          }
          DAT_00000023 = 0;
          _DAT_0000001c = 0;
          _DAT_00000018 = 0;
          _DAT_00000010 = 0;
        }
        else {
          (**(code **)(iRam00000000 + 0x18))();
          DAT_00000022 = DAT_00000022 & 0xef;
          DAT_00000023 = 0;
          _DAT_0000001c = 0;
          _DAT_00000018 = 0;
          _DAT_00000010 = 0;
        }
      }
      else {
        DAT_00000023 = (DAT_00000023 & 0x1f) - 1 | DAT_00000023 & 0xe0;
      }
      return;
    }
  }
  else {
    _ZNK6glitch5video7IBuffer5unmapEv(iVar4);
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar4);
  }
  return;
}


