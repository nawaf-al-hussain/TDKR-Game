// mspace_footprint @ 000ca51c

undefined4 mspace_footprint(int param_1)

{
  if (*(int *)(param_1 + 0x24) == *(int *)(DAT_000ca540 + 0xca530)) {
    return *(undefined4 *)(param_1 + 0x1b0);
  }
                    /* WARNING: Subroutine does not return */
  abort();
}

