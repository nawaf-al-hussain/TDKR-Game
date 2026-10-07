// _ZN9LuaThread8SaveLoadEP13CMemoryStream @ 0015bf7c

void _ZN9LuaThread8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  undefined4 *puVar7;
  int local_24;
  
  local_24 = *(int *)(DAT_0015c2d0 + 0x15bf94) + 0xc;
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 8) = uVar1;
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0xc) = uVar1;
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x10) = uVar1;
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x14) = uVar1;
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x28) = uVar1;
  uVar1 = _ZN6CLevel8GetLevelEv();
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  uVar1 = _ZN6CLevel20FindObjectOrWaypointEi(uVar1,uVar2);
  *(undefined4 *)(param_1 + 0x2c) = uVar1;
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x30) = uVar1;
  iVar3 = _ZN13CMemoryStream8ReadCharEv(param_2);
  if (iVar3 != 0) {
    uVar1 = lua_newthread(*(undefined4 *)(param_1 + 0x1c));
    *(undefined4 *)(param_1 + 0x18) = uVar1;
    uVar1 = luaL_ref(*(undefined4 *)(param_1 + 0x1c),0xffffd8f0);
    *(undefined4 *)(param_1 + 0x24) = uVar1;
    iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
    if (0 < iVar3) {
      iVar5 = 1;
      puVar7 = (undefined4 *)(DAT_0015c2d4 + 0x15c06c);
LAB_0015c068:
      do {
        uVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
        switch(uVar1) {
        case 0:
          lua_pushnil(*(undefined4 *)(param_1 + 0x18));
          goto joined_r0x0015c2b0;
        case 1:
          iVar6 = _ZN13CMemoryStream8ReadCharEv(param_2);
          lua_pushboolean(*(undefined4 *)(param_1 + 0x18),iVar6 != 0);
joined_r0x0015c2b0:
          iVar5 = iVar5 + 1;
          if (iVar3 < iVar5) goto LAB_0015c0c4;
          goto LAB_0015c068;
        case 2:
        default:
switchD_0015c074_default:
          break;
        case 3:
          uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
          lua_pushnumber(*(undefined4 *)(param_1 + 0x18),uVar1);
          break;
        case 4:
          _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                    (param_2,&local_24);
          lua_pushstring(*(undefined4 *)(param_1 + 0x18),local_24);
          break;
        case 5:
          lua_createtable(*(undefined4 *)(param_1 + 0x18),0,0);
          _ZN17CLuaScriptManager22ReadLuaTableFromStreamEP9lua_StateP13CMemoryStream
                    (*puVar7,*(undefined4 *)(param_1 + 0x18),param_2);
          goto switchD_0015c074_default;
        case 6:
          _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                    (param_2,&local_24);
          lua_getfield(*(undefined4 *)(param_1 + 0x18),0xffffd8ee,local_24);
        }
        iVar5 = iVar5 + 1;
      } while (iVar5 <= iVar3);
    }
LAB_0015c0c4:
    iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
    iVar5 = _ZN13CMemoryStream7ReadIntEv(param_2);
    *(int *)(*(int *)(param_1 + 0x18) + 0x18) =
         *(int *)(*(int *)(*(int *)(*(int *)(*(int *)(param_1 + 0x18) + 0x20) + iVar3 * 8) + 0x10) +
                 0xc) + iVar5 * 4;
    iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
    *(int *)(*(int *)(param_1 + 0x18) + 0xc) = *(int *)(*(int *)(param_1 + 0x18) + 0x20) + iVar3 * 8
    ;
    iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
    *(int *)(*(int *)(param_1 + 0x18) + 8) = *(int *)(*(int *)(param_1 + 0x18) + 0x20) + iVar3 * 8;
    iVar5 = _ZN13CMemoryStream7ReadIntEv(param_2);
    iVar3 = *(int *)(param_1 + 0x18);
    *(undefined4 *)(iVar3 + 0x14) = *(undefined4 *)(iVar3 + 0x28);
    for (; iVar5 != 0; iVar5 = iVar5 + -1) {
      iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
      **(int **)(*(int *)(param_1 + 0x18) + 0x14) =
           *(int *)(*(int *)(param_1 + 0x18) + 0x20) + iVar3 * 8;
      iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
      *(int *)(*(int *)(*(int *)(param_1 + 0x18) + 0x14) + 4) =
           *(int *)(*(int *)(param_1 + 0x18) + 0x20) + iVar3 * 8;
      iVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
      iVar6 = *(int *)(*(int *)(param_1 + 0x18) + 0x14);
      *(int *)(iVar6 + 8) = *(int *)(*(int *)(param_1 + 0x18) + 0x20) + iVar3 * 8;
      uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
      iVar3 = *(int *)(*(int *)(param_1 + 0x18) + 0x14);
      *(undefined4 *)(iVar6 + 0x10) = uVar1;
      uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
      *(undefined4 *)(iVar3 + 0x14) = uVar1;
      iVar6 = _ZN13CMemoryStream7ReadIntEv(param_2);
      iVar3 = *(int *)(param_1 + 0x18);
      iVar4 = *(int *)(iVar3 + 0x14);
      if (iVar6 == -1) {
        *(undefined4 *)(iVar4 + 0xc) = 0;
      }
      else {
        *(int *)(iVar4 + 0xc) = *(int *)(*(int *)(**(int **)(iVar4 + 4) + 0x10) + 0xc) + iVar6 * 4;
      }
      *(int *)(iVar3 + 0x14) = *(int *)(iVar3 + 0x14) + 0x18;
    }
    *(undefined1 *)(iVar3 + 6) = 1;
    *(int *)(iVar3 + 0x14) = *(int *)(iVar3 + 0x14) + -0x18;
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_24);
  return;
}


