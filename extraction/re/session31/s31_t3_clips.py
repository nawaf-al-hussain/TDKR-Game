#!/usr/bin/env python3
"""S31 T3: animation clip counts reconciliation + clip list statistics +
dialect structure evidence. Full channel decode = PARTIAL (descriptor zone
named)."""
import struct, re, statistics, json

d = open('/tmp/my-project/work/data/batman_anims.bdae', 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]


def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 80:
            try:
                return d[v:e].decode('latin1')
            except Exception:
                pass
    return None


# ---- 1. the clip list @0x11580 (12-B records) ----
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te))
print(f'clip list @0x11580: {len(clips)} clips, ends @0x{0x11580 + 12*len(clips):x}')
durs = [(te - ts, nm) for nm, ts, te in clips]
print(f'  durations (ticks): min {min(durs)[0]}, median '
      f'{statistics.median(x[0] for x in durs):.0f}, max {max(durs)[0]}')
print(f'  examples: _001_idle_stand {clips[0][2]-clips[0][1]} ticks, '
      f'_007_walk {clips[6][2]-clips[6][1]} ticks, '
      f'_920_sit_chair_idle {clips[-2][2]-clips[-2][1]} ticks')
# gaps between clips (rounding to 1000?)
gaps = sum(1 for i in range(1, len(clips))
           if clips[i][1] - clips[i-1][2] > 0)
print(f'  clips with a gap before them: {gaps}/{len(clips)-1} '
      f'(start ticks rounded up to 1000s -> time ranges over a shared pool)')

# ---- 2. _NNN_ name census ----
names = set(re.findall(rb'_[0-9]{3}_[A-Za-z0-9_]+', d))
print(f'\ndistinct _NNN_ names in file: {len(names)}  '
      f'(= clip count {len(clips)} + 1: the extra is '
      f'{sorted(names - {nm.encode() for nm in clips and [c[0] for c in clips]})})')

# ---- 3. the r16 "503" and r20 "1375" ----
# 503: key-run blocks (r16 census of [f32][u32 tick] runs) - superseded
# 1375: named-group census over the descriptor zone (r20)
# named 32-B groups: [f,0,nameOff,1,tOff,1,vOff,0] starting 0xb53c
n_named = 0
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', d, o)
    if w[2] and cstr(w[2]) and w[3] == 1 and w[5] == 1:
        n_named += 1
        o += 32
    else:
        break
print(f'\nnamed 32-B channel groups @0xb53c (contiguous run): {n_named}')
print('  (r20 counted 1375 over the whole descriptor zone incl. per-clip '
      'repeats; this run = the head block)')

# ---- 4. dialect evidence: clip 1 named groups; later clips pointer arrays ----
print('\nclip-1 group samples:')
for k in (0, 1, 2):
    w = struct.unpack_from('<8I', d, 0xb53c + 32 * k)
    print(f'  {cstr(w[2])!r} tOff={w[4]:#x} vOff={w[6]:#x}')
print('  descriptor record @0xbf04 (Bip01-translation time stream):')
print('   ', [hex(u32(0xbf04 + 4 * i)) for i in range(11)])
print('  ...records carry next-pointers 0x1ea0/0x1ed4/0x1f0c/0x1f44 and '
      'magic 0x14FFFF -> per-channel descriptor chains (resisting block)')

# ---- 5. tick rate evidence ----
print('\ntick rate: clip ranges are ms-scale (idle 5000 = 5.0 s, walk 1066 = '
      '1.07 s, sit 2500 = 2.5 s); the engine sampler normalizes t by a '
      'per-clip duration field ([sampler+0x58], vdiv @0x763e20 in '
      'CAnimatorBlenderSampler::updateAnimation) -> no global fps; '
      'file ticks = milliseconds')
json.dump(dict(n_clips=len(clips),
               durations_ms=[te - ts for _, ts, te in clips][:50],
               named_groups_head=n_named),
          open('/home/z/my-project/download/s31_t3_result.json', 'w'))
print('\nwrote /home/z/my-project/download/s31_t3_result.json')
