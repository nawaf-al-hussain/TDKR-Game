// _ZN18CGameObjectManager12CreateObjectEiP13CMemoryStreamP5CZone @ 0037774c

int * _ZN18CGameObjectManager12CreateObjectEiP13CMemoryStreamP5CZone
                (undefined4 param_1,int param_2,int *param_3,int param_4)

{
  undefined1 uVar1;
  char cVar2;
  bool bVar3;
  bool bVar4;
  int *piVar5;
  undefined4 *puVar6;
  int *piVar7;
  undefined2 uVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  char *pcVar13;
  char *pcVar14;
  int *piVar15;
  int iVar16;
  int *piVar17;
  char cVar18;
  int local_5c [2];
  undefined1 auStack_54 [4];
  undefined1 auStack_50 [4];
  int local_4c;
  int local_48;
  int *local_44;
  int local_40;
  int local_3c;
  char local_38;
  undefined1 local_37;
  undefined1 local_36;
  undefined1 local_35;
  int local_34;
  int local_30;
  int local_2c;
  
  if (param_2 == 0x2648 || param_2 == 0x4744) {
    cVar18 = '\x01';
  }
  else if (param_2 == 0xc379 || param_2 == 0xc351) {
    cVar18 = '\x01';
  }
  else {
    cVar18 = '\0';
  }
  local_5c[0] = param_2;
  if (param_2 == 0x2648) {
    piVar5 = (int *)_ZnwjPKci(0x144,DAT_00378508 + 0x378034,0x253);
    _ZN12CGroupObjectC1Ei(piVar5,local_5c[0]);
  }
  else if (param_2 == 0x2668) {
    piVar5 = (int *)_ZnwjPKci(0x4d0,DAT_00378504 + 0x378010,0x24f);
    _ZN13CCameraObjectC1Ei(piVar5,local_5c[0]);
  }
  else {
    piVar5 = (int *)_ZnwjPKci(0x134,DAT_003784dc + 0x3777c4,0x259);
    _ZN11CGameObjectC1Ei(piVar5,local_5c[0]);
  }
  puVar6 = (undefined4 *)
           _ZNSt3mapIiSt6vectorIN18CGameObjectManager11TObjectDataESaIS2_EESt4lessIiESaISt4pairIKiS4_EEEixERS8_
                     (param_1,local_5c);
  bVar3 = false;
  bVar4 = false;
  iVar11 = DAT_003784e0 + 0x377800;
  iVar9 = DAT_003784e4 + 0x37780c;
  pcVar14 = (char *)*puVar6;
  if ((char *)*puVar6 != (char *)puVar6[1]) {
    do {
      pcVar13 = pcVar14 + 0xc;
      iVar16 = *(int *)(pcVar14 + 8);
      if (iVar16 == 0x17ac851f) {
        bVar3 = true;
      }
      if (iVar16 == 0x152b87) {
        if (*pcVar14 == '\0') {
          local_3c = *(int *)(DAT_003784f4 + 0x377d30) + 0xc;
          local_40 = iVar9;
          _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                    (param_3,&local_3c);
          iVar12 = param_3[3];
          iVar16 = *param_3;
          cVar18 = *(char *)(iVar16 + iVar12);
          param_3[3] = iVar12 + 1;
          local_38 = cVar18 != '\0';
          cVar18 = *(char *)(iVar16 + iVar12 + 1);
          param_3[3] = iVar12 + 2;
          local_37 = cVar18 != '\0';
          cVar18 = *(char *)(iVar16 + iVar12 + 2);
          param_3[3] = iVar12 + 3;
          cVar18 = cVar18 != '\0';
          cVar2 = *(char *)(iVar16 + iVar12 + 3);
          param_3[3] = iVar12 + 4;
          local_35 = cVar2 != '\0';
          if (((bool)local_37) && (!(bool)cVar18)) {
            bVar4 = true;
            *(ushort *)((int)piVar5 + 0x102) = *(ushort *)((int)piVar5 + 0x102) | 1;
          }
          local_36 = cVar18;
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2189
                    (auStack_50,DAT_003784f8 + 0x377dc8);
          if ((*(ushort *)((int)piVar5 + 0x102) & 1) == 0) {
            local_48 = piVar5[0xe];
            piVar5[0xe] = *(ushort *)((int)piVar5 + 0x102) & 1;
            _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev();
            if ((local_38 == '\0') && (2 < piVar5[0x39] - 0x264dU)) {
              _ZN11CGameObject17InitComponentMeshEP14CComponentMeshP5CZoneRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS6_6memory13E_MEMORY_HINTE0EEEE_part_1592
                        (piVar5,&local_40,param_4,auStack_50);
            }
          }
          else {
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                      (piVar5 + 0x3f,&local_3c);
          }
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                    (auStack_50);
          local_40 = iVar11;
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                    (&local_3c);
          local_40 = DAT_003784fc + 0x377e50;
        }
        else {
          iVar16 = *(int *)(pcVar14 + 4);
          if (*(char *)(iVar16 + 9) != '\0') {
            bVar4 = true;
            *(ushort *)((int)piVar5 + 0x102) = *(ushort *)((int)piVar5 + 0x102) | 1;
          }
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2189
                    (auStack_54,DAT_003784e8 + 0x377abc);
          if ((*(ushort *)((int)piVar5 + 0x102) & 1) == 0) {
            local_4c = piVar5[0xe];
            piVar5[0xe] = *(ushort *)((int)piVar5 + 0x102) & 1;
            _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev();
            if ((*(char *)(iVar16 + 8) == '\0') && (2 < piVar5[0x39] - 0x264dU)) {
              _ZN11CGameObject17InitComponentMeshEP14CComponentMeshP5CZoneRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS6_6memory13E_MEMORY_HINTE0EEEE_part_1592
                        (piVar5,iVar16,param_4,auStack_54);
            }
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (auStack_54);
            cVar18 = *(char *)(iVar16 + 10);
          }
          else {
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                      (piVar5 + 0x3f,iVar16 + 4);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (auStack_54);
            cVar18 = *(char *)(iVar16 + 10);
          }
        }
      }
      else if (iVar16 == 0x2ad2a046) {
        _ZN12CGroupObject15ReadBuiltinDataEP13CMemoryStream(piVar5,param_3);
      }
      else if (iVar16 == 0x14ca79) {
        if (*pcVar14 == '\0') {
          piVar7 = (int *)_ZnwjPKci(0x34,DAT_003784ec + 0x377c9c,0x278);
          iVar16 = DAT_003784f0 + 0x377cb8;
          *(undefined1 *)(piVar7 + 1) = 0;
          *piVar7 = iVar16;
          piVar7[3] = 0;
          piVar7[2] = 0;
          piVar7[4] = 0;
          piVar7[5] = 0;
          piVar7[6] = 0;
          piVar7[7] = 0;
          piVar7[8] = 0;
          piVar7[9] = 0;
          piVar7[10] = 0;
          piVar7[0xb] = 0;
          *(undefined1 *)(piVar7 + 0xc) = 0;
          *(undefined1 *)((int)piVar7 + 0x31) = 0;
          *(undefined1 *)((int)piVar7 + 0x32) = 0;
          _ZN14CComponentBase4LoadEP13CMemoryStream(piVar7,param_3);
          iVar16 = piVar5[2];
          piVar5[0x36] = (int)piVar7;
          *(undefined1 *)(piVar5 + 0x37) = 1;
        }
        else {
          iVar16 = piVar5[2];
          piVar7 = *(int **)(pcVar14 + 4);
          *(undefined1 *)(piVar5 + 0x37) = 0;
          piVar5[0x36] = (int)piVar7;
        }
        if (iVar16 < 1) {
          piVar5[2] = piVar7[2];
        }
        iVar16 = piVar7[1];
        iVar12 = piVar7[0xc];
        piVar5[9] = piVar7[9];
        uVar1 = *(undefined1 *)((int)piVar7 + 0x31);
        piVar5[10] = piVar7[10];
        iVar10 = piVar7[0xb];
        *(char *)(piVar5 + 1) = (char)iVar16;
        *(char *)(piVar5 + 0xc) = (char)iVar12;
        piVar5[0xb] = iVar10;
        _ZN11CGameObject16SetAlwaysVisibleEb(piVar5,uVar1);
        *(undefined1 *)((int)piVar5 + 0x7d) = *(undefined1 *)((int)piVar7 + 0x32);
        if (piVar5[0x39] != 0x2648) {
          (**(code **)(*piVar5 + 0x28))(piVar5,piVar7 + 3,1);
          (**(code **)(*piVar5 + 0x2c))(piVar5,piVar7 + 6);
          (**(code **)(*piVar5 + 0x34))(piVar5,piVar7 + 9);
          if ((piVar5[0xf] != 0) && (iVar16 = _ZNK13CollisionNode8IsStaticEv(), iVar16 == 0)) {
            (**(code **)(*(int *)piVar5[0xf] + 0x14))((int *)piVar5[0xf],piVar5 + 3);
            local_34 = piVar5[6];
            local_30 = piVar5[7];
            local_2c = piVar5[8];
            (**(code **)(*(int *)piVar5[0xf] + 0x1c))((int *)piVar5[0xf],&local_34);
            (**(code **)(*(int *)piVar5[0xf] + 0x24))();
          }
          (**(code **)(*piVar5 + 0x50))(piVar5,(char)piVar5[1]);
          (**(code **)(*piVar5 + 0x80))(piVar5,(char)piVar5[0xc]);
        }
      }
      else {
        piVar7 = (int *)_ZN17CComponentFactory15CreateComponentEiP11CGameObjectPv
                                  (iVar16,piVar5,*(undefined4 *)(pcVar14 + 4));
        if (piVar7 == (int *)0x0) {
          if ((*pcVar14 == '\0') &&
             (piVar7 = (int *)_Z25GenerateComponentTemplateiP13CMemoryStream(iVar16,param_3),
             piVar7 != (int *)0x0)) {
            (**(code **)(*piVar7 + 4))();
          }
        }
        else {
          piVar15 = param_3;
          if (*pcVar14 != '\0') {
            piVar15 = (int *)0x0;
          }
          (**(code **)(*piVar7 + 8))(piVar7,piVar15);
          if ((iVar16 == 0x4ab8a7cd) && (*(int *)(**(int **)(DAT_00378500 + 0x377edc) + 0x2c) == 2))
          {
            (**(code **)(*piVar7 + 4))(piVar7);
          }
          else {
            local_44 = piVar7;
            iVar16 = (**(code **)(*piVar7 + 0x24))(piVar7);
            if (iVar16 == 0x2ef26c52) {
              piVar7 = (int *)piVar5[0x24];
              piVar5[0x35] = (int)local_44;
            }
            else if (iVar16 < 0x2ef26c53) {
              if (iVar16 == 0xddcd6c4) {
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x29] = (int)local_44;
              }
              else if (iVar16 < 0xddcd6c5) {
                if (iVar16 == 0x651bdaa) {
                  piVar7 = (int *)piVar5[0x24];
                  piVar5[0x2a] = (int)local_44;
                }
                else if (iVar16 == 0x68d1134) {
                  piVar7 = (int *)piVar5[0x24];
                  *(undefined1 *)((int)piVar5 + 0xeb) = 1;
                }
                else {
                  if (iVar16 != 0x113f791) goto LAB_00377918;
                  *(undefined1 *)((int)piVar5 + 0xeb) = 1;
                  piVar7 = (int *)piVar5[0x24];
                  piVar5[0x2f] = (int)local_44;
                }
              }
              else if (iVar16 == 0xf5f8cfd) {
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x26] = (int)local_44;
              }
              else if (iVar16 == 0x2ca13c06) {
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x34] = (int)local_44;
              }
              else {
                if (iVar16 != 0xdfe2718) goto LAB_00377918;
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x27] = (int)local_44;
              }
            }
            else if (iVar16 == 0x54989cb1) {
              piVar15 = (int *)piVar5[0x23];
              piVar7 = (int *)piVar5[0x24];
              piVar5[0x2e] = (int)local_44;
              if (piVar15 != piVar7) {
                do {
                  piVar17 = piVar15 + 1;
                  iVar16 = (**(code **)(*(int *)*piVar15 + 0x24))();
                  if (iVar16 == 0xf5f8cfd) {
                    if (((int *)piVar5[0x24] == (int *)piVar5[0x25]) ||
                       (piVar17 != (int *)piVar5[0x24])) {
                      _ZNSt6vectorIP10IComponentSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                                (piVar5 + 0x23,piVar17,&local_44);
                    }
                    else {
                      iVar16 = 0;
                      if (piVar17 != (int *)0x0) {
                        piVar15[1] = (int)local_44;
                        iVar16 = piVar5[0x24];
                      }
                      piVar5[0x24] = iVar16 + 4;
                    }
                    goto LAB_00377944;
                  }
                  piVar15 = piVar17;
                } while (piVar7 != piVar17);
                piVar7 = (int *)piVar5[0x24];
              }
            }
            else if (iVar16 < 0x54989cb2) {
              if (iVar16 == 0x4846ed83) {
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x31] = (int)local_44;
              }
              else if (iVar16 == 0x5441a117) {
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x2d] = (int)local_44;
              }
              else {
                if (iVar16 != 0x377ea715) goto LAB_00377918;
                *(undefined1 *)((int)piVar5 + 0xeb) = 1;
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x28] = (int)local_44;
              }
            }
            else if (iVar16 == 0x6754056b) {
              piVar7 = (int *)piVar5[0x24];
              piVar5[0x2b] = (int)local_44;
            }
            else if (iVar16 < 0x6754056c) {
              if (iVar16 == 0x592ce07c) {
                piVar7 = (int *)piVar5[0x24];
                piVar5[0x33] = (int)local_44;
              }
              else {
LAB_00377918:
                piVar7 = (int *)piVar5[0x24];
              }
            }
            else if (iVar16 == 0x7538c652) {
              *(undefined1 *)((int)piVar5 + 0xed) = 1;
              piVar7 = (int *)piVar5[0x24];
              piVar5[0x2c] = (int)local_44;
            }
            else {
              if (iVar16 != 0x75a9de0e) goto LAB_00377918;
              piVar7 = (int *)piVar5[0x24];
              piVar5[0x32] = (int)local_44;
            }
            if ((int *)piVar5[0x25] == piVar7) {
              _ZNSt6vectorIP10IComponentSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                        (piVar5 + 0x23,piVar7,&local_44);
            }
            else {
              iVar16 = 0;
              if (piVar7 != (int *)0x0) {
                *piVar7 = (int)local_44;
                iVar16 = piVar5[0x24];
              }
              piVar5[0x24] = iVar16 + 4;
            }
          }
        }
      }
LAB_00377944:
      pcVar14 = pcVar13;
    } while (pcVar13 != (char *)puVar6[1]);
  }
  if (*(char *)((int)piVar5 + 0xed) == '\0') {
    if ((((piVar5[0x2e] == 0) && (iVar9 = piVar5[0x39], iVar9 != 0x2c)) && (iVar9 != 0x4c752)) &&
       (iVar9 != 0x266d)) goto LAB_00377a20;
    piVar7 = (int *)_ZN17CComponentFactory15CreateComponentEiP11CGameObjectPv(0x75a9de0e,piVar5,0);
  }
  else {
    piVar7 = (int *)_ZN17CComponentFactory15CreateComponentEiP11CGameObjectPv(0x4846ed83,piVar5,0);
  }
  if (piVar7 == (int *)0x0) goto LAB_00377a20;
  local_44 = piVar7;
  iVar9 = (**(code **)(*piVar7 + 0x24))(piVar7);
  if (iVar9 == 0x2ef26c52) {
    piVar7 = (int *)piVar5[0x24];
    piVar5[0x35] = (int)local_44;
  }
  else if (iVar9 < 0x2ef26c53) {
    if (iVar9 == 0xddcd6c4) {
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x29] = (int)local_44;
    }
    else if (iVar9 < 0xddcd6c5) {
      if (iVar9 == 0x651bdaa) {
        piVar7 = (int *)piVar5[0x24];
        piVar5[0x2a] = (int)local_44;
      }
      else if (iVar9 == 0x68d1134) {
        piVar7 = (int *)piVar5[0x24];
        *(undefined1 *)((int)piVar5 + 0xeb) = 1;
      }
      else {
        if (iVar9 != 0x113f791) goto LAB_003779f8;
        *(undefined1 *)((int)piVar5 + 0xeb) = 1;
        piVar7 = (int *)piVar5[0x24];
        piVar5[0x2f] = (int)local_44;
      }
    }
    else if (iVar9 == 0xf5f8cfd) {
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x26] = (int)local_44;
    }
    else if (iVar9 == 0x2ca13c06) {
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x34] = (int)local_44;
    }
    else {
      if (iVar9 != 0xdfe2718) goto LAB_003779f8;
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x27] = (int)local_44;
    }
  }
  else if (iVar9 == 0x54989cb1) {
    piVar15 = (int *)piVar5[0x23];
    piVar7 = (int *)piVar5[0x24];
    piVar5[0x2e] = (int)local_44;
    if (piVar15 != piVar7) {
      do {
        piVar17 = piVar15 + 1;
        iVar9 = (**(code **)(*(int *)*piVar15 + 0x24))();
        if (iVar9 == 0xf5f8cfd) {
          if (((int *)piVar5[0x24] == (int *)piVar5[0x25]) || (piVar17 != (int *)piVar5[0x24])) {
            _ZNSt6vectorIP10IComponentSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                      (piVar5 + 0x23,piVar17,&local_44);
          }
          else {
            iVar9 = 0;
            if (piVar17 != (int *)0x0) {
              piVar15[1] = (int)local_44;
              iVar9 = piVar5[0x24];
            }
            piVar5[0x24] = iVar9 + 4;
          }
          goto LAB_00377a20;
        }
        piVar15 = piVar17;
      } while (piVar7 != piVar17);
      goto LAB_003779f8;
    }
  }
  else if (iVar9 < 0x54989cb2) {
    if (iVar9 == 0x4846ed83) {
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x31] = (int)local_44;
    }
    else if (iVar9 == 0x5441a117) {
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x2d] = (int)local_44;
    }
    else {
      if (iVar9 != 0x377ea715) goto LAB_003779f8;
      *(undefined1 *)((int)piVar5 + 0xeb) = 1;
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x28] = (int)local_44;
    }
  }
  else if (iVar9 == 0x6754056b) {
    piVar7 = (int *)piVar5[0x24];
    piVar5[0x2b] = (int)local_44;
  }
  else if (iVar9 < 0x6754056c) {
    if (iVar9 == 0x592ce07c) {
      piVar7 = (int *)piVar5[0x24];
      piVar5[0x33] = (int)local_44;
    }
    else {
LAB_003779f8:
      piVar7 = (int *)piVar5[0x24];
    }
  }
  else if (iVar9 == 0x7538c652) {
    *(undefined1 *)((int)piVar5 + 0xed) = 1;
    piVar7 = (int *)piVar5[0x24];
    piVar5[0x2c] = (int)local_44;
  }
  else {
    if (iVar9 != 0x75a9de0e) goto LAB_003779f8;
    piVar7 = (int *)piVar5[0x24];
    piVar5[0x32] = (int)local_44;
  }
  if ((int *)piVar5[0x25] == piVar7) {
    _ZNSt6vectorIP10IComponentSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
              (piVar5 + 0x23,piVar7,&local_44);
  }
  else {
    iVar9 = 0;
    if (piVar7 != (int *)0x0) {
      *piVar7 = (int)local_44;
      iVar9 = piVar5[0x24];
    }
    piVar5[0x24] = iVar9 + 4;
  }
LAB_00377a20:
  if (param_4 != 0) {
    if (bVar4) {
      uVar8 = 0x20;
    }
    else if ((cVar18 == '\0') || (bVar3)) {
      if (piVar5[0x2e] == 0) {
        uVar8 = 1;
      }
      else {
        uVar8 = 0x10;
      }
    }
    else {
      uVar8 = 2;
    }
    piVar5[0x22] = param_4;
    *(undefined2 *)(piVar5 + 0x41) = uVar8;
    _ZN5CZone9AddObjectEP11CGameObjectb(param_4,piVar5,0);
  }
  if ((local_5c[0] == 0x2648) && (param_4 == 0)) {
    (**(code **)(*piVar5 + 4))(piVar5);
    piVar5 = (int *)0x0;
  }
  return piVar5;
}


