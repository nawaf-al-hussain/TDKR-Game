// _ZN15IrradianceBaker14BakeMeshBufferEN5boost13intrusive_ptrIN6glitch5scene11CMeshBufferEEERKNS2_4core8vector3dIfEE @ 00311400

void _ZN15IrradianceBaker14BakeMeshBufferEN5boost13intrusive_ptrIN6glitch5scene11CMeshBufferEEERKNS2_4core8vector3dIfEE
               (undefined4 param_1,int *param_2,undefined4 param_3)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int iVar7;
  int *piVar8;
  
  iVar7 = *param_2;
  iVar2 = *(int *)(iVar7 + 8);
  iVar2 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                    (iVar2,0x10,iVar2 + 0x14,*(undefined4 *)(iVar2 + 0x10));
  iVar3 = *(int *)(iVar7 + 8);
  iVar3 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                    (iVar3,0x11,iVar3 + 0x14,*(undefined4 *)(iVar3 + 0x10));
  iVar4 = *(int *)(iVar7 + 8);
  iVar4 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                    (iVar4,0,iVar4 + 0x14,*(undefined4 *)(iVar4 + 0x10));
  iVar6 = *(int *)(*(int *)(iVar7 + 8) + 0x10);
  if ((((iVar2 == iVar6) || (iVar3 == iVar6)) || (iVar4 == iVar6)) ||
     (piVar8 = *(int **)(*(int *)(iVar7 + 8) + 0x14), piVar8 == (int *)0x0)) {
    return;
  }
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar8 + 1);
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar8 + 1);
  iVar6 = _ZNK6glitch5video7IBuffer11mapInternalEjjjj(piVar8,1,0,piVar8[5],0);
  _ZN15IrradianceBaker10BakeBufferEPvRKN6glitch4core8vector3dIfEEiiiii
            (param_1,iVar6,param_3,*(undefined4 *)(iVar4 + 4),*(undefined4 *)(iVar2 + 4),
             *(undefined4 *)(iVar3 + 4),*(undefined2 *)(iVar2 + 0xe),
             *(undefined4 *)(*(int *)(iVar7 + 8) + 8));
  if (iVar6 != 0) {
    _ZNK6glitch5video7IBuffer5unmapEv(piVar8);
  }
  _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(piVar8);
  piVar5 = piVar8 + 1;
  DataMemoryBarrier(0xf);
  do {
    iVar2 = *piVar5;
    bVar1 = (bool)hasExclusiveAccess(piVar5);
  } while (!bVar1);
  *piVar5 = iVar2 + -1;
  DataMemoryBarrier(0xf);
  if (iVar2 + -1 == 0) {
    (**(code **)(*piVar8 + 8))();
    (**(code **)(*piVar8 + 4))(piVar8);
    return;
  }
  return;
}


