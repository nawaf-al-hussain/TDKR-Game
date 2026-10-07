// _ZN13CZonesManagerC1Eb @ 002cc578

undefined4 *
_ZN13CZonesManagerC1Eb(undefined4 *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  int iVar5;
  
  puVar3 = (undefined4 *)(DAT_002cc6e4 + 0x2cc588);
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[0x1c] = 0;
  param_1[3] = 0;
  param_1[0x1d] = 0;
  param_1[4] = 0;
  param_1[0x1e] = 0;
  param_1[5] = 0;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[10] = param_1 + 8;
  param_1[0xb] = param_1 + 8;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x11] = 0;
  param_1[0x12] = 0;
  param_1[0x13] = 0xffffffff;
  *(undefined1 *)(param_1 + 0x14) = 0;
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x1b] = 0;
  *(undefined1 *)(param_1 + 0x1f) = 0;
  *(undefined1 *)((int)param_1 + 0x7e) = 1;
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  param_1[0x23] = 0;
  param_1[0x24] = 0;
  param_1[0x25] = 0;
  *(undefined1 *)(param_1 + 0x26) = 0;
  *(undefined1 *)((int)param_1 + 0x9a) = 0;
  *puVar3 = param_1;
  iVar1 = _Znwj(0x200);
  if (param_1[0x15] != 0) {
    _ZdlPv();
  }
  iVar5 = DAT_002cc6e8;
  param_1[0x17] = iVar1 + 0x200;
  iVar5 = iVar5 + 0x2cc668;
  param_1[0x15] = iVar1;
  param_1[0x16] = iVar1;
  uVar2 = _ZnwjPKci(0x24,iVar5,0x41,iVar1 + 0x200,param_4);
  _ZN21SceneNodeCacheManagerC1Ev();
  param_1[0x19] = uVar2;
  uVar2 = _ZnwjPKci(0x10,iVar5,0x42);
  _ZN22GameObjectCacheManagerC1Ev();
  param_1[0x1a] = uVar2;
  _ZN21SceneNodeCacheManager4InitEb(param_1[0x19],param_2);
  puVar3 = (undefined4 *)_ZnwjPKci(0xc,iVar5,0x4b);
  puVar4 = (undefined4 *)(DAT_002cc6ec + 0x2cc6cc);
  *puVar3 = 0;
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar4 = puVar3;
  return param_1;
}


