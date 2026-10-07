// _ZN19CPostProcessManager15BuildDoFTextureEv @ 004590d4

void _ZN19CPostProcessManager15BuildDoFTextureEv(undefined1 *param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  int iVar4;
  uint uVar5;
  int local_2c [2];
  
  if (*(int *)(param_1 + 0x38) == 3 || *(int *)(param_1 + 0x38) == 0xb) {
    iVar4 = *(int *)(param_1 + 0x3c);
    piVar3 = (int *)**(undefined4 **)(param_1 + 8);
    piVar2 = (int *)(*(undefined4 **)(param_1 + 8))[2];
    local_2c[0] = *(int *)(*(int *)(*(int *)(param_1 + 0x14) + iVar4 * 4) + 4);
    if (local_2c[0] != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_2c[0] + 4);
    }
    iVar1 = local_2c[0];
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(local_2c);
    uVar5 = *(uint *)(*(int *)(iVar1 + 0x18) + 0x24);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE(iVar1,1);
    *(undefined1 *)(piVar3[0xd] + 8) = 1;
    (**(code **)(*piVar3 + 0x20))(piVar3,4,0xffffffff);
    (**(code **)(*piVar3 + 0x24))(piVar3,iVar4);
    (**(code **)(*piVar3 + 0x28))(piVar3,4);
    *(undefined1 *)(piVar3[0xd] + 8) = 0;
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (iVar1,(uVar5 & 0x1ffff) >> 0xe);
    *(undefined1 *)(piVar2[0xd] + 8) = 0;
    (**(code **)(*piVar2 + 0x20))(piVar2,5,0xffffffff);
    (**(code **)(*piVar2 + 0x24))(piVar2,4);
    (**(code **)(*piVar2 + 0x28))(piVar2,5);
    *(undefined1 *)(piVar2[0xd] + 8) = 1;
    (**(code **)(*piVar2 + 0x20))(piVar2,6,0xffffffff);
    (**(code **)(*piVar2 + 0x24))(piVar2,5);
    (**(code **)(*piVar2 + 0x28))(piVar2,6);
    *param_1 = 1;
  }
  return;
}


