// _ZNK23CComponentBuiltinSkyBox5CloneEv @ 003cec1c

int * _ZNK23CComponentBuiltinSkyBox5CloneEv(int param_1)

{
  int *piVar1;
  int iVar2;
  
  piVar1 = (int *)_Znwj(0x10);
  *piVar1 = DAT_003cec60 + 0x3cec44;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (piVar1 + 1,param_1 + 4);
  iVar2 = *(int *)(param_1 + 0xc);
  *(undefined1 *)(piVar1 + 2) = *(undefined1 *)(param_1 + 8);
  piVar1[3] = iVar2;
  return piVar1;
}

