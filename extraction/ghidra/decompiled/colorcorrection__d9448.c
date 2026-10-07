// _ZN3glf3App26GetColorCorrectionSettingsEv @ 000d9448

void _ZN3glf3App26GetColorCorrectionSettingsEv(undefined4 *param_1,int param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x140].st_size + param_2);
  uVar1 = *(undefined4 *)((int)&__DT_SYMTAB[0x141].st_name + param_2);
  param_1[1] = *(undefined4 *)(&__DT_SYMTAB[0x140].st_info + param_2);
  *param_1 = uVar2;
  param_1[2] = uVar1;
  return;
}


