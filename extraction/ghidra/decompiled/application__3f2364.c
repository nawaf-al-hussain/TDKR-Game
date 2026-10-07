// _ZN11Application12SetTargetFPSEi @ 003f2364

void _ZN11Application12SetTargetFPSEi(int param_1,undefined4 param_2)

{
  float fVar1;
  uint in_fpscr;
  float fVar2;
  
  fVar1 = DAT_003f238c;
  fVar2 = (float)VectorSignedToFloat(param_2,(byte)(in_fpscr >> 0x16) & 3);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_size + param_1) = param_2;
  *(float *)(&__DT_SYMTAB[0x1df].st_info + param_1) = fVar1 / fVar2;
  return;
}


