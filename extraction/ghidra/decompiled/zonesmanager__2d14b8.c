// _ZN13CZonesManager18HandleZoneRequestsEb @ 002d14b8

void _ZN13CZonesManager18HandleZoneRequestsEb(int param_1,undefined4 param_2)

{
  *(undefined1 *)(*(int *)(param_1 + 100) + 0x20) = 0;
  _ZN13CZonesManager24HandleZoneUnloadRequestsEv();
  _ZN13CZonesManager22HandleZoneLoadRequestsEb(param_1,param_2);
  _ZN13CZonesManager20RefreshAllActorsPoolEv(param_1);
  *(undefined1 *)(*(int *)(param_1 + 100) + 0x20) = 1;
  return;
}


