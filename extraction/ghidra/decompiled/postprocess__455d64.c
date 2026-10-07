// _ZN19CPostProcessManager11LoadEffectsEv @ 00455d64

void _ZN19CPostProcessManager11LoadEffectsEv(int param_1)

{
  uint uVar1;
  undefined2 uVar2;
  int iVar3;
  int *piVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  int iVar16;
  int iVar17;
  int iVar18;
  int iVar19;
  int iVar20;
  int iVar21;
  int iVar22;
  int iVar23;
  undefined1 auStack_1bc [4];
  undefined1 auStack_1b8 [4];
  undefined1 auStack_1b4 [4];
  undefined1 auStack_1b0 [4];
  undefined1 auStack_1ac [4];
  undefined1 auStack_1a8 [4];
  undefined1 auStack_1a4 [4];
  undefined1 auStack_1a0 [4];
  undefined1 auStack_19c [4];
  undefined1 auStack_198 [4];
  undefined1 auStack_194 [4];
  undefined1 auStack_190 [4];
  undefined1 auStack_18c [4];
  undefined1 auStack_188 [4];
  undefined1 auStack_184 [4];
  undefined1 auStack_180 [4];
  undefined1 auStack_17c [4];
  undefined1 auStack_178 [4];
  undefined1 auStack_174 [4];
  undefined1 auStack_170 [4];
  undefined1 auStack_16c [4];
  undefined1 auStack_168 [4];
  undefined1 auStack_164 [4];
  undefined1 auStack_160 [4];
  undefined1 auStack_15c [4];
  undefined1 auStack_158 [4];
  undefined1 auStack_154 [4];
  undefined1 auStack_150 [4];
  undefined1 auStack_14c [4];
  undefined1 auStack_148 [4];
  undefined1 auStack_144 [4];
  undefined1 auStack_140 [4];
  undefined1 auStack_13c [4];
  undefined1 auStack_138 [4];
  undefined1 auStack_134 [4];
  undefined1 auStack_130 [4];
  undefined4 local_12c;
  undefined1 auStack_128 [4];
  undefined1 auStack_124 [4];
  undefined1 auStack_120 [4];
  undefined1 auStack_11c [4];
  undefined1 auStack_118 [4];
  int local_114;
  undefined1 auStack_110 [4];
  undefined1 auStack_10c [4];
  undefined1 auStack_108 [4];
  undefined1 auStack_104 [4];
  undefined4 local_100;
  undefined1 auStack_fc [8];
  undefined1 auStack_f4 [4];
  undefined4 local_f0;
  undefined1 auStack_ec [8];
  undefined1 auStack_e4 [4];
  undefined4 local_e0;
  undefined1 auStack_dc [8];
  undefined1 auStack_d4 [4];
  undefined4 local_d0;
  undefined1 auStack_cc [8];
  undefined1 auStack_c4 [4];
  undefined4 local_c0;
  undefined1 auStack_bc [8];
  undefined1 auStack_b4 [4];
  undefined4 local_b0;
  undefined1 auStack_ac [8];
  undefined1 auStack_a4 [4];
  undefined4 local_a0;
  undefined1 auStack_9c [8];
  undefined1 auStack_94 [4];
  undefined4 local_90;
  undefined1 auStack_8c [8];
  undefined1 auStack_84 [4];
  undefined4 local_80;
  undefined1 auStack_7c [8];
  undefined1 auStack_74 [4];
  undefined4 local_70;
  undefined1 auStack_6c [8];
  undefined1 auStack_64 [4];
  undefined4 local_60;
  undefined1 auStack_5c [8];
  undefined1 auStack_54 [4];
  undefined4 local_50;
  undefined1 auStack_4c [4];
  undefined4 local_48;
  undefined1 auStack_44 [8];
  int local_3c [6];
  
  _ZN6glitch7collada16CColladaDatabaseC1EPKcPNS0_15CColladaFactoryE
            (local_3c,DAT_00456bbc + 0x455d80,0);
  if (local_3c[0] != 0) {
    iVar3 = *(int *)(param_1 + 8);
    local_12c = 0;
    uVar1 = *(int *)(param_1 + 0xc) - iVar3 >> 2;
    if (uVar1 < 0xc) {
      _ZNSt6vectorIP18CPostProcessEffectSaIS1_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS1_S3_EEjRKS1_
                (param_1 + 8,*(int *)(param_1 + 0xc),0xc - uVar1,&local_12c);
      iVar3 = *(int *)(param_1 + 8);
    }
    else if (uVar1 != 0xc) {
      *(int *)(param_1 + 0xc) = iVar3 + 0x30;
    }
    iVar7 = 0;
    while( true ) {
      *(undefined4 *)(iVar3 + iVar7) = 0;
      iVar3 = DAT_00456bcc;
      iVar7 = iVar7 + 4;
      if (iVar7 == 0x30) break;
      iVar3 = *(int *)(param_1 + 8);
    }
    iVar9 = param_1 + 0x20;
    iVar7 = DAT_00456bc0 + 0x455df8;
    iVar8 = DAT_00456bc4 + 0x455e00;
    iVar10 = DAT_00456bc8 + 0x455e0c;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1bc,iVar7);
    piVar4 = (int *)_Z11CustomAllocjPKci(0x4c,iVar8,0x8e);
    iVar3 = iVar3 + 0x455e28;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_128,auStack_1bc);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_128,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_128);
    puVar6 = *(undefined4 **)(param_1 + 8);
    *piVar4 = DAT_00456bd0 + 0x455e68;
    *puVar6 = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1bc);
    iVar11 = **(int **)(param_1 + 8);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1b8,iVar7);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar11 + 0x3c,auStack_1b8);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1b8);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1b4,iVar7);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_1b4);
    local_50 = 0;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1b4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_104,auStack_54);
    local_100 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_fc,iVar9,auStack_104);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_104);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1b0,iVar10);
    piVar4 = (int *)_Z11CustomAllocjPKci(0x58,iVar8,0x8f);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_124,auStack_1b0);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_124,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_124);
    iVar7 = DAT_00456bd8;
    uVar5 = *(undefined4 *)(piVar4[0xd] + 4);
    *piVar4 = DAT_00456bd4 + 0x455f58;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar5,iVar7 + 0x455f60,0);
    iVar7 = DAT_00456c00;
    iVar11 = DAT_00456be0 + 0x455f80;
    iVar12 = DAT_00456be8 + 0x455f8c;
    iVar13 = DAT_00456bdc + 0x455f94;
    iVar14 = DAT_00456be4 + 0x455fa8;
    iVar15 = DAT_00456bec + 0x455fb4;
    iVar16 = DAT_00456bf0 + 0x455fc0;
    iVar17 = DAT_00456bf4 + 0x455fcc;
    iVar18 = DAT_00456bf8 + 0x455fd8;
    iVar19 = DAT_00456bfc + 0x455fe4;
    *(undefined2 *)((int)piVar4 + 0x4a) = uVar2;
    iVar7 = iVar7 + 0x455ff4;
    iVar20 = DAT_00456c04 + 0x456004;
    iVar21 = DAT_00456c08 + 0x456014;
    iVar22 = DAT_00456c0c + 0x456020;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar11,0);
    iVar11 = DAT_00456c10 + 0x45603c;
    iVar23 = DAT_00456c14 + 0x456040;
    *(undefined2 *)(piVar4 + 0x13) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar11,0);
    iVar11 = DAT_00456c18 + 0x456060;
    *(undefined2 *)((int)piVar4 + 0x4e) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar11,0);
    iVar11 = *(int *)(param_1 + 8);
    piVar4[0x15] = -0x40800000;
    *(undefined2 *)(piVar4 + 0x14) = uVar2;
    *(int **)(iVar11 + 4) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1b0);
    iVar11 = *(int *)(*(int *)(param_1 + 8) + 4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1ac,iVar10);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar11 + 0x3c,auStack_1ac);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1ac);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1a8,iVar10);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_1a8);
    local_50 = 1;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1a8);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_f4,auStack_54);
    local_f0 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_ec,iVar9,auStack_f4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_f4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1a4,iVar3);
    piVar4 = (int *)_Z11CustomAllocjPKci(0x5c,iVar8,0x90);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_120,auStack_1a4);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_120,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_120);
    iVar11 = DAT_00456c20;
    uVar5 = *(undefined4 *)(piVar4[0xd] + 4);
    *piVar4 = DAT_00456c1c + 0x456174;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar5,iVar11 + 0x45617c,0);
    iVar11 = DAT_00456c24 + 0x456198;
    piVar4[0x13] = 0x3cf5c28f;
    *(undefined2 *)(piVar4 + 0x16) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar11,0);
    iVar11 = *(int *)(param_1 + 8);
    piVar4[0x14] = 0x3d4ccccd;
    piVar4[0x15] = 0x3f666666;
    *(undefined2 *)((int)piVar4 + 0x5a) = uVar2;
    *(int **)(iVar11 + 8) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1a4);
    iVar11 = *(int *)(*(int *)(param_1 + 8) + 8);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_1a0,iVar3);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar11 + 0x3c,auStack_1a0);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_1a0);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_19c,iVar3);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_19c);
    local_50 = 2;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_19c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_e4,auStack_54);
    local_e0 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_dc,iVar9,auStack_e4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_e4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_198,iVar12);
    piVar4 = (int *)_Z11CustomAllocjPKci(100,iVar8,0x97);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_11c,auStack_198);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_11c,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_11c);
    uVar5 = *(undefined4 *)(piVar4[0xd] + 4);
    *piVar4 = DAT_00456c28 + 0x4562c0;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar5,iVar13,0);
    piVar4[0x13] = 0x40c00000;
    *(undefined2 *)(piVar4 + 0x17) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar14,0);
    piVar4[0x15] = 0x3f800000;
    piVar4[0x16] = 0x40800000;
    *(undefined2 *)(piVar4 + 0x18) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar15,0);
    iVar3 = *(int *)(param_1 + 8);
    piVar4[0x14] = 0x40800000;
    *(undefined2 *)((int)piVar4 + 0x5e) = uVar2;
    *(int **)(iVar3 + 0xc) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_198);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0xc);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_194,iVar12);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_194);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_194);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_190,iVar12);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_190);
    local_50 = 3;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_190);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_d4,auStack_54);
    local_d0 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_cc,iVar9,auStack_d4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_d4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_18c,iVar16);
    piVar4 = (int *)_Z11CustomAllocjPKci(0x5c,iVar8,0x98);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_118,auStack_18c);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_118,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_118);
    iVar3 = DAT_00456c2c;
    piVar4[0x13] = 0;
    piVar4[0x14] = 0;
    uVar5 = *(undefined4 *)(piVar4[0xd] + 4);
    *piVar4 = iVar3 + 0x456428;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar5,iVar17,0);
    iVar3 = *(int *)(param_1 + 8);
    piVar4[0x15] = 0x3f800000;
    *(undefined2 *)(piVar4 + 0x16) = uVar2;
    *(int **)(iVar3 + 0x10) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_18c);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x10);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_188,iVar16);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_188);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_188);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_184,iVar16);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_184);
    local_50 = 4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_184);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_c4,auStack_54);
    local_c0 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_bc,iVar9,auStack_c4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_c4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_180,iVar18);
    piVar4 = (int *)_Z11CustomAllocjPKci(100,iVar8,0x9a);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_110,auStack_180);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_110,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_110);
    iVar11 = DAT_00456c34;
    iVar3 = DAT_00456c30;
    piVar4[0x17] = 0;
    piVar4[0x14] = 0;
    *piVar4 = iVar3 + 0x45653c;
    piVar4[0x15] = 0;
    piVar4[0x16] = 0;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar11 + 0x456548,0);
    piVar4[0x13] = 0x3f800000;
    iVar3 = DAT_00456c38 + 0x456570;
    *(undefined2 *)(piVar4 + 0x18) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar3,0);
    local_114 = piVar4[0x17];
    piVar4[0x17] = 0;
    piVar4[0x14] = 0;
    piVar4[0x15] = 0;
    piVar4[0x16] = 0;
    *(undefined2 *)((int)piVar4 + 0x62) = uVar2;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_114);
    *(int **)(*(int *)(param_1 + 8) + 0x14) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_180);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x14);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_17c,iVar18);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_17c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_17c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_178,iVar18);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_178);
    local_50 = 5;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_178);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_b4,auStack_54);
    local_b0 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_ac,iVar9,auStack_b4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_b4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_174,iVar19);
    uVar5 = _Z11CustomAllocjPKci(0x54,iVar8,0x9b);
    _ZN23CPostProcessEffect_HurtC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
              (uVar5,auStack_174,local_3c,param_1);
    *(undefined4 *)(*(int *)(param_1 + 8) + 0x18) = uVar5;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_174);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x18);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_170,iVar19);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_170);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_170);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_16c,iVar19);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_16c);
    local_50 = 6;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_16c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_a4,auStack_54);
    local_a0 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_9c,iVar9,auStack_a4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_a4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_168,iVar7);
    uVar5 = _Z11CustomAllocjPKci(0x80,iVar8,0x9e);
    _ZN27CPostProcessEffect_HeatHazeC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
              (uVar5,auStack_168,local_3c,param_1);
    *(undefined4 *)(*(int *)(param_1 + 8) + 0x1c) = uVar5;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_168);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x1c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_164,iVar7);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_164);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_164);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_160,iVar7);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_160);
    local_50 = 7;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_160);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_94,auStack_54);
    local_90 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_8c,iVar9,auStack_94);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_94);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_15c,iVar20);
    uVar5 = _Z11CustomAllocjPKci(0x5c,iVar8,0x9f);
    _ZN34CPostProcessEffect_ColorCorrectionC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
              (uVar5,auStack_15c,local_3c,param_1);
    *(undefined4 *)(*(int *)(param_1 + 8) + 0x20) = uVar5;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_15c);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x20);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_158,iVar20);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_158);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_158);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_154,iVar20);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_154);
    local_50 = 8;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_154);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_84,auStack_54);
    local_80 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_7c,iVar9,auStack_84);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_84);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_150,iVar21);
    piVar4 = (int *)_Z11CustomAllocjPKci(0x4c,iVar8,0xa1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_10c,auStack_150);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_10c,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_10c);
    uVar5 = *(undefined4 *)(piVar4[0xd] + 4);
    *piVar4 = DAT_00456c3c + 0x4568e8;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar5,iVar17,0);
    iVar3 = *(int *)(param_1 + 8);
    *(undefined2 *)((int)piVar4 + 0x4a) = uVar2;
    *(int **)(iVar3 + 0x24) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_150);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x24);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_14c,iVar21);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_14c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_14c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_148,iVar21);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_148);
    local_50 = 9;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_148);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_74,auStack_54);
    local_70 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_6c,iVar9,auStack_74);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_74);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_144,iVar22);
    uVar5 = _Z11CustomAllocjPKci(0x58,iVar8,0xa2);
    _ZN30CPostProcessEffect_CC_HeatHazeC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
              (uVar5,auStack_144,local_3c,param_1);
    *(undefined4 *)(*(int *)(param_1 + 8) + 0x28) = uVar5;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_144);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x28);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_140,iVar22);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_140);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_140);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_13c,iVar22);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_13c);
    local_50 = 10;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_13c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_64,auStack_54);
    local_60 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_5c,iVar9,auStack_64);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_64);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_138,iVar23);
    piVar4 = (int *)_Z11CustomAllocjPKci(0x50,iVar8,0xa3);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_108,auStack_138);
    _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
              (piVar4,auStack_108,local_3c,param_1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_108);
    uVar5 = *(undefined4 *)(piVar4[0xd] + 4);
    *piVar4 = DAT_00456c40 + 0x456ab0;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar5,iVar13,0);
    *(undefined2 *)((int)piVar4 + 0x4a) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar15,0);
    *(undefined2 *)(piVar4 + 0x13) = uVar2;
    uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(piVar4[0xd] + 4),iVar14,0);
    iVar3 = *(int *)(param_1 + 8);
    *(undefined2 *)((int)piVar4 + 0x4e) = uVar2;
    *(int **)(iVar3 + 0x2c) = piVar4;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_138);
    iVar3 = *(int *)(*(int *)(param_1 + 8) + 0x2c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_134,iVar23);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (iVar3 + 0x3c,auStack_134);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_134);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_130,iVar23);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_54,auStack_130);
    local_50 = 0xb;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_130);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_4c,auStack_54);
    local_48 = local_50;
    _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB_
              (auStack_44,iVar9,auStack_4c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_4c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_54);
  }
  (*(code *)**(undefined4 **)**(undefined4 **)(param_1 + 8))
            ((undefined4 *)**(undefined4 **)(param_1 + 8),0);
  _ZN6glitch7collada16CColladaDatabaseD1Ev(local_3c);
  return;
}


