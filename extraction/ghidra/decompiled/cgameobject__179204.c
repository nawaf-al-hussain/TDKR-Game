// _Z20CSetHelicopterFollowP11CGameObjectb @ 00179204

void _Z20CSetHelicopterFollowP11CGameObjectb(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  
  if (param_1 == 0) {
    return;
  }
  uVar1 = _ZNK11CGameObject12GetComponentEi(param_1,0x786f6ecb);
  _ZN16CHelicopterLogic19SetHelicopterFollowEb(uVar1,param_2);
  return;
}

