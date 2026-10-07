// _Z25CSpawnHelicopterNearActorP11CGameObjectfRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESB_ff @ 00179154

int _Z25CSpawnHelicopterNearActorP11CGameObjectfRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESB_ff
              (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
              undefined4 param_5,undefined4 param_6)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  
  iVar1 = 0;
  if (param_1 != 0) {
    _ZN6CLevel8GetLevelEv();
    iVar1 = _ZN6CLevel10GetNavMeshEv();
    if (iVar1 == 0) {
      iVar1 = 0;
    }
    else {
      iVar1 = _ZN13CZonesManager20SpawnObjectNearActorEP11CGameObjectRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEESC_fffb
                        (**(undefined4 **)(DAT_00179200 + 0x17919c),param_1,param_3,param_4,param_2,
                         param_5,param_6,1);
      if (iVar1 != 0) {
        _ZN11CGameObject12IsHelicopterEv();
        iVar2 = _ZN11CGameObject12IsHelicopterEv(iVar1);
        if (iVar2 != 0) {
          uVar3 = _ZNK11CGameObject12GetComponentEi(iVar1,0x786f6ecb);
          _ZN16CHelicopterLogic13SetWantedHeliEb(uVar3,1);
        }
      }
    }
  }
  return iVar1;
}

