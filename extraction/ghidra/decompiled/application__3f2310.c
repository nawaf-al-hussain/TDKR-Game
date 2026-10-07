// _ZN11Application19UnRegisterForUpdateEP10IUpdatable @ 003f2310

void _ZN11Application19UnRegisterForUpdateEP10IUpdatable(int param_1,int param_2)

{
  undefined4 *puVar1;
  
  if (param_2 == 0) {
    return;
  }
  puVar1 = *(undefined4 **)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
  while( true ) {
    if ((undefined4 *)((int)&__DT_SYMTAB[0x1de].st_value + param_1) == puVar1) {
      return;
    }
    if (param_2 == puVar1[2]) break;
    puVar1 = (undefined4 *)*puVar1;
  }
  _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar1);
  if (puVar1 == (undefined4 *)0x0) {
    return;
  }
  (*(code *)PTR_free_00c18adc)();
  return;
}


