// _ZN13CAIController23RemoveDestroyableObjectEP11CGameObject @ 0018e300

void _ZN13CAIController23RemoveDestroyableObjectEP11CGameObject(int param_1,int param_2)

{
  int *piVar1;
  int *piVar2;
  int *__dest;
  int iVar3;
  int iVar4;
  int *piVar5;
  int *piVar6;
  int *piVar7;
  
  piVar6 = *(int **)(param_1 + 0x160);
  piVar1 = *(int **)(param_1 + 0x15c);
  iVar4 = (int)piVar6 - (int)piVar1;
  iVar3 = iVar4 >> 4;
  if (0 < iVar3) {
    piVar2 = piVar1;
    if (*piVar1 != param_2) {
      if (piVar1[1] == param_2) {
        piVar2 = piVar1 + 1;
      }
      else if (piVar1[2] == param_2) {
        piVar2 = piVar1 + 2;
      }
      else {
        piVar5 = piVar1;
        if (piVar1[3] != param_2) {
          do {
            iVar3 = iVar3 + -1;
            piVar1 = piVar5 + 4;
            __dest = piVar5 + 5;
            if (iVar3 == 0) {
              iVar4 = (int)piVar6 - (int)piVar1;
              goto LAB_0018e3bc;
            }
            piVar7 = piVar5 + 7;
            piVar2 = piVar1;
            if (piVar5[4] == param_2) goto LAB_0018e3d8;
            if (piVar5[5] == param_2) {
              if (piVar6 == __dest) {
                return;
              }
              goto LAB_0018e3e0;
            }
            if (piVar5[6] == param_2) {
              __dest = piVar5 + 6;
              if (piVar6 == piVar5 + 6) {
                return;
              }
              goto LAB_0018e3e0;
            }
            piVar2 = piVar5 + 7;
            piVar5 = piVar1;
          } while (*piVar2 != param_2);
          __dest = piVar7;
          if (piVar6 == piVar7) {
            return;
          }
          goto LAB_0018e3e0;
        }
        piVar2 = piVar1 + 3;
      }
    }
    goto LAB_0018e3d8;
  }
LAB_0018e3bc:
  iVar4 = iVar4 >> 2;
  if (iVar4 == 2) {
LAB_0018e42c:
    piVar2 = piVar1;
    if (*piVar1 != param_2) {
      piVar1 = piVar1 + 1;
LAB_0018e43c:
      if (*piVar1 != param_2) {
        piVar1 = piVar6;
      }
      __dest = piVar1;
      if (piVar6 == piVar1) {
        return;
      }
      goto LAB_0018e3e0;
    }
  }
  else if (iVar4 == 3) {
    piVar2 = piVar1;
    if (*piVar1 != param_2) {
      piVar1 = piVar1 + 1;
      goto LAB_0018e42c;
    }
  }
  else {
    piVar2 = piVar6;
    if (iVar4 == 1) goto LAB_0018e43c;
  }
LAB_0018e3d8:
  __dest = piVar2;
  if (piVar6 == piVar2) {
    return;
  }
LAB_0018e3e0:
  piVar1 = __dest + 1;
  if ((piVar6 != piVar1) && (iVar3 = (int)piVar6 - (int)piVar1 >> 2, iVar3 != 0)) {
    memmove(__dest,piVar1,iVar3 << 2);
    *(int *)(param_1 + 0x160) = *(int *)(param_1 + 0x160) + -4;
    return;
  }
  *(int **)(param_1 + 0x160) = piVar6 + -1;
  return;
}

