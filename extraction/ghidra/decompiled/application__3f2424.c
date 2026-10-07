// _ZN11Application15WriteSaveToFileEPKciP13CMemoryStream @ 003f2424

undefined4
_ZN11Application15WriteSaveToFileEPKciP13CMemoryStream
          (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 *param_4)

{
  char cVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  int *piVar5;
  undefined4 uStack_1c;
  int *piStack_18;
  undefined4 uStack_14;
  
  cVar1 = *(char *)(DAT_003eedfc + 0x3eec90);
  *(char *)(DAT_003eee00 + 0x3eeca4) = cVar1;
  uStack_1c = param_3;
  if (cVar1 == '\0') {
    iVar2 = _ZN11Application11GetInstanceEv();
    iVar2 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + iVar2);
    iVar2 = *(int *)(iVar2 + 8) + *(int *)(*(int *)(iVar2 + 0xc) + 0x1330) * 2;
    if (iVar2 == 0) {
      uVar4 = 0;
    }
    else {
      iVar3 = _Znaj(0x100);
      _Z21_ConvertUnicodeToUTF8PcPKt(iVar3,iVar2);
      iVar2 = _ZN11Application11GetInstanceEv();
      (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar2) + 0x5c))
                (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar2),iVar3);
      uVar4 = 0;
      if (iVar3 != 0) {
        _ZdaPv();
        uVar4 = 0;
      }
    }
  }
  else {
    iVar2 = _ZN11Application11GetInstanceEv();
    piVar5 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
    (**(code **)(*piVar5 + 0x14))(&piStack_18,piVar5,param_2,0,0);
    uVar4 = 0;
    if (piStack_18 != (int *)0x0) {
      (**(code **)(*piStack_18 + 0xc))(piStack_18,&uStack_1c,4);
      _ZN11CEncryption15PrepareForWriteEP13CMemoryStream
                (*(undefined4 *)(DAT_003eee04 + 0x3eed90),param_4);
      uStack_14 = param_4[2];
      (**(code **)(*piStack_18 + 0xc))(piStack_18,&uStack_14,4);
      (**(code **)(*piStack_18 + 0xc))(piStack_18,*param_4,uStack_14);
      piVar5 = piStack_18;
      piStack_18 = (int *)0x0;
      if ((piVar5 == (int *)0x0) ||
         (_ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(), piStack_18 == (int *)0x0))
      {
        uVar4 = 1;
      }
      else {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        uVar4 = 1;
      }
    }
  }
  return uVar4;
}


