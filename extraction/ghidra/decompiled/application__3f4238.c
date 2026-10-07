// _ZN11Application9ResetDrawEv @ 003f4238

void _ZN11Application9ResetDrawEv(void)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 local_48 [5];
  undefined4 local_34;
  undefined4 local_20;
  undefined4 local_c;
  
  iVar1 = _ZN11Application11GetInstanceEv();
  uVar2 = *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  memset(local_48,0,0x40);
  local_48[0] = 0x3f800000;
  local_34 = 0x3f800000;
  local_20 = 0x3f800000;
  local_c = 0x3f800000;
  _ZN6glitch5video12IVideoDriver12setTransformENS0_22E_TRANSFORMATION_STATEERKNS_4core8CMatrix4IfEEj
            (uVar2,2,local_48,0);
  return;
}


