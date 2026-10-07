// _ZN11Application20SetLogicalScreenSizeEv @ 003ee898

void _ZN11Application20SetLogicalScreenSizeEv(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int *piVar3;
  undefined4 *puVar4;
  uint in_fpscr;
  float fVar5;
  float fVar6;
  float fVar7;
  
  piVar3 = *(int **)(DAT_003ee94c + 0x3ee8b0);
  puVar4 = (undefined4 *)(DAT_003ee950 + 0x3ee8b4);
  uVar1 = _ZN14GameEngineBase10GetScreenWEv(*piVar3);
  uVar2 = _ZN14GameEngineBase10GetScreenHEv(*piVar3);
  fVar5 = (float)VectorSignedToFloat(uVar1,(byte)(in_fpscr >> 0x16) & 3);
  fVar6 = (float)VectorSignedToFloat(*(undefined4 *)(DAT_003ee954 + 0x3ee8d8),
                                     (byte)(in_fpscr >> 0x16) & 3);
  fVar7 = (float)VectorSignedToFloat(*puVar4,(byte)(in_fpscr >> 0x16) & 3);
  fVar5 = fVar5 / fVar6;
  fVar6 = (float)VectorSignedToFloat(uVar2,(byte)(in_fpscr >> 0x16) & 3);
  fVar6 = fVar6 / fVar7;
  _ZN14GameEngineBase17SetLogicalScreenWEi(*piVar3,*(undefined4 *)(DAT_003ee954 + 0x3ee8d8));
  _ZN14GameEngineBase17SetLogicalScreenHEi(*piVar3,*puVar4);
  _ZN14GameEngineBase15SetScreenScaleWEf(*piVar3,fVar5);
  _ZN14GameEngineBase15SetScreenScaleHEf(*piVar3,fVar6);
  _ZN14GameEngineBase19SetScreenScaleHperWEf(*piVar3,fVar6 / fVar5);
  *(float *)(*piVar3 + 0xa4) = fVar5 / fVar6;
  return;
}


