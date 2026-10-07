// _ZNK11Application20getIgpGLLiveLanguageEv @ 003eb2f4

int _ZNK11Application20getIgpGLLiveLanguageEv(int param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1);
  switch(iVar1) {
  case 0:
    break;
  case 1:
    break;
  case 2:
    break;
  case 3:
    return 4;
  case 4:
    goto LAB_003eb340;
  case 5:
    return 8;
  case 6:
    goto LAB_003eb340;
  case 7:
    goto LAB_003eb340;
  case 8:
LAB_003eb340:
    return iVar1 + -1;
  default:
    iVar1 = 0;
  }
  return iVar1;
}


