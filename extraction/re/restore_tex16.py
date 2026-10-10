#!/usr/bin/env python3
"""Restore the two texture .gla containers into raw/<arch>/ chunk files."""
import sys
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
import restore_raw as R  # noqa: E402

OBB = R.OBB  # already ends with /com.gameloft.android.AMAZ.GloftKRAS/files
for arch, sub in (("l_gothamcity_tex", "textures"), ("commons_tex", "textures")):
    gla = f"{OBB}/{sub}/{arch}.gla"
    n, tot = R.pull_chunks(gla, f"{R.RAW}/{arch}")
    print(f"{arch}: pulled {n}/{tot} chunks")
