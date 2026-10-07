// _Z23PostProcessingEffectAddP9lua_State @ 0015e50c

undefined4 _Z23PostProcessingEffectAddP9lua_State(undefined4 param_1)

{
  bool bVar1;
  bool bVar2;
  char *pcVar3;
  int iVar4;
  undefined4 uVar5;
  int iVar6;
  size_t sVar7;
  float fVar8;
  int *piVar9;
  int *piVar10;
  char *pcVar11;
  undefined1 auStack_7c [4];
  undefined1 auStack_78 [4];
  undefined1 auStack_74 [4];
  undefined1 auStack_70 [4];
  undefined1 auStack_6c [4];
  undefined1 auStack_68 [4];
  undefined1 auStack_64 [4];
  char *local_60;
  int local_5c;
  int local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined1 auStack_44 [4];
  int local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  int local_2c;
  
  iVar4 = _ZN6CLevel8GetLevelEv();
  iVar6 = DAT_0015ed08;
  if (iVar4 != 0) {
    uVar5 = lua_tolstring(param_1,1,0);
    iVar4 = DAT_0015ed0c;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
              (auStack_68,uVar5);
    local_54 = 0xbf800000;
    local_50 = 0xbf800000;
    local_4c = 0xbf800000;
    local_48 = 0x3f800000;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
              (auStack_44,iVar6 + 0x15e548);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
              (&local_40,iVar6 + 0x15e548);
    local_3c = -1;
    local_2c = -1;
    local_38 = 0x41200000;
    local_34 = 0x3f000000;
    local_30 = 0x41a00000;
    iVar6 = lua_type(param_1,2);
    piVar10 = *(int **)(iVar4 + 0x15e5c4);
    if (iVar6 == 5) {
      iVar6 = 2;
    }
    else {
      iVar6 = 0;
    }
    if ((*(int *)(*piVar10 + 0x178) != 0) && (iVar6 != 0)) {
      pcVar11 = *(char **)(DAT_0015ed10 + 0x15e5f8);
      local_60 = pcVar11 + 0xc;
      lua_pushstring(param_1,DAT_0015ed14 + 0x15e5fc);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_54 = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed18 + 0x15e640);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_50 = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed1c + 0x15e67c);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_4c = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed20 + 0x15e6b8);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_48 = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed24 + 0x15e6f4);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isstring(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        bVar1 = true;
        _ZNSsC1ERKSs(&local_5c,&local_60);
      }
      else {
        uVar5 = lua_tolstring(param_1,0xffffffff,0);
        bVar1 = false;
        _ZNSsC1EPKcRKSaIcE(&local_5c,uVar5,auStack_7c);
      }
      _ZNSs6assignERKSs(&local_60,&local_5c);
      if ((char *)(local_5c + -0xc) != pcVar11) {
        piVar9 = (int *)(local_5c + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar4 = *piVar9;
          bVar2 = (bool)hasExclusiveAccess(piVar9);
        } while (!bVar2);
        *piVar9 = iVar4 + -1;
        DataMemoryBarrier(0xf);
        if (iVar4 < 1) {
          _ZNSs4_Rep10_M_destroyERKSaIcE((char *)(local_5c + -0xc),auStack_78);
        }
      }
      lua_settop(param_1,0xfffffffe);
      pcVar3 = local_60;
      if (!bVar1) {
        sVar7 = strlen(local_60);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                  (&local_40,pcVar3,sVar7);
      }
      lua_pushstring(param_1,DAT_0015ed28 + 0x15e76c);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        fVar8 = (float)lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_3c = (int)fVar8;
      }
      lua_pushstring(param_1,DAT_0015ed2c + 0x15e7a8);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_38 = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed30 + 0x15e7e4);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_34 = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed34 + 0x15e820);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_30 = uVar5;
      }
      lua_pushstring(param_1,DAT_0015ed38 + 0x15e85c);
      lua_gettable(param_1,iVar6);
      iVar4 = lua_isnumber(param_1,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_1,0xffffffff), iVar4 == 0)) {
        lua_settop(param_1,0xfffffffe);
      }
      else {
        fVar8 = (float)lua_tonumber(param_1,0xffffffff);
        lua_settop(param_1,0xfffffffe);
        local_2c = (int)fVar8;
      }
      lua_pushstring(param_1,DAT_0015ed3c + 0x15e898);
      lua_gettable(param_1,iVar6);
      iVar6 = lua_isstring(param_1,0xffffffff);
      if ((iVar6 == 0) || (iVar6 = lua_type(param_1,0xffffffff), iVar6 == 0)) {
        bVar1 = true;
        _ZNSsC1ERKSs(&local_58,&local_60);
      }
      else {
        uVar5 = lua_tolstring(param_1,0xffffffff,0);
        bVar1 = false;
        _ZNSsC1EPKcRKSaIcE(&local_58,uVar5,auStack_74);
      }
      _ZNSs6assignERKSs(&local_60,&local_58);
      if ((char *)(local_58 + -0xc) != pcVar11) {
        piVar9 = (int *)(local_58 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar6 = *piVar9;
          bVar2 = (bool)hasExclusiveAccess(piVar9);
        } while (!bVar2);
        *piVar9 = iVar6 + -1;
        DataMemoryBarrier(0xf);
        if (iVar6 < 1) {
          _ZNSs4_Rep10_M_destroyERKSaIcE((char *)(local_58 + -0xc),auStack_70);
        }
      }
      lua_settop(param_1,0xfffffffe);
      pcVar3 = local_60;
      if (!bVar1) {
        sVar7 = strlen(local_60);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                  (auStack_44,pcVar3,sVar7);
      }
      if (local_60 + -0xc != pcVar11) {
        piVar9 = (int *)(local_60 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar6 = *piVar9;
          bVar1 = (bool)hasExclusiveAccess(piVar9);
        } while (!bVar1);
        *piVar9 = iVar6 + -1;
        DataMemoryBarrier(0xf);
        if (iVar6 < 1) {
          _ZNSs4_Rep10_M_destroyERKSaIcE(local_60 + -0xc,auStack_6c);
        }
      }
    }
    if (*(int *)(local_40 + -0xc) == 0) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                (&local_40,DAT_0015ed40 + 0x15e98c,10);
    }
    iVar6 = *(int *)(*piVar10 + 0x178);
    if (iVar6 != 0) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (auStack_64,auStack_68);
      _ZN19CPostProcessManager12EnableEffectESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEER20PostEffectScriptData
                (iVar6,auStack_64,&local_54);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (auStack_64);
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (&local_40);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_44);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_68);
  }
  return 0;
}


