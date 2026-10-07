// _Z21PostProcessReadConfigR20PostEffectScriptDataiP9lua_State @ 0015dde8

undefined4
_Z21PostProcessReadConfigR20PostEffectScriptDataiP9lua_State
          (undefined4 *param_1,int param_2,undefined4 param_3)

{
  bool bVar1;
  bool bVar2;
  char *pcVar3;
  int iVar4;
  undefined4 uVar5;
  size_t sVar6;
  float fVar7;
  int *piVar8;
  char *pcVar9;
  undefined1 auStack_48 [4];
  undefined1 auStack_44 [4];
  undefined1 auStack_40 [4];
  undefined1 auStack_3c [4];
  undefined1 auStack_38 [4];
  char *local_34;
  int local_30;
  int local_2c;
  
  uVar5 = 0;
  if (*(int *)(**(int **)(DAT_0015e4d8 + 0x15ddfc) + 0x178) != 0) {
    if (param_2 == 0) {
      uVar5 = 0;
    }
    else {
      pcVar9 = *(char **)(DAT_0015e4dc + 0x15de38);
      local_34 = pcVar9 + 0xc;
      lua_pushstring(param_3,DAT_0015e4e0 + 0x15de3c);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        *param_1 = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e4e4 + 0x15de80);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[1] = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e4e8 + 0x15debc);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[2] = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e4ec + 0x15def8);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[3] = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e4f0 + 0x15df34);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isstring(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        bVar1 = true;
        _ZNSsC1ERKSs(&local_30,&local_34);
      }
      else {
        uVar5 = lua_tolstring(param_3,0xffffffff,0);
        bVar1 = false;
        _ZNSsC1EPKcRKSaIcE(&local_30,uVar5,auStack_48);
      }
      _ZNSs6assignERKSs(&local_34,&local_30);
      if ((char *)(local_30 + -0xc) != pcVar9) {
        piVar8 = (int *)(local_30 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar4 = *piVar8;
          bVar2 = (bool)hasExclusiveAccess(piVar8);
        } while (!bVar2);
        *piVar8 = iVar4 + -1;
        DataMemoryBarrier(0xf);
        if (iVar4 < 1) {
          _ZNSs4_Rep10_M_destroyERKSaIcE((char *)(local_30 + -0xc),auStack_44);
        }
      }
      lua_settop(param_3,0xfffffffe);
      pcVar3 = local_34;
      if (!bVar1) {
        sVar6 = strlen(local_34);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                  (param_1 + 5,pcVar3,sVar6);
      }
      lua_pushstring(param_3,DAT_0015e4f4 + 0x15dfac);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        fVar7 = (float)lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[6] = (int)fVar7;
      }
      lua_pushstring(param_3,DAT_0015e4f8 + 0x15dfe8);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[7] = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e4fc + 0x15e024);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[8] = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e500 + 0x15e060);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        uVar5 = lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[9] = uVar5;
      }
      lua_pushstring(param_3,DAT_0015e504 + 0x15e09c);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isnumber(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        lua_settop(param_3,0xfffffffe);
      }
      else {
        fVar7 = (float)lua_tonumber(param_3,0xffffffff);
        lua_settop(param_3,0xfffffffe);
        param_1[10] = (int)fVar7;
      }
      lua_pushstring(param_3,DAT_0015e508 + 0x15e0d8);
      lua_gettable(param_3,param_2);
      iVar4 = lua_isstring(param_3,0xffffffff);
      if ((iVar4 == 0) || (iVar4 = lua_type(param_3,0xffffffff), iVar4 == 0)) {
        bVar1 = true;
        _ZNSsC1ERKSs(&local_2c,&local_34);
      }
      else {
        uVar5 = lua_tolstring(param_3,0xffffffff,0);
        bVar1 = false;
        _ZNSsC1EPKcRKSaIcE(&local_2c,uVar5,auStack_40);
      }
      _ZNSs6assignERKSs(&local_34,&local_2c);
      if ((char *)(local_2c + -0xc) != pcVar9) {
        piVar8 = (int *)(local_2c + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar4 = *piVar8;
          bVar2 = (bool)hasExclusiveAccess(piVar8);
        } while (!bVar2);
        *piVar8 = iVar4 + -1;
        DataMemoryBarrier(0xf);
        if (iVar4 < 1) {
          _ZNSs4_Rep10_M_destroyERKSaIcE((char *)(local_2c + -0xc),auStack_3c);
        }
      }
      lua_settop(param_3,0xfffffffe);
      pcVar3 = local_34;
      if (!bVar1) {
        sVar6 = strlen(local_34);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                  (param_1 + 4,pcVar3,sVar6);
      }
      if (local_34 + -0xc != pcVar9) {
        piVar8 = (int *)(local_34 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar4 = *piVar8;
          bVar1 = (bool)hasExclusiveAccess(piVar8);
        } while (!bVar1);
        *piVar8 = iVar4 + -1;
        DataMemoryBarrier(0xf);
        if (iVar4 < 1) {
          _ZNSs4_Rep10_M_destroyERKSaIcE(local_34 + -0xc,auStack_38);
          return 1;
        }
      }
      uVar5 = 1;
    }
  }
  return uVar5;
}


