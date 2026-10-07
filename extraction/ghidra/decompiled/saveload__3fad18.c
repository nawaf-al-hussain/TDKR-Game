// _ZN14AnalogJoystick8SaveLoadEP13CMemoryStreamf @ 003fad18

undefined4
_ZN14AnalogJoystick8SaveLoadEP13CMemoryStreamf(int *param_1,undefined4 param_2,float param_3)

{
  uint in_fpscr;
  float fVar1;
  short local_1c;
  short local_1a [3];
  
  _ZN13CMemoryStream4ReadERs(param_2,&local_1c);
  _ZN13CMemoryStream4ReadERs(param_2,local_1a);
  fVar1 = (float)VectorSignedToFloat((int)local_1c,(byte)(in_fpscr >> 0x16) & 3);
  (**(code **)(*param_1 + 0x44))(param_1,(int)(short)(int)(param_3 * fVar1));
  fVar1 = (float)VectorSignedToFloat((int)local_1a[0],(byte)(in_fpscr >> 0x16) & 3);
  (**(code **)(*param_1 + 0x48))(param_1,(int)(short)(int)(param_3 * fVar1));
  return 1;
}


