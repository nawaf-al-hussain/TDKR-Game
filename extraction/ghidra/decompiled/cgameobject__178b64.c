// _Z14CPlayAnimationP9lua_StateP11CGameObjectSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS5_6memory13E_MEMORY_HINTE0EEEEbbf @ 00178b64

undefined4
_Z14CPlayAnimationP9lua_StateP11CGameObjectSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS5_6memory13E_MEMORY_HINTE0EEEEbbf
          (undefined4 param_1,int param_2,undefined4 *param_3,int param_4,undefined1 param_5,
          undefined4 param_6)

{
  bool bVar1;
  int *piVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  int *piVar6;
  int *piVar7;
  float fVar8;
  
  if (param_2 != 0) {
    piVar2 = (int *)_ZNK11CGameObject12GetComponentEi(param_2,0xf5f8cfd);
    if (piVar2 == (int *)0x0) {
      return 0;
    }
    (**(code **)(*piVar2 + 0x30))(piVar2,1);
    iVar3 = _ZN19CAnimationComponent22GetAnimationIdFromNameEPKc(piVar2,*param_3);
    if (-1 < iVar3) {
      _ZN19CAnimationComponent13PlayAnimationEi(piVar2);
    }
    if (piVar2[0xb] != 0) {
      *(undefined1 *)(piVar2 + 0x14) = param_5;
      puVar5 = (undefined4 *)(**(code **)(*(int *)piVar2[0x1a] + 0x44))();
      piVar7 = (int *)*puVar5;
      if (piVar7 != (int *)0x0) {
        piVar6 = (int *)((int)piVar7 + *(int *)(*piVar7 + -0xc) + 4);
        DataMemoryBarrier(0xf);
        do {
          bVar1 = (bool)hasExclusiveAccess(piVar6);
        } while (!bVar1);
        *piVar6 = *piVar6 + 1;
        DataMemoryBarrier(0xf);
      }
      (**(code **)(*piVar7 + 0x44))(piVar7,param_5);
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar7 + *(int *)(*piVar7 + -0xc));
      if (piVar2[8] != 0) {
        puVar5 = (undefined4 *)(**(code **)(*(int *)piVar2[9] + 0x44))();
        (**(code **)(*(int *)*puVar5 + 0x44))((int *)*puVar5,param_5);
        _ZN19CAnimationComponent24SetCurrentAnimationSpeedEf(piVar2,param_6);
        if (param_4 == 0) {
          return 0;
        }
        goto LAB_00178bec;
      }
    }
    _ZN19CAnimationComponent24SetCurrentAnimationSpeedEf(piVar2,param_6);
    if (param_4 != 0) {
LAB_00178bec:
      if ((float)piVar2[0x13] == 0.0) {
        fVar8 = (float)piVar2[0x10];
      }
      else {
        fVar8 = (float)piVar2[0x10] / (float)piVar2[0x13];
      }
      lua_pushinteger(param_1,2);
      lua_pushinteger(param_1,(int)fVar8);
      uVar4 = lua_yield(param_1,2);
      return uVar4;
    }
  }
  return 0;
}

