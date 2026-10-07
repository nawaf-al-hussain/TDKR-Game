// _ZN13CZonesManager18ResetCrtTargetZoneEP5CZone @ 002cce4c

void _ZN13CZonesManager18ResetCrtTargetZoneEP5CZone(int param_1,int param_2)

{
  if ((param_2 != 0) && (*(char *)(param_2 + 0x17d) != '\0')) {
    *(undefined1 *)(param_1 + 0x7c) = 0;
    return;
  }
  *(int *)(param_1 + 0x6c) = param_2;
  *(undefined1 *)(param_1 + 0x7c) = 0;
  return;
}


