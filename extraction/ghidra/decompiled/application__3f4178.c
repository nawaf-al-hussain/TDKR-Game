// _ZN11Application16ResetAllProgressEv @ 003f4178

void _ZN11Application16ResetAllProgressEv(int param_1)

{
  int iVar1;
  int *piVar2;
  char acStack_94 [128];
  int local_14;
  
  piVar2 = *(int **)(DAT_003f4224 + 0x3f4198);
  local_14 = *piVar2;
  sprintf(acStack_94,(char *)(DAT_003f4228 + 0x3f41a0),
          *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1));
  unlink(acStack_94);
  sprintf(acStack_94,(char *)(DAT_003f422c + 0x3f41cc),
          *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1));
  unlink(acStack_94);
  _ZN11Application23ResetGlobalDataFromFileEPKci_constprop_2441(param_1,DAT_003f4230 + 0x3f41e4);
  _ZN11Application23ResetGlobalDataFromFileEPKci_constprop_2441(param_1,DAT_003f4234 + 0x3f41f4);
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (iVar1 != 0) {
    _ZN6CLevel13ResetProgressEv();
  }
  if (local_14 == *piVar2) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(1);
}


