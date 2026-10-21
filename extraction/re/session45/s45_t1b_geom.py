#!/usr/bin/env python3
"""s45 T1b step 2: geometric correspondence with proper stride inference + frame fit."""
import struct, io, zipfile, json
import numpy as np
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
from s45_t1b_parse import allsegs, pairs, ld, seg_hdr  # reuses parsed state
