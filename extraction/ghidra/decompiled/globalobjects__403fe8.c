// _ZN6CLevel17SaveGlobalObjectsEP13CMemoryStream @ 00403fe8

void _ZN6CLevel17SaveGlobalObjectsEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  undefined4 uVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  
  iVar9 = *(int *)(DAT_0040410c + 0x404008);
  _ZN13CMemoryStream5WriteEi(param_2,iVar9);
  if (0 < iVar9) {
    iVar3 = *(int *)(param_1 + 0xb84);
    iVar8 = 0;
    iVar7 = 0;
    do {
      _ZN13CMemoryStream5WriteEi(param_2,*(undefined4 *)(iVar3 + iVar8 + 0x14));
      iVar3 = *(int *)(param_1 + 0xb84);
      iVar2 = iVar3 + iVar8;
      iVar4 = *(int *)(iVar2 + 0xc);
      while (iVar2 + 4 != iVar4) {
        uVar6 = *(undefined4 *)(iVar4 + 0x10);
        uVar5 = (uint)*(byte *)(iVar4 + 0x14);
        if (*(int *)(param_1 + 0xc0) == iVar7) {
          piVar1 = (int *)_ZN13CZonesManager10FindObjectEit
                                    (**(undefined4 **)(DAT_00404110 + 0x4040a0),uVar6,0x11);
          if (piVar1 != (int *)0x0) {
            uVar5 = (**(code **)(*piVar1 + 0x54))();
            if ((uVar5 != 0) &&
               (iVar3 = _ZNK11CGameObject23GetCollectibleComponentEv(piVar1), iVar3 != 0)) {
              iVar3 = _ZN21CCollectibleComponent11IsCollectedEv();
              if (iVar3 != 0) {
                uVar5 = 0;
              }
              *(char *)(iVar4 + 0x14) = (char)uVar5;
              goto LAB_00404040;
            }
          }
          *(char *)(iVar4 + 0x14) = (char)uVar5;
        }
LAB_00404040:
        _ZN13CMemoryStream5WriteEi(param_2,uVar6);
        _ZN13CMemoryStream5WriteEb(param_2,uVar5);
        iVar4 = _ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(iVar4);
        iVar3 = *(int *)(param_1 + 0xb84);
        iVar2 = iVar3 + iVar8;
      }
      iVar7 = iVar7 + 1;
      iVar8 = iVar8 + 0x18;
    } while (iVar7 != iVar9);
  }
  return;
}

