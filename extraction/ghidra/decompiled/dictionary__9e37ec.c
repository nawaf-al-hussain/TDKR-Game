// deflateSetDictionary @ 009e37ec

undefined4 deflateSetDictionary(int param_1,void *param_2,uint param_3,undefined4 param_4)

{
  byte *pbVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  int iVar10;
  
  if (((param_1 == 0) || (iVar5 = *(int *)(param_1 + 0x1c), iVar5 == 0 || param_2 == (void *)0x0))
     || (iVar3 = *(int *)(iVar5 + 0x18), iVar3 == 2)) {
    return 0xfffffffe;
  }
  if (iVar3 == 1) {
    iVar3 = *(int *)(iVar5 + 4);
    if (iVar3 != 0x2a) {
      return 0xfffffffe;
    }
  }
  else if (iVar3 == 0) goto LAB_009e382c;
  uVar2 = adler32(*(undefined4 *)(param_1 + 0x30),param_2,param_3,iVar3,param_4);
  *(undefined4 *)(param_1 + 0x30) = uVar2;
LAB_009e382c:
  if (2 < param_3) {
    uVar6 = *(int *)(iVar5 + 0x2c) - 0x106;
    if (uVar6 < param_3) {
      param_2 = (void *)((int)param_2 + (param_3 - uVar6));
      param_3 = uVar6;
    }
    memcpy(*(void **)(iVar5 + 0x38),param_2,param_3);
    *(uint *)(iVar5 + 0x6c) = param_3;
    uVar4 = 0;
    *(uint *)(iVar5 + 0x5c) = param_3;
    uVar6 = (uint)**(byte **)(iVar5 + 0x38);
    uVar8 = *(uint *)(iVar5 + 0x58);
    iVar3 = *(int *)(iVar5 + 0x40);
    *(uint *)(iVar5 + 0x48) = uVar6;
    uVar9 = *(uint *)(iVar5 + 0x34);
    pbVar1 = *(byte **)(iVar5 + 0x38) + 1;
    iVar10 = *(int *)(iVar5 + 0x44);
    uVar7 = *(uint *)(iVar5 + 0x54);
    uVar6 = ((uint)*pbVar1 ^ uVar6 << (uVar8 & 0xff)) & uVar7;
    *(uint *)(iVar5 + 0x48) = uVar6;
    do {
      pbVar1 = pbVar1 + 1;
      uVar6 = ((uint)*pbVar1 ^ uVar6 << (uVar8 & 0xff)) & uVar7;
      *(uint *)(iVar5 + 0x48) = uVar6;
      *(undefined2 *)(iVar3 + (uVar4 & uVar9) * 2) = *(undefined2 *)(iVar10 + uVar6 * 2);
      *(short *)(iVar10 + uVar6 * 2) = (short)uVar4;
      uVar4 = uVar4 + 1;
    } while (uVar4 <= param_3 - 3);
    return 0;
  }
  return 0;
}


