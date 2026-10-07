// _ZN11Application19InitTrackingManagerEv @ 003ec098

void _ZN11Application19InitTrackingManagerEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  void *__s;
  int iVar4;
  int *piVar5;
  int *local_1c [2];
  
  iVar1 = _ZN11Application11GetInstanceEv();
  uVar2 = (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 100))
                    (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1),0);
  iVar1 = _ZN11Application11GetInstanceEv();
  uVar3 = (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x68))();
  _ZN4glot15TrackingManager14setIdentifiersEPKcS2_(uVar2,uVar3);
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar5 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
  (**(code **)(*piVar5 + 0xc))(local_1c,piVar5,DAT_003ec1ec + 0x3ec108);
  iVar1 = (**(code **)(*local_1c[0] + 0x20))();
  __s = (void *)_Z11CustomAllocjPKci(iVar1 + 1U,DAT_003ec1f0 + 0x3ec13c,0x701);
  *(void **)((int)&__DT_SYMTAB[0x1e0].st_value + param_1) = __s;
  memset(__s,0,iVar1 + 1U);
  (**(code **)(*local_1c[0] + 0xc))
            (local_1c[0],*(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_value + param_1),iVar1);
  piVar5 = local_1c[0];
  local_1c[0] = (int *)0x0;
  if (piVar5 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  iVar4 = atoi((char *)(DAT_003ec1f4 + 0x3ec194));
  uVar2 = _Z11CustomAllocjPKci(0xf0,DAT_003ec1f8 + 0x3ec1a4,0x707);
  _ZN4glot15TrackingManagerC1EPKciNS_20trackingServerConfigEPcj
            (uVar2,DAT_003ec1fc + 0x3ec1d0,iVar4,1,
             *(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_value + param_1),iVar1);
  if (local_1c[0] != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  return;
}


