// _ZN6glitch5scene16CSkyBoxSceneNode27onRegisterSceneNodeInternalEPKv @ 0096a53c

undefined4
_ZN6glitch5scene16CSkyBoxSceneNode27onRegisterSceneNodeInternalEPKv(int param_1,undefined4 param_2)

{
  int *piVar1;
  undefined4 local_14 [2];
  
  piVar1 = *(int **)(*(int *)(param_1 + 0xe8) + 0x2c);
  local_14[0] = 0;
  (**(code **)(*piVar1 + 8))(piVar1,param_1,param_2,local_14,0,2,0,0x7fffffff);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_14);
  return 1;
}

