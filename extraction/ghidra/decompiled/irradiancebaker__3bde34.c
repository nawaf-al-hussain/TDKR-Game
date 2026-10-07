// _ZN15IrradianceBaker8BakeMeshEN5boost13intrusive_ptrIN6glitch5scene5IMeshEEE.constprop.3178 @ 003bde34

void _ZN15IrradianceBaker8BakeMeshEN5boost13intrusive_ptrIN6glitch5scene5IMeshEEE_constprop_3178
               (undefined4 param_1,undefined4 *param_2)

{
  int iVar1;
  float *pfVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int local_38;
  float local_34;
  float local_30;
  float local_2c;
  
  pfVar2 = (float *)(**(code **)(*(int *)*param_2 + 0x24))();
  local_34 = (*pfVar2 + pfVar2[3]) * 0.5;
  local_30 = (pfVar2[1] + pfVar2[4]) * 0.5;
  local_2c = (pfVar2[2] + pfVar2[5]) * 0.5;
  iVar3 = (**(code **)(*(int *)*param_2 + 0x10))();
  if (0 < iVar3) {
    iVar9 = 0;
    do {
      (**(code **)(*(int *)*param_2 + 0x14))(&local_38,(int *)*param_2,iVar9);
      iVar1 = local_38;
      if (local_38 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_38 + 4);
      }
      iVar4 = *(int *)(iVar1 + 8);
      iVar4 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                        (iVar4,0x10,iVar4 + 0x14,*(undefined4 *)(iVar4 + 0x10));
      iVar5 = *(int *)(iVar1 + 8);
      iVar5 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                        (iVar5,0x11,iVar5 + 0x14,*(undefined4 *)(iVar5 + 0x10));
      iVar6 = *(int *)(iVar1 + 8);
      iVar6 = _ZN6glitch5video14CVertexStreams9getStreamENS0_18E_VERTEX_ATTRIBUTEEPNS0_13SVertexStreamES4_
                        (iVar6,0,iVar6 + 0x14,*(undefined4 *)(iVar6 + 0x10));
      iVar8 = *(int *)(*(int *)(iVar1 + 8) + 0x10);
      if ((((iVar4 != iVar8) && (iVar5 != iVar8)) && (iVar6 != iVar8)) &&
         (iVar8 = *(int *)(*(int *)(iVar1 + 8) + 0x14), iVar8 != 0)) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar8 + 4);
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar8 + 4);
        iVar7 = _ZNK6glitch5video7IBuffer11mapInternalEjjjj
                          (iVar8,1,0,*(undefined4 *)(iVar8 + 0x14),0);
        _ZN15IrradianceBaker10BakeBufferEPvRKN6glitch4core8vector3dIfEEiiiii
                  (param_1,iVar7,&local_34,*(undefined4 *)(iVar6 + 4),*(undefined4 *)(iVar4 + 4),
                   *(undefined4 *)(iVar5 + 4),*(undefined2 *)(iVar4 + 0xe),
                   *(undefined4 *)(*(int *)(iVar1 + 8) + 8));
        if (iVar7 != 0) {
          _ZNK6glitch5video7IBuffer5unmapEv(iVar8);
        }
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar8);
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar8);
      }
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar1);
      if (local_38 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      iVar9 = iVar9 + 1;
    } while (iVar3 != iVar9);
  }
  return;
}

