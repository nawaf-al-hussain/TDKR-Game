// _ZN13CAIController17Alliance_RegisterEP11CGameObject11AI_ALLIANCE @ 001884e8

void _ZN13CAIController17Alliance_RegisterEP11CGameObject11AI_ALLIANCE
               (int param_1,undefined4 param_2,uint param_3)

{
  undefined4 local_1c;
  undefined1 auStack_18 [8];
  undefined1 auStack_10 [12];
  
  local_1c = param_2;
  if ((param_3 & 1) == 0) {
    if ((param_3 & 2) != 0) {
      _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE6insertERKS1_(auStack_10,param_1 + 0xac,&local_1c)
      ;
    }
  }
  else {
    _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE6insertERKS1_(auStack_18,param_1 + 0xdc,&local_1c);
  }
  return;
}

