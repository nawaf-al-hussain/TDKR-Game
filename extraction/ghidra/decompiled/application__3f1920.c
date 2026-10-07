// _ZN11Application9UpdateAppEv @ 003f1920

void _ZN11Application9UpdateAppEv(int param_1)

{
  char cVar1;
  int iVar2;
  int *piVar3;
  undefined4 uVar4;
  float fVar5;
  int *piVar6;
  int iVar7;
  float *pfVar8;
  int *piVar9;
  int *piVar10;
  undefined4 *puVar11;
  code *pcVar12;
  int iVar13;
  float fVar14;
  int local_30;
  int local_2c [2];
  
  iVar7 = DAT_003f208c;
  *(int *)((int)&__DT_SYMTAB[0x1ed].st_size + param_1) =
       *(int *)((int)&__DT_SYMTAB[0x1ed].st_size + param_1) + 1;
  iVar7 = iVar7 + 0x3f1950;
  if (((*(char *)(**(int **)(iVar7 + DAT_003f2090) + 0xb5) == '\0') ||
      (iVar2 = _ZN11Application11GetInstanceEv(),
      *(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) == 0)) ||
     (iVar2 = _ZN11Application11GetInstanceEv(),
     *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8) == 0)) {
    iVar2 = _ZN11Application11GetInstanceEv();
    iVar2 = *(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2);
  }
  else {
    iVar2 = _ZN11Application11GetInstanceEv();
    piVar3 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
    (**(code **)(*piVar3 + 0x94))(piVar3,3);
    iVar2 = _ZN11Application11GetInstanceEv();
    iVar2 = *(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2);
  }
  if (iVar2 == 0) {
    _ZN6glitch14createDeviceExEPN3glf3AppE(&local_30,param_1);
    iVar7 = local_30;
    if (local_30 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_30 + 4);
    }
    iVar2 = *(int *)((int)&__DT_SYMTAB[0x1de].st_name + param_1);
    *(int *)((int)&__DT_SYMTAB[0x1de].st_name + param_1) = iVar7;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_30 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    iVar7 = _ZN11Application11GetInstanceEv();
    local_2c[0] = *(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar7);
    if (local_2c[0] != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_2c[0] + 4);
    }
    _ZN11Application4InitEN5boost13intrusive_ptrIN6glitch7IDeviceEEE(param_1,local_2c);
    if (local_2c[0] == 0) {
      return;
    }
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    return;
  }
  iVar2 = _ZN11Application11GetInstanceEv();
  _ZN6glitch7IDevice3runEv(*(undefined4 *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2));
  iVar2 = _ZNK3glf3App19GetCreationSettingsEv(param_1);
  if (*(char *)(iVar2 + 0x41) == '\0') {
    iVar2 = _ZN11Application11GetInstanceEv();
    iVar13 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
    iVar2 = _ZNK3glf3App14GetOrientationEv(param_1);
    if (iVar2 != *(int *)((int)&__DT_SYMTAB[0x1e9].st_size + param_1)) {
      if (iVar2 == 4) {
        piVar3 = (int *)**(int **)(iVar13 + 0x11c);
        if (piVar3[0xe] != 3) {
          (**(code **)(*piVar3 + 0x18))(piVar3,3);
        }
      }
      else if ((iVar2 == 8) && (piVar3 = (int *)**(int **)(iVar13 + 0x11c), piVar3[0xe] != 1)) {
        (**(code **)(*piVar3 + 0x18))(piVar3,1);
      }
    }
    *(int *)((int)&__DT_SYMTAB[0x1e9].st_size + param_1) = iVar2;
  }
  cVar1 = *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1);
  *(undefined1 *)((int)&__DT_SYMTAB[0x1f0].st_size + param_1) = 0;
  if (cVar1 == '\0') {
    piVar9 = *(int **)(iVar7 + DAT_003f2094);
  }
  else {
    cVar1 = *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1);
    if (cVar1 == '\x03') {
      piVar9 = *(int **)(iVar7 + DAT_003f2094);
      piVar3 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar9 + 4);
      if (((piVar3 != (int *)0x0) && (iVar2 = _ZN6CLevel8GetLevelEv(), iVar2 != 0)) &&
         (iVar2 = (**(code **)(*piVar3 + 8))(piVar3,2), iVar2 != 0)) {
        uVar4 = _ZN6CLevel8GetLevelEv();
        _ZN6CLevel14OpenIngameMenuEb(uVar4,0);
      }
      if (*(char *)((int)&__DT_SYMTAB[0x1f1].st_size + param_1) != '\0') {
        *(undefined1 *)((int)&__DT_SYMTAB[0x1f1].st_size + param_1) = 0;
        if (**(int **)(iVar7 + DAT_003f20ac) != 0) {
          _ZN10IAPManager5ResetEv();
        }
        if (**(int **)(iVar7 + DAT_003f20b0) != 0) {
          _ZN17FederationManager11GetMessagesEv();
        }
      }
    }
    else {
      if (cVar1 == '\x14') {
        *(undefined1 *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) = 0xff;
        piVar9 = *(int **)(iVar7 + DAT_003f2094);
        *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) =
             *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) + '\x01';
        goto LAB_003f19c4;
      }
      piVar9 = *(int **)(iVar7 + DAT_003f2094);
      if (cVar1 == '\x01') {
        piVar3 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar9 + 4);
        if (piVar3 == (int *)0x0) {
          *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) =
               *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) + '\x01';
        }
        else {
          iVar2 = (**(code **)(*piVar3 + 8))(piVar3,8);
          if (iVar2 == 0) {
            iVar2 = (**(code **)(*piVar3 + 8))(piVar3,2);
            if (iVar2 == 0) {
              if (**(int **)(iVar7 + DAT_003f20bc) != 0) goto LAB_003f2058;
            }
            else if (((*(char *)((int)piVar3 + 0x15) == '\0') &&
                     ((*(uint *)(*(int *)(DAT_003f20b8 + 0x3f2040) + 0x4c8) & 0x19ea144) == 0)) &&
                    (*(char *)(*(int *)(DAT_003f20b8 + 0x3f2040) + 0x498) == '\0')) {
LAB_003f2058:
              _ZN15VoxSoundManager15ResumeAllSoundsEif
                        (**(undefined4 **)(iVar7 + DAT_003f209c),0xffffffff,0x3f000000);
            }
          }
          else {
            *(uint *)(DAT_003f20a8 + 0x3f1e48) = *(uint *)(DAT_003f20a8 + 0x3f1e48) | 1;
          }
        }
        iVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
        if (iVar2 != 0) {
          iVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
          *(undefined1 *)(iVar2 + 0x88) = 1;
        }
      }
    }
    *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) =
         *(char *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) + '\x01';
  }
LAB_003f19c4:
  _ZN11Application14CheckLoadLevelEv(param_1);
  if (*(char *)((int)&__DT_SYMTAB[0x1e8].st_name + param_1) != '\0') {
    _ZN11GS_BaseMenu16ReturnToMainMenuEb(0);
    *(undefined1 *)((int)&__DT_SYMTAB[0x1e8].st_name + param_1) = 0;
  }
  pfVar8 = (float *)((int)&__DT_SYMTAB[0x1ef].st_name + param_1);
  *pfVar8 = 1.0;
  iVar2 = _ZN6CLevel8GetLevelEv();
  if (iVar2 == 0) {
LAB_003f1c0c:
    fVar5 = *pfVar8;
  }
  else {
    piVar3 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar9 + 4);
    iVar2 = (**(code **)(*piVar3 + 8))(piVar3,2);
    if (iVar2 == 0) goto LAB_003f1c0c;
    uVar4 = _ZN6CLevel8GetLevelEv();
    _ZN6CLevel16UpdateSlowMotionEf(uVar4,*(undefined4 *)(&__DT_SYMTAB[0x1ee].st_info + param_1));
    _ZN6CLevel8GetLevelEv();
    fVar5 = (float)_ZNK6CLevel19GetSlowMotionFactorEv();
    *pfVar8 = fVar5;
  }
  fVar14 = *(float *)((int)&__DT_SYMTAB[0x1ee].st_name + param_1);
  pfVar8 = (float *)((int)&__DT_SYMTAB[0x1ee].st_value + param_1);
  fVar5 = *(float *)(**(int **)(iVar7 + DAT_003f2098) + 0x1c) *
          *(float *)(&__DT_SYMTAB[0x1ee].st_info + param_1) * fVar5;
  *pfVar8 = fVar5;
  *(float *)((int)&__DT_SYMTAB[0x1ee].st_name + param_1) = fVar5 + fVar14;
  _ZN11Application7_UpdateEf(param_1,fVar5);
  piVar3 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar9 + 4);
  if (piVar3 == (int *)0x0) {
LAB_003f1cac:
    if (*(char *)((int)&__DT_SYMTAB[0x1f0].st_size + param_1) == '\0') {
      if ((piVar3 != (int *)0x0) && (iVar7 = (**(code **)(*piVar3 + 8))(piVar3,0x17), iVar7 == 0)) {
        _ZN11Application5_DrawEv(param_1);
      }
      _ZN11Application10UpdateGiftEv(param_1);
    }
  }
  else {
    iVar2 = (**(code **)(*piVar3 + 8))(piVar3,2);
    if (iVar2 == 0) {
LAB_003f1c28:
      (**(code **)(*piVar3 + 0x14))(piVar3);
      piVar9 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar9 + 4);
      if (piVar3 == piVar9) goto LAB_003f1cac;
    }
    else {
      iVar2 = _ZN6CLevel8GetLevelEv();
      if (0.0 < *(float *)(iVar2 + 0x150)) {
        *pfVar8 = 50.0;
        piVar10 = *(int **)(iVar7 + DAT_003f209c);
        puVar11 = (undefined4 *)(DAT_003f20a0 + 0x3f1af4);
        *(undefined1 *)(*piVar10 + 0x1c) = 1;
        _ZN15VoxSoundManager13StopAllSoundsEv();
        iVar2 = _ZN6CLevel8GetLevelEv();
        fVar5 = *(float *)(iVar2 + 0x150);
        while (0.0 < fVar5) {
          piVar6 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar9 + 4);
          iVar2 = (**(code **)(*piVar6 + 8))(piVar6,2);
          if (iVar2 == 0) break;
          (**(code **)(*piVar3 + 0x14))(piVar3);
          piVar6 = (int *)*puVar11;
          pcVar12 = *(code **)(*piVar6 + 0x58);
          iVar2 = _ZN11Application11GetInstanceEv();
          (*pcVar12)(piVar6,*(undefined4 *)((int)&__DT_SYMTAB[0x1ee].st_value + iVar2),0);
          iVar2 = _ZN6CLevel8GetLevelEv();
          *(float *)(iVar2 + 0x150) = *(float *)(iVar2 + 0x150) - *pfVar8;
          iVar2 = _ZN6CLevel8GetLevelEv();
          fVar5 = *(float *)(iVar2 + 0x150);
        }
        _ZN10CCameraMgr6UpdateEf(**(undefined4 **)(iVar7 + DAT_003f20a4),0);
        *(undefined1 *)(*piVar10 + 0x1c) = 0;
        _ZN11gxGameState13ResetControlsEv(piVar3);
        _ZN12gxStateStack10ResetTouchEv(*piVar9 + 4);
        return;
      }
      iVar2 = _ZN6CLevel8GetLevelEv();
      if (*(char *)(iVar2 + 0x14c) == '\0') goto LAB_003f1c28;
      *pfVar8 = 50.0;
      piVar10 = *(int **)(iVar7 + DAT_003f209c);
      iVar13 = *piVar10;
      iVar2 = _ZN6CLevel8GetLevelEv();
      *(undefined1 *)(iVar13 + 0x1c) = *(undefined1 *)(iVar2 + 0x14c);
      iVar2 = _ZN17CLuaScriptManager13SkipCinematicEv(**(undefined4 **)(iVar7 + DAT_003f20b4));
      if (iVar2 != 0) {
        puVar11 = *(undefined4 **)(iVar7 + DAT_003f20a4);
        _ZN10CCameraMgr16ResetCameraShakeEv(*puVar11);
        _ZN10CCameraMgr6UpdateEf(*puVar11,0);
        iVar7 = _ZN6CLevel8GetLevelEv();
        iVar2 = *piVar10;
        *(undefined1 *)(iVar7 + 0x14c) = 0;
        iVar7 = _ZN6CLevel8GetLevelEv();
        *(undefined1 *)(iVar2 + 0x1c) = *(undefined1 *)(iVar7 + 0x14c);
        _ZN11gxGameState13ResetControlsEv(piVar3);
        _ZN12gxStateStack10ResetTouchEv(*piVar9 + 4);
        return;
      }
    }
    *(undefined1 *)((int)&__DT_SYMTAB[0x1f0].st_size + param_1) = 1;
  }
  return;
}


