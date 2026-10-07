// _ZN25CMainStoryQuestsComponent14SaveLoadGlobalEP13CMemoryStream @ 001906f4

void _ZN25CMainStoryQuestsComponent14SaveLoadGlobalEP13CMemoryStream
               (int *param_1,undefined4 param_2)

{
  char cVar1;
  
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 8);
  _ZN13CMemoryStream4ReadERf(param_2);
  param_1[0xb] = 0;
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xc);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 10);
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 0x31);
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 0x32);
  cVar1 = **(char **)(DAT_00190790 + 0x19076c);
  param_1[9] = param_1[10];
  if (cVar1 != '\0') {
    (**(code **)(*param_1 + 0x18))(param_1);
  }
  return;
}


