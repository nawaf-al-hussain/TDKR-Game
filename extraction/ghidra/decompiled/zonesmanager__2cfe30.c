// _ZN13CZonesManager16RunInitialScriptEv @ 002cfe30

void _ZN13CZonesManager16RunInitialScriptEv(int param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  
  piVar4 = *(int **)(param_1 + 0x84);
  piVar2 = *(int **)(param_1 + 0x80);
  do {
    piVar3 = piVar2;
    if (piVar2 == piVar4) {
      return;
    }
    while( true ) {
      piVar2 = piVar3 + 1;
      iVar1 = *piVar3;
      if (*(char *)(iVar1 + 0x17c) == '\0') break;
      if (0 < *(int *)(iVar1 + 0x178)) {
        _ZN17CLuaScriptManager13StartFunctionEiiP11ScriptParamP15CGameObjectBaseiii
                  (**(undefined4 **)(DAT_002cfeb0 + 0x2cfe88),*(int *)(iVar1 + 0x178),0,0,0,
                   0xffffffff,0xffffffff,2);
        piVar4 = *(int **)(param_1 + 0x84);
      }
      *(undefined1 *)(iVar1 + 0x17c) = 0;
      piVar3 = piVar2;
      if (piVar2 == piVar4) {
        return;
      }
    }
  } while( true );
}


