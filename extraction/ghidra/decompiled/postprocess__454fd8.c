// _ZN18CPostProcessEffectC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 00454fd8

int * _ZN18CPostProcessEffectC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 *param_2,undefined4 param_3,int param_4)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  int local_30;
  int *local_2c;
  int *local_28;
  int local_24;
  
  iVar2 = DAT_0045518c + 0x454ff8;
  iVar3 = DAT_00455190 + 0x455008;
  param_1[1] = -0x40800000;
  *param_1 = iVar3;
  param_1[2] = -0x40800000;
  param_1[3] = -0x40800000;
  param_1[4] = 0x3f800000;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (param_1 + 5,iVar2);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (param_1 + 6,iVar2);
  iVar2 = *(int *)(DAT_00455194 + 0x455050);
  param_1[7] = -1;
  param_1[0xb] = -1;
  param_1[0xf] = iVar2 + 0xc;
  param_1[0xd] = 0;
  param_1[8] = 0x41200000;
  param_1[9] = 0x3f000000;
  param_1[10] = 0x41a00000;
  iVar2 = _ZN11Application11GetInstanceEv();
  local_28 = (int *)0x0;
  _ZNK6glitch7collada16CColladaDatabase15constructEffectEPNS_5video12IVideoDriverEPKcRKN5boost13intrusive_ptrINS0_14CRootSceneNodeEEE
            (&local_2c,param_3,
             *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8),*param_2,
             &local_28);
  _ZN6glitch5video9CMaterial8allocateERKN5boost13intrusive_ptrINS0_17CMaterialRendererEEEPKch
            (&local_30,&local_2c,0,0);
  local_24 = local_30;
  if (local_30 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar2 = param_1[0xd];
  param_1[0xd] = local_24;
  local_24 = iVar2;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev();
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_30);
  if (local_2c != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar2 = *local_2c;
      bVar1 = (bool)hasExclusiveAccess(local_2c);
    } while (!bVar1);
    *local_2c = iVar2 + -1;
    DataMemoryBarrier(0xf);
    if (iVar2 + -1 == 0) {
      _ZN6glitch5video17CMaterialRendererD2Ev(local_2c);
      free(local_2c);
    }
  }
  if (local_28 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)local_28 + *(int *)(*local_28 + -0x10));
  }
  param_1[0xe] = param_4;
  param_1[0x11] = 0;
  *(undefined1 *)(param_1 + 0xc) = 0;
  param_1[0x10] = 3;
  *(undefined1 *)(param_1 + 0x12) = 0;
  return param_1;
}


