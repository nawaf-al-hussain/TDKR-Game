// _ZN13CAIController11SendAIEventEiP11CGameObjectS1_iP11ScriptParam @ 0018ca84

void _ZN13CAIController11SendAIEventEiP11CGameObjectS1_iP11ScriptParam
               (undefined4 param_1,undefined4 param_2,int param_3,int *param_4,int *param_5,
               int param_6)

{
  int *piVar1;
  int iVar2;
  undefined4 uVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  int local_54 [3];
  undefined4 local_48;
  int *local_44;
  undefined4 local_40;
  int *local_3c;
  undefined1 local_38;
  undefined4 local_34;
  undefined1 local_30;
  undefined4 local_2c;
  undefined1 local_28;
  undefined4 local_24;
  undefined1 local_20;
  undefined4 local_1c;
  
  if (param_3 == 0) {
    local_3c = param_5;
    if (param_4[0x2f] == 0) {
      local_40 = 0;
    }
    else {
      local_40 = *(undefined4 *)(param_4[0x2f] + 0x27c);
    }
    local_54[0] = DAT_0018cb94 + 0x18cb0c;
    local_48 = 0;
    local_38 = 0;
    piVar5 = param_4;
    if (0 < (int)param_5) {
      piVar5 = (int *)0x0;
    }
    local_34 = 0;
    piVar6 = param_5;
    if (0 < (int)param_5) {
      piVar6 = (int *)((int)param_5 << 3);
    }
    local_30 = 0;
    local_2c = 0;
    local_28 = 0;
    local_24 = 0;
    local_20 = 0;
    local_1c = 0;
    piVar4 = (int *)0x0;
    if (0 < (int)param_5) {
      piVar4 = local_54;
    }
    local_54[1] = 0x76;
    if (0 < (int)param_5) {
      do {
        piVar1 = (int *)(param_6 + (int)piVar5);
        piVar5 = piVar5 + 2;
        iVar2 = piVar1[1];
        piVar4[7] = *piVar1;
        piVar4[8] = iVar2;
        piVar4 = piVar4 + 2;
      } while (piVar5 != piVar6);
    }
    local_54[2] = param_2;
    local_44 = param_4;
    _ZN16EventManagerBase9raiseSyncERK6IEvent(**(undefined4 **)(DAT_0018cb98 + 0x18cb8c),local_54);
  }
  else {
    if (param_4 == (int *)0x0) {
      uVar3 = 0xffffffff;
    }
    else {
      uVar3 = (**(code **)(*param_4 + 0x14))(param_4);
    }
    if (*(int *)(param_3 + 0xbc) != 0) {
      _ZN15CNpcAIComponent11RunAIScriptEiiiP11ScriptParam
                (*(int *)(param_3 + 0xbc),param_2,uVar3,param_5,param_6);
    }
  }
  return;
}

