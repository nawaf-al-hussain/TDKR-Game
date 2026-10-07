// _ZN15IrradianceBaker14BakeMeshBufferEN5boost13intrusive_ptrIN6glitch5scene11CMeshBufferEEERKNS2_4core8vector3dIfEE @ 00311400

void _ZN15IrradianceBaker14BakeMeshBufferEN5boost13intrusive_ptrIN6glitch5scene11CMeshBufferEEERKNS2_4core8vector3dIfEE
               (undefined4 param_1,int *param_2,undefined4 param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  
  iVar6 = *param_2;
  iVar1 = *(int *)(iVar6 + 8);
  iVar1 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                    (iVar1,0x10,iVar1 + 0x14,*(undefined4 *)(iVar1 + 0x10));
  iVar2 = *(int *)(iVar6 + 8);
  iVar2 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                    (iVar2,0x11,iVar2 + 0x14,*(undefined4 *)(iVar2 + 0x10));
  iVar3 = *(int *)(iVar6 + 8);
  iVar3 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                    (iVar3,0,iVar3 + 0x14,*(undefined4 *)(iVar3 + 0x10));
  iVar5 = *(int *)(*(int *)(iVar6 + 8) + 0x10);
  if ((((iVar1 != iVar5) && (iVar2 != iVar5)) && (iVar3 != iVar5)) &&
     (iVar5 = *(int *)(*(int *)(iVar6 + 8) + 0x14), iVar5 != 0)) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar5 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar5 + 4);
    iVar4 = _ZNK6glitch5video7IBuffer11mapInternalEjjjj(iVar5,1,0,*(undefined4 *)(iVar5 + 0x14),0);
    _ZN15IrradianceBaker10BakeBufferEPvRKN6glitch4core8vector3dIfEEiiiii
              (param_1,iVar4,param_3,*(undefined4 *)(iVar3 + 4),*(undefined4 *)(iVar1 + 4),
               *(undefined4 *)(iVar2 + 4),*(undefined2 *)(iVar1 + 0xe),
               *(undefined4 *)(*(int *)(iVar6 + 8) + 8));
    if (iVar4 != 0) {
      _ZNK6glitch5video7IBuffer5unmapEv(iVar5);
    }
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar5);
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar5);
    return;
  }
  return;
}

