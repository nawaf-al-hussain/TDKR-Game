// _ZN22GameObjectCacheManager11PopSaveLoadEiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE @ 001fb8e8

int * _ZN22GameObjectCacheManager11PopSaveLoadEiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (int param_1,int param_2,int param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  undefined8 uVar6;
  
  iVar2 = *(int *)(param_1 + 4);
  iVar3 = *(int *)(param_1 + 8) - iVar2 >> 2;
  iVar4 = iVar3 + -1;
  if (-1 < iVar4) {
    iVar3 = (iVar3 + 0x3fffffff) * 4;
    iVar1 = param_2;
    while( true ) {
      piVar5 = *(int **)(iVar2 + iVar3);
      iVar3 = iVar3 + -4;
      if (piVar5[0x39] == param_2) {
        uVar6 = (**(code **)(*piVar5 + 0xa0))(piVar5,iVar1);
        iVar1 = (int)((ulonglong)uVar6 >> 0x20);
        if ((int)uVar6 == 0) {
          iVar2 = _ZN11CGameObject11CanBeReusedEv(piVar5);
          iVar1 = param_3;
          if (iVar2 != 0) {
            uVar6 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                              (piVar5 + 0x3f);
            iVar1 = (int)((ulonglong)uVar6 >> 0x20);
            if ((int)uVar6 == 0) {
              return piVar5;
            }
          }
        }
      }
      iVar4 = iVar4 + -1;
      if (iVar4 < 0) break;
      iVar2 = *(int *)(param_1 + 4);
    }
  }
  return (int *)0x0;
}


