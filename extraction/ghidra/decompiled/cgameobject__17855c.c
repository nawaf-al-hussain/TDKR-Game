// _Z28CDisableInteractionForObjectP11CGameObject @ 0017855c

void _Z28CDisableInteractionForObjectP11CGameObject
               (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  
  piVar1 = (int *)_ZNK11CGameObject12GetComponentEi(param_1,0x34747ebe,param_3,param_4,param_4);
  if (piVar1 == (int *)0x0) {
    return;
  }
  (**(code **)(*piVar1 + 0x30))(piVar1,0);
  return;
}

