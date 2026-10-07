// _ZN19CPostProcessManager8PostDrawEi @ 004578fc

void _ZN19CPostProcessManager8PostDrawEi(undefined1 *param_1)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  uint uVar6;
  int local_2c [2];
  
  _ZN11Application11GetInstanceEv();
  piVar4 = *(int **)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x38) * 4);
  (**(code **)(*piVar4 + 0x28))(piVar4,*(undefined4 *)(param_1 + 0x3c));
  if (*(int *)(param_1 + 0x38) == 3 || *(int *)(param_1 + 0x38) == 0xb) {
    iVar2 = *(int *)(param_1 + 0x3c);
    piVar5 = (int *)**(undefined4 **)(param_1 + 8);
    piVar3 = (int *)(*(undefined4 **)(param_1 + 8))[2];
    local_2c[0] = *(int *)(*(int *)(*(int *)(param_1 + 0x14) + iVar2 * 4) + 4);
    if (local_2c[0] != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_2c[0] + 4);
    }
    iVar1 = local_2c[0];
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(local_2c);
    uVar6 = *(uint *)(*(int *)(iVar1 + 0x18) + 0x24);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE(iVar1,1);
    *(undefined1 *)(piVar5[0xd] + 8) = 1;
    (**(code **)(*piVar5 + 0x20))(piVar5,4,0xffffffff);
    (**(code **)(*piVar5 + 0x24))(piVar5,iVar2);
    (**(code **)(*piVar5 + 0x28))(piVar5,4);
    *(undefined1 *)(piVar5[0xd] + 8) = 0;
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (iVar1,(uVar6 & 0x1ffff) >> 0xe);
    *(undefined1 *)(piVar3[0xd] + 8) = 0;
    (**(code **)(*piVar3 + 0x20))(piVar3,5,0xffffffff);
    (**(code **)(*piVar3 + 0x24))(piVar3,4);
    (**(code **)(*piVar3 + 0x28))(piVar3,5);
    *(undefined1 *)(piVar3[0xd] + 8) = 1;
    (**(code **)(*piVar3 + 0x20))(piVar3,6,0xffffffff);
    (**(code **)(*piVar3 + 0x24))(piVar3,5);
    (**(code **)(*piVar3 + 0x28))(piVar3,6);
    *param_1 = 1;
  }
  if (((*(uint *)(param_1 + 0x40) & 0x10) == 0) &&
     (99 < *(int *)(**(int **)(DAT_00457b74 + 0x45799c) + 0x88))) {
    iVar2 = **(int **)(param_1 + 0x14);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar2 + 4),0);
    _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar2 + 4),0);
    if (param_1[0x66] != '\0') {
      iVar2 = *(int *)(*(int *)(param_1 + 0x14) + 4);
      _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
                (*(undefined4 *)(iVar2 + 4),0);
      _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
                (*(undefined4 *)(iVar2 + 4),0);
    }
  }
  else {
    iVar2 = **(int **)(param_1 + 0x14);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar2 + 4),1);
    _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(iVar2 + 4),1);
    if (param_1[0x66] != '\0') {
      iVar2 = *(int *)(*(int *)(param_1 + 0x14) + 4);
      _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
                (*(undefined4 *)(iVar2 + 4),1);
      _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
                (*(undefined4 *)(iVar2 + 4),1);
    }
  }
  (**(code **)(*piVar4 + 0x24))(piVar4,*(undefined4 *)(param_1 + 0x3c));
  return;
}


