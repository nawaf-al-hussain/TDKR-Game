// _ZN13CZonesManager8FindZoneEi @ 002d15fc

undefined4 _ZN13CZonesManager8FindZoneEi(int param_1,int param_2)

{
  undefined4 *puVar1;
  int iVar2;
  undefined4 *puVar3;
  
  puVar1 = *(undefined4 **)(param_1 + 0x80);
  do {
    puVar3 = puVar1;
    if (*(undefined4 **)(param_1 + 0x84) == puVar3) {
      return 0;
    }
    iVar2 = (**(code **)(*(int *)*puVar3 + 0x14))();
    puVar1 = puVar3 + 1;
  } while (iVar2 != param_2);
  return *puVar3;
}


