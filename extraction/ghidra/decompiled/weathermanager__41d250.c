// _ZN15CWeatherManager15SetIlluminationEiff @ 0041d250

void _ZN15CWeatherManager15SetIlluminationEiff
               (int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  
  if (-1 < param_2) {
    iVar4 = *(int *)(param_1 + 0xc);
    iVar2 = *(int *)(param_1 + 0x10) - iVar4 >> 2;
    if (iVar2 == 0) {
      iVar2 = 0;
      iVar5 = 0;
    }
    else {
      iVar1 = 0;
      iVar5 = 0;
      do {
        if (param_2 == *(int *)(*(int *)(iVar4 + iVar1 * 4) + 8)) {
          iVar5 = iVar1;
        }
        iVar1 = iVar1 + 1;
      } while (iVar1 != iVar2);
      iVar2 = iVar5 << 2;
    }
    iVar1 = *(int *)(param_1 + 0x58);
    *(int *)(param_1 + 8) = iVar5;
    *(undefined1 *)(param_1 + 4) = 1;
    iVar5 = *(int *)(iVar4 + iVar2);
    if (iVar1 == 0) {
      *(undefined4 *)(param_1 + 0x78) = *(undefined4 *)(iVar5 + 0xc);
      *(undefined4 *)(param_1 + 0x7c) = *(undefined4 *)(iVar5 + 0x10);
      *(undefined4 *)(param_1 + 0x80) = *(undefined4 *)(iVar5 + 0xc);
      uVar3 = *(undefined4 *)(iVar5 + 0x10);
      *(undefined4 *)(param_1 + 0x88) = 0;
      *(undefined4 *)(param_1 + 0x8c) = param_4;
      *(undefined4 *)(param_1 + 0x84) = uVar3;
      *(undefined4 *)(param_1 + 0x94) = *(undefined4 *)(iVar5 + 0x14);
      uVar3 = *(undefined4 *)(iVar5 + 0x14);
      *(undefined4 *)(param_1 + 0x9c) = 0;
      *(undefined4 *)(param_1 + 0xa0) = param_4;
      *(undefined4 *)(param_1 + 0x98) = uVar3;
      iVar5 = *(int *)(iVar4 + iVar2);
      *(undefined4 *)(param_1 + 0xa8) = *(undefined4 *)(iVar5 + 0x18);
      *(undefined4 *)(param_1 + 0xac) = *(undefined4 *)(iVar5 + 0x1c);
      *(undefined4 *)(param_1 + 0xb0) = *(undefined4 *)(iVar5 + 0x18);
      uVar3 = *(undefined4 *)(iVar5 + 0x1c);
      *(undefined4 *)(param_1 + 0xb8) = 0;
      *(undefined4 *)(param_1 + 0xbc) = param_4;
      *(undefined4 *)(param_1 + 0xb4) = uVar3;
      *(undefined4 *)(param_1 + 0xc4) = *(undefined4 *)(iVar5 + 0x20);
      uVar3 = *(undefined4 *)(iVar5 + 0x20);
      *(undefined4 *)(param_1 + 0xcc) = 0;
      *(undefined4 *)(param_1 + 0xd0) = param_4;
      *(undefined4 *)(param_1 + 200) = uVar3;
      iVar2 = *(int *)(iVar4 + iVar2);
      *(undefined4 *)(param_1 + 0xd8) = *(undefined4 *)(iVar2 + 0x58);
      uVar3 = *(undefined4 *)(iVar2 + 0x58);
      *(undefined4 *)(param_1 + 0xe0) = 0;
      *(undefined4 *)(param_1 + 0xe4) = param_4;
      *(undefined4 *)(param_1 + 0xdc) = uVar3;
    }
    else {
      *(undefined4 *)(param_1 + 0x78) = *(undefined4 *)(iVar1 + 0xc);
      *(undefined4 *)(param_1 + 0x7c) = *(undefined4 *)(iVar1 + 0x10);
      *(undefined4 *)(param_1 + 0x80) = *(undefined4 *)(iVar5 + 0xc);
      uVar3 = *(undefined4 *)(iVar5 + 0x10);
      *(undefined4 *)(param_1 + 0x88) = 0;
      *(undefined4 *)(param_1 + 0x8c) = param_4;
      *(undefined4 *)(param_1 + 0x84) = uVar3;
      *(undefined4 *)(param_1 + 0x94) = *(undefined4 *)(iVar1 + 0x14);
      uVar3 = *(undefined4 *)(iVar5 + 0x14);
      *(undefined4 *)(param_1 + 0x9c) = 0;
      *(undefined4 *)(param_1 + 0xa0) = param_4;
      *(undefined4 *)(param_1 + 0x98) = uVar3;
      iVar5 = *(int *)(iVar4 + iVar2);
      *(undefined4 *)(param_1 + 0xa8) = *(undefined4 *)(iVar1 + 0x18);
      *(undefined4 *)(param_1 + 0xac) = *(undefined4 *)(iVar1 + 0x1c);
      *(undefined4 *)(param_1 + 0xb0) = *(undefined4 *)(iVar5 + 0x18);
      uVar3 = *(undefined4 *)(iVar5 + 0x1c);
      *(undefined4 *)(param_1 + 0xb8) = 0;
      *(undefined4 *)(param_1 + 0xbc) = param_4;
      *(undefined4 *)(param_1 + 0xb4) = uVar3;
      *(undefined4 *)(param_1 + 0xc4) = *(undefined4 *)(iVar1 + 0x20);
      uVar3 = *(undefined4 *)(iVar5 + 0x20);
      *(undefined4 *)(param_1 + 0xcc) = 0;
      *(undefined4 *)(param_1 + 0xd0) = param_4;
      *(undefined4 *)(param_1 + 200) = uVar3;
      iVar2 = *(int *)(iVar4 + iVar2);
      *(undefined4 *)(param_1 + 0xd8) = *(undefined4 *)(iVar1 + 0x58);
      uVar3 = *(undefined4 *)(iVar2 + 0x58);
      *(undefined4 *)(param_1 + 0xe0) = 0;
      *(undefined4 *)(param_1 + 0xe4) = param_4;
      *(undefined4 *)(param_1 + 0xdc) = uVar3;
    }
    uVar3 = *(undefined4 *)(iVar2 + 0xc);
    *(int *)(param_1 + 0x58) = iVar2;
    *(undefined4 *)(param_1 + 0x5c) = uVar3;
    *(undefined4 *)(param_1 + 0x60) = *(undefined4 *)(iVar2 + 0x10);
    *(undefined4 *)(param_1 + 100) = *(undefined4 *)(iVar2 + 0x14);
    *(undefined4 *)(param_1 + 0x68) = *(undefined4 *)(iVar2 + 0x18);
    *(undefined4 *)(param_1 + 0x6c) = *(undefined4 *)(iVar2 + 0x1c);
    *(undefined4 *)(param_1 + 0x70) = *(undefined4 *)(iVar2 + 0x20);
    *(undefined4 *)(param_1 + 0x74) = *(undefined4 *)(iVar2 + 0x58);
  }
  return;
}


