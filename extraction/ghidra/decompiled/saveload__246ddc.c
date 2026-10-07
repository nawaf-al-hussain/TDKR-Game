// _ZN21CInteractionComponent8SaveLoadEP13CMemoryStream @ 00246ddc

void _ZN21CInteractionComponent8SaveLoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  undefined4 uVar8;
  int iVar9;
  uint uVar10;
  int *piVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  undefined1 uStack_28;
  undefined1 uStack_27;
  undefined1 auStack_1c [12];
  undefined4 uStack_10;
  
  uStack_10 = param_4;
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  uVar8 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x18) = uVar8;
  uVar8 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x1c) = uVar8;
  uVar8 = _ZN13CMemoryStream7ReadIntEv(param_2);
  piVar11 = *(int **)(DAT_00246e6c + 0x246e20);
  *(undefined4 *)(param_1 + 0x24) = uVar8;
  piVar11 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar11 + 4);
  iVar9 = (**(code **)(*piVar11 + 8))(piVar11,2);
  iVar7 = DAT_0043647c;
  iVar6 = DAT_00436478;
  iVar5 = DAT_00436474;
  iVar4 = DAT_00436470;
  iVar3 = DAT_0043646c;
  iVar2 = DAT_00436468;
  iVar1 = DAT_00436460;
  if (iVar9 == 0) {
    return;
  }
  uVar10 = *(uint *)(param_1 + 4);
  iVar9 = **(int **)(DAT_00246e70 + 0x246e5c);
  if (uVar10 != 0) {
    uVar10 = uVar10 + 0x34;
  }
  iVar14 = iVar9 + 0x430;
  iVar13 = *(int *)(iVar9 + 0x434);
  iVar12 = iVar14;
  while (iVar13 != 0) {
    if (*(uint *)(iVar13 + 0x10) < uVar10) {
      iVar13 = *(int *)(iVar13 + 0xc);
    }
    else {
      iVar13 = *(int *)(iVar13 + 8);
      iVar12 = iVar13;
    }
  }
  iVar13 = iVar14;
  if ((iVar14 != iVar12) && (iVar13 = iVar12, uVar10 < *(uint *)(iVar12 + 0x10))) {
    iVar13 = iVar14;
  }
  if (iVar14 != iVar13) {
    uStack_28 = 0;
    uStack_27 = 0;
    switch(uVar8) {
    case 0:
      *(undefined1 *)(iVar9 + 3) = 0;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar2 + 0x4363d0);
      break;
    case 1:
      *(undefined1 *)(iVar9 + 3) = 0;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar3 + 0x4363ec);
      break;
    case 2:
      *(undefined1 *)(iVar9 + 3) = 0;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar4 + 0x436408);
      break;
    case 3:
      *(undefined1 *)(iVar9 + 3) = 0;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar5 + 0x436424);
      break;
    case 4:
      *(undefined1 *)(iVar9 + 3) = 0;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar6 + 0x436440);
      break;
    case 5:
      *(undefined1 *)(iVar9 + 3) = 1;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar7 + 0x43645c);
      break;
    case 6:
      *(undefined1 *)(iVar9 + 3) = 1;
      _ZN7gameswf7ASValue9setStringEPKc(&uStack_28,iVar1 + 0x43637c);
    }
    _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
              (auStack_1c,iVar13 + 0x14,DAT_00436464 + 0x436394,&uStack_28,1);
    _ZN7gameswf7ASValue8dropRefsEv(auStack_1c);
    *(undefined4 *)(iVar13 + 0x130) = uVar8;
    _ZN7gameswf7ASValue8dropRefsEv(&uStack_28);
  }
  return;
}


