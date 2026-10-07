// _ZN13CZonesManager14TeleportInZoneEP5CZone @ 002cd9cc

void _ZN13CZonesManager14TeleportInZoneEP5CZone(int param_1,int param_2)

{
  int *piVar1;
  int *piVar2;
  int *piVar3;
  
  *(undefined1 *)(param_1 + 0x7c) = 1;
  if (param_2 == 0) {
    return;
  }
  if (*(int *)(param_1 + 0x6c) == param_2) {
    return;
  }
  piVar1 = *(int **)(param_1 + 0x84);
  piVar2 = *(int **)(param_1 + 0x80);
  while (piVar3 = piVar2, piVar2 != piVar1) {
    while (piVar2 = piVar3 + 1, *(char *)(*piVar3 + 0x15c) != '\0') {
      _ZN5CZone12SetInvisibleEv_part_1066();
      piVar1 = *(int **)(param_1 + 0x84);
      piVar3 = piVar2;
      if (piVar2 == piVar1) goto LAB_002cda20;
    }
  }
LAB_002cda20:
  if (*(char *)(param_2 + 0x17d) == '\0') {
    *(int *)(param_1 + 0x6c) = param_2;
  }
  else {
    param_2 = *(int *)(param_1 + 0x6c);
    if (param_2 == 0) {
      return;
    }
  }
  if (*(char *)(param_2 + 0x15c) == '\0') {
    *(undefined1 *)(param_2 + 0x15c) = 1;
    *(int *)(param_2 + 0x154) = *(int *)(param_2 + 0x154) + 1;
  }
  return;
}


