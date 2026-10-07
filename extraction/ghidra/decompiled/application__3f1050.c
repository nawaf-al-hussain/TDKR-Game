// _ZN11Application5_DrawEv @ 003f1050

void _ZN11Application5_DrawEv(int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  undefined4 local_3c;
  int local_38;
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  int local_28;
  int local_24;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  piVar6 = *(int **)(DAT_003f1388 + 0x3f1074);
  piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
  piVar3 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar6 + 4);
  (**(code **)(*piVar4 + 0x10))(piVar4,0);
  if (*(char *)(**(int **)(DAT_003f138c + 0x3f10a8) + 0xb5) == '\0') {
    (**(code **)(*piVar4 + 0x94))(piVar4,0xffffffff);
  }
  if (piVar3 == (int *)0x0) {
    (**(code **)(*piVar4 + 0x14))(piVar4);
  }
  else {
    (**(code **)(*piVar3 + 0x1c))(piVar3);
    (**(code **)(*piVar4 + 0x14))(piVar4);
    if (*(char *)(DAT_003f1390 + 0x3f10e8) != '\0') {
      (**(code **)(*piVar3 + 0x18))(piVar3);
      piVar3 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar6 + 4);
      if (piVar3 == (int *)0x0) goto LAB_003f113c;
    }
    (**(code **)(*piVar4 + 0x18))(piVar4);
    _ZN6glitch5video12IVideoDriver28DebugPolysSetCurrentObjectIDEi(piVar4,8);
    (**(code **)(*piVar3 + 0x20))(piVar3);
    _ZN6glitch5video12IVideoDriver28DebugPolysSetCurrentObjectIDEi(piVar4,999999);
    (**(code **)(*piVar4 + 0x1c))(piVar4);
  }
LAB_003f113c:
  iVar2 = DAT_003f13a4;
  if (*(char *)(DAT_003f1394 + 0x3f1148) != '\0') {
    _ZN6glitch5video12IVideoDriver28DebugPolysSetCurrentObjectIDEi(piVar4,7);
    iVar9 = *(int *)(iVar2 + 0x3f1310);
    iVar7 = *(int *)(iVar9 + 0x14);
    iVar2 = *(int *)(iVar9 + 0x18) - iVar7 >> 2;
    if (0 < iVar2) {
      if (iVar2 < 6) {
        iVar5 = 0;
      }
      else {
        iVar5 = iVar2 + -5;
      }
      iVar8 = iVar5 << 2;
      while( true ) {
        puVar1 = (undefined4 *)(iVar7 + iVar8);
        iVar5 = iVar5 + 1;
        iVar8 = iVar8 + 4;
        (**(code **)(*(int *)*puVar1 + 0x34))();
        if (iVar2 <= iVar5) break;
        iVar7 = *(int *)(iVar9 + 0x14);
      }
    }
    _ZN6glitch5video12IVideoDriver28DebugPolysSetCurrentObjectIDEi(piVar4,999999);
  }
  _ZN6glitch5video12IVideoDriver28DebugPolysSetCurrentObjectIDEi(piVar4,8);
  (**(code **)(*piVar4 + 0x18))(piVar4);
  _ZN9CheatMenu6RenderEv(*(undefined4 *)((int)&__DT_SYMTAB[0x1f1].st_value + param_1));
  if (*(char *)(DAT_003f1398 + 0x3f1188) != '\0') {
    iVar2 = _ZNK6glitch5video12IVideoDriver16getDrawCallCountEi(piVar4,0);
    if (iVar2 < 0x97) {
      if (iVar2 < 0x65) {
        local_3c = 0xff00ff00;
      }
      else {
        local_3c = 0xff2684f8;
      }
    }
    else {
      local_3c = 0xff0000ff;
    }
    piVar3 = *(int **)((int)&__DT_SYMTAB[0x1e9].st_name + param_1);
    iVar7 = DAT_003f139c + 0x3f11d4;
    iVar2 = DAT_003f13a0 + 0x3f11e4;
    (**(code **)(*piVar3 + 0x20))(&local_38,piVar3,iVar7);
    local_28 = local_38 + 5;
    local_24 = local_34 + 5;
    local_30 = 5;
    local_2c = 5;
    _Z6strcpyPwPKc(iVar2,iVar7);
    piVar3 = *(int **)((int)&__DT_SYMTAB[0x1e9].st_name + param_1);
    (**(code **)(*piVar3 + 0xc))(piVar3,iVar2,&local_30,local_3c,0,0,0);
  }
  iVar2 = _ZN6CLevel8GetLevelEv();
  if (iVar2 != 0) {
    _ZN6CLevel8GetLevelEv();
    iVar2 = _ZN6CLevel15GetZonesManagerEv();
    if (iVar2 != 0) {
      _ZN6CLevel8GetLevelEv();
      _ZN6CLevel15GetZonesManagerEv();
      _ZN13CZonesManager8Render2DEv();
    }
  }
  (**(code **)(*piVar4 + 0x1c))(piVar4);
  _ZN6glitch5video12IVideoDriver28DebugPolysSetCurrentObjectIDEi(piVar4,999999);
  _ZN6glitch5video12IVideoDriver11swapBuffersEi(piVar4,0);
  return;
}


