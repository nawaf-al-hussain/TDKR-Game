// _ZNK6glitch7collada20CAnimationDictionary13resolveClipIDERKN5boost13intrusive_ptrINS0_13CAnimationSetEEEiPKc @ 0076d994

int _ZNK6glitch7collada20CAnimationDictionary13resolveClipIDERKN5boost13intrusive_ptrINS0_13CAnimationSetEEEiPKc
              (undefined4 param_1,int *param_2,int param_3,char *param_4)

{
  undefined4 *puVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  int iVar6;
  char *pcVar7;
  
  if (param_4 == (char *)0x0) {
    return 0;
  }
  if (*param_4 == '\0') {
    return 0;
  }
  param_3 = param_3 * 0x14;
  iVar3 = *(int *)(*param_2 + 0x44);
  iVar4 = *(int *)(iVar3 + param_3);
  iVar6 = *(int *)(*(int *)(*(int *)(iVar4 + 0x10) + 0x20) + 0x38);
  pcVar7 = param_4;
  if (0 < iVar6) {
    iVar4 = 0;
    do {
      puVar1 = (undefined4 *)
               _ZNK6glitch7collada16CColladaDatabase16getAnimationClipEi(iVar3 + param_3,iVar4);
      iVar2 = strcmp(param_4,(char *)*puVar1);
      if (iVar2 == 0) {
        return iVar4;
      }
      iVar4 = iVar4 + 1;
    } while (iVar4 != iVar6);
    iVar4 = *(int *)(*(int *)(*param_2 + 0x44) + param_3);
  }
  uVar5 = 0;
  if (iVar4 != 0) {
    uVar5 = *(undefined4 *)(iVar4 + 0xc);
  }
  _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(3,DAT_00799cf0 + 0x799ce4,param_4,uVar5,pcVar7);
  return 0;
}


