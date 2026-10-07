// _ZN11Application9DrawLinesEPN6glitch4core8vector2dIiEEiRKNS0_5video6SColorEf @ 003f4580

void _ZN11Application9DrawLinesEPN6glitch4core8vector2dIiEEiRKNS0_5video6SColorEf
               (undefined4 param_1,int *param_2,int param_3,undefined4 *param_4,float param_5)

{
  bool bVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined2 *puVar4;
  float fVar5;
  undefined4 uVar6;
  int *piVar7;
  undefined4 *puVar8;
  uint uVar9;
  undefined4 *puVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  undefined2 *puVar14;
  short sVar15;
  byte bVar16;
  uint in_fpscr;
  float fVar17;
  float fVar18;
  float fVar19;
  undefined4 local_50;
  undefined1 auStack_4c [4];
  undefined1 auStack_48 [4];
  int *local_44;
  undefined4 local_40;
  undefined1 auStack_3c [8];
  
  if (1 < param_3) {
    iVar2 = _ZN11Application11GetInstanceEv();
    iVar11 = 0;
    local_50 = 0;
    iVar2 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
    fVar19 = *(float *)(iVar2 + 0x10);
    uVar9 = in_fpscr & 0xfffffff | (uint)(param_5 == fVar19) << 0x1e;
    *(float *)(iVar2 + 0x10) = param_5;
    bVar16 = *(byte *)(iVar2 + 0x291);
    if (!SUB41(uVar9 >> 0x1e,0)) {
      bVar16 = bVar16 | 1;
    }
    *(byte *)(iVar2 + 0x291) = bVar16;
    _ZN6glitch5video9C2DDriver12set2DTextureEPNS0_12IVideoDriverERKN5boost13intrusive_ptrINS0_8ITextureEEEb
              (auStack_4c,iVar2,&local_50,0);
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(auStack_4c);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_50);
    puVar3 = (undefined4 *)_Znaj(param_3 << 2);
    puVar10 = puVar3;
    do {
      iVar11 = iVar11 + 1;
      *puVar10 = 0;
      iVar13 = DAT_003f4898;
      puVar10 = puVar10 + 1;
    } while (param_3 != iVar11);
    iVar12 = param_3 + -1;
    sVar15 = 1;
    puVar4 = (undefined2 *)_Znaj(iVar12 * 4);
    iVar11 = 0;
    puVar8 = *(undefined4 **)(iVar13 + 0x3f4660);
    puVar10 = puVar3;
    piVar7 = param_2;
    puVar14 = puVar4;
    do {
      *puVar10 = *param_4;
      fVar17 = (float)VectorSignedToFloat(*piVar7,(byte)(uVar9 >> 0x16) & 3);
      fVar5 = (float)_ZN14GameEngineBase15GetScreenScaleWEv(*puVar8);
      fVar18 = (float)VectorSignedToFloat(piVar7[1],(byte)(uVar9 >> 0x16) & 3);
      uVar6 = *puVar8;
      *piVar7 = (int)(fVar17 * fVar5);
      fVar5 = (float)_ZN14GameEngineBase15GetScreenScaleHEv(uVar6);
      piVar7[1] = (int)(fVar18 * fVar5);
      if (iVar11 < iVar12) {
        *puVar14 = (short)iVar11;
        puVar14[1] = sVar15;
      }
      iVar11 = iVar11 + 1;
      sVar15 = sVar15 + 1;
      piVar7 = piVar7 + 2;
      puVar14 = puVar14 + 2;
      puVar10 = puVar10 + 1;
    } while (iVar11 != param_3);
    iVar11 = _ZN11Application11GetInstanceEv();
    _ZN6glitch5video12IVideoDriver12setTransformENS0_22E_TRANSFORMATION_STATEERKNS_4core8CMatrix4IfEEj
              (*(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar11) + 8),2,
               *(undefined4 *)(DAT_003f489c + 0x3f4710),0);
    iVar11 = _ZN11Application11GetInstanceEv();
    iVar13 = *(int *)(*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar11) + 8) + 0x148);
    iVar11 = _ZN11Application11GetInstanceEv();
    uVar9 = (uint)*(ushort *)(iVar13 + 0x5c);
    if (uVar9 == 0xffff) {
      uVar9 = _ZN6glitch5video24CMaterialRendererManager22createMaterialRendererEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
                        (iVar13,*(undefined4 *)
                                 (*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar11) + 8),0,0);
    }
    _ZN6glitch5video24CMaterialRendererManager19getMaterialInstanceEtb(auStack_48,iVar13,uVar9,1);
    iVar11 = _ZN11Application11GetInstanceEv();
    local_44 = (int *)0x0;
    _ZN6glitch5video12IVideoDriver11setMaterialERKN5boost13intrusive_ptrINS0_9CMaterialEEERKNS3_IKNS0_27CMaterialVertexAttributeMapEEE
              (*(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar11) + 8),auStack_48);
    piVar7 = local_44;
    if (local_44 != (int *)0x0) {
      DataMemoryBarrier(0xf);
      do {
        iVar11 = *local_44;
        bVar1 = (bool)hasExclusiveAccess(local_44);
      } while (!bVar1);
      *local_44 = iVar11 + -1;
      DataMemoryBarrier(0xf);
      if (iVar11 + -1 == 0) {
        _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(local_44);
        free(piVar7);
      }
    }
    iVar11 = _ZN11Application11GetInstanceEv();
    local_40 = 0;
    _ZN6glitch5video9C2DDriver12set2DTextureEPNS0_12IVideoDriverERKN5boost13intrusive_ptrINS0_8ITextureEEEb
              (auStack_3c,*(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar11) + 8),
               &local_40,0);
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(auStack_3c);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_40);
    iVar11 = _ZN11Application11GetInstanceEv();
    piVar7 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar11) + 8);
    (**(code **)(*piVar7 + 0x34))(piVar7,param_2,puVar4,puVar3,param_3,iVar12);
    fVar5 = *(float *)(iVar2 + 0x10);
    bVar16 = *(byte *)(iVar2 + 0x291);
    *(float *)(iVar2 + 0x10) = fVar19;
    if (fVar19 != fVar5) {
      bVar16 = bVar16 | 1;
    }
    *(byte *)(iVar2 + 0x291) = bVar16;
    if (puVar3 != (undefined4 *)0x0) {
      _ZdaPv(puVar3);
    }
    if (puVar4 != (undefined2 *)0x0) {
      _ZdaPv(puVar4);
    }
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(auStack_48);
  }
  return;
}


