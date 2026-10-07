// _ZN11Application21GetLanguageFromDeviceEv @ 003ead60

void _ZN11Application21GetLanguageFromDeviceEv(int param_1)

{
  int iVar1;
  uint uVar2;
  int *piVar3;
  char acStack_24 [16];
  int local_14;
  
  piVar3 = *(int **)(DAT_003eafd8 + 0x3ead7c);
  local_14 = *piVar3;
  _ZN3glf23AndroidGetPhoneLanguageEPc(acStack_24);
  iVar1 = strcmp(acStack_24,(char *)(DAT_003eafdc + 0x3ead94));
  if (iVar1 == 0) {
    *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 0;
    uVar2 = 0;
  }
  else {
    iVar1 = strcmp(acStack_24,(char *)(DAT_003eafe8 + 0x3eadec));
    if (iVar1 == 0) {
      uVar2 = 2;
      *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 2;
    }
    else {
      iVar1 = strcmp(acStack_24,(char *)(DAT_003eafec + 0x3eae1c));
      if (iVar1 == 0) {
        uVar2 = 1;
        *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 1;
      }
      else {
        iVar1 = strcmp(acStack_24,(char *)(DAT_003eaff0 + 0x3eae34));
        if (iVar1 == 0) {
          uVar2 = 4;
          *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 4;
        }
        else {
          iVar1 = strcmp(acStack_24,(char *)(DAT_003eaff4 + 0x3eae7c));
          if (iVar1 == 0) {
            uVar2 = 3;
            *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 3;
          }
          else {
            iVar1 = strncmp(acStack_24,(char *)(DAT_003eaff8 + 0x3eae98),2);
            if (iVar1 == 0) {
              uVar2 = 6;
              *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 6;
            }
            else {
              iVar1 = strncmp(acStack_24,(char *)(DAT_003eaffc + 0x3eaee4),2);
              if (iVar1 == 0) {
                uVar2 = 7;
                *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 7;
              }
              else {
                iVar1 = strncmp(acStack_24,(char *)(DAT_003eb000 + 0x3eaf18),2);
                if (iVar1 == 0) {
                  uVar2 = 8;
                  *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 8;
                }
                else {
                  iVar1 = strncmp(acStack_24,(char *)(DAT_003eb004 + 0x3eaf4c),2);
                  if (iVar1 == 0) {
                    uVar2 = 5;
                    *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 5;
                  }
                  else {
                    iVar1 = strncmp(acStack_24,(char *)(DAT_003eb008 + 0x3eaf80),2);
                    if (iVar1 == 0) {
                      uVar2 = 9;
                      *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 9;
                    }
                    else {
                      uVar2 = *(uint *)(&__DT_SYMTAB[0x1ef].st_info + param_1);
                      if (9 < uVar2) {
                        *(undefined4 *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = 0;
                        strncpy((char *)(DAT_003eb00c + 0x3eafd0),acStack_24,2);
                        goto LAB_003eadc4;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  strcpy((char *)(DAT_003eafe4 + 0x3eadc0),*(char **)(DAT_003eafe0 + 0x3eadbc + uVar2 * 4));
LAB_003eadc4:
  if (local_14 == *piVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


