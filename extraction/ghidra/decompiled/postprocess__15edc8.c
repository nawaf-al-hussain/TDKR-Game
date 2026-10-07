// _Z24GetPostProcessingEffectsP9lua_State @ 0015edc8

uint _Z24GetPostProcessingEffectsP9lua_State(undefined4 param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  int local_24;
  int local_20;
  undefined4 local_1c;
  
  local_24 = 0;
  local_20 = 0;
  local_1c = 0;
  iVar3 = _ZN6CLevel8GetLevelEv();
  if ((iVar3 != 0) && (iVar3 = *(int *)(**(int **)(DAT_0015eeac + 0x15edfc) + 0x178), iVar3 != 0)) {
    _ZN19CPostProcessManager17GetEnabledEffectsERSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESaIS9_EE
              (iVar3,&local_24);
  }
  uVar5 = local_20 - local_24 >> 2;
  if (uVar5 == 0) {
    uVar5 = 1;
    lua_pushnil(param_1);
    iVar3 = local_24;
    iVar1 = local_20;
  }
  else {
    if (0x11 < uVar5) {
      uVar5 = 0x12;
    }
    iVar3 = local_24;
    iVar1 = local_20;
    if (uVar5 != 0) {
      uVar4 = 0;
      do {
        iVar3 = uVar4 * 4;
        uVar4 = uVar4 + 1;
        lua_pushstring(param_1,*(undefined4 *)(local_24 + iVar3));
        iVar3 = local_24;
        iVar1 = local_20;
      } while (uVar4 != uVar5);
    }
  }
  for (; iVar2 = local_20, iVar3 != local_20; iVar3 = iVar3 + 4) {
    local_20 = iVar1;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev(iVar3)
    ;
    iVar1 = local_20;
    local_20 = iVar2;
  }
  if (local_24 != 0) {
    local_20 = iVar1;
    _ZdlPv(local_24);
  }
  return uVar5;
}


