// _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream @ 003eeaf4

undefined4
_ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
          (undefined4 param_1,undefined4 param_2,int param_3,undefined4 *param_4)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  undefined4 uVar5;
  int *local_1c;
  int iStack_18;
  uint local_14;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
  (**(code **)(*piVar4 + 0xc))(&local_1c,piVar4,param_2);
  if (local_1c == (int *)0x0) {
LAB_003eec74:
    uVar5 = 0;
  }
  else {
    (**(code **)(*local_1c + 0xc))(local_1c,&iStack_18,4);
    if (iStack_18 == param_3) {
      local_14 = 0;
      (**(code **)(*local_1c + 0xc))(local_1c,&local_14,4);
      iVar2 = (**(code **)(*local_1c + 0x20))();
      uVar1 = local_14;
      if (iVar2 - 8U < local_14) goto joined_r0x003eec70;
      param_4[3] = 0;
      _ZN13CMemoryStream13AssureAddSizeEi(param_4,local_14);
      param_4[2] = uVar1;
      (**(code **)(*local_1c + 0xc))(local_1c,*param_4,local_14);
      piVar4 = local_1c;
      local_1c = (int *)0x0;
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
                  (*(undefined4 *)(DAT_003eec7c + 0x3eec5c),0,local_14,*param_4);
      }
      else {
        uVar5 = 0;
      }
    }
    else {
joined_r0x003eec70:
      if (local_1c == (int *)0x0) goto LAB_003eec74;
      local_1c = (int *)0x0;
      uVar5 = 0;
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_1c != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
  }
  return uVar5;
}


