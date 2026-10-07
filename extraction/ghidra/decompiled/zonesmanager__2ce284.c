// _ZN13CZonesManager19SpawnObjectThreadedEPiiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS2_10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEi @ 002ce284

int * _ZN13CZonesManager19SpawnObjectThreadedEPiiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS2_10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEi
                (int param_1,undefined4 param_2,undefined4 param_3,float *param_4,undefined4 param_5
                ,int param_6)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  size_t sVar4;
  int *piVar5;
  int *piVar6;
  char cVar7;
  code *pcVar8;
  int *piVar9;
  char *pcVar10;
  char *pcVar11;
  char *local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  if (param_6 == -1) {
    _ZN6CLevel8GetLevelEv();
    iVar3 = _ZN6CLevel15GetZonesManagerEv();
    piVar6 = *(int **)(iVar3 + 0x80);
    piVar5 = piVar6;
    do {
      if (*(int **)(iVar3 + 0x84) == piVar5) {
        if ((uint)((int)*(int **)(iVar3 + 0x84) - (int)piVar6) >> 2 == 0) goto LAB_002ce60c;
        iVar2 = *piVar6;
        break;
      }
      piVar9 = piVar5 + 1;
      iVar2 = *piVar5;
      piVar5 = piVar9;
    } while ((((*param_4 < *(float *)(iVar2 + 0x19c)) || (*(float *)(iVar2 + 0x1a8) < *param_4)) ||
             (param_4[1] < *(float *)(iVar2 + 0x1a0))) ||
            (((*(float *)(iVar2 + 0x1ac) < param_4[1] || (param_4[2] < *(float *)(iVar2 + 0x1a4)))
             || (*(float *)(iVar2 + 0x1b0) < param_4[2]))));
  }
  else {
    uVar1 = _ZN6CLevel8GetLevelEv();
    iVar2 = _ZNK6CLevel27FindZoneForObjectOrWaypointEi(uVar1,param_6);
  }
  if (iVar2 == 0) {
LAB_002ce60c:
    iVar2 = *(int *)(param_1 + 0x6c);
  }
  _Z14StrGetFileNameRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE
            (&local_3c,param_5);
  pcVar11 = local_3c;
  if (*(int *)(local_3c + -0xc) == 0) {
    iVar3 = _ZN6CLevel8GetLevelEv();
    uVar1 = _ZN18CGameObjectManager17GetMeshNameFromIdEi(*(undefined4 *)(iVar3 + 0xa94),param_3);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (&local_3c,uVar1);
    pcVar11 = local_3c;
  }
  sVar4 = strlen(pcVar11);
  pcVar10 = pcVar11;
  while (pcVar10 != pcVar11 + sVar4) {
    cVar7 = *pcVar10;
    if ((uint)(int)cVar7 < 0x100) {
      cVar7 = (char)*(undefined2 *)(**(int **)(DAT_002ce614 + 0x2ce320) + cVar7 * 2 + 2);
    }
    *pcVar10 = cVar7;
    pcVar10 = pcVar10 + 1;
  }
  pcVar11[sVar4] = '\0';
  piVar5 = (int *)_ZN22GameObjectCacheManager3PopEiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                            (*(undefined4 *)(param_1 + 0x68),param_3,&local_3c);
  if (piVar5 == (int *)0x0) {
    iVar3 = _ZN6CLevel8GetLevelEv();
    piVar5 = (int *)_ZN18CGameObjectManager23CreateObjectFromLibraryEiP5CZoneRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEE
                              (*(undefined4 *)(iVar3 + 0xa94),param_3,0,&local_3c);
    pcVar8 = *(code **)(*piVar5 + 0x24);
    **(int **)(param_1 + 0x68) = **(int **)(param_1 + 0x68) + 1;
    (*pcVar8)();
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (piVar5 + 0x3f,&local_3c);
    pcVar10 = (char *)piVar5[0x3f];
    sVar4 = strlen(pcVar10);
    pcVar11 = pcVar10;
    while (pcVar11 != pcVar10 + sVar4) {
      cVar7 = *pcVar11;
      if ((uint)(int)cVar7 < 0x100) {
        cVar7 = (char)*(undefined2 *)(**(int **)(DAT_002ce618 + 0x2ce540) + cVar7 * 2 + 2);
      }
      *pcVar11 = cVar7;
      pcVar11 = pcVar11 + 1;
    }
    pcVar10[sVar4] = '\0';
    (**(code **)(*piVar5 + 0x50))(piVar5,1);
    (**(code **)(*piVar5 + 0x80))(piVar5,1);
    _ZN11CGameObject11SetDontSaveEb(piVar5,*(undefined1 *)(param_1 + 0x98));
    _ZN11CGameObject7SetZoneEP5CZoneb(piVar5,iVar2,1);
    _ZN22GameObjectCacheManager4PushEP11CGameObject(*(undefined4 *)(param_1 + 0x68),piVar5);
    (**(code **)(*piVar5 + 0x74))(piVar5);
    (**(code **)(*piVar5 + 0x28))(piVar5,param_4,1);
    local_2c = 0;
    local_28 = 0;
    local_24 = 0;
    (**(code **)(*piVar5 + 0x2c))(piVar5,&local_2c);
  }
  else {
    pcVar8 = *(code **)(*piVar5 + 0x24);
    **(int **)(param_1 + 0x68) = **(int **)(param_1 + 0x68) + 1;
    (*pcVar8)();
    (**(code **)(*piVar5 + 0x50))(piVar5,1);
    (**(code **)(*piVar5 + 0x80))(piVar5,1);
    piVar5[3] = (int)*param_4;
    pcVar8 = *(code **)(*piVar5 + 0x28);
    piVar5[4] = (int)param_4[1];
    piVar5[5] = (int)param_4[2];
    (*pcVar8)(piVar5,param_4,1);
    local_38 = 0;
    local_34 = 0;
    local_30 = 0;
    (**(code **)(*piVar5 + 0x2c))(piVar5,&local_38);
    _ZN11CGameObject11SetDontSaveEb(piVar5,*(undefined1 *)(param_1 + 0x98));
    _ZN11CGameObject7SetZoneEP5CZoneb(piVar5,iVar2,0);
    _ZN11CGameObject6ReInitEb(piVar5,1);
    (**(code **)(*piVar5 + 0x78))(piVar5);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_3c);
  return piVar5;
}


