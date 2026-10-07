// _ZN15CNpcAIComponent8SaveLoadEP13CMemoryStream @ 00295c40

void _ZN15CNpcAIComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined1 local_15;
  int local_14 [2];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  *(int *)(param_1 + 0x2c) = local_14[0];
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  *(int *)(param_1 + 0x44) = local_14[0];
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  if (0 < local_14[0]) {
    uVar1 = _ZN6CLevel8GetLevelEv();
    uVar1 = _ZN6CLevel19FindWayPointInRoomsEi(uVar1,local_14[0]);
    iVar2 = *(int *)(param_1 + 200);
    if (iVar2 != 0) {
      if (*(int *)(iVar2 + 0x74) != 0) {
        *(undefined4 *)(iVar2 + 0x74) = 0;
      }
      *(undefined1 *)(param_1 + 0xd0) = 0;
    }
    *(undefined4 *)(param_1 + 200) = uVar1;
    _ZN15CWayPointObject18GenerateRandomNextEv();
    if (*(int *)(param_1 + 200) != 0) {
      *(undefined4 *)(*(int *)(param_1 + 200) + 0x74) = *(undefined4 *)(param_1 + 4);
    }
  }
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x160);
  _ZN13CMemoryStream4ReadERb(param_2,&local_15);
  *(undefined1 *)(param_1 + 0x161) = local_15;
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x15c);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x164);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x1d0);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x16b);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x178);
  _ZN13CMemoryStream4ReadERb(param_2,&local_15);
  *(undefined1 *)(param_1 + 0x1e0) = local_15;
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  *(int *)(param_1 + 0x34) = local_14[0];
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  *(int *)(param_1 + 0x434) = local_14[0];
  if (*(int *)(param_1 + 0x2c) == 0x400000) {
    *(undefined4 *)(param_1 + 0x34) = 2;
    _ZN15CNpcAIComponent8SetStateENS_7E_STATEEPKvb(param_1,2,0,0);
    *(undefined4 *)(param_1 + 0xe0) = 0;
  }
  return;
}


