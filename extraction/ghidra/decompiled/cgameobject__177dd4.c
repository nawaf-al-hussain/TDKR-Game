// _Z12CActorLookToP15CGameObjectBaseS0_ffff @ 00177dd4

void _Z12CActorLookToP15CGameObjectBaseS0_ffff
               (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,float param_6)

{
  int iVar1;
  float local_24;
  undefined4 local_20;
  undefined4 local_1c;
  
  local_24 = param_6;
  local_20 = param_5;
  local_1c = param_4;
  iVar1 = (**(code **)(*param_1 + 0x14))();
  if (iVar1 == 0) {
    param_1 = param_1 + -0xd;
  }
  else {
    param_1 = (int *)param_1[0x1d];
  }
  if (param_1 != (int *)0x0) {
    _ZN11CGameObject6LookAtEP15CGameObjectBasefRKN6glitch4core8vector3dIfEEib
              (param_1,param_2,param_3,&local_24,2,param_6 == 0.0);
  }
  return;
}

