// _ZN11Application17InitShaderOptionsEv @ 003ec200

void _ZN11Application17InitShaderOptionsEv(void)

{
  char cVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  int *piVar5;
  undefined4 local_14 [2];
  
  iVar2 = _ZN11Application11GetInstanceEv();
  iVar4 = DAT_003ec618;
  iVar2 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (local_14,DAT_003ec614 + 0x3ec224);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (local_14,DAT_003ec61c + 0x3ec240);
  piVar5 = *(int **)(iVar4 + 0x3ec248);
  iVar4 = *piVar5;
  if (*(int *)(iVar4 + 0x2c) == 0) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec620 + 0x3ec264);
    iVar4 = *piVar5;
  }
  else if (*(int *)(iVar4 + 0x2c) == 1) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec634 + 0x3ec3f0);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x30);
    goto joined_r0x003ec3fc;
  }
  cVar1 = *(char *)(iVar4 + 0x30);
joined_r0x003ec3fc:
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x31);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec638 + 0x3ec410);
    cVar1 = *(char *)(*piVar5 + 0x31);
  }
  if (cVar1 == '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec63c + 0x3ec430);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x32);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec624 + 0x3ec290);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x32);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x33);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec640 + 0x3ec450);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x33);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x39);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec644 + 0x3ec470);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x39);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x24);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec648 + 0x3ec490);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x24);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x36);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec64c + 0x3ec4b0);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x36);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x8c);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec650 + 0x3ec4d0);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x8c);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x38);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec654 + 0x3ec4f0);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x38);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x3a);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec658 + 0x3ec510);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x3a);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x35);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec65c + 0x3ec530);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x35);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x37);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec660 + 0x3ec550);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x37);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x34);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec664 + 0x3ec570);
    iVar4 = *piVar5;
    cVar1 = *(char *)(iVar4 + 0x34);
  }
  if (cVar1 == '\0') {
    cVar1 = *(char *)(iVar4 + 0x3d);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec668 + 0x3ec590);
    cVar1 = *(char *)(*piVar5 + 0x3d);
  }
  if (cVar1 != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec66c + 0x3ec5b0);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (local_14,DAT_003ec628 + 0x3ec334);
  piVar3 = *(int **)(iVar2 + 0x144);
  (**(code **)(*piVar3 + 0xc))(piVar3,local_14[0],1);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
            (local_14,DAT_003ec62c + 0x3ec360,0);
  iVar4 = *piVar5;
  if (*(char *)(iVar4 + 0x25) != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec67c + 0x3ec60c);
    iVar4 = *piVar5;
  }
  if (*(char *)(iVar4 + 0x26) != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec678 + 0x3ec5f4);
    iVar4 = *piVar5;
  }
  if (*(char *)(iVar4 + 0x27) != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec674 + 0x3ec5dc);
    iVar4 = *piVar5;
  }
  if (*(char *)(iVar4 + 0x28) != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec670 + 0x3ec5c4);
    iVar4 = *piVar5;
  }
  if (*(char *)(iVar4 + 0x29) != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
              (local_14,DAT_003ec630 + 0x3ec3b0);
  }
  piVar5 = *(int **)(iVar2 + 0x144);
  (**(code **)(*piVar5 + 0xc))(piVar5,local_14[0],2);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (local_14);
  return;
}


