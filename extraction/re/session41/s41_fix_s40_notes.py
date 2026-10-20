#!/usr/bin/env python3
"""s41 T1: correct the s40 modifier-table note (engine table IS the standard ETC1 table)."""
import io, sys

P = '/tmp/my-project/work/TDKR-Game/extraction/re/session40/s40_NOTES.md'
OLD = """   MODIFIER TABLES = the ENGINE's 8 tables (32 entries @0xb88710); tables 5-7
   DIFFER from the ETC2-spec punchthrough numbers: {24,80},{33,106},{47,183}
   (not 74/109/159) - using spec numbers breaks 521/647 textures."""
OLD = OLD.replace(' - ', ' \u2014 ')  # the file uses an em dash
NEW = """   MODIFIER TABLES = the ENGINE's 8 tables (32 entries @0xb88710) = the
   STANDARD ETC1 intensity modifier tables [CORRECTED s41 T1: rows 5-7 are
   {24,80},{33,106},{47,183} exactly as in the ETC1 spec; the earlier claim
   that they "DIFFER from the ETC2-spec punchthrough numbers" was WRONG -
   74/109/159 was a misreading, and using it broke 521/647 textures
   precisely because the engine/files use the standard table]."""
NEW = NEW.replace(' - ', ' \u2014 ')

raw = open(P, 'rb').read().decode('utf-8')
n = raw.count(OLD)
assert n == 1, f'expected exactly 1 occurrence, found {n}'
out = raw.replace(OLD, NEW)
open(P, 'wb').write(out.encode('utf-8'))
chk = open(P, 'rb').read().decode('utf-8')
assert NEW in chk and OLD not in chk
print('s40_NOTES.md corrected: standard-ETC1-table note in place, byte-verified')
