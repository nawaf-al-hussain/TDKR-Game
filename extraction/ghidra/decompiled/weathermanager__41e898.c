// _ZN15CWeatherManager4SaveEP13CMemoryStream @ 0041e898

undefined4
_ZN15CWeatherManager4SaveEP13CMemoryStream
          (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  
  _ZN13CMemoryStream5WriteEb(param_2,*(undefined1 *)(param_1 + 4),param_3,param_4,param_4);
  _ZN13CMemoryStream5WriteEb(param_2,*(undefined1 *)(param_1 + 0x28));
  if (*(char *)(param_1 + 4) == '\0') {
    uVar1 = 0xffffffff;
  }
  else {
    uVar1 = *(undefined4 *)(param_1 + 8);
  }
  _ZN13CMemoryStream5WriteEi(param_2,uVar1);
  return 1;
}

