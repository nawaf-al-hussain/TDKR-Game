// _ZN28CSurveillanceCameraComponent8SaveLoadEP13CMemoryStream @ 00257d00

void _ZN28CSurveillanceCameraComponent8SaveLoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  uint in_fpscr;
  float fVar4;
  
  _ZN13CMemoryStream5WriteEb(param_2,*(undefined1 *)(param_1 + 0xd),param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x374);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x428);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x380);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x388);
  switch(*(int *)(param_1 + 0x374)) {
  case 0:
    break;
  case 1:
    break;
  case 2:
    break;
  case 3:
    uVar3 = 1;
    goto LAB_00257dbc;
  case 4:
    uVar2 = 2;
    goto LAB_00257d80;
  case 5:
    goto LAB_00257de4;
  case 6:
    uVar3 = 0;
LAB_00257dbc:
    *(uint *)(param_1 + 0x10) = uVar3;
    *(undefined4 *)(param_1 + 0x14) = 0xffffffff;
    _ZN28CSurveillanceCameraComponent32UpdateCrtColorFromBlendingFactorEv(param_1);
    goto LAB_00257d98;
  case 7:
LAB_00257de4:
    *(bool *)(param_1 + 0x400) = *(int *)(param_1 + 0x374) == 5;
    *(undefined4 *)(param_1 + 0x364) = 0;
    iVar1 = _Z7getRandv();
    uVar3 = (uint)*(byte *)(param_1 + 0x400);
    *(undefined4 *)(param_1 + 0x10) = 0;
    *(undefined4 *)(param_1 + 0x14) = 0xffffffff;
    fVar4 = (float)VectorSignedToFloat(iVar1 % 0x42,(byte)(in_fpscr >> 0x16) & 3);
    *(float *)(param_1 + 0x404) = fVar4 + DAT_00257e60;
    _ZN28CSurveillanceCameraComponent32UpdateCrtColorFromBlendingFactorEv(param_1);
    goto LAB_00257d98;
  default:
    uVar3 = 1;
    goto LAB_00257d98;
  }
  uVar2 = 0;
LAB_00257d80:
  *(undefined4 *)(param_1 + 0x10) = uVar2;
  *(undefined4 *)(param_1 + 0x14) = 0xffffffff;
  uVar3 = 1;
  _ZN28CSurveillanceCameraComponent32UpdateCrtColorFromBlendingFactorEv(param_1);
LAB_00257d98:
  *(undefined4 *)(param_1 + 0x358) = 0;
  (**(code **)(**(int **)(param_1 + 0x390) + 0x4c))(*(int **)(param_1 + 0x390),uVar3);
  return;
}


