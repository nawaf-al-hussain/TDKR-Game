// _ZN13CZonesManager15CheckWorldBoxesEv @ 002d039c

void _ZN13CZonesManager15CheckWorldBoxesEv(int param_1)

{
  int iVar1;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  
  _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
            (&local_20,*(undefined4 *)(**(int **)(DAT_002d0410 + 0x2d03ac) + 0xe4));
  local_14 = local_20;
  local_10 = local_1c;
  local_c = local_18;
  iVar1 = _ZN13CZonesManager17GetZoneByWorldBoxEN6glitch4core8vector3dIfEEP5CZone
                    (param_1,&local_14,*(undefined4 *)(param_1 + 0x6c));
  if (((iVar1 != 0) && (*(int *)(param_1 + 0x6c) != iVar1)) && (*(char *)(iVar1 + 0x17d) == '\0')) {
    *(int *)(param_1 + 0x6c) = iVar1;
  }
  return;
}


