// _Z23CStartSoundAtObjectNodeSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEP11CGameObjectfibb @ 00177c44

void _Z23CStartSoundAtObjectNodeSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEP11CGameObjectfibb
               (undefined4 *param_1,int *param_2,undefined4 param_3,undefined4 param_4,char param_5,
               undefined1 param_6)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined1 auStack_c8 [40];
  undefined1 auStack_a0 [40];
  int local_78 [2];
  undefined4 local_70;
  undefined4 uStack_6c;
  int local_68;
  int local_64;
  int local_60;
  int local_5c;
  int local_58;
  undefined1 auStack_50 [44];
  
  if ((param_2[0x2c] == 0) || (param_5 == '\0')) {
    puVar4 = *(undefined4 **)(DAT_00177dcc + 0x177c88);
    uVar1 = _ZN15VoxSoundManager17GetDynamicEmitterEP11CGameObject(*puVar4,param_2);
    _ZN3vox13EmitterHandleC1ERKS0_(auStack_c8,uVar1);
    iVar2 = _ZN15VoxSoundManager21IsEmitterPlayingSoundERN3vox13EmitterHandleEPKc
                      (*puVar4,auStack_c8,*param_1);
    if (iVar2 == 0) {
      uVar3 = *puVar4;
      uVar5 = *param_1;
      uVar1 = (**(code **)(*param_2 + 0x18))(param_2);
      _ZN15VoxSoundManager6Play3DEPKciRKN6glitch4core8vector3dIfEEbff
                (auStack_a0,uVar3,uVar5,param_4,uVar1,param_6,0x3f800000,param_3);
      if (param_5 != '\0') {
        local_78[0] = *(int *)(DAT_00177dd0 + 0x177d24) + 8;
        local_70 = 0xffffffff;
        uStack_6c = 0xffffffff;
        local_68 = iVar2;
        local_64 = iVar2;
        local_60 = iVar2;
        local_5c = iVar2;
        local_58 = iVar2;
        iVar2 = _ZNK3vox6HandleeqERKS0_(auStack_c8,local_78);
        _ZN3vox13EmitterHandleD1Ev(local_78);
        if (iVar2 == 0) {
          uVar1 = *puVar4;
          _ZN3vox13EmitterHandleC1ERKS0_(auStack_50,auStack_c8);
          _ZN15VoxSoundManager4StopEN3vox13EmitterHandleEi(uVar1,auStack_50,100);
          _ZN3vox13EmitterHandleD1Ev(auStack_50);
        }
        _ZN15VoxSoundManager23AddDynamicEmitterObjectEP11CGameObjectRKN3vox13EmitterHandleEb
                  (*puVar4,param_2,auStack_a0,0);
      }
      _ZN3vox13EmitterHandleD1Ev(auStack_a0);
    }
    _ZN3vox13EmitterHandleD1Ev(auStack_c8);
  }
  else {
    _ZN15PlayerComponent10StartSoundEPKcibff
              (param_2[0x2c],*param_1,param_4,param_6,0x3f800000,param_3);
  }
  return;
}

