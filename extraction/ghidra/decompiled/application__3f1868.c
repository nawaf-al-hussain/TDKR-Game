// _ZN11Application17UpdateOrientationEv @ 003f1868

void _ZN11Application17UpdateOrientationEv(int param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  
  iVar1 = _ZNK3glf3App19GetCreationSettingsEv();
  if (*(char *)(iVar1 + 0x41) != '\0') {
    return;
  }
  iVar1 = _ZN11Application11GetInstanceEv();
  iVar3 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  iVar1 = _ZNK3glf3App14GetOrientationEv(param_1);
  if (*(int *)((int)&__DT_SYMTAB[0x1e9].st_size + param_1) != iVar1) {
    if (iVar1 == 4) {
      piVar2 = (int *)**(int **)(iVar3 + 0x11c);
      if (piVar2[0xe] != 3) {
        (**(code **)(*piVar2 + 0x18))(piVar2,3);
      }
    }
    else if ((iVar1 == 8) && (piVar2 = (int *)**(int **)(iVar3 + 0x11c), piVar2[0xe] != 1)) {
      (**(code **)(*piVar2 + 0x18))(piVar2,1);
    }
  }
  *(int *)((int)&__DT_SYMTAB[0x1e9].st_size + param_1) = iVar1;
  return;
}


