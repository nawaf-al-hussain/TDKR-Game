// _ZN11Application6UpdateEv @ 003f6244

void _ZN11Application6UpdateEv(int param_1)

{
  uint uVar1;
  byte bVar2;
  int iVar3;
  char *pcVar4;
  uint *puVar5;
  byte *pbVar6;
  uint in_fpscr;
  uint uVar7;
  double dVar8;
  double dVar9;
  float fVar12;
  float fVar13;
  double dVar10;
  undefined8 uVar11;
  float fVar14;
  timeval local_28;
  
  iVar3 = DAT_003f648c;
  if (*(char *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1 + 2) == '\0') {
    _ZN3glf3App6UpdateEv();
    puVar5 = (uint *)(iVar3 + 0x3f628c);
    gettimeofday(&local_28,(__timezone_ptr_t)0x0);
    if (((*puVar5 & 1) == 0) && (iVar3 = __cxa_guard_acquire(puVar5), iVar3 != 0)) {
      uVar11 = VectorSignedToFloat(local_28.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
      *(undefined8 *)(DAT_003f64a8 + 0x3f6440) = uVar11;
      __cxa_guard_release(puVar5);
    }
    dVar8 = (double)VectorSignedToFloat(local_28.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
    pbVar6 = &__DT_SYMTAB[0x1ee].st_info + param_1;
    pcVar4 = *(char **)((int)&__DT_SYMTAB[0x1f1].st_value + param_1);
    dVar9 = (double)VectorSignedToFloat(local_28.tv_usec,(byte)(in_fpscr >> 0x16) & 3);
    fVar14 = (float)((dVar9 + (dVar8 - *(double *)(DAT_003f6490 + 0x3f62b0)) * DAT_003f6478) *
                    DAT_003f6480);
    fVar12 = fVar14 - *(float *)(&__DT_SYMTAB[0x1ed].st_info + param_1);
    *(float *)(&__DT_SYMTAB[0x1ed].st_info + param_1) = fVar14;
    *(float *)pbVar6 = fVar12;
    fVar13 = DAT_003f6488;
    if (*pcVar4 == '\0') {
      uVar1 = in_fpscr & 0xfffffff | (uint)(fVar12 < DAT_003f6488) << 0x1f |
              (uint)(fVar12 == DAT_003f6488) << 0x1e;
      in_fpscr = uVar1 | (uint)(NAN(fVar12) || NAN(DAT_003f6488)) << 0x1c;
      bVar2 = (byte)(uVar1 >> 0x18);
      if (!(bool)(bVar2 >> 6 & 1) && bVar2 >> 7 == ((byte)(in_fpscr >> 0x1c) & 1)) {
        *(float *)pbVar6 = DAT_003f6488;
        fVar12 = fVar13;
      }
    }
    else {
      *(undefined4 *)pbVar6 = 0;
      fVar12 = 0.0;
    }
    *(float *)((int)&__DT_SYMTAB[0x1ee].st_size + param_1) =
         fVar12 + *(float *)((int)&__DT_SYMTAB[0x1ee].st_size + param_1);
    _ZN11Application9UpdateAppEv(param_1);
    _ZN12gxStateStack16DeleteStatesListEv(**(int **)(DAT_003f6494 + 0x3f632c) + 4);
    _ZN19MemoryDefragManager6UpdateEv();
    iVar3 = DAT_003f649c;
    fVar13 = *(float *)(DAT_003f6498 + 0x3f634c);
    uVar1 = in_fpscr & 0xfffffff | (uint)(fVar13 < 0.0) << 0x1f;
    uVar7 = uVar1 | (uint)NAN(fVar13) << 0x1c;
    if ((byte)(uVar1 >> 0x1f) == ((byte)(uVar7 >> 0x1c) & 1)) {
      *(float *)(DAT_003f6498 + 0x3f634c) = fVar13 - *(float *)pbVar6;
    }
    puVar5 = (uint *)(iVar3 + 0x3f6364);
    gettimeofday(&local_28,(__timezone_ptr_t)0x0);
    if (((*puVar5 & 1) == 0) && (iVar3 = __cxa_guard_acquire(puVar5), iVar3 != 0)) {
      uVar11 = VectorSignedToFloat(local_28.tv_sec,(byte)(uVar7 >> 0x16) & 3);
      *(undefined8 *)(DAT_003f64ac + 0x3f6470) = uVar11;
      __cxa_guard_release(puVar5);
    }
    fVar13 = *(float *)(&__DT_SYMTAB[0x1df].st_info + param_1);
    dVar8 = *(double *)(DAT_003f64a0 + 0x3f6390);
    _ZN3glf6Thread5SleepEj(1);
    if (*(char *)(DAT_003f64a4 + 0x3f63ac) == '\0') {
      dVar9 = (double)VectorSignedToFloat(local_28.tv_sec,(byte)(uVar7 >> 0x16) & 3);
      dVar10 = (double)VectorSignedToFloat(local_28.tv_usec,(byte)(uVar7 >> 0x16) & 3);
      fVar13 = (fVar14 + fVar13) - (float)((dVar10 + (dVar9 - dVar8) * DAT_003f6478) * DAT_003f6480)
      ;
      if (0.0 < fVar13) {
        _ZN3glf6Thread5SleepEj((int)fVar13);
      }
    }
  }
  return;
}


