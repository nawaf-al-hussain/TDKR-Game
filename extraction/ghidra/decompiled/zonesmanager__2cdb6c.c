// _ZN13CZonesManager16CreateBatchNodesEv @ 002cdb6c

void _ZN13CZonesManager16CreateBatchNodesEv(int param_1)

{
  undefined4 *puVar1;
  
  for (puVar1 = *(undefined4 **)(param_1 + 0x80); *(undefined4 **)(param_1 + 0x84) != puVar1;
      puVar1 = puVar1 + 1) {
    _ZN5CZone15CreateBatchNodeEv(*puVar1);
  }
  return;
}


