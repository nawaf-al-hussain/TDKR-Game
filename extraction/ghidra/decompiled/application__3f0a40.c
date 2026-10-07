// _ZN11Application23SendTrackingEventUnlockEiii @ 003f0a40

void _ZN11Application23SendTrackingEventUnlockEiii
               (undefined4 param_1,int param_2,int param_3,int param_4)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  
  if (param_2 < 0) {
    return;
  }
  if (1 < param_2) {
    if (param_2 != 2) {
      return;
    }
    if (7 < param_3 - 6U) {
      return;
    }
    param_4 = *(int *)(DAT_003f0e64 + 0x3f0b28 + (param_3 - 6U) * 4);
    if (param_4 == 0) {
      return;
    }
    uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
    uVar2 = 0x8a72;
    iVar4 = 0;
    iVar3 = 0;
    goto LAB_003f0b4c;
  }
  switch(param_3) {
  case 0:
    iVar3 = 0x8b15;
    param_4 = param_4 + 0x8b25;
    iVar4 = 0x8ae9;
    break;
  case 1:
    iVar3 = 0x8b15;
    param_4 = param_4 + 0x8b22;
    iVar4 = 0x8ae9;
    break;
  case 2:
    iVar3 = 0x8b15;
    param_4 = param_4 + 0x8b1d;
    iVar4 = 0x8ae9;
    break;
  case 3:
    iVar3 = 0x8b16;
    param_4 = param_4 + 0x8b34;
    iVar4 = 0x8ae9;
    break;
  case 4:
    iVar3 = 0x8b16;
    param_4 = param_4 + 0x8b2a;
    iVar4 = 0x8ae9;
    break;
  case 5:
    iVar3 = 0x8b16;
    param_4 = param_4 + 0x8b2f;
    iVar4 = 0x8ae9;
    break;
  case 6:
  default:
switchD_003f0a5c_default:
    iVar3 = 0;
    iVar4 = iVar3;
    param_4 = iVar3;
    break;
  case 7:
    iVar3 = 0x8b17;
    param_4 = param_4 + 0x8b4b;
    iVar4 = 0x8ae9;
    break;
  case 8:
    iVar3 = 0x8b17;
    param_4 = param_4 + 0x8b46;
    iVar4 = 0x8ae9;
    break;
  case 9:
    goto switchD_003f0a5c_default;
  case 10:
    iVar3 = 0x8b18;
    param_4 = param_4 + 0x8b39;
    iVar4 = 0x8ae9;
    break;
  case 0xb:
    iVar3 = 0x8b18;
    param_4 = param_4 + 0x8b3e;
    iVar4 = 0x8ae9;
    break;
  case 0xc:
    iVar3 = 0x8b18;
    param_4 = param_4 + 0x8b43;
    iVar4 = 0x8ae9;
    break;
  case 0xd:
    goto switchD_003f0a5c_default;
  case 0xe:
    iVar3 = 0x8b19;
    param_4 = param_4 + 0x8b50;
    iVar4 = 0x8ae9;
    break;
  case 0xf:
    iVar3 = 0x8b19;
    param_4 = param_4 + 0x8b55;
    iVar4 = 0x8ae9;
    break;
  case 0x10:
    iVar3 = 0x8b1a;
    param_4 = param_4 + 0x8b5a;
    iVar4 = 0x8aea;
    break;
  case 0x11:
    iVar3 = 0x8b1a;
    param_4 = param_4 + 0x8b5d;
    iVar4 = 0x8aea;
    break;
  case 0x12:
    iVar3 = 0x8b1a;
    param_4 = param_4 + 0x8b60;
    iVar4 = 0x8aea;
    break;
  case 0x13:
    iVar3 = 0x8b1a;
    param_4 = param_4 + 0x8b63;
    iVar4 = 0x8aea;
    break;
  case 0x14:
    iVar3 = 0x8b1a;
    param_4 = param_4 + 0x8b72;
    iVar4 = 0x8aea;
    break;
  case 0x15:
    iVar3 = 0x8b1a;
    param_4 = param_4 + 0x8b78;
    iVar4 = 0x8aea;
    break;
  case 0x16:
    iVar3 = 0x8b1b;
    param_4 = param_4 + 0x8b66;
    iVar4 = 0x8aea;
    break;
  case 0x17:
    iVar3 = 0x8b1b;
    param_4 = param_4 + 0x8b69;
    iVar4 = 0x8aea;
    break;
  case 0x18:
    iVar3 = 0x8b1b;
    param_4 = param_4 + 0x8b6c;
    iVar4 = 0x8aea;
    break;
  case 0x19:
    iVar3 = 0x8b1b;
    param_4 = param_4 + 0x8b6f;
    iVar4 = 0x8aea;
    break;
  case 0x1a:
    iVar3 = 0x8b1b;
    param_4 = param_4 + 0x8b75;
    iVar4 = 0x8aea;
    break;
  case 0x1b:
    iVar3 = 0x8b1b;
    param_4 = param_4 + 0x8b7b;
    iVar4 = 0x8aea;
    break;
  case 0x1c:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b92;
    iVar4 = 0x8aeb;
    break;
  case 0x1d:
    goto switchD_003f0a5c_default;
  case 0x1e:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b8f;
    iVar4 = 0x8aeb;
    break;
  case 0x1f:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b98;
    iVar4 = 0x8aeb;
    break;
  case 0x20:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b95;
    iVar4 = 0x8aeb;
    break;
  case 0x21:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b9b;
    iVar4 = 0x8aeb;
    break;
  case 0x22:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b7e;
    iVar4 = 0x8aeb;
    break;
  case 0x23:
    goto switchD_003f0a5c_default;
  case 0x24:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b80;
    iVar4 = 0x8aeb;
    break;
  case 0x25:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b82;
    iVar4 = 0x8aeb;
    break;
  case 0x26:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b87;
    iVar4 = 0x8aeb;
    break;
  case 0x27:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8b8c;
    iVar4 = 0x8aeb;
    break;
  case 0x28:
    iVar3 = 0x8b1c;
    param_4 = param_4 + 0x8c34;
    iVar4 = 0x8aeb;
  }
  uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
  uVar2 = 0x8a70;
LAB_003f0b4c:
  _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
            (uVar1,uVar2,0,param_4,iVar4,iVar3,0,0,0,0);
  return;
}


