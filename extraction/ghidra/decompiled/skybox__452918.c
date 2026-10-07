// _ZN22CCustomSkyBoxSceneNode19PlaySkyboxAnimationEPKc @ 00452918

void _ZN22CCustomSkyBoxSceneNode19PlaySkyboxAnimationEPKc(int param_1,char *param_2)

{
  int iVar1;
  int *piVar2;
  undefined4 uVar3;
  int *local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  float local_20;
  float local_1c;
  
  if (*(int **)(param_1 + 0x10c) != (int *)0x0) {
    (**(code **)(**(int **)(param_1 + 0x10c) + 0x38))();
    if (*(int *)(param_1 + 0x110) != 0) {
      _ZN20CSmartLightComponent14ResetAnimationEv();
      _ZN20CSmartLightComponent11EnableLightEib(*(undefined4 *)(param_1 + 0x110),0,1);
      _ZN6glitch5scene10ISceneNode20getSceneNodeFromNameEPKc
                (&local_40,*(undefined4 *)(param_1 + 0x108),param_2);
      if (local_40 != (int *)0x0) {
        piVar2 = *(int **)(*(int *)(param_1 + 0xe8) + 0xe4);
        if (piVar2 != (int *)0x0) {
          _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                    ((int)piVar2 + *(int *)(*piVar2 + -0x10) + 4);
        }
        uVar3 = *(undefined4 *)(param_1 + 0x110);
        _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv(&local_3c,piVar2);
        _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv(&local_30,local_40);
        local_24 = local_30 + local_3c;
        local_20 = local_2c + local_38;
        local_1c = local_28 + local_34;
        _ZN20CSmartLightComponent11SetPositionEN6glitch4core8vector3dIfEE(uVar3,&local_24);
        if (piVar2 != (int *)0x0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                    ((int)piVar2 + *(int *)(*piVar2 + -0x10));
        }
      }
      iVar1 = strcmp(param_2,(char *)(DAT_00452a5c + 0x452a20));
      if (iVar1 == 0) {
        _ZN20CSmartLightComponent11EnableLightEib(*(undefined4 *)(param_1 + 0x110),0,0);
      }
      if (local_40 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                  ((int)local_40 + *(int *)(*local_40 + -0x10));
      }
    }
  }
  return;
}

