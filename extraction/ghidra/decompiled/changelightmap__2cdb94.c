// _ZN13CZonesManager14ChangeLightMapEPKcS1_ @ 002cdb94

void _ZN13CZonesManager14ChangeLightMapEPKcS1_
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 *puVar1;
  
  for (puVar1 = *(undefined4 **)(param_1 + 0x80); *(undefined4 **)(param_1 + 0x84) != puVar1;
      puVar1 = puVar1 + 1) {
    _ZN5CZone14ChangeLightMapEPKcS1_
              (*puVar1,param_2,param_3,*(undefined4 **)(param_1 + 0x84),param_4);
  }
  return;
}

