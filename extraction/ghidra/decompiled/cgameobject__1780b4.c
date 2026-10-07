// _Z22CGetDistBetweenObjectsP15CGameObjectBaseS0_ @ 001780b4

void _Z22CGetDistBetweenObjectsP15CGameObjectBaseS0_
               (int *param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 extraout_r2;
  
  uVar1 = (**(code **)(*param_1 + 0xc))();
  uVar2 = (**(code **)(*param_2 + 0xc))(param_2);
  _ZNK6glitch4core8vector3dIfE15getDistanceFromERKS2_(uVar1,uVar2,extraout_r2,param_4);
  return;
}

