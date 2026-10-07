// _ZNK6glitch5video13CGenericBaker4bakeERKNS0_20SBatchBakerInputDescERKNS0_21SBatchBakerOutputDescEPKNS0_12IVideoDriverE @ 007bd170

void _ZNK6glitch5video13CGenericBaker4bakeERKNS0_20SBatchBakerInputDescERKNS0_21SBatchBakerOutputDescEPKNS0_12IVideoDriverE
               (undefined4 param_1,int *param_2,int *param_3,undefined4 param_4)

{
  int local_54;
  int local_50;
  int local_4c;
  int local_48;
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  undefined1 local_2c;
  undefined1 local_2b;
  
  if ((param_2[1] != 0) && (param_3[1] != 0)) {
    _ZN6glitch4core23overridePrimitiveStreamERKNS_5video16CPrimitiveStreamEjjRS2_ji
              (param_2[1],param_2[7],param_2[8],param_3[1],param_3[6],param_3[4] - param_2[5]);
  }
  local_3c = *param_2;
  if ((local_3c != 0) && (local_50 = *param_3, local_50 != 0)) {
    local_38 = param_2[5];
    local_40 = param_2[4];
    local_2c = (undefined1)param_2[3];
    local_34 = param_2[6];
    local_54 = param_3[3];
    local_4c = param_3[4];
    local_30 = param_2[2];
    local_48 = param_3[5];
    local_2b = (undefined1)param_2[9];
    local_44 = param_3[8];
    _ZN6glitch4core21overrideVertexStreamsERKNS0_31SOverrideVertexStreamsInputDescERKNS0_32SOverrideVertexStreamsOutputDescEPKNS_5video12IVideoDriverEbbb
              (&local_40,&local_54,param_4,1,1,1);
  }
  return;
}


