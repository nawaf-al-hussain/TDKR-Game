// _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc @ 0076d70c

void _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
               (undefined4 param_1,int param_2,char *param_3)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  char *pcVar4;
  undefined4 uVar5;
  char *pcVar6;
  int *piVar7;
  char *pcVar8;
  int iVar9;
  code *pcVar10;
  int iVar11;
  int iVar12;
  int *piVar13;
  char *local_830;
  undefined1 auStack_82c [4];
  char *local_828;
  undefined1 auStack_824 [1024];
  undefined1 auStack_424 [1024];
  int local_24;
  
  piVar7 = *(int **)(DAT_0076d980 + 0x76d734);
  iVar11 = *(int *)(*(int *)(param_2 + 0x20) + 4);
  pcVar8 = *(char **)(DAT_0076d984 + 0x76d73c);
  local_24 = *piVar7;
  local_830 = pcVar8 + 0xc;
  if (iVar11 != 0) {
    iVar12 = *(int *)(*(int *)(param_2 + 0x20) + 8);
    iVar9 = 0;
LAB_0076d768:
    iVar2 = strcmp(*(char **)(iVar12 + iVar9 * 8),param_3);
    if (iVar2 != 0) goto LAB_0076d75c;
    uVar5 = 0;
    if (*(int *)(param_2 + 0xc) != 0) {
      uVar5 = *(undefined4 *)(*(int *)(param_2 + 0xc) + 0xc);
    }
    _ZN3glf9VJoinPathEPcjjz
              (auStack_824,0x400,3,uVar5,DAT_0076d988 + 0x76d798,
               *(undefined4 *)(iVar12 + iVar9 * 8 + 4));
    _ZN3glf13NormalizePathEPcjPKc(auStack_424,0x400,auStack_824);
    piVar13 = *(int **)(*(int *)(**(int **)(DAT_0076d98c + 0x76d7d8) + 0x20) + 0x28);
    pcVar10 = *(code **)(*piVar13 + 0x38);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1119
              (auStack_82c,auStack_424);
    (*pcVar10)(&local_828,piVar13,auStack_82c);
    pcVar6 = local_830 + -0xc;
    pcVar4 = local_830;
    if (local_828 + -0xc != pcVar6) {
      if (*(int *)(local_828 + -4) < 0) {
        local_828 = (char *)_ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE4_Rep7_M_grabERKS6_SA__isra_1110_part_1111
                                      ();
        pcVar6 = local_830 + -0xc;
      }
      else if (local_828 + -0xc != pcVar8) {
        piVar13 = (int *)(local_828 + -4);
        DataMemoryBarrier(0xf);
        do {
          bVar1 = (bool)hasExclusiveAccess(piVar13);
        } while (!bVar1);
        *piVar13 = *piVar13 + 1;
        DataMemoryBarrier(0xf);
        pcVar6 = local_830 + -0xc;
      }
      pcVar4 = local_828;
      if (pcVar6 != pcVar8) {
        piVar13 = (int *)(local_830 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar11 = *piVar13;
          bVar1 = (bool)hasExclusiveAccess(piVar13);
        } while (!bVar1);
        *piVar13 = iVar11 + -1;
        DataMemoryBarrier(0xf);
        if (iVar11 < 1) {
          _Z10GlitchFreePv(pcVar6);
        }
      }
    }
    local_830 = pcVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (&local_828);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_82c);
  }
LAB_0076d848:
  pcVar8 = local_830;
  iVar9 = *(int *)(*(int *)(param_2 + 0x24) + 0x44);
  iVar11 = (*(int *)(*(int *)(param_2 + 0x24) + 0x48) - iVar9 >> 2) * -0x33333333;
  if (0 < iVar11) {
    iVar2 = 0;
    iVar12 = 0;
    do {
      iVar3 = *(int *)(iVar9 + iVar2);
      pcVar4 = (char *)0x0;
      if (iVar3 != 0) {
        pcVar4 = *(char **)(iVar3 + 0xc);
      }
      iVar3 = strcmp(pcVar8,pcVar4);
      if (iVar3 == 0) goto LAB_0076d8d4;
      iVar12 = iVar12 + 1;
      iVar2 = iVar2 + 0x14;
    } while (iVar12 != iVar11);
  }
  iVar12 = 0;
  _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(3,DAT_0076d990 + 0x76d8d4,param_3);
LAB_0076d8d4:
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_830);
  if (local_24 == *piVar7) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(iVar12);
LAB_0076d75c:
  iVar9 = iVar9 + 1;
  if (iVar11 == iVar9) goto LAB_0076d848;
  goto LAB_0076d768;
}


