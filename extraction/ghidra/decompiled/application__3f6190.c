// _ZN11Application11GetRealTimeEv @ 003f6190

float _ZN11Application11GetRealTimeEv(void)

{
  int iVar1;
  uint *puVar2;
  uint in_fpscr;
  double dVar3;
  double dVar4;
  undefined8 uVar5;
  timeval local_10;
  
  puVar2 = (uint *)(DAT_003f6238 + 0x3f61ac);
  gettimeofday(&local_10,(__timezone_ptr_t)0x0);
  if (((*puVar2 & 1) == 0) && (iVar1 = __cxa_guard_acquire(puVar2), iVar1 != 0)) {
    uVar5 = VectorSignedToFloat(local_10.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
    *(undefined8 *)(DAT_003f6240 + 0x3f6220) = uVar5;
    __cxa_guard_release(puVar2);
  }
  dVar3 = (double)VectorSignedToFloat(local_10.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
  dVar4 = (double)VectorSignedToFloat(local_10.tv_usec,(byte)(in_fpscr >> 0x16) & 3);
  return (float)((dVar4 + (dVar3 - *(double *)(DAT_003f623c + 0x3f61d0)) * DAT_003f6228) *
                DAT_003f6230);
}


