// _ZN24CElectricTurretComponent8SaveLoadEP13CMemoryStream @ 0023f8f8

void _ZN24CElectricTurretComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  int local_18;
  undefined4 local_14;
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  _ZN13CMemoryStream4ReadERi(param_2,&local_18);
  local_14 = 0xffffffff;
  _ZN13CMemoryStream4ReadERi(param_2);
  uVar1 = *(undefined4 *)(DAT_0023f9ac + 0x23f94c);
  *(undefined4 *)(param_1 + 0x18) = 0;
  iVar2 = _ZN13CZonesManager10FindObjectEit(uVar1,local_14,0x11);
  iVar3 = *(int *)(param_1 + 0x74);
  if (iVar2 != 0) {
    *(int *)(param_1 + 0x18) = iVar2;
  }
  if (local_18 != iVar3) {
    if ((iVar3 == 0x20) && (*(int *)(param_1 + 0xa4) != 0)) {
      _ZN11CGameObject13ReqInvalidateEv();
      iVar3 = *(int *)(param_1 + 0x74);
      *(undefined4 *)(param_1 + 0xa4) = 0;
    }
    *(int *)(param_1 + 0x78) = iVar3;
    *(int *)(param_1 + 0x74) = local_18;
    _ZN24CElectricTurretComponent12OnEnterStateENS_15E_TURRET_STATESES0_(param_1,local_18);
  }
  return;
}


