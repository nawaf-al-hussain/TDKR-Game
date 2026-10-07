// _ZN13CAIController10GroundSlamEP11CGameObjectffi @ 0018d9b0

void _ZN13CAIController10GroundSlamEP11CGameObjectffi
               (int param_1,int *param_2,float param_3,float param_4,int param_5)

{
  undefined8 uVar1;
  float *pfVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  undefined1 auStack_7c [4];
  undefined1 auStack_78 [4];
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  float local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  int *local_4c;
  
  pfVar2 = (float *)(**(code **)(*param_2 + 0x18))(param_2);
  iVar7 = DAT_0018dbf0 + 0x18da00;
  fVar10 = *pfVar2;
  uVar1 = *(undefined8 *)(pfVar2 + 1);
  iVar5 = *(int *)(param_1 + 0xb8);
  local_58 = 0;
  local_54 = 0;
  local_50 = 0;
  local_60 = 0xffffffff;
  iVar4 = DAT_0018dbf4 + 0x18da3c;
  local_5c = 0;
  local_64 = 2;
  local_68 = param_4;
  local_4c = param_2;
  while (param_1 + 0xb0 != iVar5) {
    piVar6 = *(int **)(iVar5 + 0x10);
    iVar5 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar5);
    if ((((piVar6 != (int *)0x0) && (iVar3 = (**(code **)(*piVar6 + 0x54))(piVar6), iVar3 != 0)) &&
        (iVar3 = _ZN11CGameObject7IsHumanEv(piVar6), iVar3 != 0)) &&
       ((iVar3 = _ZNK11CGameObject6IsDeadEv(piVar6), iVar3 == 0 &&
        (iVar3 = _ZNK11CGameObject13IsInStateTypeEib(piVar6,0x100), iVar3 == 0)))) {
      pfVar2 = (float *)(**(code **)(*piVar6 + 0x18))(piVar6);
      fVar8 = pfVar2[1] - (float)uVar1;
      fVar9 = pfVar2[2] - (float)((ulonglong)uVar1 >> 0x20);
      fVar8 = (*pfVar2 - fVar10) * (*pfVar2 - fVar10) + fVar8 * fVar8 + fVar9 * fVar9;
      if ((fVar8 < param_3 * param_3) &&
         ((param_5 == -1 || (iVar3 = _ZN11CGameObject13GetAIBehaviorEv(piVar6), iVar3 == param_5))))
      {
        local_68 = (1.0 - fVar8 * (1.0 / (param_3 * param_3))) * param_4;
        iVar3 = _ZN11CGameObject11IsLookingAtEP15CGameObjectBasef(piVar6,piVar6 + 0xd,0x43340000);
        if (iVar3 == 0) {
          iVar3 = piVar6[0x2f];
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
                    (auStack_78,iVar7);
          _ZN15CNpcAIComponent13NPCDamageTakeERK7CDamageRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS5_6memory13E_MEMORY_HINTE0EEEEbib
                    (iVar3,&local_68,auStack_78,0,200,1);
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                    (auStack_78);
        }
        else {
          local_74 = 0;
          local_70 = 0;
          local_6c = 0;
          _ZN11CGameObject6LookAtEP15CGameObjectBasefRKN6glitch4core8vector3dIfEEib
                    (piVar6,piVar6 + 0xd,0,&local_74,1,1);
          iVar3 = piVar6[0x2f];
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
                    (auStack_7c,iVar4);
          _ZN15CNpcAIComponent13NPCDamageTakeERK7CDamageRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS5_6memory13E_MEMORY_HINTE0EEEEbib
                    (iVar3,&local_68,auStack_7c,0,200,1);
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                    (auStack_7c);
        }
      }
    }
  }
  return;
}

