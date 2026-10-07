// _ZN24CPostProcessEffect_Blend6RenderEi @ 004599a4

/* WARNING: Removing unreachable block (ram,0x00459a28) */
/* WARNING: Removing unreachable block (ram,0x00459a30) */
/* WARNING: Removing unreachable block (ram,0x00459a38) */
/* WARNING: Removing unreachable block (ram,0x00459a3c) */
/* WARNING: Removing unreachable block (ram,0x00459a44) */
/* WARNING: Removing unreachable block (ram,0x00459a50) */

void _ZN24CPostProcessEffect_Blend6RenderEi(int param_1,int param_2)

{
  bool bVar1;
  int *__ptr;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  code *pcVar6;
  int *piVar7;
  int *__ptr_00;
  byte bVar8;
  uint uVar9;
  int *local_48;
  int local_44;
  int local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 uStack_34;
  int local_30 [5];
  char *local_1c;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  iVar3 = *(int *)(*(int *)(param_1 + 0x38) + 0x14);
  piVar7 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
  if (((param_2 < *(int *)(*(int *)(param_1 + 0x38) + 0x18) - iVar3 >> 2) && (-1 < param_2)) &&
     (iVar2 = *(int *)(iVar3 + param_2 * 4), iVar2 != 0)) {
    (**(code **)(*piVar7 + 0x18))(piVar7);
    _ZN6glitch5video12IVideoDriver11setMaterialERKN5boost13intrusive_ptrINS0_9CMaterialEEERKNS3_IKNS0_27CMaterialVertexAttributeMapEEE
              (piVar7,param_1 + 0x34);
    local_38 = *(undefined4 *)(iVar2 + 0x18);
    uStack_34 = *(undefined4 *)(iVar2 + 0x1c);
    iVar2 = *(int *)(piVar7[0x48] + -4);
    local_40 = *(int *)(iVar2 + 0x1c) - *(int *)(iVar2 + 0x14);
    local_3c = *(int *)(iVar2 + 0x20) - *(int *)(iVar2 + 0x18);
    _ZN19CPostProcessManager18UpdateVertexBufferERKN6glitch4core11dimension2dIiEES5_S5__constprop_2530
              (*(undefined4 *)(param_1 + 0x38),&local_38,&local_40);
    __ptr_00 = *(int **)(*(int *)(param_1 + 0x38) + 0x54);
    uVar9 = (piVar7[2] & 0x1fffffU) >> 0x14;
    piVar7[2] = piVar7[2] & 0xffefffff;
    *(byte *)((int)piVar7 + 0x291) = (byte)uVar9 | *(byte *)((int)piVar7 + 0x291);
    local_48 = __ptr_00;
    if (__ptr_00 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(__ptr_00);
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(__ptr_00);
    }
    local_30[2] = 4;
    local_30[4] = 4;
    local_1c = "ivdi3";
    local_30[0] = 0;
    local_30[1] = 0;
    local_30[3] = 0;
    local_44 = 0;
    (**(code **)(*piVar7 + 0x3c))(piVar7,&local_48,local_30,0,&local_44);
    if (local_44 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_30[0] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    __ptr = local_48;
    if (local_48 != (int *)0x0) {
      DataMemoryBarrier(0xf);
      do {
        iVar2 = *local_48;
        bVar1 = (bool)hasExclusiveAccess(local_48);
      } while (!bVar1);
      *local_48 = iVar2 + -1;
      DataMemoryBarrier(0xf);
      if (iVar2 + -1 == 0) {
        _ZN6glitch5video14CVertexStreamsD1Ev(local_48);
        free(__ptr);
      }
    }
    if (__ptr_00 != (int *)0x0) {
      DataMemoryBarrier(0xf);
      do {
        iVar2 = *__ptr_00;
        bVar1 = (bool)hasExclusiveAccess(__ptr_00);
      } while (!bVar1);
      *__ptr_00 = iVar2 + -1;
      DataMemoryBarrier(0xf);
      if (iVar2 + -1 == 0) {
        _ZN6glitch5video14CVertexStreamsD1Ev(__ptr_00);
        free(__ptr_00);
      }
    }
    uVar4 = piVar7[2];
    bVar8 = *(byte *)((int)piVar7 + 0x291);
    if (uVar9 == 0) {
      uVar5 = uVar4 & 0xffefffff;
    }
    else {
      uVar5 = uVar4 | 0x100000;
    }
    piVar7[2] = uVar5;
    if (uVar9 != (uVar4 & 0x1fffff) >> 0x14) {
      bVar8 = bVar8 | 1;
    }
    pcVar6 = *(code **)(*piVar7 + 0x1c);
    *(byte *)((int)piVar7 + 0x291) = bVar8;
    (*pcVar6)(piVar7);
  }
  return;
}


