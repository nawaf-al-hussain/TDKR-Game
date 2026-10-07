// _ZN11Application14LoadGameConfigEv @ 003ed3dc

void _ZN11Application14LoadGameConfigEv(int param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  undefined4 *puVar4;
  void *__dest;
  void *__s2;
  int iVar5;
  char *__src;
  int iVar6;
  int iVar7;
  uint *puVar8;
  int iVar9;
  size_t sVar10;
  int *piVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  uint uVar15;
  uint uVar16;
  int iVar17;
  int *piVar18;
  void *__dest_00;
  undefined4 uVar19;
  uint uVar20;
  int iVar21;
  int iVar22;
  int iVar23;
  int *__src_00;
  uint uVar24;
  uint uVar25;
  uint uVar26;
  int iVar27;
  undefined4 *puVar28;
  bool bVar29;
  int local_1b4;
  int *local_1b0;
  uint local_1ac;
  char *local_1a4;
  undefined4 *local_19c;
  char *local_198;
  char *local_194;
  undefined1 auStack_15c [4];
  undefined1 auStack_158 [4];
  int *local_154;
  undefined1 auStack_150 [4];
  char *local_14c;
  undefined1 auStack_148 [4];
  char *local_144;
  int local_140;
  int local_13c;
  undefined4 local_138;
  uint local_134;
  char acStack_130 [64];
  char acStack_f0 [64];
  char acStack_b0 [64];
  char local_70 [64];
  int local_30;
  int local_2c;
  
  iVar27 = DAT_003ede98 + 0x3ed400;
  piVar11 = *(int **)(iVar27 + DAT_003ede9c);
  local_2c = *piVar11;
  if (*(char *)((int)&__DT_SYMTAB[0x1e7].st_name + param_1 + 2) == '\0') {
    iVar1 = _ZN11Application11GetInstanceEv();
    piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
    (**(code **)(*piVar2 + 0x78))(piVar2,DAT_003edea0 + 0x3ed454,1,1);
    iVar1 = _ZN11Application11GetInstanceEv();
    iVar17 = DAT_003edeac;
    iVar12 = *(int *)(iVar27 + DAT_003edea4);
    local_30 = iVar12 + 0xc;
    iVar13 = *(int *)(*(int *)(*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28) +
                              0x38) + -4);
    iVar14 = *(int *)(iVar13 + 0x20);
    iVar1 = *(int *)(iVar13 + 0x24) - iVar14 >> 4;
    if (0 < iVar1) {
      iVar6 = DAT_003edea8 + 0x3ed4d8;
      iVar7 = DAT_003edeb0 + 0x3ed4f0;
      local_1b4 = 0;
      do {
        uVar19 = *(undefined4 *)(iVar14 + local_1b4 * 0x10 + 8);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                  (auStack_15c,uVar19);
        _Z15StrGetExtensionRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE
                  (auStack_158,auStack_15c);
        iVar14 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                           (auStack_158,iVar17 + 0x3ed554);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_158);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_15c);
        if (iVar14 == 0) {
          iVar14 = _ZN6CLevel19LoadLevelPropertiesEPKc(uVar19);
          piVar2 = *(int **)(iVar27 + DAT_003edeb4);
          if (iVar14 == 0) {
LAB_003ed6bc:
            piVar3 = (int *)*piVar2;
          }
          else {
            iVar22 = *piVar2;
            iVar14 = *(int *)(iVar22 + 0x24);
            if ((*(int *)(iVar22 + 0x28) - iVar14 >> 2) * 0x11111111 == 0) {
              local_19c = *(undefined4 **)(iVar27 + DAT_003edeb8);
            }
            else {
              __s2 = (void *)(DAT_003edec4 + 0x3ed864);
              local_19c = *(undefined4 **)(iVar27 + DAT_003edeb8);
              iVar5 = DAT_003edec8 + 0x3ed898;
              iVar21 = 0;
              local_1ac = 0;
              do {
                puVar28 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
                iVar23 = *(int *)(iVar14 + iVar21 + 0x18);
                iVar22 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar28 >> 2;
                if (iVar22 == 0) {
LAB_003ed8f8:
                  local_154 = (int *)_Z11CustomAllocjPKci(0x18,iVar6,0x94a);
                  iVar14 = *(int *)(*piVar2 + 0x24);
                  local_154[1] = iVar12 + 0xc;
                  local_154[2] = iVar12 + 0xc;
                  local_154[3] = 0;
                  local_154[4] = 0;
                  local_154[5] = 0;
                  *local_154 = iVar23;
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                            (local_154 + 2,iVar14 + iVar21 + 0x20);
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                            (local_154 + 1,*(int *)(*piVar2 + 0x24) + iVar21 + 0x1c);
                  puVar28 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_size + param_1);
                  if (puVar28 == *(undefined4 **)(&__DT_SYMTAB[0x1e8].st_info + param_1)) {
                    _ZNSt6vectorIP12LevelChapterSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                              (param_1 + 0x11f98,puVar28,&local_154);
                    iVar14 = *(int *)(*piVar2 + 0x24);
                  }
                  else {
                    if (puVar28 != (undefined4 *)0x0) {
                      *puVar28 = local_154;
                    }
                    iVar22 = *piVar2;
                    iVar14 = 0;
                    if (puVar28 != (undefined4 *)0x0) {
                      iVar14 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1);
                    }
                    *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) = iVar14 + 4;
                    iVar14 = *(int *)(iVar22 + 0x24);
                  }
                }
                else if (iVar23 != *(int *)*puVar28) {
                  iVar9 = 0;
                  do {
                    iVar9 = iVar9 + 1;
                    if (iVar9 == iVar22) goto LAB_003ed8f8;
                  } while (iVar23 != *(int *)puVar28[iVar9]);
                }
                local_194 = acStack_f0;
                local_198 = acStack_130;
                uVar19 = *(undefined4 *)(iVar14 + iVar21 + 0x24);
                puVar28 = (undefined4 *)_Z11CustomAllocjPKci(0x1c,iVar7,0x957);
                iVar14 = *(int *)(*piVar2 + 0x24);
                iVar22 = iVar12 + 0xc;
                puVar28[2] = iVar22;
                puVar28[3] = iVar22;
                puVar28[4] = iVar22;
                puVar28[5] = iVar22;
                *puVar28 = uVar19;
                puVar28[1] = 0;
                *(undefined1 *)(puVar28 + 6) = 0;
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                          (puVar28 + 2,iVar14 + iVar21 + 0x2c);
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                          (puVar28 + 4,*(int *)(*piVar2 + 0x24) + iVar21 + 0x28);
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                          (puVar28 + 3,*(int *)(*piVar2 + 0x24) + iVar21 + 0x30);
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                          (puVar28 + 5,*(int *)(*piVar2 + 0x24) + iVar21 + 0x34);
                iVar14 = *piVar2;
                __src = (char *)*local_19c;
                local_134 = 0;
                *(undefined1 *)(puVar28 + 6) =
                     *(undefined1 *)(*(int *)(iVar14 + 0x24) + iVar21 + 0x38);
                strcpy(local_194,__src);
                iVar14 = *(int *)(iVar14 + 0x24);
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                          (auStack_150,iVar5);
                _Z18StrChangeExtensionRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEES9_
                          (&local_14c,iVar14 + iVar21 + 0xc,auStack_150);
                strcpy(local_198,local_14c);
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                          (&local_14c);
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                          (auStack_150);
                local_13c = -1;
                iVar14 = *(int *)(*piVar2 + 0x24) + iVar21;
                uVar26 = *(uint *)((int)*(void **)(iVar14 + 4) + -0xc);
                sVar10 = uVar26;
                if (0xb < uVar26) {
                  sVar10 = 0xc;
                }
                iVar22 = memcmp(*(void **)(iVar14 + 4),__s2,sVar10);
                if ((iVar22 != 0) || (uVar26 != 0xc)) {
                  iVar14 = _ZN11Application11GetInstanceEv();
                  local_13c = _ZN8CStrings19GetStringIdFromNameEPKc
                                        (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + iVar14),
                                         *(undefined4 *)(*(int *)(*piVar2 + 0x24) + iVar21 + 4));
                  iVar14 = *(int *)(*piVar2 + 0x24) + iVar21;
                }
                local_138 = 0xffffffff;
                iVar14 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                                   (iVar14 + 8,__s2);
                if (iVar14 != 0) {
                  iVar14 = _ZN11Application11GetInstanceEv();
                  local_138 = _ZN8CStrings19GetStringIdFromNameEPKc
                                        (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + iVar14),
                                         *(undefined4 *)(*(int *)(*piVar2 + 0x24) + iVar21 + 8));
                }
                local_1a4 = acStack_b0;
                iVar14 = _ZN11Application11GetInstanceEv();
                local_140 = _ZN8CStrings19GetStringIdFromNameEPKc
                                      (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + iVar14),
                                       *(undefined4 *)(*piVar2 + 0x10));
                iVar14 = *piVar2;
                strcpy(local_1a4,*(char **)(iVar14 + 0x34));
                if (*(char *)(iVar14 + 0x30) != '\0') {
                  local_134 = local_134 | 1;
                }
                if (*(char *)(*(int *)(iVar14 + 0x24) + iVar21 + 0x10) != '\0') {
                  local_134 = local_134 | 2;
                }
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                          (&local_30);
                strcpy(local_70,*(char **)(*(int *)(*piVar2 + 0x24) + iVar21 + 0x14));
                if (local_13c < 0) {
                  local_13c = local_140;
                }
                if ((local_134 & 3) != 0) {
                  _ZN11GS_BaseMenu12AddLevelInfoERK10sLevelInfob_constprop_2514(&local_140);
                }
                if ((local_134 & 2) == 0) {
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                            (puVar28 + 5);
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                            (puVar28 + 4);
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                            (puVar28 + 3);
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                            (puVar28 + 2);
                  _ZdlPv(puVar28);
                }
                else {
                  puVar4 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
                  iVar14 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar4 >> 2;
                  if (iVar14 != 0) {
                    piVar3 = (int *)*puVar4;
                    if (iVar23 != *piVar3) {
                      iVar22 = 0;
                      do {
                        iVar22 = iVar22 + 1;
                        if (iVar22 == iVar14) goto LAB_003edc20;
                        piVar3 = (int *)puVar4[iVar22];
                      } while (iVar23 != *piVar3);
                    }
                    piVar18 = (int *)piVar3[5];
                    __src_00 = (int *)piVar3[4];
                    puVar28[1] = local_13c;
                    if (__src_00 == piVar18) {
                      uVar26 = (int)__src_00 - piVar3[3] >> 2;
                      if (uVar26 == 0) {
                        iVar14 = 4;
                      }
                      else {
                        uVar25 = uVar26 * 2;
                        if (uVar25 < uVar26) {
                          iVar14 = -4;
                        }
                        else {
                          if (0x3ffffffe < uVar25) {
                            uVar25 = 0x3fffffff;
                          }
                          iVar14 = uVar25 << 2;
                        }
                      }
                      __dest = (void *)_Znwj(iVar14);
                      if ((void *)((int)__dest + uVar26 * 4) != (void *)0x0) {
                        *(undefined4 **)((int)__dest + uVar26 * 4) = puVar28;
                      }
                      iVar22 = (int)__src_00 - piVar3[3] >> 2;
                      sVar10 = 0;
                      if (iVar22 != 0) {
                        sVar10 = iVar22 << 2;
                        memmove(__dest,(void *)piVar3[3],sVar10);
                      }
                      __dest_00 = (void *)((int)__dest + sVar10 + 4);
                      iVar22 = piVar3[4] - (int)__src_00 >> 2;
                      sVar10 = 0;
                      if (iVar22 != 0) {
                        sVar10 = iVar22 << 2;
                        memmove(__dest_00,__src_00,sVar10);
                      }
                      if (piVar3[3] != 0) {
                        _ZdlPv();
                      }
                      piVar3[3] = (int)__dest;
                      piVar3[4] = (int)__dest_00 + sVar10;
                      piVar3[5] = (int)__dest + iVar14;
                    }
                    else {
                      iVar14 = 0;
                      if (__src_00 != (int *)0x0) {
                        *__src_00 = (int)puVar28;
                        iVar14 = piVar3[4];
                      }
                      piVar3[4] = iVar14 + 4;
                    }
                  }
                }
LAB_003edc20:
                iVar22 = *piVar2;
                iVar21 = iVar21 + 0x3c;
                iVar14 = *(int *)(iVar22 + 0x24);
                local_1ac = local_1ac + 1;
              } while (local_1ac < (uint)((*(int *)(iVar22 + 0x28) - iVar14 >> 2) * -0x11111111));
            }
            local_194 = acStack_f0;
            local_198 = acStack_130;
            local_1a4 = acStack_b0;
            local_134 = 0;
            strcpy(local_194,(char *)*local_19c);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                      (auStack_148,DAT_003edebc + 0x3ed5fc);
            _Z18StrChangeExtensionRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEES9_
                      (&local_144,iVar22 + 0x18,auStack_148);
            strcpy(local_198,local_144);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (&local_144);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (auStack_148);
            iVar14 = _ZN11Application11GetInstanceEv();
            local_140 = _ZN8CStrings19GetStringIdFromNameEPKc
                                  (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + iVar14),
                                   *(undefined4 *)(*piVar2 + 0x10));
            iVar14 = *piVar2;
            local_13c = local_140;
            strcpy(local_1a4,*(char **)(iVar14 + 0x34));
            bVar29 = *(char *)(iVar14 + 0x30) != '\0';
            uVar26 = 0;
            if (bVar29) {
              uVar26 = local_134;
            }
            if (bVar29) {
              local_134 = uVar26 | 1;
            }
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
                      (&local_30,0,*(undefined4 *)(local_30 + -0xc),0);
            piVar3 = (int *)*piVar2;
            if ((char)piVar3[7] != '\0') {
              local_134 = local_134 | 2;
            }
            local_70[0] = '\0';
            if ((local_134 & 3) != 0) {
              _ZN11GS_BaseMenu12AddLevelInfoERK10sLevelInfob_constprop_2514(&local_140);
              goto LAB_003ed6bc;
            }
          }
          if (piVar3 != (int *)0x0) {
            (**(code **)(*piVar3 + 4))();
            *piVar2 = 0;
          }
        }
        if (local_1b4 + 1 == iVar1) break;
        local_1b4 = local_1b4 + 1;
        iVar14 = *(int *)(iVar13 + 0x20);
      } while( true );
    }
    local_1b0 = &local_30;
    _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
    _ZN19cAchievementManager21LoadAchievementStatusEv();
    puVar28 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
    uVar26 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar28 >> 2;
    if (uVar26 != 0) {
      uVar25 = 0;
      iVar27 = DAT_003edec0 + 0x3ed738;
      do {
        if (uVar26 == 0) {
          puVar8 = (uint *)0x0;
        }
        else {
          puVar8 = (uint *)*puVar28;
          if (uVar25 != *puVar8) {
            uVar15 = 0;
            do {
              uVar15 = uVar15 + 1;
              if (uVar15 == uVar26) {
                puVar8 = (uint *)0x0;
                break;
              }
              puVar8 = (uint *)puVar28[uVar15];
            } while (uVar25 != *puVar8);
          }
        }
        uVar15 = (int)(puVar8[4] - puVar8[3]) >> 2;
        if (uVar15 != 0) {
          uVar24 = *puVar8;
          uVar20 = 1;
LAB_003ed79c:
          do {
            if (uVar26 == 0) {
              puVar8 = (uint *)0x0;
            }
            else {
              puVar8 = (uint *)*puVar28;
              if (uVar24 != *puVar8) {
                uVar16 = 0;
                do {
                  uVar16 = uVar16 + 1;
                  if (uVar26 == uVar16) {
                    puVar8 = (uint *)0x0;
                    break;
                  }
                  puVar8 = (uint *)puVar28[uVar16];
                } while (uVar24 != *puVar8);
              }
            }
            puVar4 = (undefined4 *)puVar8[3];
            iVar1 = (int)(puVar8[4] - (int)puVar4) >> 2;
            if (iVar1 == 0) {
LAB_003ed82c:
              uVar20 = uVar20 + 1;
              if (uVar15 < uVar20) break;
              goto LAB_003ed79c;
            }
            puVar8 = (uint *)*puVar4;
            if (uVar20 != *puVar8) {
              iVar17 = 0;
              do {
                iVar17 = iVar17 + 1;
                if (iVar1 == iVar17) goto LAB_003ed82c;
                puVar8 = (uint *)puVar4[iVar17];
              } while (uVar20 != *puVar8);
            }
            iVar1 = 0;
            uVar16 = 0;
            do {
              if ((*(int *)(iVar1 + iVar27) != -1) && (*(uint *)(iVar1 + iVar27 + 4) == puVar8[1]))
              {
                puVar8[1] = uVar16;
              }
              iVar1 = iVar1 + 0x114;
              uVar16 = uVar16 + 1;
            } while (iVar1 != 0x8a00);
            uVar20 = uVar20 + 1;
          } while (uVar20 <= uVar15);
        }
        uVar25 = uVar25 + 1;
      } while (uVar25 < uVar26);
    }
    *(undefined1 *)((int)&__DT_SYMTAB[0x1e7].st_name + param_1 + 2) = 1;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (local_1b0);
    if (local_2c != *piVar11) {
LAB_003ede68:
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
  else if (local_2c != *piVar11) goto LAB_003ede68;
  return;
}


