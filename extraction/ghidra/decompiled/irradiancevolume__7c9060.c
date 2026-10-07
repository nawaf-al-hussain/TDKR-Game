// _ZN6glitch10irradiance17CIrradianceVolume14fromDataStreamERN5boost13intrusive_ptrINS_2io9IReadFileEEERKNS_4core8vector3dIfEE @ 007c9060

int * _ZN6glitch10irradiance17CIrradianceVolume14fromDataStreamERN5boost13intrusive_ptrINS_2io9IReadFileEEERKNS_4core8vector3dIfEE
                (undefined4 *param_1,float *param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  char local_66;
  char local_65;
  float local_64;
  float local_60;
  float local_5c;
  float local_58;
  float local_54;
  float local_50;
  undefined4 local_4c;
  undefined4 local_48;
  int local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_64,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_60,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_5c,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_58,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_54,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_50,4);
  fVar5 = *param_2 + local_64;
  fVar6 = param_2[1] + local_60;
  fVar7 = param_2[2] + local_5c;
  fVar8 = *param_2 + local_58;
  fVar9 = param_2[1] + local_54;
  fVar4 = param_2[2] + local_50;
  local_64 = fVar5;
  local_60 = fVar6;
  local_5c = fVar7;
  local_58 = fVar8;
  local_54 = fVar9;
  local_50 = fVar4;
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_4c,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_48,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_44,4);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_66,1);
  (**(code **)(*(int *)*param_1 + 0xc))((int *)*param_1,&local_65,1);
  local_40 = fVar5;
  local_3c = fVar6;
  local_38 = fVar7;
  local_34 = fVar8;
  local_30 = fVar9;
  local_2c = fVar4;
  piVar2 = (int *)_Znwj(0x50);
  _ZN6glitch10irradiance17CIrradianceVolumeC1ENS_4core8aabbox3dIfEEffibb
            (piVar2,&local_40,local_4c,local_48,local_44,local_66,local_65);
  if ((local_66 != '\0') && (0 < local_44)) {
    iVar3 = 0;
    do {
      iVar1 = iVar3 * 4;
      iVar3 = iVar3 + 1;
      (**(code **)(*(int *)*param_1 + 0xc))
                ((int *)*param_1,*(undefined4 *)(*piVar2 + iVar1),piVar2[0x11] * 0x84);
    } while (iVar3 < local_44);
  }
  if ((local_65 != '\0') && (0 < local_44)) {
    iVar3 = 0;
    do {
      iVar1 = iVar3 * 4;
      iVar3 = iVar3 + 1;
      (**(code **)(*(int *)*param_1 + 0xc))
                ((int *)*param_1,*(undefined4 *)(piVar2[3] + iVar1),piVar2[0x11] * 0x24);
    } while (iVar3 < local_44);
  }
  return piVar2;
}


