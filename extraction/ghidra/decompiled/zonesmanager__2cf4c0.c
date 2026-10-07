// _ZN13CZonesManager10FindObjectEit @ 002cf4c0

int _ZN13CZonesManager10FindObjectEit(int param_1,int param_2,uint param_3)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  
  if (((param_3 & 0x10) != 0) && (iVar1 = _ZN6CLevel8GetLevelEv(), *(int *)(iVar1 + 0xec) != 0)) {
    iVar1 = _ZN6CLevel8GetLevelEv();
    iVar1 = (**(code **)(**(int **)(iVar1 + 0xec) + 0x14))();
    if (iVar1 == param_2) {
      iVar1 = _ZN6CLevel8GetLevelEv();
      return *(int *)(iVar1 + 0xec);
    }
  }
  iVar1 = _ZN17CLuaScriptManager18GetCurrentObjectIDEv(**(undefined4 **)(DAT_002cf5e8 + 0x2cf4e4));
  if (param_2 == iVar1) {
    iVar1 = **(int **)(DAT_002cf5ec + 0x2cf5dc);
    if (iVar1 != 0) {
      iVar1 = iVar1 + -0x34;
    }
    return iVar1;
  }
  piVar3 = *(int **)(param_1 + 0x84);
  piVar4 = *(int **)(param_1 + 0x80);
  do {
    piVar5 = piVar4;
    if (piVar4 == piVar3) {
      return 0;
    }
    while( true ) {
      piVar4 = piVar5 + 1;
      iVar1 = *piVar5;
      if (param_2 < 0) break;
      if (param_3 == 0) {
        iVar2 = _ZN11ObjManagers10FindObjectEit(*(undefined4 *)(iVar1 + 0x134),param_2,0);
        if (iVar2 != 0) {
          return iVar2;
        }
      }
      else {
        iVar2 = _ZN23ObjManager_BinarySearch10FindObjectEi(*(undefined4 *)(iVar1 + 0x138),param_2);
        if (iVar2 != 0) {
          return iVar2;
        }
      }
      piVar3 = *(int **)(iVar1 + 0x13c);
      do {
        piVar5 = piVar3;
        if (piVar5 == *(int **)(iVar1 + 0x140)) goto LAB_002cf558;
        iVar2 = (**(code **)(*(int *)*piVar5 + 0x14))();
        piVar3 = piVar5 + 1;
      } while (param_2 != iVar2);
      if (*piVar5 != 0) {
        return *piVar5;
      }
LAB_002cf558:
      piVar3 = *(int **)(param_1 + 0x84);
      piVar5 = piVar4;
      if (piVar4 == piVar3) {
        return 0;
      }
    }
  } while( true );
}


