// _ZN15PlayerComponent8SaveLoadEP13CMemoryStream @ 0026cc2c

void _ZN15PlayerComponent8SaveLoadEP13CMemoryStream(int *param_1,undefined4 param_2)

{
  int iVar1;
  int *piVar2;
  code *pcVar3;
  undefined4 local_28;
  undefined1 auStack_24 [4];
  int local_20;
  int local_1c;
  
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 0xd);
  _ZN13CMemoryStream4ReadERi(param_2,&local_28);
  _ZN13CMemoryStream4ReadERi(param_2,auStack_24);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x9d);
  iVar1 = _ZN6CLevel8GetLevelEv();
  pcVar3 = *(code **)(*param_1 + 0x50);
  *(undefined4 *)(iVar1 + 0x10c) = local_28;
  (*pcVar3)(param_1);
  iVar1 = param_1[0x9c];
  param_1[0x9c] = 0;
  param_1[0x9d] = iVar1;
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xb8);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xca);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x56);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x13a);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x122);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x123);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x124);
  local_20 = *(int *)(DAT_0026cdd4 + 0x26cd08) + 0xc;
  _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_20);
  local_1c = -1;
  _ZN13CMemoryStream4ReadERi(param_2);
  if ((0 < local_1c) &&
     (iVar1 = _ZN13CZonesManager10FindObjectEit(*(undefined4 *)(DAT_0026cdd8 + 0x26cd44),local_1c,1)
     , iVar1 != 0)) {
    piVar2 = (int *)_ZNK11CGameObject12GetComponentEi(iVar1,0x222500f6);
    if (piVar2 == (int *)0x0) {
      piVar2 = (int *)_ZNK11CGameObject12GetComponentEi(iVar1,0xd1839c4);
      param_1[0x16e] = (int)piVar2;
      if (piVar2 != (int *)0x0) {
        (**(code **)(*piVar2 + 0x34))(piVar2,1);
      }
    }
    else {
      iVar1 = *piVar2;
      param_1[0x16e] = (int)piVar2;
      (**(code **)(iVar1 + 0x34))(piVar2,1);
    }
  }
  (**(code **)(*(int *)param_1[1] + 0x80))((int *)param_1[1],1);
  _ZN11CGameObject10ChangeMeshEPKc(param_1[1],local_20);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_20);
  return;
}


