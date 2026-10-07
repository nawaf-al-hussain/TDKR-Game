// _ZN11Application16ReadSaveFromFileEPKciP13CMemoryStream @ 003f2428

undefined4
_ZN11Application16ReadSaveFromFileEPKciP13CMemoryStream
          (undefined4 param_1,undefined4 param_2,int param_3,undefined4 *param_4)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  undefined4 uVar5;
  int *piStack_1c;
  int iStack_18;
  uint uStack_14;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
  (**(code **)(*piVar4 + 0xc))(&piStack_1c,piVar4,param_2);
  if (piStack_1c == (int *)0x0) {
LAB_003eec74:
    uVar5 = 0;
  }
  else {
    (**(code **)(*piStack_1c + 0xc))(piStack_1c,&iStack_18,4);
    if (iStack_18 == param_3) {
      uStack_14 = 0;
      (**(code **)(*piStack_1c + 0xc))(piStack_1c,&uStack_14,4);
      iVar2 = (**(code **)(*piStack_1c + 0x20))();
      uVar1 = uStack_14;
      if (iVar2 - 8U < uStack_14) goto joined_r0x003eec70;
      param_4[3] = 0;
      _ZN13CMemoryStream13AssureAddSizeEi(param_4,uStack_14);
      param_4[2] = uVar1;
      (**(code **)(*piStack_1c + 0xc))(piStack_1c,*param_4,uStack_14);
      piVar4 = piStack_1c;
      piStack_1c = (int *)0x0;
      if (piVar4 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      uVar5 = param_4[3];
      param_4[3] = param_4[2] + -8;
      iVar2 = _ZN13CMemoryStream7ReadIntEv(param_4);
      iVar3 = _Z10ComputeCRCPhi(*param_4,param_4[2] + -8);
      param_4[3] = uVar5;
      if (iVar2 == iVar3) {
        uVar5 = 1;
        _ZN11CEncryption13EncryptBufferEbjPh
                  (*(undefined4 *)(DAT_003eec7c + 0x3eec5c),0,uStack_14,*param_4);
      }
      else {
        uVar5 = 0;
      }
    }
    else {
joined_r0x003eec70:
      if (piStack_1c == (int *)0x0) goto LAB_003eec74;
      piStack_1c = (int *)0x0;
      uVar5 = 0;
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (piStack_1c != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
  }
  return uVar5;
}


