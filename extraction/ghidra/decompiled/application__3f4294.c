// _ZN11Application13DrawRectangleEN6glitch5video6SColorERKNS0_4core4rectIiEE @ 003f4294

void _ZN11Application13DrawRectangleEN6glitch5video6SColorERKNS0_4core4rectIiEE
               (undefined4 param_1,undefined4 param_2,undefined4 *param_3)

{
  int iVar1;
  int iVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  undefined4 *puVar7;
  undefined4 uVar8;
  uint in_fpscr;
  uint uVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  undefined4 local_58;
  undefined1 auStack_54 [4];
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  iVar1 = DAT_003f4400;
  local_58 = 0;
  uVar8 = *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
  local_50 = param_2;
  local_4c = param_2;
  local_48 = param_2;
  local_44 = param_2;
  _ZN6glitch5video9C2DDriver12set2DTextureEPNS0_12IVideoDriverERKN5boost13intrusive_ptrINS0_8ITextureEEEb
            (auStack_54,uVar8,&local_58,0);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(auStack_54);
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_58);
  puVar7 = *(undefined4 **)(iVar1 + 0x3f4308);
  fVar3 = (float)_ZN14GameEngineBase15GetScreenScaleWEv(*puVar7);
  uVar9 = in_fpscr & 0xfffffff | (uint)(fVar3 == 1.0) << 0x1e;
  if (SUB41(uVar9 >> 0x1e,0)) {
    fVar3 = (float)_ZN14GameEngineBase15GetScreenScaleHEv(*puVar7);
    uVar9 = uVar9 & 0xfffffff | (uint)(fVar3 == 1.0) << 0x1e;
    if (SUB41(uVar9 >> 0x1e,0)) {
      _ZN6glitch5video9C2DDriver15draw2DRectangleEPNS0_12IVideoDriverERKNS_4core4rectIiEES8_PKNS0_6SColorEPS7_
                (uVar8,param_3,param_3,&local_50,0);
      return;
    }
  }
  fVar11 = (float)VectorSignedToFloat(*param_3,(byte)(uVar9 >> 0x16) & 3);
  fVar3 = (float)_ZN14GameEngineBase15GetScreenScaleWEv(*puVar7);
  fVar12 = (float)VectorSignedToFloat(param_3[1],(byte)(uVar9 >> 0x16) & 3);
  fVar4 = (float)_ZN14GameEngineBase15GetScreenScaleHEv(*puVar7);
  fVar10 = (float)VectorSignedToFloat(param_3[2],(byte)(uVar9 >> 0x16) & 3);
  fVar5 = (float)_ZN14GameEngineBase15GetScreenScaleWEv(*puVar7);
  fVar13 = (float)VectorSignedToFloat(param_3[3],(byte)(uVar9 >> 0x16) & 3);
  fVar6 = (float)_ZN14GameEngineBase15GetScreenScaleHEv(*puVar7);
  local_40 = (int)(fVar3 * fVar11);
  local_34 = (int)(fVar6 * fVar13);
  local_3c = (int)(fVar4 * fVar12);
  local_38 = (int)(fVar5 * fVar10);
  _ZN6glitch5video9C2DDriver15draw2DRectangleEPNS0_12IVideoDriverERKNS_4core4rectIiEES8_PKNS0_6SColorEPS7_
            (uVar8,&local_40,param_3,&local_50,0);
  return;
}


