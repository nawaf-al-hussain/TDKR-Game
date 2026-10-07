// _ZN19CPostProcessManager21CreateRenderToTextureEv @ 00456f28

/* WARNING: Type propagation algorithm not settling */

void _ZN19CPostProcessManager21CreateRenderToTextureEv(int param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int *piVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  undefined4 uVar15;
  int iVar16;
  undefined4 uVar17;
  undefined4 local_ec;
  undefined4 local_e8;
  undefined4 local_e4;
  undefined4 local_e0;
  int local_dc [8];
  undefined1 auStack_bc [4];
  undefined4 local_b8;
  int local_b4;
  int local_b0 [28];
  undefined4 local_40;
  undefined1 local_3c;
  undefined1 local_3b;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  
  local_e8 = 0;
  uVar1 = *(int *)(param_1 + 0x18) - *(int *)(param_1 + 0x14) >> 2;
  iVar14 = DAT_004572ec + 0x456f58;
  if (uVar1 < 7) {
    _ZNSt6vectorIP10CRTTObjectSaIS1_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS1_S3_EEjRKS1_
              (param_1 + 0x14,*(int *)(param_1 + 0x18),7 - uVar1,&local_e8);
  }
  else if (uVar1 != 7) {
    *(int *)(param_1 + 0x18) = *(int *)(param_1 + 0x14) + 0x1c;
  }
  iVar12 = 0;
  iVar13 = *(int *)(*(int *)(iVar14 + DAT_004572f0) + 4);
  uVar6 = *(undefined4 *)(*(int *)(iVar14 + DAT_004572f0) + 8);
  iVar5 = *(int *)(iVar14 + DAT_004572f4) + 8;
  if (*(char *)(param_1 + 0x66) == '\0') {
    iVar4 = 1;
  }
  else {
    iVar4 = 2;
  }
  iVar7 = DAT_004572f8 + 0x456fc0;
  iVar16 = *(int *)(iVar14 + DAT_004572fc);
  iVar8 = *(int *)(iVar14 + DAT_00457300);
  iVar9 = *(int *)(iVar14 + DAT_00457304);
  iVar10 = *(int *)(iVar14 + DAT_00457308);
  piVar11 = *(int **)(iVar14 + DAT_0045730c);
  do {
    _ZNSt8ios_baseC1Ev(local_b0);
    local_3c = 0;
    iVar14 = *(int *)(iVar13 + -0xc);
    local_40 = 0;
    local_dc[0] = iVar13;
    local_b0[0] = iVar5;
    *(undefined4 *)((int)local_dc + iVar14) = uVar6;
    local_3b = 0;
    local_38 = 0;
    local_34 = 0;
    local_30 = 0;
    local_2c = 0;
    _ZNSt9basic_iosIcSt11char_traitsIcEE4initEPSt15basic_streambufIcS1_E((int)local_dc + iVar14,0);
    local_dc[0] = iVar16 + 0xc;
    local_b0[0] = iVar16 + 0x20;
    local_dc[1] = iVar8 + 8;
    local_dc[2] = 0;
    local_dc[3] = 0;
    local_dc[4] = 0;
    local_dc[5] = 0;
    local_dc[6] = 0;
    local_dc[7] = 0;
    _ZNSt6localeC1Ev(auStack_bc);
    local_b8 = 0x10;
    local_dc[1] = iVar9 + 8;
    local_b4 = iVar10 + 0xc;
    _ZNSt9basic_iosIcSt11char_traitsIcEE4initEPSt15basic_streambufIcS1_E(local_b0,local_dc + 1);
    _ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_i
              (local_dc,iVar7,0x10);
    _ZNSolsEi(local_dc,iVar12);
    _ZNKSt15basic_stringbufIcSt11char_traitsIcESaIcEE3strEv(&local_ec,local_dc + 1);
    uVar2 = local_ec;
    uVar17 = *(undefined4 *)(param_1 + 0x4c);
    uVar15 = 0;
    if ((*(uint *)(*piVar11 + 0x80) & 8) != 0) {
      uVar15 = *(undefined4 *)(param_1 + 0x50);
    }
    uVar3 = _Znwj(0x24);
    _ZN10CRTTObjectC2ERN6glitch4core11dimension2dIiEEPKcNS0_5video21E_TEXTURE_FILTER_TYPEEPNS7_13IRenderBufferEPNS7_8ITextureENS7_22E_ANTIALIASING_SETTINGE_constprop_2449
              (uVar3,param_1 + 0x44,uVar2,0,uVar17,uVar15);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + iVar12 * 4) = uVar3;
    iVar12 = iVar12 + 1;
    _ZNSsD1Ev(&local_ec);
    local_b0[0] = iVar16 + 0x20;
    local_dc[0] = iVar16 + 0xc;
    local_dc[1] = iVar9 + 8;
    _ZNSsD1Ev(&local_b4);
    local_dc[1] = iVar8 + 8;
    _ZNSt6localeD1Ev(auStack_bc);
    local_dc[0] = iVar13;
    *(undefined4 *)((int)local_dc + *(int *)(iVar13 + -0xc)) = uVar6;
    local_b0[0] = iVar5;
    _ZNSt8ios_baseD1Ev(local_b0);
  } while (iVar12 < iVar4);
  local_e4 = 0x100;
  local_e0 = 0x100;
  if (*(char *)(*piVar11 + 0x84) != '\0') {
    uVar6 = _Znwj(0x24);
    _ZN10CRTTObjectC2ERN6glitch4core11dimension2dIiEEPKcNS0_5video21E_TEXTURE_FILTER_TYPEEPNS7_13IRenderBufferEPNS7_8ITextureENS7_22E_ANTIALIASING_SETTINGE_constprop_2449
              (uVar6,&local_e4,DAT_00457310 + 0x4571dc,1,0,0);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 8) = uVar6;
  }
  local_e4 = 0x200;
  local_e0 = 0x10;
  uVar6 = _Znwj(0x24);
  _ZN10CRTTObjectC2ERN6glitch4core11dimension2dIiEEPKcNS0_5video21E_TEXTURE_FILTER_TYPEEPNS7_13IRenderBufferEPNS7_8ITextureENS7_22E_ANTIALIASING_SETTINGE_constprop_2449
            (uVar6,&local_e4,DAT_00457314 + 0x457224,1,0,0);
  local_e4 = 0x100;
  local_e0 = 0x100;
  *(undefined4 *)(*(int *)(param_1 + 0x14) + 0xc) = uVar6;
  uVar6 = _Znwj(0x24);
  _ZN10CRTTObjectC2ERN6glitch4core11dimension2dIiEEPKcNS0_5video21E_TEXTURE_FILTER_TYPEEPNS7_13IRenderBufferEPNS7_8ITextureENS7_22E_ANTIALIASING_SETTINGE_constprop_2449
            (uVar6,&local_e4,DAT_00457318 + 0x457260,1,0,0);
  *(undefined4 *)(*(int *)(param_1 + 0x14) + 0x14) = uVar6;
  uVar6 = _Znwj(0x24);
  _ZN10CRTTObjectC2ERN6glitch4core11dimension2dIiEEPKcNS0_5video21E_TEXTURE_FILTER_TYPEEPNS7_13IRenderBufferEPNS7_8ITextureENS7_22E_ANTIALIASING_SETTINGE_constprop_2449
            (uVar6,&local_e4,DAT_0045731c + 0x457290,1,0,0);
  *(undefined4 *)(*(int *)(param_1 + 0x14) + 0x18) = uVar6;
  uVar6 = _Znwj(0x24);
  _ZN10CRTTObjectC2ERN6glitch4core11dimension2dIiEEPKcNS0_5video21E_TEXTURE_FILTER_TYPEEPNS7_13IRenderBufferEPNS7_8ITextureENS7_22E_ANTIALIASING_SETTINGE_constprop_2449
            (uVar6,&local_e4,DAT_00457320 + 0x4572c0,1,0,0);
  *(undefined4 *)(*(int *)(param_1 + 0x14) + 0x10) = uVar6;
  return;
}


