// _ZN11Application13SetScreenSizeEii @ 003ee784

void _ZN11Application13SetScreenSizeEii(undefined4 param_1,uint param_2,int param_3)

{
  int *piVar1;
  undefined4 *puVar2;
  uint in_fpscr;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  undefined4 local_20;
  uint local_1c;
  
  puVar2 = *(undefined4 **)(DAT_003ee888 + 0x3ee7a4);
  _ZN14GameEngineBase10SetScreenWEi(*puVar2);
  _ZN14GameEngineBase10SetScreenHEi(*puVar2,param_3);
  fVar3 = (float)VectorSignedToFloat(param_2,(byte)(in_fpscr >> 0x16) & 3);
  fVar4 = (float)VectorSignedToFloat(*(undefined4 *)(DAT_003ee88c + 0x3ee7c8),
                                     (byte)(in_fpscr >> 0x16) & 3);
  fVar6 = (float)VectorSignedToFloat(*(undefined4 *)(DAT_003ee890 + 0x3ee7d4),
                                     (byte)(in_fpscr >> 0x16) & 3);
  fVar5 = (float)VectorSignedToFloat(param_3,(byte)(in_fpscr >> 0x16) & 3);
  fVar3 = fVar3 / fVar4;
  fVar5 = fVar5 / fVar6;
  _ZN14GameEngineBase15SetScreenScaleWEf(*puVar2,fVar3);
  _ZN14GameEngineBase15SetScreenScaleHEf(*puVar2,fVar5);
  _ZN14GameEngineBase19SetScreenScaleHperWEf(*puVar2,fVar5 / fVar3);
  _ZN14GameEngineBase19SetScreenScaleWperHEf(*puVar2,fVar3 / fVar5);
  piVar1 = (int *)**(int **)(DAT_003ee894 + 0x3ee830);
  if (piVar1 != (int *)0x0) {
    local_1c = param_2 & 0xffff | param_3 << 0x10;
    *(undefined2 *)(piVar1 + 6) = 0;
    *(undefined2 *)((int)piVar1 + 0x1a) = 0;
    *(short *)(piVar1 + 7) = (short)param_2;
    *(short *)((int)piVar1 + 0x1e) = (short)param_3;
    local_20 = 0;
    (**(code **)(*piVar1 + 0x1c))(piVar1,&local_20);
  }
  return;
}


