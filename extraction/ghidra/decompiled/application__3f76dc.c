// _ZN11Application17ClearTextureSpaceEv @ 003f76dc

void _ZN11Application17ClearTextureSpaceEv(int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  int *__src;
  int iVar3;
  int *piVar4;
  int *__dest;
  int *piVar5;
  int *apiStack_24 [2];
  
  puVar1 = *(undefined4 **)(*(int *)(*(int *)((int)&__DT_SYMTAB[0x1e6].st_size + param_1) + 8) + 8);
  _ZN3glf18ReadWriteMutexLock9writeLockEj(puVar1 + 6);
  __dest = (int *)*puVar1;
  piVar4 = (int *)puVar1[1];
  while (__dest != piVar4) {
    if (*(char *)(*__dest + 8) == '\0') {
      iVar2 = (**(code **)(**(int **)(*(int *)(*__dest + 0x18) + 0xc) + 0x3c))();
      if (iVar2 == 0) {
        __dest = __dest + 1;
        piVar4 = (int *)puVar1[1];
      }
      else {
        piVar4 = (int *)puVar1[1];
        __src = __dest + 1;
        piVar5 = (int *)*__dest;
        if ((__src != piVar4) && (iVar2 = (int)piVar4 - (int)__src >> 2, iVar2 != 0)) {
          memmove(__dest,__src,iVar2 << 2);
          piVar4 = (int *)puVar1[1];
        }
        piVar4 = piVar4 + -1;
        puVar1[1] = piVar4;
        if (piVar5 != (int *)0x0) {
          iVar2 = piVar5[6];
          if ((*(byte *)(iVar2 + 0x2c) & 8) != 0) {
            apiStack_24[0] = piVar5;
            _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar5 + 1);
            (**(code **)(*apiStack_24[0] + 8))(apiStack_24[0],0,1,0);
            *(ushort *)(apiStack_24[0][6] + 0x2a) = *(ushort *)(apiStack_24[0][6] + 0x2a) & 0xfffe;
            _ZN6glitch5video8ITexture6unbindEjj(apiStack_24[0],4,0);
            _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(apiStack_24);
            iVar2 = piVar5[6];
          }
          iVar2 = _ZN6glitch5video12pixel_format18computeSizeInBytesENS0_14E_PIXEL_FORMATEjjjhb
                            ((*(uint *)(iVar2 + 0x24) & 0xfff) >> 6,piVar5[7],piVar5[8],piVar5[9],
                             *(undefined1 *)(iVar2 + 0x2f),0);
          piVar4 = (int *)puVar1[1];
          if ((*(uint *)(piVar5[6] + 0x24) & 7) == 3) {
            iVar3 = 6;
          }
          else {
            iVar3 = 1;
          }
          puVar1[4] = puVar1[4] - iVar2 * iVar3;
        }
      }
    }
    else {
      __dest = __dest + 1;
    }
  }
  _ZN3glf18ReadWriteMutexLock11writeUnlockEv(puVar1 + 6);
  return;
}


