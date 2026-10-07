// _ZN13CZonesManager14SetCurrentZoneEP5CZone @ 002cdbfc

void _ZN13CZonesManager14SetCurrentZoneEP5CZone(int param_1,int param_2)

{
  if ((param_2 != 0) && (*(char *)(param_2 + 0x17d) != '\0')) {
    return;
  }
  *(int *)(param_1 + 0x6c) = param_2;
  return;
}


