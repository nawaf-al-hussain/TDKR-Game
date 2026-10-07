// _ZN11Application6ResumeEv @ 003f4d20

void _ZN11Application6ResumeEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  float fVar4;
  float extraout_r0;
  int iVar5;
  uint *puVar6;
  uint in_fpscr;
  float __x;
  double dVar7;
  double dVar8;
  double dVar9;
  undefined8 uVar10;
  int local_68;
  int local_64;
  timeval local_60;
  undefined1 auStack_58 [60];
  
  iVar1 = _ZN11Application11GetInstanceEv();
  iVar5 = DAT_003f4fcc + 0x3f4d48;
  if (*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) == 0) {
    *(undefined1 *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1 + 2) = 0;
    **(undefined4 **)(iVar5 + DAT_003f4fe4) = 0;
  }
  else {
    if (*(char *)(DAT_003f4fd0 + 0x3f4d5c) != '\0') {
      *(char *)(DAT_003f4fd0 + 0x3f4d5c) = '\0';
      uVar2 = _ZN3glf24AndroidGLLiveGetUsernameEv();
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                (&local_68,uVar2);
      uVar2 = _ZN3glf24AndroidGLLiveGetPasswordEv();
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                (&local_64,uVar2);
      if (1 < (uint)(*(int *)(local_64 + -0xc) + *(int *)(local_68 + -0xc))) {
        _ZN17FederationManager13OnGLLiveLoginEv(**(undefined4 **)(iVar5 + DAT_003f4fec));
      }
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&local_64);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&local_68);
    }
    iVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
    if (iVar1 != 0) {
      if (*(int *)(DAT_003f4fd4 + 0x3f4d7c) != 0) {
        _ZN13CMemoryStreamC1Ei(auStack_58,0x400);
        iVar1 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                          (param_1,DAT_003f4fd8 + 0x3f4da0,3,auStack_58);
        if (iVar1 != 0) {
          *(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1) = 0;
          uVar2 = _ZN13CMemoryStream7ReadIntEv(auStack_58);
          *(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1) = uVar2;
          fVar4 = (float)_ZN13CMemoryStream9ReadFloatEv(auStack_58);
          uVar2 = _ZN3glf22AndroidGetMillisecondsEv();
          VectorSignedToFloat(uVar2,(byte)(in_fpscr >> 0x16) & 3);
          ceilf(__x);
          iVar1 = (int)(extraout_r0 - fVar4);
          if (iVar1 < 1) {
            iVar1 = 1;
          }
          *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1) = iVar1;
        }
        _ZN13CMemoryStreamD2Ev(auStack_58);
      }
      iVar1 = _ZN11Application11GetInstanceEv();
      uVar2 = (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 100))
                        (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1),0);
      iVar1 = _ZN11Application11GetInstanceEv();
      uVar3 = (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x68))();
      _ZN4glot15TrackingManager14setIdentifiersEPKcS2_(uVar2,uVar3);
      _ZN4glot15TrackingManager11GetInstanceEv();
      _ZN4glot15TrackingManager17updateIdentifiersEv();
      _ZN11Application23SendTrackingEventResumeEi(param_1,0);
    }
    puVar6 = (uint *)(DAT_003f4fdc + 0x3f4e20);
    gettimeofday(&local_60,(__timezone_ptr_t)0x0);
    if (((*puVar6 & 1) == 0) && (iVar1 = __cxa_guard_acquire(puVar6), iVar1 != 0)) {
      uVar10 = VectorSignedToFloat(local_60.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
      *(undefined8 *)(DAT_003f4fe8 + 0x3f4eb8) = uVar10;
      __cxa_guard_release(puVar6);
    }
    dVar7 = (double)VectorSignedToFloat(local_60.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
    dVar8 = *(double *)(DAT_003f4fe0 + 0x3f4e44);
    *(undefined1 *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1 + 2) = 0;
    dVar9 = (double)VectorSignedToFloat(local_60.tv_usec,(byte)(in_fpscr >> 0x16) & 3);
    *(float *)(&__DT_SYMTAB[0x1ed].st_info + param_1) =
         (float)((dVar9 + (dVar7 - dVar8) * DAT_003f4fb8) * DAT_003f4fc0);
    **(undefined4 **)(iVar5 + DAT_003f4fe4) = 0;
  }
  return;
}


