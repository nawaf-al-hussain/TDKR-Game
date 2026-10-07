// _ZN15CWeatherManager4InitEv @ 0041d01c

void _ZN15CWeatherManager4InitEv(int param_1)

{
  char cVar1;
  undefined2 uVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int *piVar6;
  code *pcVar7;
  undefined4 uVar8;
  int *local_1c;
  
  piVar6 = (int *)(DAT_0041d234 + 0x41d03c);
  iVar3 = *piVar6;
  iVar4 = DAT_0041d238 + 0x41d050;
  *(bool *)(param_1 + 0x28) = *(int *)(param_1 + 0x44) != 0;
  uVar8 = *(undefined4 *)(*(int *)(iVar3 + 0x10) + 0x154);
  uVar2 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                    (uVar8,iVar4,0,5,1,0xff);
  iVar3 = DAT_0041d23c + 0x41d088;
  *(undefined2 *)(param_1 + 0x4c) = uVar2;
  uVar2 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                    (uVar8,iVar3,2,0xd,1,0xff);
  iVar3 = DAT_0041d240 + 0x41d0c4;
  *(undefined2 *)(param_1 + 0x48) = uVar2;
  uVar2 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                    (uVar8,iVar3,0,8,1,0xff);
  iVar3 = DAT_0041d244 + 0x41d100;
  *(undefined2 *)(param_1 + 0x4a) = uVar2;
  uVar2 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                    (uVar8,iVar3,0,5,1,0xff);
  iVar3 = DAT_0041d248;
  *(undefined4 *)(param_1 + 0x30) = 0;
  piVar5 = *(int **)(iVar3 + 0x41d134);
  *(undefined1 *)(param_1 + 0x54) = 0;
  cVar1 = *(char *)(*piVar5 + 0x3c);
  *(undefined2 *)(param_1 + 0x4e) = uVar2;
  if (cVar1 != '\0') {
    piVar5 = (int *)_Znwj(0x16c);
    _ZN14CRainSceneNodeC1Ei(piVar5,0xffffffff);
    iVar3 = *piVar6;
    *(int **)(param_1 + 0x50) = piVar5;
    piVar6 = *(int **)(iVar3 + 0x180);
    if (piVar6 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                ((int)piVar6 + *(int *)(*piVar6 + -0x10) + 4);
      piVar5 = *(int **)(param_1 + 0x50);
    }
    pcVar7 = *(code **)(*piVar6 + 0x68);
    local_1c = piVar5;
    if (piVar5 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                ((int)piVar5 + *(int *)(*piVar5 + -0x10) + 4);
    }
    (*pcVar7)(piVar6,&local_1c);
    if (local_1c != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_1c + *(int *)(*local_1c + -0x10));
    }
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar6 + *(int *)(*piVar6 + -0x10));
    (**(code **)(**(int **)(param_1 + 0x50) + 0x34))
              (*(int **)(param_1 + 0x50),DAT_0041d24c + 0x41d218);
    (**(code **)(**(int **)(param_1 + 0x50) + 0x4c))(*(int **)(param_1 + 0x50),1);
  }
  return;
}


