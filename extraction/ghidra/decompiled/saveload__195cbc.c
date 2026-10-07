// _ZN13CQuestManager16SaveLoadHotSpotsEP13CMemoryStream @ 00195cbc

void _ZN13CQuestManager16SaveLoadHotSpotsEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  undefined1 local_1a;
  undefined1 local_19;
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x7c);
  iVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar1) {
    iVar6 = 0;
    do {
      iVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
      _ZN13CMemoryStream8ReadBoolERb(param_2,&local_1a);
      _ZN13CMemoryStream8ReadBoolERb(param_2,&local_19);
      iVar4 = *(int *)(param_1 + 0x78);
      if ((iVar4 == 0) || (iVar3 = iVar4, iVar2 != *(int *)(iVar4 + 8))) {
        piVar5 = *(int **)(param_1 + 0x34);
        do {
          if (*(int **)(param_1 + 0x38) == piVar5) goto LAB_00195d50;
          iVar3 = *piVar5;
          piVar5 = piVar5 + 1;
        } while (iVar2 != *(int *)(iVar3 + 8));
      }
      *(undefined1 *)(iVar3 + 0x24) = local_1a;
LAB_00195d50:
      if ((iVar4 == 0) || (iVar2 != *(int *)(iVar4 + 8))) {
        piVar5 = *(int **)(param_1 + 0x34);
        do {
          if (*(int **)(param_1 + 0x38) == piVar5) goto joined_r0x00195d94;
          iVar4 = *piVar5;
          piVar5 = piVar5 + 1;
        } while (iVar2 != *(int *)(iVar4 + 8));
      }
      *(undefined1 *)(iVar4 + 0x26) = local_19;
joined_r0x00195d94:
      iVar6 = iVar6 + 1;
    } while (iVar6 != iVar1);
  }
  *(undefined1 *)(param_1 + 0x68) = 0;
  *(undefined4 *)(param_1 + 0x78) = 0;
  _ZN13CQuestManager16AddHotSpotsToMapEv(param_1);
  return;
}


