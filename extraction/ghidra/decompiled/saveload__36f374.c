// _ZN11CGameObject14SaveLoadGlobalEP13CMemoryStream @ 0036f374

void _ZN11CGameObject14SaveLoadGlobalEP13CMemoryStream
               (int *param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  code *pcVar2;
  bool bVar3;
  
  iVar1 = param_2[3] + 1;
  pcVar2 = *(code **)(*param_1 + 0x50);
  bVar3 = *(char *)(*param_2 + param_2[3]) != '\0';
  param_2[3] = iVar1;
  (*pcVar2)(param_1,bVar3,iVar1,pcVar2,param_4);
  if (bVar3) {
    return;
  }
  (**(code **)(*param_1 + 0x80))(param_1,0);
  return;
}


