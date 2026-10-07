// _ZN19CAnimationComponent8SaveLoadEP13CMemoryStream @ 003a43d4

void _ZN19CAnimationComponent8SaveLoadEP13CMemoryStream(int *param_1,int *param_2)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  float fVar4;
  undefined1 uVar5;
  undefined4 *puVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  int *piVar10;
  int *piVar11;
  code *pcVar12;
  int local_50;
  undefined1 local_4c;
  float local_48;
  undefined1 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  int *local_34;
  
  if (*(char *)(param_1[0x8b] + 0x24) != '\0') {
    iVar7 = param_2[3];
    iVar9 = *param_2;
    *(bool *)((int)param_1 + 0xd) = *(char *)(iVar9 + iVar7) != '\0';
    param_2[3] = iVar7 + 1;
    param_1[0x5d] = (int)*(char *)(iVar9 + iVar7 + 1) << 0x18;
    param_2[3] = iVar7 + 2;
    param_1[0x5d] = param_1[0x5d] | (uint)*(byte *)(iVar9 + iVar7 + 2) << 0x10;
    param_2[3] = iVar7 + 3;
    param_1[0x5d] = param_1[0x5d] | (uint)*(byte *)(iVar9 + iVar7 + 3) << 8;
    param_2[3] = iVar7 + 4;
    local_40 = 0;
    local_3c = 0;
    local_38 = 0;
    param_1[0x5d] = param_1[0x5d] | (uint)*(byte *)(iVar9 + iVar7 + 4);
    local_34 = (int *)0x0;
    param_2[3] = iVar7 + 5;
    cVar3 = *(char *)(iVar9 + iVar7 + 5);
    param_2[3] = iVar7 + 6;
    bVar1 = *(byte *)(iVar9 + iVar7 + 6);
    param_2[3] = iVar7 + 7;
    bVar2 = *(byte *)(iVar9 + iVar7 + 7);
    param_2[3] = iVar7 + 8;
    uVar8 = (int)cVar3 << 0x18 | (uint)bVar1 << 0x10 | (uint)bVar2 << 8 |
            (uint)*(byte *)(iVar9 + iVar7 + 8);
    param_2[3] = iVar7 + 9;
    _ZN13CMemoryStream4ReadERf(param_2,&local_50);
    iVar7 = param_2[3];
    cVar3 = *(char *)(*param_2 + iVar7);
    param_2[3] = iVar7 + 1;
    local_4c = cVar3 != '\0';
    cVar3 = *(char *)(*param_2 + iVar7 + 1);
    param_2[3] = iVar7 + 2;
    local_44 = cVar3 != '\0';
    _ZN13CMemoryStream4ReadERf(param_2,&local_48);
    param_1[0xf] = -1;
    _ZN19CAnimationComponent13PlayAnimationEi(param_1,uVar8);
    uVar5 = local_4c;
    param_1[0x15] = (int)local_48;
    param_1[0x13] = local_50;
    *(undefined1 *)(param_1 + 0x14) = local_4c;
    param_1[0xf] = uVar8;
    *(undefined1 *)(param_1 + 0x16) = local_44;
    if (param_1[0xb] == 0) {
      _ZN19CAnimationComponent24SetCurrentAnimationSpeedEif(param_1,0);
      iVar7 = param_1[0xb];
      fVar4 = local_48;
    }
    else {
      puVar6 = (undefined4 *)(**(code **)(*(int *)param_1[0x1a] + 0x44))();
      piVar10 = (int *)*puVar6;
      if (piVar10 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                  ((int)piVar10 + *(int *)(*piVar10 + -0xc) + 4);
      }
      (**(code **)(*piVar10 + 0x44))(piVar10,uVar5);
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar10 + *(int *)(*piVar10 + -0xc));
      if (param_1[8] != 0) {
        puVar6 = (undefined4 *)(**(code **)(*(int *)param_1[9] + 0x44))();
        (**(code **)(*(int *)*puVar6 + 0x44))((int *)*puVar6,uVar5);
      }
      _ZN19CAnimationComponent24SetCurrentAnimationSpeedEif(param_1,0,local_50);
      iVar7 = param_1[0xb];
      fVar4 = local_48;
    }
    if (iVar7 != 0) {
      param_1[0x15] = (int)fVar4;
      puVar6 = (undefined4 *)(**(code **)(*(int *)param_1[0x1a] + 0x44))();
      piVar10 = (int *)*puVar6;
      if (piVar10 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                  ((int)piVar10 + *(int *)(*piVar10 + -0xc) + 4);
      }
      pcVar12 = *(code **)(*piVar10 + 0x10);
      puVar6 = (undefined4 *)(**(code **)(*(int *)param_1[0x1a] + 0x44))();
      piVar11 = (int *)*puVar6;
      if (piVar11 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
                  ((int)piVar11 + *(int *)(*piVar11 + -0xc) + 4);
      }
      (*pcVar12)(piVar10,fVar4 + (float)piVar11[4]);
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar11 + *(int *)(*piVar11 + -0xc));
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar10 + *(int *)(*piVar10 + -0xc));
      if (param_1[8] != 0) {
        puVar6 = (undefined4 *)(**(code **)(*(int *)param_1[9] + 0x44))();
        piVar11 = (int *)*puVar6;
        pcVar12 = *(code **)(*piVar11 + 0x10);
        piVar10 = (int *)(**(code **)(*(int *)param_1[9] + 0x44))((int *)param_1[9]);
        (*pcVar12)(piVar11,fVar4 + *(float *)(*piVar10 + 0x10));
      }
    }
    if (-1 < (int)uVar8) {
      (**(code **)(*param_1 + 0x1c))(param_1,0);
    }
    if (local_34 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_34 + *(int *)(*local_34 + -0xc));
    }
  }
  return;
}


