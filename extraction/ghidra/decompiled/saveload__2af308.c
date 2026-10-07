// _ZN18CStateSetComponent8SaveLoadEP13CMemoryStream @ 002af308

void _ZN18CStateSetComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint in_fpscr;
  float fVar4;
  undefined4 uVar5;
  int local_24;
  undefined1 auStack_20 [12];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  local_24 = *(int *)(DAT_002af410 + 0x2af338) + 0xc;
  _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_24);
  iVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (*(char *)(*(int *)(param_1 + 4) + 0xed) == '\0') {
    _ZN18CStateSetComponent11GetStateIdxEPKc(auStack_20,param_1,local_24);
    _ZN18CStateSetComponent22SetStateWithTransitionERK9SStateIdxsfiiP17CContainerTrigger
              (param_1,auStack_20,1,0,0xffffffff,0xffffffff,0);
    iVar2 = _ZN18CStateSetComponent8GetStateERK9SStateIdx(param_1,param_1 + 0xd8);
    if (iVar2 == 0) {
      iVar3 = *(int *)(*(int *)(param_1 + 4) + 0x98);
    }
    else {
      iVar3 = *(int *)(*(int *)(param_1 + 4) + 0x98);
      if ((*(uint *)(iVar2 + 4) & 0x100) != 0) {
        in_fpscr = in_fpscr & 0xfffffff | (uint)(*(float *)(iVar3 + 0x4c) == 0.0) << 0x1e;
        if (SUB41(in_fpscr >> 0x1e,0)) {
          fVar4 = *(float *)(iVar3 + 0x40);
        }
        else {
          fVar4 = *(float *)(iVar3 + 0x40) / *(float *)(iVar3 + 0x4c);
        }
        iVar1 = (int)fVar4;
      }
    }
    uVar5 = VectorSignedToFloat(iVar1,(byte)(in_fpscr >> 0x16) & 3);
    _ZN19CAnimationComponent23SetCurrentAnimationTimeEif(iVar3,0,uVar5);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_24);
  return;
}


