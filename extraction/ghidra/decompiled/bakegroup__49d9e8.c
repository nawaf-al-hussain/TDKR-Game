// _ZN18CTemplateBakeGroupD0Ev @ 0049d9e8

int * _ZN18CTemplateBakeGroupD0Ev(int *param_1)

{
  int iVar1;
  
  iVar1 = DAT_0049da48 + 0x49da0c;
  *param_1 = DAT_0049da44 + 0x49da04;
  param_1[0xd] = iVar1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x10);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0xe);
  iVar1 = DAT_0049da4c + 0x49da38;
  param_1[0xd] = iVar1;
  *param_1 = iVar1;
  _ZdlPv(param_1);
  return param_1;
}

