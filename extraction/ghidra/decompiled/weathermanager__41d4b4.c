// _ZN15CWeatherManager18UpdateIlluminationEf @ 0041d4b4

void _ZN15CWeatherManager18UpdateIlluminationEf(int *param_1,float param_2)

{
  bool bVar1;
  int iVar2;
  int *piVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  char *pcVar7;
  int *piVar8;
  int *piVar9;
  int iVar10;
  uint uVar11;
  undefined4 *puVar12;
  code *pcVar13;
  int *piVar14;
  uint uVar15;
  int *piVar16;
  char *__needle;
  int *piVar17;
  int iVar18;
  float extraout_s12;
  float extraout_s12_00;
  float extraout_s12_01;
  float extraout_s12_02;
  float extraout_s12_03;
  float extraout_s13;
  float extraout_s13_00;
  float extraout_s13_01;
  float extraout_s13_02;
  float fVar19;
  float extraout_s13_03;
  float fVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  undefined1 auStack_144 [4];
  int *local_140;
  float local_13c;
  int local_138;
  undefined1 auStack_134 [4];
  int *local_130;
  char *local_12c;
  undefined4 local_128;
  char *local_124;
  undefined1 auStack_120 [4];
  int *local_11c;
  int local_118;
  float local_114;
  undefined4 local_110;
  undefined4 local_10c;
  undefined4 local_108;
  undefined4 local_104;
  undefined4 local_100;
  undefined4 local_fc;
  undefined4 local_f8;
  undefined4 local_f4;
  undefined4 local_f0;
  undefined4 local_ec;
  undefined4 local_e8;
  float local_e4;
  undefined1 auStack_e0 [12];
  undefined1 auStack_d4 [12];
  undefined4 local_c8;
  undefined4 local_c4;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined4 local_b8;
  undefined4 local_b4;
  undefined4 local_b0;
  undefined4 local_ac;
  undefined4 local_a8;
  undefined4 local_a4;
  undefined4 local_a0;
  undefined4 local_9c;
  undefined4 local_98;
  undefined4 local_94;
  undefined4 local_90;
  undefined4 local_8c;
  undefined4 local_88;
  undefined4 local_84;
  undefined1 auStack_80 [12];
  int *local_74;
  int *local_70;
  int *local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  float local_5c;
  undefined1 auStack_58 [44];
  
  iVar2 = _ZN6CLevel8GetLevelEv();
  iVar18 = DAT_0041e4a4 + 0x41d4e0;
  piVar3 = *(int **)(iVar2 + 0xec);
  if (param_1[0x16] == 0) {
    iVar2 = *param_1;
    if (iVar2 == 0) {
      param_1[0x16] = 0;
    }
    else {
      iVar5 = *(int *)(iVar2 + 0xc4);
      param_1[0x16] = iVar2 + 0xb8;
      param_1[0x17] = iVar5;
      param_1[0x18] = *(int *)(iVar2 + 200);
      param_1[0x19] = *(int *)(iVar2 + 0xcc);
      param_1[0x1a] = *(int *)(iVar2 + 0xd0);
      param_1[0x1b] = *(int *)(iVar2 + 0xd4);
      param_1[0x1c] = *(int *)(iVar2 + 0xd8);
      param_1[0x1d] = *(int *)(iVar2 + 0x110);
    }
  }
  _ZN6CLevel8GetLevelEv();
  fVar23 = extraout_s12;
  fVar19 = extraout_s13;
  if (*(char *)(**(int **)(iVar18 + DAT_0041e4a8) + 0xa0) != '\0') {
    if (param_1[0xd] == 0) {
      if (piVar3 != (int *)0x0) {
        uVar4 = _ZN6CLevel8GetLevelEv();
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                  (auStack_144,DAT_0041e4e4 + 0x41e310);
        local_110 = 0;
        local_10c = 0;
        local_108 = 0;
        local_104 = 0;
        local_100 = 0;
        local_fc = 0;
        local_140 = (int *)_ZNK11CGameObject12GetSceneNodeEv(piVar3);
        if (local_140 != (int *)0x0) {
          _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                    ((int)local_140 + *(int *)(*local_140 + -0x10) + 4);
        }
        local_f8 = 0x3f800000;
        local_f4 = 0x3f800000;
        local_f0 = 0x3f800000;
        iVar2 = _ZN6CLevel11StartEffectERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEENS3_8vector3dIfEESC_N5boost13intrusive_ptrINS2_5scene10ISceneNodeEEESC_bP11CGameObject
                          (uVar4,auStack_144,&local_110,&local_104,&local_140,&local_f8,0,piVar3);
        param_1[0xd] = iVar2;
        if (local_140 != (int *)0x0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                    ((int)local_140 + *(int *)(*local_140 + -0x10));
        }
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_144);
        local_74 = (int *)0x0;
        local_70 = (int *)0x0;
        local_6c = (int *)0x0;
        uVar4 = _ZNK11CGameObject12GetSceneNodeEv(param_1[0xd]);
        _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
                  (uVar4,0x5f796e61,&local_74);
        piVar9 = local_70;
        if (local_74 != local_70) {
          iVar2 = DAT_0041e4e8 + 0x41e414;
          piVar14 = local_74;
          do {
            piVar17 = piVar14 + 1;
            piVar14 = (int *)*piVar14;
            if (piVar14 != (int *)0x0) {
              _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                        ((int)piVar14 + *(int *)(*piVar14 + -0x10) + 4);
            }
            piVar16 = (int *)piVar14[0x3e];
            if (piVar16 == (int *)0x0) {
              piVar16 = (int *)_Znwj(0xc);
              *piVar16 = iVar2;
              piVar16[1] = 0;
              _ZN14CustomNodeData4grabEv();
              piVar8 = (int *)piVar14[0x3e];
              piVar14[0x3e] = (int)piVar16;
              if (piVar8 != (int *)0x0) {
                (**(code **)(*piVar8 + 0xc))(piVar8);
                piVar16 = (int *)piVar14[0x3e];
              }
            }
            iVar5 = *piVar14;
            piVar16[1] = piVar16[1] | 0x10;
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                      ((int)piVar14 + *(int *)(iVar5 + -0x10));
            piVar14 = piVar17;
          } while (piVar9 != piVar17);
        }
        _ZNSt6vectorIN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEENS2_4core10SAllocatorIS5_LNS2_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (&local_74);
        fVar23 = extraout_s12_03;
        fVar19 = extraout_s13_03;
      }
    }
    else {
      iVar2 = (**(code **)(*piVar3 + 0x18))(piVar3);
      local_e4 = -*(float *)(iVar2 + 8);
      local_ec = 0;
      local_e8 = 0;
      (**(code **)(*(int *)param_1[0xd] + 0x28))((int *)param_1[0xd],&local_ec,1);
      fVar23 = extraout_s12_00;
      fVar19 = extraout_s13_00;
    }
  }
  if ((char)param_1[1] != '\0') {
    if ((float)param_1[0x27] < (float)param_1[0x28]) {
      if ((float)param_1[0x28] <= 0.0) goto LAB_0041d588;
      _ZN12InterpolatorIN6glitch5video6SColorEfE6updateERS2_f_part_263
                (param_1 + 0x25,param_1 + 0x19);
      fVar20 = (float)param_1[0x22];
      fVar22 = (float)param_1[0x23];
      fVar23 = extraout_s12_01;
      fVar19 = extraout_s13_01;
      if (fVar22 <= fVar20) goto LAB_0041d59c;
LAB_0041e18c:
      if (fVar22 <= 0.0) goto LAB_0041d5ac;
      fVar20 = param_2 + fVar20;
      *(undefined1 *)(param_1 + 0x24) = 0;
      if (fVar22 < fVar20) {
        fVar19 = 1.0;
        fVar23 = DAT_0041e4fc;
        fVar21 = DAT_0041e4fc;
      }
      else {
        fVar19 = fVar20 / fVar22;
        fVar23 = (1.0 - fVar19) * (float)param_1[0x1e];
        fVar21 = (1.0 - fVar19) * (float)param_1[0x1f];
        fVar22 = fVar20;
      }
      param_1[0x22] = (int)fVar22;
      fVar22 = (float)param_1[0x34];
      fVar23 = fVar23 + fVar19 * (float)param_1[0x20];
      param_1[0x18] = (int)(fVar21 + fVar19 * (float)param_1[0x21]);
      param_1[0x17] = (int)fVar23;
      if ((float)param_1[0x33] < fVar22) goto LAB_0041e200;
LAB_0041d5c0:
      param_1[0x1c] = param_1[0x32];
LAB_0041d5c8:
      fVar20 = (float)param_1[0x2e];
      fVar22 = (float)param_1[0x2f];
      if (fVar20 < fVar22) goto LAB_0041e230;
LAB_0041d5dc:
      param_1[0x1a] = param_1[0x2c];
      param_1[0x1b] = param_1[0x2d];
LAB_0041d5ec:
      fVar20 = (float)param_1[0x38];
      fVar22 = (float)param_1[0x39];
      if (fVar20 < fVar22) {
LAB_0041e2a4:
        if (0.0 < fVar22) {
          fVar20 = param_2 + fVar20;
          *(undefined1 *)(param_1 + 0x3a) = 0;
          bVar1 = fVar22 < fVar20;
          fVar21 = DAT_0041e4fc;
          if (!bVar1) {
            fVar19 = fVar20 / fVar22;
            fVar23 = (float)param_1[0x36];
            fVar21 = 1.0;
            fVar22 = fVar20;
          }
          param_1[0x38] = (int)fVar22;
          if (!bVar1) {
            fVar21 = (fVar21 - fVar19) * fVar23;
          }
          if (bVar1) {
            fVar19 = 1.0;
          }
          param_1[0x1d] = (int)(fVar21 + fVar19 * (float)param_1[0x37]);
        }
        goto LAB_0041d608;
      }
    }
    else {
      param_1[0x19] = param_1[0x26];
LAB_0041d588:
      fVar20 = (float)param_1[0x22];
      fVar22 = (float)param_1[0x23];
      if (fVar20 < fVar22) goto LAB_0041e18c;
LAB_0041d59c:
      param_1[0x17] = param_1[0x20];
      param_1[0x18] = param_1[0x21];
LAB_0041d5ac:
      fVar22 = (float)param_1[0x34];
      if (fVar22 <= (float)param_1[0x33]) goto LAB_0041d5c0;
LAB_0041e200:
      if (fVar22 <= 0.0) goto LAB_0041d5c8;
      _ZN12InterpolatorIN6glitch5video6SColorEfE6updateERS2_f_part_263
                (param_1 + 0x31,param_1 + 0x1c);
      fVar20 = (float)param_1[0x2e];
      fVar22 = (float)param_1[0x2f];
      fVar23 = extraout_s12_02;
      fVar19 = extraout_s13_02;
      if (fVar22 <= fVar20) goto LAB_0041d5dc;
LAB_0041e230:
      if (fVar22 <= 0.0) goto LAB_0041d5ec;
      fVar20 = param_2 + fVar20;
      *(undefined1 *)(param_1 + 0x30) = 0;
      if (fVar22 < fVar20) {
        fVar19 = 1.0;
        fVar23 = DAT_0041e4fc;
        fVar21 = DAT_0041e4fc;
      }
      else {
        fVar19 = fVar20 / fVar22;
        fVar23 = (1.0 - fVar19) * (float)param_1[0x2a];
        fVar21 = (1.0 - fVar19) * (float)param_1[0x2b];
        fVar22 = fVar20;
      }
      param_1[0x2e] = (int)fVar22;
      fVar22 = (float)param_1[0x39];
      fVar23 = fVar23 + fVar19 * (float)param_1[0x2c];
      param_1[0x1b] = (int)(fVar21 + fVar19 * (float)param_1[0x2d]);
      fVar20 = (float)param_1[0x38];
      param_1[0x1a] = (int)fVar23;
      if (fVar20 < fVar22) goto LAB_0041e2a4;
    }
    param_1[0x1d] = param_1[0x37];
  }
LAB_0041d608:
  _ZN15CWeatherManager25ApplyIlluminationSettingsEv(param_1);
  piVar9 = (int *)param_1[0x11];
  if (piVar9 != (int *)0x0) {
    pcVar13 = *(code **)(*piVar9 + 0xb8);
    _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
              (auStack_e0,*(undefined4 *)(*(int *)(DAT_0041e4ac + 0x41d630) + 0xe4));
    (*pcVar13)(piVar9,auStack_e0);
  }
  iVar2 = param_1[0x14];
  if (iVar2 != 0) {
    _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
              (auStack_d4,*(undefined4 *)(*(int *)(DAT_0041e4b0 + 0x41d660) + 0xe4));
    _ZN14CRainSceneNode11SetPositionERKN6glitch4core8vector3dIfEE(iVar2,auStack_d4);
  }
  if (((char)param_1[0x15] == '\0') && (piVar3 != (int *)0x0)) {
    _ZN6CLevel8GetLevelEv();
    uVar4 = _ZNK6CLevel18GetPlayerComponentEv();
    _ZN15PlayerComponent6SetWetEb(uVar4,(char)param_1[10]);
    *(undefined1 *)(param_1 + 0x15) = 1;
  }
  piVar9 = (int *)(uint)*(byte *)(param_1 + 10);
  fVar23 = (float)param_1[0xc];
  if (piVar9 == (int *)0x0) {
    if (fVar23 <= 0.0) {
      piVar3 = (int *)param_1[0x11];
      if (piVar3 != (int *)0x0) {
        (**(code **)(*piVar3 + 0x4c))(piVar3,0);
      }
      piVar3 = (int *)param_1[0xd];
      if (piVar3 != (int *)0x0) {
        (**(code **)(*piVar3 + 0x80))(piVar3,0);
      }
      piVar3 = (int *)param_1[0x14];
      if (piVar3 != (int *)0x0) {
        (**(code **)(*piVar3 + 0x4c))(piVar3,0);
      }
      param_1[0xc] = 0;
    }
    else {
      param_1[0xc] = (int)(fVar23 - param_2);
      if (param_1[0x11] != 0) {
        local_74 = piVar9;
        local_70 = piVar9;
        local_6c = piVar9;
        _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
                  (param_1[0x11],0x6d796e61,&local_74);
        piVar9 = local_70;
        if (local_74 != local_70) {
          iVar2 = DAT_0041e4dc + 0x41de14;
          piVar14 = local_74;
          do {
            piVar17 = piVar14 + 1;
            iVar5 = (**(code **)(*(int *)*piVar14 + 0xa0))();
            if (iVar5 != 0) {
              iVar6 = 0;
              do {
                iVar10 = iVar6 + 1;
                (**(code **)(*(int *)*piVar14 + 0x9c))(&local_118,(int *)*piVar14,iVar6);
                iVar6 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                                  (*(undefined4 *)(local_118 + 4),iVar2,0);
                if (iVar6 != 0xffff) {
                  local_68 = 0;
                  local_64 = 0;
                  local_60 = 0;
                  local_5c = 0.0;
                  _ZNK6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12getParameterINS_4core8vector4dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRSE_
                            (local_118,iVar6,0,&local_68);
                  local_5c = (float)param_1[0xc] / (float)param_1[0xb];
                  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector4dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
                            (local_118,iVar6,0,&local_68);
                }
                _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_118);
                iVar6 = iVar10;
              } while (iVar10 != iVar5);
            }
            piVar8 = local_70;
            piVar14 = piVar17;
            piVar16 = local_74;
          } while (piVar9 != piVar17);
          while (piVar8 != piVar16) {
            piVar14 = piVar16 + 1;
            piVar9 = (int *)*piVar16;
            piVar16 = piVar14;
            if (piVar9 != (int *)0x0) {
              _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                        ((int)piVar9 + *(int *)(*piVar9 + -0x10));
            }
          }
        }
        if (local_74 != (int *)0x0) {
          free(local_74);
        }
      }
      piVar9 = (int *)param_1[0x14];
      if (piVar9 != (int *)0x0) {
        (**(code **)(*piVar9 + 0x4c))(piVar9,1);
        _ZN14CRainSceneNode8SetAlphaEf(param_1[0x14],(float)param_1[0xc] / (float)param_1[0xb]);
      }
      if (piVar3 != (int *)0x0) {
        local_74 = (int *)0x0;
        local_70 = (int *)0x0;
        local_6c = (int *)0x0;
        uVar4 = _ZNK11CGameObject12GetSceneNodeEv(piVar3);
        _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
                  (uVar4,0x6d796e61,&local_74);
        piVar3 = local_70;
        if (local_74 != local_70) {
          iVar2 = DAT_0041e4e0 + 0x41dfb0;
          piVar9 = local_74;
          do {
            piVar14 = piVar9 + 1;
            piVar9 = (int *)*piVar9;
            if (piVar9 != (int *)0x0) {
              _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                        ((int)piVar9 + *(int *)(*piVar9 + -0x10) + 4);
            }
            iVar5 = (**(code **)(*piVar9 + 0xa0))(piVar9);
            if (iVar5 != 0) {
              iVar6 = 0;
              do {
                iVar10 = iVar6 + 1;
                (**(code **)(*piVar9 + 0x9c))(&local_118,piVar9,iVar6);
                iVar6 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                                  (*(undefined4 *)(local_118 + 4),iVar2,0);
                if (iVar6 != 0xffff) {
                  local_114 = (float)param_1[0xc] / (float)param_1[0xb];
                  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
                            (local_118,iVar6,0,&local_114);
                }
                _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_118);
                iVar6 = iVar10;
              } while (iVar10 != iVar5);
            }
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                      ((int)piVar9 + *(int *)(*piVar9 + -0x10));
            piVar16 = local_70;
            piVar9 = piVar14;
            piVar17 = local_74;
          } while (piVar3 != piVar14);
          while (piVar16 != piVar17) {
            piVar9 = piVar17 + 1;
            piVar3 = (int *)*piVar17;
            piVar17 = piVar9;
            if (piVar3 != (int *)0x0) {
              _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                        ((int)piVar3 + *(int *)(*piVar3 + -0x10));
            }
          }
        }
        if (local_74 != (int *)0x0) {
          free(local_74);
        }
      }
    }
    if (0 < param_1[9]) {
      _ZN15VoxSoundManager4StopEii(**(undefined4 **)(iVar18 + DAT_0041e4f8),param_1[9],0x9c4);
      param_1[9] = -1;
    }
    iVar2 = param_1[0xe];
    if ((uint)(param_1[0xf] - iVar2) >> 2 == 0) {
      return;
    }
    uVar15 = 0;
    do {
      uVar11 = uVar15 + 1;
      iVar2 = (**(code **)(**(int **)(iVar2 + uVar15 * 4) + 0x84))();
      if (iVar2 != 0) {
        piVar3 = *(int **)(param_1[0xe] + uVar15 * 4);
        (**(code **)(*piVar3 + 0x80))(piVar3,0);
      }
      iVar2 = param_1[0xe];
      uVar15 = uVar11;
    } while (uVar11 < (uint)(param_1[0xf] - iVar2 >> 2));
    return;
  }
  if (fVar23 <= 0.0) {
    param_1[0xc] = 0;
  }
  else {
    piVar9 = (int *)param_1[0xd];
    param_1[0xc] = (int)(fVar23 - param_2);
    if (piVar9 != (int *)0x0) {
      (**(code **)(*piVar9 + 0x80))(piVar9,1);
    }
    piVar9 = (int *)param_1[0x11];
    if (piVar9 != (int *)0x0) {
      (**(code **)(*piVar9 + 0x4c))(piVar9,1);
      local_74 = (int *)0x0;
      local_70 = (int *)0x0;
      local_6c = (int *)0x0;
      _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
                (param_1[0x11],0x6d796e61,&local_74);
      piVar9 = local_70;
      if (local_74 != local_70) {
        iVar2 = DAT_0041e4b4 + 0x41d74c;
        piVar14 = local_74;
        do {
          piVar17 = piVar14 + 1;
          iVar5 = (**(code **)(*(int *)*piVar14 + 0xa0))();
          if (iVar5 != 0) {
            iVar6 = 0;
            do {
              iVar10 = iVar6 + 1;
              (**(code **)(*(int *)*piVar14 + 0x9c))(&local_118,(int *)*piVar14,iVar6);
              iVar6 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                                (*(undefined4 *)(local_118 + 4),iVar2,0);
              if (iVar6 != 0xffff) {
                local_68 = 0;
                local_64 = 0;
                local_60 = 0;
                local_5c = 0.0;
                _ZNK6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12getParameterINS_4core8vector4dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRSE_
                          (local_118,iVar6,0,&local_68);
                local_5c = 1.0 - (float)param_1[0xc] / (float)param_1[0xb];
                _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector4dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
                          (local_118,iVar6,0,&local_68);
              }
              _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_118);
              iVar6 = iVar10;
            } while (iVar10 != iVar5);
          }
          piVar8 = local_70;
          piVar14 = piVar17;
          piVar16 = local_74;
        } while (piVar9 != piVar17);
        while (piVar16 != piVar8) {
          piVar14 = piVar16 + 1;
          piVar9 = (int *)*piVar16;
          piVar16 = piVar14;
          if (piVar9 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                      ((int)piVar9 + *(int *)(*piVar9 + -0x10));
          }
        }
      }
      if (local_74 != (int *)0x0) {
        free(local_74);
      }
    }
    piVar9 = (int *)param_1[0x14];
    if (piVar9 != (int *)0x0) {
      (**(code **)(*piVar9 + 0x4c))(piVar9,1);
      _ZN14CRainSceneNode8SetAlphaEf(param_1[0x14],1.0 - (float)param_1[0xc] / (float)param_1[0xb]);
    }
    if (piVar3 != (int *)0x0) {
      local_74 = (int *)0x0;
      local_70 = (int *)0x0;
      local_6c = (int *)0x0;
      uVar4 = _ZNK11CGameObject12GetSceneNodeEv(piVar3);
      _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
                (uVar4,0x6d796e61,&local_74);
      piVar9 = local_70;
      if (local_74 != local_70) {
        iVar2 = DAT_0041e4b8 + 0x41d8f8;
        piVar14 = local_74;
        do {
          piVar17 = piVar14 + 1;
          piVar14 = (int *)*piVar14;
          if (piVar14 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                      ((int)piVar14 + *(int *)(*piVar14 + -0x10) + 4);
          }
          iVar5 = (**(code **)(*piVar14 + 0xa0))(piVar14);
          if (iVar5 != 0) {
            iVar6 = 0;
            do {
              iVar10 = iVar6 + 1;
              (**(code **)(*piVar14 + 0x9c))(&local_118,piVar14,iVar6);
              iVar6 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                                (*(undefined4 *)(local_118 + 4),iVar2,0);
              if (iVar6 != 0xffff) {
                local_13c = 1.0 - (float)param_1[0xc] / (float)param_1[0xb];
                _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
                          (local_118,iVar6,0);
              }
              _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_118);
              iVar6 = iVar10;
            } while (iVar10 != iVar5);
          }
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                    ((int)piVar14 + *(int *)(*piVar14 + -0x10));
          piVar8 = local_70;
          piVar14 = piVar17;
          piVar16 = local_74;
        } while (piVar9 != piVar17);
        while (piVar16 != piVar8) {
          piVar14 = piVar16 + 1;
          piVar9 = (int *)*piVar16;
          piVar16 = piVar14;
          if (piVar9 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                      ((int)piVar9 + *(int *)(*piVar9 + -0x10));
          }
        }
      }
      if (local_74 != (int *)0x0) {
        free(local_74);
      }
    }
  }
  iVar2 = param_1[0xe];
  piVar9 = (int *)(param_1[0xf] - iVar2 >> 2);
  if (piVar9 == (int *)0x0) {
    iVar2 = _ZN6CLevel8GetLevelEv();
    if (*(int *)(iVar2 + 0xec) != 0) {
      local_74 = piVar9;
      local_70 = piVar9;
      local_6c = piVar9;
      uVar4 = _ZNK11CGameObject12GetSceneNodeEv(piVar3);
      _ZN6glitch5scene10ISceneNode21getSceneNodesFromTypeENS0_17E_SCENE_NODE_TYPEERSt6vectorIN5boost13intrusive_ptrIS1_EENS_4core10SAllocatorIS6_LNS_6memory13E_MEMORY_HINTE0EEEE
                (uVar4,0x5f796e61,&local_74);
      piVar9 = local_70;
      if (local_74 != local_70) {
        __needle = (char *)(DAT_0041e4ec + 0x41e554);
        iVar2 = DAT_0041e4f0 + 0x41e55c;
        piVar14 = local_74;
        do {
          while( true ) {
            piVar17 = piVar14 + 1;
            pcVar7 = (char *)(**(code **)(*(int *)*piVar14 + 0x30))();
            pcVar7 = strstr(pcVar7,__needle);
            if (pcVar7 != (char *)0x0) break;
LAB_0041e570:
            piVar14 = piVar17;
            piVar16 = local_74;
            piVar8 = local_70;
            if (piVar9 == piVar17) goto joined_r0x0041e690;
          }
          uVar4 = _ZN6CLevel8GetLevelEv();
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                    (auStack_134,iVar2);
          local_130 = (int *)*piVar14;
          local_c8 = 0;
          local_c4 = 0;
          local_c0 = 0;
          local_bc = 0;
          local_b8 = 0;
          local_b4 = 0;
          if (local_130 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                      ((int)local_130 + *(int *)(*local_130 + -0x10) + 4);
          }
          local_b0 = 0x3f800000;
          local_ac = 0x3f800000;
          local_a8 = 0x3f800000;
          local_138 = _ZN6CLevel11StartEffectERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEENS3_8vector3dIfEESC_N5boost13intrusive_ptrINS2_5scene10ISceneNodeEEESC_bP11CGameObject
                                (uVar4,auStack_134,&local_c8,&local_bc,&local_130,&local_b0,0,piVar3
                                );
          if (local_130 != (int *)0x0) {
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                      ((int)local_130 + *(int *)(*local_130 + -0x10));
          }
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                    (auStack_134);
          if (local_138 == 0) goto LAB_0041e570;
          piVar14 = (int *)param_1[0xf];
          if (piVar14 != (int *)param_1[0x10]) {
            iVar5 = 0;
            if (piVar14 != (int *)0x0) {
              *piVar14 = local_138;
              iVar5 = param_1[0xf];
            }
            param_1[0xf] = iVar5 + 4;
            goto LAB_0041e570;
          }
          _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                    (param_1 + 0xe,piVar14,&local_138);
          piVar14 = piVar17;
          piVar16 = local_74;
          piVar8 = local_70;
        } while (piVar9 != piVar17);
joined_r0x0041e690:
        while (piVar3 = local_70, bVar1 = piVar16 != local_70, local_70 = piVar8, bVar1) {
          piVar14 = piVar16 + 1;
          piVar9 = (int *)*piVar16;
          piVar16 = piVar14;
          local_70 = piVar3;
          if (piVar9 != (int *)0x0) {
            local_70 = piVar8;
            _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                      ((int)piVar9 + *(int *)(*piVar9 + -0x10));
            piVar8 = local_70;
            local_70 = piVar3;
          }
        }
      }
      if (local_74 != (int *)0x0) {
        free(local_74);
      }
      goto LAB_0041da98;
    }
    iVar2 = param_1[0xe];
    if ((uint)(param_1[0xf] - iVar2) >> 2 == 0) goto LAB_0041da98;
  }
  uVar15 = 0;
  do {
    while( true ) {
      uVar11 = uVar15 + 1;
      iVar2 = (**(code **)(**(int **)(iVar2 + uVar15 * 4) + 0x84))();
      if (iVar2 != 0) break;
      piVar3 = *(int **)(param_1[0xe] + uVar15 * 4);
      (**(code **)(*piVar3 + 0x80))(piVar3,1);
      iVar2 = param_1[0xe];
      uVar15 = uVar11;
      if ((uint)(param_1[0xf] - iVar2 >> 2) <= uVar11) goto LAB_0041da98;
    }
    iVar2 = param_1[0xe];
    uVar15 = uVar11;
  } while (uVar11 < (uint)(param_1[0xf] - iVar2 >> 2));
LAB_0041da98:
  piVar3 = (int *)param_1[0x11];
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 0x4c))(piVar3,1);
  }
  piVar3 = (int *)param_1[0x14];
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 0x4c))(piVar3,1);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (&local_12c,param_1[0x16] + 0x38);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (&local_128,param_1[0x16] + 0x3c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (&local_124,param_1[0x16] + 0x34);
  iVar2 = strcasecmp(local_124,(char *)param_1[7]);
  if ((iVar2 != 0) &&
     (iVar2 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                        (&local_124,DAT_0041e4bc + 0x41db24), iVar2 != 0)) {
    if (((int *)param_1[0x11] != (int *)0x0) &&
       ((**(code **)(*(int *)param_1[0x11] + 0x84))(), param_1[0x11] != 0)) {
      piVar3 = *(int **)(*(int *)(DAT_0041e4c0 + 0x41db5c) + 0x180);
      if (piVar3 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                  ((int)piVar3 + *(int *)(*piVar3 + -0x10) + 4);
      }
      (**(code **)(*piVar3 + 0x68))(piVar3,param_1 + 0x11);
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar3 + *(int *)(*piVar3 + -0x10));
      (**(code **)(*(int *)param_1[0x11] + 0x4c))((int *)param_1[0x11],1);
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (param_1 + 7,&local_124);
  }
  iVar2 = strcasecmp(local_12c,(char *)param_1[6]);
  if (iVar2 != 0) {
    iVar2 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                      (&local_128,DAT_0041e4c4 + 0x41dbe0);
    if (iVar2 != 0) {
      if (param_1[9] < 1) {
        puVar12 = *(undefined4 **)(iVar18 + DAT_0041e4f8);
      }
      else {
        puVar12 = *(undefined4 **)(iVar18 + DAT_0041e4f8);
        _ZN15VoxSoundManager4StopEii(*puVar12,param_1[9],0x9c4);
        param_1[9] = -1;
      }
      iVar2 = _ZNK15VoxSoundManager21GetSoundIndexFromNameEPKc(*puVar12,local_128);
      uVar4 = *puVar12;
      param_1[9] = iVar2;
      _ZN15VoxSoundManager19PlayUninterruptibleEPKcNS_6E_LOOPEi(auStack_58,uVar4,local_128,1,0x9c4);
      _ZN3vox13EmitterHandleD1Ev(auStack_58);
    }
    if (param_1[8] != 0) {
      _ZN6CLevel8GetLevelEv();
      _ZNK11CGameObject12GetComponentEi(param_1[8],0x154bb0);
      _ZN14CPoolComponent13ReqInvalidateEv();
      iVar2 = DAT_0041e4c8;
      param_1[8] = 0;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                (auStack_120,iVar2 + 0x41dc78);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                (param_1 + 6,auStack_120);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (auStack_120);
    }
    iVar2 = strcasecmp(local_124,(char *)(DAT_0041e4cc + 0x41dc9c));
    if ((iVar2 == 0) && ((int *)param_1[0x11] != (int *)0x0)) {
      (**(code **)(*(int *)param_1[0x11] + 0x84))();
    }
    iVar2 = strcasecmp(local_12c,(char *)(DAT_0041e4d0 + 0x41dcd0));
    if ((iVar2 != 0) &&
       (iVar2 = strcasecmp(local_12c,(char *)(DAT_0041e4f4 + 0x41e740)), iVar2 != 0)) {
      uVar4 = _ZN6CLevel8GetLevelEv();
      local_a4 = 0;
      local_a0 = 0;
      local_9c = 0;
      local_98 = 0;
      local_94 = 0;
      local_90 = 0;
      local_11c = (int *)0x0;
      local_8c = 0x3f800000;
      local_88 = 0x3f800000;
      local_84 = 0x3f800000;
      piVar3 = (int *)_ZN6CLevel11StartEffectERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEENS3_8vector3dIfEESC_N5boost13intrusive_ptrINS2_5scene10ISceneNodeEEESC_bP11CGameObject
                                (uVar4,&local_12c,&local_a4,&local_98,&local_11c,&local_8c,0,0);
      param_1[8] = (int)piVar3;
      if (local_11c != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                  ((int)local_11c + *(int *)(*local_11c + -0x10));
        piVar3 = (int *)param_1[8];
      }
      (**(code **)(*piVar3 + 0x80))(piVar3,0);
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (param_1 + 6,&local_12c);
  }
  piVar3 = (int *)param_1[8];
  if (piVar3 != (int *)0x0) {
    pcVar13 = *(code **)(*piVar3 + 0x28);
    _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
              (auStack_80,*(undefined4 *)(*(int *)(DAT_0041e4d4 + 0x41dd04) + 0xe4));
    (*pcVar13)(piVar3,auStack_80,1);
    (**(code **)(*(int *)param_1[8] + 0x6c))((int *)param_1[8],param_2);
  }
  if (*(char *)(DAT_0041e4d8 + 0x41dd3c) == '\0') {
    if ((int *)param_1[8] != (int *)0x0) {
      (**(code **)(*(int *)param_1[8] + 0x80))();
    }
    piVar3 = (int *)param_1[0x11];
    if (piVar3 != (int *)0x0) {
      (**(code **)(*piVar3 + 0x4c))(piVar3,0);
    }
    piVar3 = (int *)param_1[0x14];
    if (piVar3 != (int *)0x0) {
      (**(code **)(*piVar3 + 0x4c))(piVar3,0);
    }
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_124);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_128);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_12c);
  return;
}

