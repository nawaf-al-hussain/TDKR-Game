// _ZN11CGameObject8SaveLoadEP13CMemoryStream @ 0036e820

/* WARNING: Control flow encountered bad instruction data */

undefined4 _ZN11CGameObject8SaveLoadEP13CMemoryStream(int *param_1,int *param_2)

{
  byte bVar1;
  byte bVar2;
  undefined1 uVar3;
  undefined1 uVar4;
  char cVar5;
  ushort uVar6;
  undefined4 uVar7;
  int iVar8;
  int *piVar9;
  size_t __n;
  undefined1 *__dest;
  uint uVar10;
  byte bVar11;
  int iVar12;
  undefined4 *puVar13;
  code *pcVar14;
  int iVar15;
  int iVar16;
  uint uVar17;
  undefined1 *puVar18;
  uint *puVar19;
  undefined1 *__src;
  undefined4 *puVar20;
  int local_5c;
  undefined1 *local_58;
  undefined4 local_54;
  undefined1 auStack_50 [4];
  undefined4 local_4c;
  int local_48;
  int *local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  
  cVar5 = *(char *)(*param_2 + param_2[3]);
  pcVar14 = *(code **)(*param_1 + 0x50);
  iVar16 = DAT_0036f074 + 0x36e854;
  param_2[3] = param_2[3] + 1;
  (*pcVar14)(param_1,cVar5 != '\0');
  cVar5 = *(char *)(*param_2 + param_2[3]);
  pcVar14 = *(code **)(*param_1 + 0x80);
  param_2[3] = param_2[3] + 1;
  (*pcVar14)(param_1,cVar5 != '\0');
  cVar5 = *(char *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  _ZN11CGameObject16SetAlwaysVisibleEb(param_1,cVar5 != '\0');
  cVar5 = *(char *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  local_40 = 0;
  local_3c = 0;
  *(bool *)((int)param_1 + 0x7d) = cVar5 != '\0';
  local_38 = 0;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_40 = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_3c = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_38 = local_5c;
  (**(code **)(*param_1 + 0x28))(param_1,&local_40,1);
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_40 = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_3c = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_38 = local_5c;
  (**(code **)(*param_1 + 0x2c))(param_1,&local_40);
  if ((param_1[0xf] != 0) && (iVar8 = _ZNK13CollisionNode8IsStaticEv(), iVar8 == 0)) {
    local_34 = param_1[6];
    local_30 = param_1[7];
    local_2c = param_1[8];
    (**(code **)(*(int *)param_1[0xf] + 0x1c))((int *)param_1[0xf],&local_34);
    (**(code **)(*(int *)param_1[0xf] + 0x24))();
  }
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_40 = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_3c = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_38 = local_5c;
  (**(code **)(*param_1 + 0x34))(param_1,&local_40);
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  param_1[0x19] = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  param_1[0x1a] = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  iVar8 = param_2[3];
  iVar15 = *param_2;
  param_1[0x1b] = local_5c;
  cVar5 = *(char *)(iVar15 + iVar8);
  iVar12 = iVar8 + 4;
  param_2[3] = iVar8 + 1;
  bVar1 = *(byte *)(iVar15 + iVar8 + 1);
  param_2[3] = iVar8 + 2;
  bVar11 = *(byte *)(iVar15 + iVar8 + 2);
  param_2[3] = iVar8 + 3;
  bVar2 = *(byte *)(iVar15 + iVar8 + 3);
  param_2[3] = iVar12;
  uVar10 = (uint)bVar2 | (int)cVar5 << 0x18 | (uint)bVar1 << 0x10 | (uint)bVar11 << 8;
  if ((int)uVar10 < 0) goto LAB_0036ed98;
  puVar19 = (uint *)(DAT_0036f07c + 0x36ea88);
  piVar9 = (int *)_ZN13CZonesManager10FindObjectEit
                            (**(undefined4 **)(iVar16 + DAT_0036f078),uVar10,0x11);
  puVar18 = *(undefined1 **)(iVar16 + DAT_0036f080);
  local_58 = puVar18 + 0xc;
  __n = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (((*puVar19 & 1) == 0) && (iVar8 = __cxa_guard_acquire(puVar19), iVar8 != 0)) {
    iVar8 = DAT_0036f088 + 0x36efb8;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2189
              (iVar8,DAT_0036f08c + 0x36efbc);
    __cxa_guard_release(puVar19);
    __aeabi_atexit(iVar8,*(undefined4 *)(iVar16 + DAT_0036f090),
                   *(undefined4 *)(iVar16 + DAT_0036f094));
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (&local_58,DAT_0036f084 + 0x36eac8);
  if (0 < (int)__n) {
    iVar16 = *(int *)(local_58 + -0xc);
    if (0x3ffffffcU - iVar16 < __n) {
      _ZSt20__throw_length_errorPKc((int)&DAT_0036f074 + DAT_0036f098);
                    /* WARNING: Bad instruction - Truncating control flow here */
      halt_baddata();
    }
    uVar10 = *(uint *)(local_58 + -8);
    uVar17 = __n + iVar16;
    __src = (undefined1 *)(*param_2 + param_2[3]);
    if ((uVar10 < uVar17) || (0 < *(int *)(local_58 + -4))) {
      if ((__src < local_58) || (__dest = local_58 + iVar16, __dest < __src)) {
        if ((uVar17 == uVar10) && (*(int *)(local_58 + -4) < 1)) goto LAB_0036f03c;
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1588
                  (&local_58,uVar17);
        __dest = local_58 + *(int *)(local_58 + -0xc);
      }
      else {
        iVar16 = (int)__src - (int)local_58;
        if ((uVar17 == uVar10) && (*(int *)(local_58 + -4) < 1)) {
          __src = local_58 + iVar16;
        }
        else {
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1588
                    (&local_58,uVar17);
          __src = local_58 + iVar16;
          __dest = local_58 + *(int *)(local_58 + -0xc);
        }
      }
    }
    else {
LAB_0036f03c:
      __dest = local_58 + iVar16;
    }
    if (__n == 1) {
      *__dest = *__src;
    }
    else {
      memcpy(__dest,__src,__n);
    }
    if (local_58 + -0xc != puVar18) {
      *(uint *)(local_58 + -0xc) = uVar17;
      *(undefined4 *)(local_58 + -4) = 0;
      local_58[uVar17] = 0;
    }
    param_2[3] = param_2[3] + __n;
  }
  local_54 = 0;
  if (piVar9 != (int *)0x0) {
    _ZN6glitch5scene10ISceneNode20getSceneNodeFromNameEPKc(auStack_50,piVar9[0xe],local_58);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2ERKS4_(&local_4c,auStack_50);
    uVar7 = local_4c;
    local_4c = local_54;
    local_54 = uVar7;
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_4c);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_50);
  }
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_40 = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_3c = local_5c;
  _ZN13CMemoryStream4ReadERf(param_2,&local_5c);
  local_38 = local_5c;
  bVar1 = *(byte *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  if (param_1 == piVar9) {
    bVar11 = *(byte *)(param_1 + 0x48);
  }
  else {
    iVar16 = param_1[0x43];
    if (iVar16 != 0) {
      puVar13 = *(undefined4 **)(iVar16 + 0x110);
      iVar8 = *(int *)(iVar16 + 0x114) - (int)puVar13 >> 2;
      if (iVar8 != 0) {
        puVar20 = puVar13;
        if (param_1 != (int *)*puVar13) {
          iVar12 = 0;
          do {
            iVar12 = iVar12 + 1;
            if (iVar12 == iVar8) goto LAB_0036ecb0;
            puVar20 = puVar13 + iVar12;
          } while (param_1 != (int *)puVar13[iVar12]);
        }
        *puVar20 = 0;
        iVar16 = param_1[0x43];
      }
LAB_0036ecb0:
      if (*(char *)(iVar16 + 0x120) < '\0') {
        *(uint *)(param_1[0xe] + 0xf4) = *(uint *)(param_1[0xe] + 0xf4) | 0x1000;
        *(byte *)(iVar16 + 0x120) = *(byte *)(iVar16 + 0x120) & 0x7f;
      }
    }
    param_1[0x43] = (int)piVar9;
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2ERKS4_(&local_48,&local_54);
    iVar16 = param_1[0x47];
    param_1[0x47] = local_48;
    local_48 = iVar16;
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_48);
    iVar16 = param_1[0x43];
    if (iVar16 == 0) {
      bVar11 = *(byte *)(param_1 + 0x48);
    }
    else {
      piVar9 = *(int **)(iVar16 + 0x114);
      puVar13 = *(undefined4 **)(iVar16 + 0x110);
      iVar8 = (int)piVar9 - (int)puVar13 >> 2;
      local_44 = param_1;
      if (iVar8 == 0) {
LAB_0036ed3c:
        if (piVar9 == *(int **)(iVar16 + 0x118)) {
          _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                    (iVar16 + 0x110,piVar9,&local_44);
        }
        else {
          iVar8 = 0;
          if (piVar9 != (int *)0x0) {
            *piVar9 = (int)param_1;
            iVar8 = *(int *)(iVar16 + 0x114);
          }
          *(int *)(iVar16 + 0x114) = iVar8 + 4;
        }
      }
      else if (param_1 != (int *)*puVar13) {
        iVar12 = 0;
        do {
          iVar12 = iVar12 + 1;
          if (iVar8 == iVar12) goto LAB_0036ed3c;
        } while (param_1 != (int *)puVar13[iVar12]);
      }
      bVar11 = 1;
    }
  }
  param_1[0x4b] = local_38;
  *(byte *)(param_1 + 0x48) = bVar11 | bVar1;
  param_1[0x49] = local_40;
  param_1[0x4a] = local_3c;
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_54);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_58);
  iVar15 = *param_2;
  iVar12 = param_2[3];
LAB_0036ed98:
  uVar3 = *(undefined1 *)(iVar15 + iVar12);
  param_2[3] = iVar12 + 1;
  iVar16 = 0;
  uVar4 = *(undefined1 *)(iVar15 + iVar12 + 1);
  param_2[3] = iVar12 + 2;
  uVar6 = CONCAT11(uVar3,uVar4);
  do {
    while( true ) {
      uVar6 = uVar6 - 1;
      if ((uVar6 & 0x8000) != 0) {
        if (param_1[0x2f] != 0) {
          iVar16 = _ZN15CNpcAIComponent7IsEnemyEv();
          _ZN15CNpcAIComponent8SetEnemyEb(param_1[0x2f],iVar16);
          if ((iVar16 != 0) && (iVar16 = param_1[0x2b], iVar16 != 0)) {
            iVar8 = _ZN6CLevel8GetLevelEv();
            _ZN19CAwarenessComponent16SetCurrentTargetEP11CGameObject
                      (iVar16,*(undefined4 *)(iVar8 + 0xec));
          }
        }
        return 1;
      }
      iVar12 = param_2[3];
      iVar8 = *param_2;
      piVar9 = *(int **)(param_1[0x23] + iVar16 * 4);
      cVar5 = *(char *)(iVar8 + iVar12);
      param_2[3] = iVar12 + 1;
      bVar1 = *(byte *)(iVar8 + iVar12 + 1);
      iVar15 = *piVar9;
      param_2[3] = iVar12 + 2;
      bVar11 = *(byte *)(iVar8 + iVar12 + 2);
      param_2[3] = iVar12 + 3;
      bVar2 = *(byte *)(iVar8 + iVar12 + 3);
      pcVar14 = *(code **)(iVar15 + 0x24);
      param_2[3] = iVar12 + 4;
      uVar17 = (uint)bVar2 | (int)cVar5 << 0x18 | (uint)bVar1 << 0x10 | (uint)bVar11 << 8;
      uVar10 = (*pcVar14)(piVar9);
      if (uVar10 != uVar17) break;
      piVar9 = *(int **)(param_1[0x23] + iVar16 * 4);
      param_2[3] = param_2[3] + 2;
LAB_0036ee94:
      iVar16 = iVar16 + 1;
      (**(code **)(*piVar9 + 0x2c))(piVar9,param_2);
      param_2[3] = param_2[3] + 1;
    }
    iVar12 = param_1[0x23];
    iVar8 = param_1[0x24] - iVar12 >> 2;
    iVar16 = iVar8 + -1;
    if (-1 < iVar16) {
      iVar8 = (iVar8 + 0x3fffffff) * 4;
      while (uVar10 = (**(code **)(**(int **)(iVar12 + iVar8) + 0x24))(), uVar10 != uVar17) {
        iVar16 = iVar16 + -1;
        iVar8 = iVar8 + -4;
        if (iVar16 < 0) goto LAB_0036ef0c;
        iVar12 = param_1[0x23];
      }
      piVar9 = *(int **)(param_1[0x23] + iVar8);
      param_2[3] = param_2[3] + 2;
      goto LAB_0036ee94;
    }
LAB_0036ef0c:
    iVar8 = param_2[3];
    uVar3 = *(undefined1 *)(*param_2 + iVar8);
    param_2[3] = iVar8 + 1;
    param_2[3] = iVar8 + (uint)CONCAT11(uVar3,*(undefined1 *)(*param_2 + iVar8 + 1)) + 3;
  } while( true );
}


