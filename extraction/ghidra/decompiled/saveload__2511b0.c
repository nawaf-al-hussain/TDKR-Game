// _ZN16CSniperComponent8SaveLoadEP13CMemoryStream @ 002511b0

void _ZN16CSniperComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  undefined4 local_14 [2];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x25);
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x2c);
  if (*(char *)(param_1 + 0x25) != '\0') {
    *(undefined1 *)(param_1 + 0x25) = 0;
    uVar1 = _ZN6CLevel8GetLevelEv();
    uVar1 = _ZN6CLevel20FindObjectOrWaypointEi(uVar1,local_14[0]);
    *(undefined4 *)(param_1 + 0x28) = uVar1;
    if ((*(char *)(param_1 + 0x25) != '\0') ||
       (_ZN16CSniperComponent8ActivateEv(param_1), *(char *)(param_1 + 0x25) != '\0')) {
      _ZN16CSniperComponent9State_setENS_7E_STATEENS_7E_SCOPEEb(param_1,2,1,1);
    }
  }
  return;
}


