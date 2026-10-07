// _ZN13CZonesManager16UpdateVisibilityEPKN6glitch5scene12SViewFrustumENS0_4core8vector3dIfEE @ 002cf854

void _ZN13CZonesManager16UpdateVisibilityEPKN6glitch5scene12SViewFrustumENS0_4core8vector3dIfEE
               (int param_1,undefined4 *param_2,undefined4 *param_3)

{
  int iVar1;
  char cVar2;
  int iVar3;
  int *piVar4;
  undefined4 uVar5;
  int *piVar6;
  int *piVar7;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  
  iVar3 = DAT_002cfa70 + 0x2cf86c;
  if (((**(char **)(iVar3 + DAT_002cfa74) != '\0') || (**(char **)(iVar3 + DAT_002cfa78) != '\0'))
     || (**(char **)(iVar3 + DAT_002cfa80) != '\0')) {
    _ZN3occ16OcclusionManager6updateEv(*(undefined4 *)(iVar3 + DAT_002cfa7c));
  }
  if (*(char *)(param_1 + 0x7e) == '\0') {
    return;
  }
  iVar3 = *(int *)(param_1 + 0x6c);
  if (iVar3 == 0) {
    iVar3 = _ZN13CZonesManager14GetZoneFromPosERKN6glitch4core8vector3dIfEE(param_1,param_2);
    if ((iVar3 != 0) && (*(char *)(iVar3 + 0x17d) != '\0')) {
      *(undefined4 *)(param_1 + 0x70) = *param_2;
      *(undefined4 *)(param_1 + 0x74) = param_2[1];
      *(undefined4 *)(param_1 + 0x78) = param_2[2];
      goto LAB_002cf93c;
    }
    *(int *)(param_1 + 0x6c) = iVar3;
LAB_002cf8e8:
    iVar1 = iVar3;
    *(undefined4 *)(param_1 + 0x70) = *param_2;
    *(undefined4 *)(param_1 + 0x74) = param_2[1];
    *(undefined4 *)(param_1 + 0x78) = param_2[2];
    if (iVar1 == 0) goto LAB_002cf93c;
  }
  else {
    if (*(char *)(iVar3 + 0x15c) != '\0') {
      _ZN5CZone12SetInvisibleEv_part_1066(iVar3);
      iVar3 = *(int *)(param_1 + 0x6c);
    }
    if (*(char *)(param_1 + 0x7c) != '\0') {
      *(undefined1 *)(param_1 + 0x7c) = 0;
      goto LAB_002cf8e8;
    }
    iVar1 = _ZN5CZone16CheckChangedZoneERKN6glitch4core8vector3dIfEES5_b
                      (iVar3,param_1 + 0x70,param_2,1);
    if ((iVar1 == 0) || (*(char *)(iVar1 + 0x17d) != '\0')) goto LAB_002cf8e8;
    uVar5 = *param_2;
    *(int *)(param_1 + 0x6c) = iVar1;
    *(undefined4 *)(param_1 + 0x70) = uVar5;
    *(undefined4 *)(param_1 + 0x74) = param_2[1];
    *(undefined4 *)(param_1 + 0x78) = param_2[2];
  }
  _ZN5CZone10SetVisibleEPKN6glitch5scene12SViewFrustumEPK11CZonePortal(iVar1,param_2,0);
  local_24 = *param_3;
  local_20 = param_3[1];
  local_1c = param_3[2];
  _ZN5CZone4DrawEN6glitch4core8vector3dIfEE(*(undefined4 *)(param_1 + 0x6c),&local_24);
LAB_002cf93c:
  piVar7 = *(int **)(param_1 + 0x84);
  piVar6 = *(int **)(param_1 + 0x80);
  do {
    piVar4 = piVar6;
    if (piVar6 == piVar7) {
      return;
    }
    while( true ) {
      piVar6 = piVar4 + 1;
      iVar3 = *piVar4;
      cVar2 = *(char *)(iVar3 + 0x15c);
      if ((*(char *)(iVar3 + 0x17d) != '\0') && (cVar2 == '\0')) {
        *(undefined1 *)(iVar3 + 0x15c) = 1;
        cVar2 = '\x01';
        *(int *)(iVar3 + 0x154) = *(int *)(iVar3 + 0x154) + 1;
      }
      piVar4 = *(int **)(iVar3 + 0x1dc);
      if (((piVar4[0x3d] & 0x18U) == 0x18) == (bool)cVar2) break;
      (**(code **)(*piVar4 + 0x4c))(piVar4);
      piVar7 = *(int **)(param_1 + 0x84);
      piVar4 = piVar6;
      if (piVar6 == piVar7) {
        return;
      }
    }
  } while( true );
}


