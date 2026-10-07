// _ZN11CHUDDisplay8SaveLoadEP13CMemoryStream @ 0043a4e4

void _ZN11CHUDDisplay8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  uint uVar1;
  char *pcVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  int *piVar6;
  undefined1 local_82;
  undefined1 local_81;
  int local_80;
  undefined4 local_7c;
  undefined1 auStack_78 [4];
  int local_74;
  undefined1 auStack_70 [4];
  undefined1 auStack_6c [4];
  undefined4 local_68;
  char local_64 [64];
  int local_24;
  
  iVar4 = DAT_0043a710 + 0x43a504;
  piVar6 = *(int **)(iVar4 + DAT_0043a714);
  local_24 = *piVar6;
  _ZN13CMemoryStream8ReadDataEPvi(param_2,local_64,0x40);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x550);
  iVar3 = *(int *)(param_1 + 0x3ec);
  pcVar2 = (char *)((int)&local_68 + 3);
  do {
    pcVar2 = pcVar2 + 1;
    if (*pcVar2 == '\0') {
      uVar1 = *(uint *)(iVar3 + 0xfc) & 0xfffffff9;
    }
    else {
      uVar1 = *(uint *)(iVar3 + 0xfc) | 6;
    }
    *(uint *)(iVar3 + 0xfc) = uVar1;
    iVar3 = iVar3 + 0x128;
  } while (pcVar2 != local_64 + 0x18);
  iVar3 = 0;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (auStack_78,DAT_0043a718 + 0x43a570);
  local_82 = 0;
  local_74 = *(int *)(iVar4 + DAT_0043a71c) + 0xc;
  local_81 = 0;
  _ZN13CMemoryStream4ReadERi(param_2,&local_80);
  puVar5 = *(undefined4 **)(iVar4 + DAT_0043a720);
  if (0 < local_80) {
    do {
      while( true ) {
        _ZN13CMemoryStream4ReadERi(param_2,&local_7c);
        _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                  (param_2,&local_74);
        _ZN13CMemoryStream4ReadERb(param_2,&local_82);
        _ZN13CMemoryStream4ReadERb(param_2,&local_81);
        iVar4 = _ZN13CZonesManager10FindObjectEit(*puVar5,local_7c,0x11);
        if (iVar4 == 0) break;
        iVar4 = iVar4 + 0x34;
LAB_0043a5ac:
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_70,auStack_78);
        iVar3 = iVar3 + 1;
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_6c,&local_74);
        _ZN11CHUDDisplay19AddObjectiveToSceneEP15CGameObjectBaseSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEESA_bbP7HotSpotbb_constprop_2539
                  (param_1,iVar4,auStack_70,auStack_6c,local_82,local_81);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_6c);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_70);
        if (local_80 <= iVar3) goto LAB_0043a678;
      }
      iVar4 = _ZN13CZonesManager12FindWayPointEi(*puVar5,local_7c);
      if (iVar4 != 0) goto LAB_0043a5ac;
      iVar3 = iVar3 + 1;
    } while (iVar3 < local_80);
  }
LAB_0043a678:
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_74);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_78);
  local_68 = 0xffffffff;
  _ZN13CMemoryStream4ReadERi(param_2);
  iVar3 = _ZN13CZonesManager9FindActorEi(*puVar5,local_68);
  if ((iVar3 == 0) || (*(int *)(iVar3 + 0xa4) == 0)) {
    *(undefined4 *)(param_1 + 0xfb4) = 0;
    _ZN7gameswf15CharacterHandle10setVisibleEb(param_1 + 0xc48);
  }
  else {
    *(int *)(param_1 + 0xfb4) = iVar3;
    *(undefined4 *)(param_1 + 0xfb8) = 0xffffffff;
    _ZN7gameswf15CharacterHandle10setVisibleEb(param_1 + 0xc48,1);
    _ZN11CHUDDisplay20UpdateEnemyHealthBarEv(param_1);
  }
  if (local_24 == *piVar6) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


