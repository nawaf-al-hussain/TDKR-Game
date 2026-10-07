// _ZN7gameswf21render_handler_glitch11postProcessEbRKNS_4RectES3_.constprop.402 @ 006c85e8

void _ZN7gameswf21render_handler_glitch11postProcessEbRKNS_4RectES3__constprop_402
               (int *param_1,int param_2,undefined4 *param_3,undefined4 *param_4)

{
  bool bVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  undefined4 uVar8;
  int iVar9;
  byte bVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  int iVar14;
  int local_40 [3];
  undefined1 auStack_34 [16];
  
  iVar7 = param_1[0x203];
  if (param_1[0x205] == iVar7) {
    iVar7 = param_1[0x204];
  }
  if (param_2 != 0) {
    (**(code **)(*(int *)param_1[0x56] + 0x70))((int *)param_1[0x56],iVar7 + 0x70);
    piVar6 = *(int **)(*(int *)(param_1[0x56] + 0x120) + -4);
    (**(code **)(*piVar6 + 0xc))(piVar6,param_1 + 0x1fd);
    iVar5 = param_1[0x56];
    iVar14 = *(int *)(iVar5 + 0x28);
    *(undefined4 *)(iVar5 + 0x28) = 0;
    piVar6 = (int *)param_1[0x56];
    bVar10 = *(byte *)(iVar5 + 0x292);
    iVar9 = *piVar6;
    if ((*(uint *)(iVar5 + 0x24) & 0xf0000) != 0xf0000) {
      bVar10 = bVar10 | 1;
    }
    if (iVar14 != 0) {
      bVar10 = bVar10 | 1;
    }
    *(uint *)(iVar5 + 0x24) = *(uint *)(iVar5 + 0x24) | 0xf0000;
    *(byte *)(iVar5 + 0x292) = bVar10;
    (**(code **)(iVar9 + 0x94))(piVar6,7);
  }
  puVar4 = (undefined4 *)param_1[0x226];
  uVar12 = *param_3;
  uVar13 = param_3[2];
  uVar2 = param_3[1];
  uVar3 = param_3[3];
  uVar11 = *param_4;
  uVar8 = param_4[2];
  puVar4[3] = uVar12;
  *puVar4 = uVar11;
  puVar4[1] = uVar8;
  uVar11 = param_4[1];
  uVar8 = param_4[2];
  puVar4[4] = uVar13;
  puVar4[6] = uVar11;
  puVar4[7] = uVar8;
  uVar8 = param_4[3];
  uVar11 = *param_4;
  puVar4[10] = uVar13;
  puVar4[0xd] = uVar8;
  puVar4[0xc] = uVar11;
  uVar11 = param_4[3];
  uVar8 = param_4[1];
  puVar4[5] = 0;
  puVar4[0x13] = uVar11;
  puVar4[9] = uVar2;
  puVar4[0xb] = 0;
  puVar4[0xf] = uVar12;
  puVar4[0x10] = uVar3;
  puVar4[0x11] = 0;
  puVar4[0x15] = uVar2;
  puVar4[0x16] = uVar3;
  puVar4[0x17] = 0;
  puVar4[0x12] = uVar8;
  local_40[1] = 0xffffffff;
  puVar4[0x14] = 0xffffffff;
  iVar5 = DAT_006c88bc;
  puVar4[0xe] = *(undefined4 *)(param_1[0x226] + 0x50);
  puVar4[8] = *(undefined4 *)(param_1[0x226] + 0x38);
  *(undefined4 *)(param_1[0x226] + 8) = *(undefined4 *)(param_1[0x226] + 0x20);
  memcpy(auStack_34,(void *)(iVar5 + 0x6c86d0),0xc);
  uVar2 = *(undefined4 *)(param_1[0x205] + 0x6c);
  *(undefined4 *)(param_1[0x227] + 8) = 4;
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,0,1);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,1,1);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,2,1);
  iVar9 = param_1[0x205];
  iVar5 = *(int *)(iVar9 + 0x6c);
  if ((param_1[0x1d4] != iVar5) && (param_1[0xd4] != 0)) {
    _ZN7gameswf16BufferedRenderer5flushEv_part_215(param_1 + 200);
    iVar5 = *(int *)(iVar9 + 0x6c);
  }
  if (iVar5 != 0) {
    piVar6 = (int *)(iVar5 + 4);
    DataMemoryBarrier(0xf);
    do {
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = *piVar6 + 1;
    DataMemoryBarrier(0xf);
  }
  local_40[2] = param_1[0x1d4];
  param_1[0x1d4] = iVar5;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
  _ZN7gameswf16BufferedRenderer21queueIndexedTrianglesEPKNS_6VertexEiPKti
            (param_1 + 200,*(undefined4 *)(*(int *)(param_1[0x227] + 0x14) + 0xc),
             *(undefined4 *)(param_1[0x227] + 8),auStack_34,6);
  _ZN7gameswf13RenderHandler9flushListERNS_9BatchListE(param_1,param_1 + 0x43);
  _ZN7gameswf13RenderHandler9flushListERNS_9BatchListE(param_1,param_1 + 0x4b);
  (**(code **)(*param_1 + 0x80))(param_1);
  if ((param_2 != 0) && ((**(code **)(*(int *)param_1[0x56] + 0x74))(local_40), local_40[0] != 0)) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  param_1[0x205] = iVar7;
  return;
}


