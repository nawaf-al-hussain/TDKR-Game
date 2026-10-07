// _ZN11Application4InitERN3glf16CreationSettingsE @ 003ee48c

int _ZN11Application4InitERN3glf16CreationSettingsE(int param_1,undefined4 *param_2)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  uint uVar6;
  undefined4 *puVar7;
  int iVar8;
  uint in_fpscr;
  float fVar9;
  float fVar10;
  float fVar11;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  uint local_2c;
  
  uVar2 = _ZN11Application11GetInstanceEv();
  iVar8 = DAT_003ee764 + 0x3ee4c0;
  _Z11CustomAllocjPKci(0xb8,DAT_003ee760 + 0x3ee4b8,0x90);
  _ZN13DeviceOptionsC1Ev();
  _ZN13DeviceOptions11SetProfilesEiii
            (**(undefined4 **)(iVar8 + DAT_003ee768),
             *(undefined4 *)((int)&__DT_SYMTAB[0x1eb].st_size + param_1),
             *(undefined4 *)(&__DT_SYMTAB[0x1eb].st_info + param_1),
             *(undefined4 *)((int)&__DT_SYMTAB[0x1ec].st_name + param_1));
  *(undefined1 *)(param_2 + 0xb) = 0x10;
  *(undefined1 *)((int)param_2 + 0x2d) = 0x18;
  cVar1 = *(char *)((int)&__DT_SYMTAB[0x1eb].st_name + param_1);
  *(undefined1 *)(param_2 + 0xe) = 1;
  *(undefined1 *)((int)param_2 + 0x13) = 1;
  if (cVar1 != '\0') {
    *(undefined1 *)(param_2 + 5) = 1;
  }
  param_2[0xf] = 1;
  *(undefined1 *)(param_2 + 4) = 0;
  *param_2 = 0;
  param_2[1] = 0;
  *(undefined1 *)((int)param_2 + 0x41) = 1;
  param_2[0x11] = 4;
  *(undefined1 *)(param_2 + 0xe) = 0;
  param_2[0x12] = 0xc;
  param_2[10] = 8;
  param_2[10] = 2;
  *(undefined4 *)((int)&__DT_SYMTAB[0x1e9].st_size + param_1) = 4;
  memcpy(param_2 + 0x13,(void *)(DAT_003ee76c + 0x3ee594),5);
  iVar3 = _ZN3glf3App4InitERNS_16CreationSettingsE(param_1,param_2);
  if (iVar3 == 0) {
    puVar7 = *(undefined4 **)(iVar8 + DAT_003ee770);
  }
  else {
    _ZNK3glf3App13GetScreenSizeERiS1_i(param_1,&local_38,&local_34,0);
    puVar7 = *(undefined4 **)(iVar8 + DAT_003ee770);
    _ZN14GameEngineBase10InitEngineEiPKciiiiffiiib
              (*puVar7,0,DAT_003ee780 + 0x3ee734,local_38,local_34,local_38,local_34,0x3f800000,
               0x3f800000,1,0x10,0x18,1);
  }
  iVar8 = DAT_003ee774;
  uVar4 = _ZN3glf3App5GetFsEv(uVar2);
  _ZN3glf3App11GetInstanceEv();
  _ZN3glf3App5GetFsEv();
  uVar5 = _ZN3glf2Fs10GetDataDirEv();
  _ZN3glf2Fs10SetHomeDirEPKc(uVar4,uVar5);
  uVar2 = _ZN3glf3App5GetFsEv(uVar2);
  _ZN3glf3App11GetInstanceEv();
  _ZN3glf3App5GetFsEv();
  uVar4 = _ZN3glf2Fs10GetDataDirEv();
  _ZN3glf2Fs10SetTempDirEPKc(uVar2,uVar4);
  _ZN11Application11GetInstanceEv();
  uVar2 = _ZN14GameEngineBase10GetScreenWEv(*puVar7);
  uVar4 = _ZN14GameEngineBase10GetScreenHEv(*puVar7);
  fVar9 = (float)VectorSignedToFloat(uVar2,(byte)(in_fpscr >> 0x16) & 3);
  fVar10 = (float)VectorSignedToFloat(*(undefined4 *)(DAT_003ee778 + 0x3ee62c),
                                      (byte)(in_fpscr >> 0x16) & 3);
  fVar11 = (float)VectorSignedToFloat(*(undefined4 *)(iVar8 + 0x3ee5c4),(byte)(in_fpscr >> 0x16) & 3
                                     );
  fVar9 = fVar9 / fVar10;
  fVar10 = (float)VectorSignedToFloat(uVar4,(byte)(in_fpscr >> 0x16) & 3);
  fVar10 = fVar10 / fVar11;
  _ZN14GameEngineBase17SetLogicalScreenWEi(*puVar7,*(undefined4 *)(DAT_003ee778 + 0x3ee62c));
  _ZN14GameEngineBase17SetLogicalScreenHEi(*puVar7,*(undefined4 *)(iVar8 + 0x3ee5c4));
  _ZN14GameEngineBase15SetScreenScaleWEf(*puVar7,fVar9);
  _ZN14GameEngineBase15SetScreenScaleHEf(*puVar7,fVar10);
  _ZN14GameEngineBase19SetScreenScaleHperWEf(*puVar7,fVar10 / fVar9);
  _ZN14GameEngineBase19SetScreenScaleWperHEf(*puVar7,fVar9 / fVar10);
  uVar6 = _ZN14GameEngineBase10GetScreenWEv(*puVar7);
  iVar8 = _ZN14GameEngineBase10GetScreenHEv(*puVar7);
  local_30 = 0;
  local_2c = uVar6 & 0xffff | iVar8 << 0x10;
  uVar2 = _Z11CustomAllocjPKci(0x24,DAT_003ee77c + 0x3ee6c8,0xa8a);
  _ZN11TouchScreenC1EN6glitch4core4rectIsEE(uVar2,&local_30);
  return iVar3;
}


