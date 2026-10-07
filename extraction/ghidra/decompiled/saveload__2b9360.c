// _ZN15CWayPointObject8SaveLoadEP13CMemoryStream @ 002b9360

void _ZN15CWayPointObject8SaveLoadEP13CMemoryStream(int param_1,int *param_2)

{
  int iVar1;
  
  iVar1 = param_2[3];
  *(bool *)(param_1 + 100) = *(char *)(*param_2 + iVar1) != '\0';
  param_2[3] = iVar1 + 1;
  return;
}


