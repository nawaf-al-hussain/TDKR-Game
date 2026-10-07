// _ZN13CZonesManager17GetObjectFromPoolEiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEEi @ 002cf138

int * _ZN13CZonesManager17GetObjectFromPoolEiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEEi
                (int param_1,undefined4 param_2,float *param_3,undefined4 param_4,int param_5)

{
  char *pcVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  size_t sVar5;
  int *piVar6;
  int *piVar7;
  char cVar8;
  code *pcVar9;
  int *piVar10;
  char *__s;
  char *local_24 [2];
  
  if (param_5 == -1) {
    _ZN6CLevel8GetLevelEv();
    iVar4 = _ZN6CLevel15GetZonesManagerEv();
    piVar7 = *(int **)(iVar4 + 0x80);
    piVar6 = piVar7;
    do {
      if (piVar6 == *(int **)(iVar4 + 0x84)) {
        if ((uint)((int)piVar6 - (int)piVar7) >> 2 == 0) goto LAB_002cf36c;
        iVar3 = *piVar7;
        break;
      }
      piVar10 = piVar6 + 1;
      iVar3 = *piVar6;
      piVar6 = piVar10;
    } while ((((*param_3 < *(float *)(iVar3 + 0x19c)) || (*(float *)(iVar3 + 0x1a8) < *param_3)) ||
             (param_3[1] < *(float *)(iVar3 + 0x1a0))) ||
            (((*(float *)(iVar3 + 0x1ac) < param_3[1] || (param_3[2] < *(float *)(iVar3 + 0x1a4)))
             || (*(float *)(iVar3 + 0x1b0) < param_3[2]))));
  }
  else {
    uVar2 = _ZN6CLevel8GetLevelEv();
    iVar3 = _ZNK6CLevel27FindZoneForObjectOrWaypointEi(uVar2,param_5);
  }
  if (iVar3 == 0) {
LAB_002cf36c:
    iVar3 = *(int *)(param_1 + 0x6c);
  }
  _Z14StrGetFileNameRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE
            (local_24,param_4);
  __s = local_24[0];
  if (*(int *)(local_24[0] + -0xc) == 0) {
    iVar4 = _ZN6CLevel8GetLevelEv();
    uVar2 = _ZN18CGameObjectManager17GetMeshNameFromIdEi(*(undefined4 *)(iVar4 + 0xa94),param_2);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (local_24,uVar2);
    __s = local_24[0];
  }
  sVar5 = strlen(__s);
  pcVar1 = __s;
  while (pcVar1 != __s + sVar5) {
    cVar8 = *pcVar1;
    if ((uint)(int)cVar8 < 0x100) {
      cVar8 = (char)*(undefined2 *)(**(int **)(DAT_002cf374 + 0x2cf1d8) + cVar8 * 2 + 2);
    }
    *pcVar1 = cVar8;
    pcVar1 = pcVar1 + 1;
  }
  __s[sVar5] = '\0';
  piVar6 = (int *)_ZN22GameObjectCacheManager3PopEiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                            (*(undefined4 *)(param_1 + 0x68),param_2,local_24);
  if (piVar6 != (int *)0x0) {
    pcVar9 = *(code **)(*piVar6 + 0x24);
    **(int **)(param_1 + 0x68) = **(int **)(param_1 + 0x68) + 1;
    (*pcVar9)();
    (**(code **)(*piVar6 + 0x50))(piVar6,1);
    (**(code **)(*piVar6 + 0x80))(piVar6,1);
    piVar6[3] = (int)*param_3;
    pcVar9 = *(code **)(*piVar6 + 0x28);
    piVar6[4] = (int)param_3[1];
    piVar6[5] = (int)param_3[2];
    (*pcVar9)(piVar6,param_3,1);
    _ZN11CGameObject11SetDontSaveEb(piVar6,*(undefined1 *)(param_1 + 0x98));
    _ZN11CGameObject7SetZoneEP5CZoneb(piVar6,iVar3,0);
    _ZN11CGameObject6ReInitEb(piVar6,1);
    (**(code **)(*piVar6 + 0x78))(piVar6);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (local_24);
  return piVar6;
}


