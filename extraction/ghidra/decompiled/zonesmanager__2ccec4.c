// _ZN13CZonesManager13ReqUnloadZoneEi @ 002ccec4

void _ZN13CZonesManager13ReqUnloadZoneEi(int param_1,undefined4 param_2)

{
  undefined4 *puVar1;
  undefined4 local_c [2];
  
  puVar1 = *(undefined4 **)(param_1 + 0x44);
  if (puVar1 == *(undefined4 **)(param_1 + 0x48)) {
    local_c[0] = param_2;
    _ZNSt6vectorIiSaIiEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPiS1_EERKi
              (param_1 + 0x40,puVar1,local_c);
  }
  else {
    if (puVar1 != (undefined4 *)0x0) {
      *puVar1 = param_2;
    }
    *(undefined4 **)(param_1 + 0x44) = puVar1 + 1;
  }
  return;
}


