// mspace_max_footprint @ 000ca544

undefined4 mspace_max_footprint(int param_1)

{
  if (*(int *)(param_1 + 0x24) == *(int *)(DAT_000ca568 + 0xca558)) {
    return *(undefined4 *)(param_1 + 0x1b4);
  }
                    /* WARNING: Subroutine does not return */
  abort();
}

