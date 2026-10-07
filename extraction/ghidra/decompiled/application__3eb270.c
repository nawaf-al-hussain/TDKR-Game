// _ZN11Application12InitFromLogoEv @ 003eb270

void _ZN11Application12InitFromLogoEv(void)

{
  undefined4 uVar1;
  int iVar2;
  float fVar3;
  float *pfVar4;
  undefined4 in_r3;
  int *piVar5;
  int *piVar6;
  float fVar7;
  
  piVar6 = *(int **)(DAT_003eb2e8 + 0x3eb288);
  piVar5 = *(int **)(DAT_003eb2ec + 0x3eb28c);
  _ZN15VoxSoundManager14SetSoundVolumeEif
            (*piVar5,0xffc,*(undefined4 *)(*piVar6 + 0x24),*piVar6,in_r3);
  _ZN15VoxSoundManager14SetSoundVolumeEif(*piVar5,0xf000,*(undefined4 *)(*piVar6 + 0x28));
  _ZN15VoxSoundManager14SetSoundVolumeEif
            (*piVar5,2,**(float **)(DAT_003eb2f0 + 0x3eb2c0) * *(float *)(*piVar6 + 0x2c));
  iVar2 = *piVar5;
  fVar3 = *(float *)(*piVar6 + 0x30);
  if (*(char *)(iVar2 + 0x14) == '\0') {
    uVar1 = *(undefined4 *)(iVar2 + 0xc);
    fVar7 = fVar3;
  }
  else {
    uVar1 = *(undefined4 *)(iVar2 + 0xc);
    fVar7 = 0.0;
  }
  _ZN3vox9VoxEngine13SetMasterGainEff(uVar1,fVar7,0);
  if (**(int **)(DAT_0031c668 + 0x31c5d0) != 0) {
    pfVar4 = (float *)(**(int **)(DAT_0031c668 + 0x31c5d0) + 0x474);
    fVar7 = fVar3 * *pfVar4;
    *pfVar4 = fVar7;
    if (1.0 < fVar7) {
      *pfVar4 = 1.0;
    }
    else if (fVar7 < 0.0) {
      *pfVar4 = 0.0;
    }
  }
  if (**(int **)(DAT_0031c66c + 0x31c60c) != 0) {
    pfVar4 = (float *)(**(int **)(DAT_0031c66c + 0x31c60c) + 0x474);
    fVar3 = fVar3 * *pfVar4;
    *pfVar4 = fVar3;
    if (1.0 < fVar3) {
      *pfVar4 = 1.0;
    }
    else if (fVar3 < 0.0) {
      *pfVar4 = 0.0;
    }
  }
  return;
}


