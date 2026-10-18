#!/usr/bin/env python3
"""S35 T1a2: dump 28-B chain records @0xcd00 raw fields + clip list,
reconcile with engine reads ([0]=tickStart? [4]=tickEnd? [8]=flag?)."""
import struct, json

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

print('=== first 20 chain records @0xcd00 (stride 0x1c) ===')
print(f'{"i":>3} {"f0":>8} {"f4":>8} {"f8":>6} {"fC":>9} {"f10":>9} {"f14":>6} {"f18":>8}')
for i in range(20):
    o = 0xcd00 + i * 0x1c
    f = [u32a(o + 4 * k) for k in range(7)]
    print(f'{i:3d} {f[0]:8d} {f[1]:8d} {f[2]:6d} {f[3]:9d} {f[4]:9d} {f[5]:6d} {f[6]:8d}')

# field stats over all records
cnt = 0
f0s, f4s, f8s, ptrs, dists = [], [], [], [], []
while True:
    o = 0xcd00 + cnt * 0x1c
    f = [u32a(o + 4 * k) for k in range(7)]
    if f[3] == 0 or f[3] >= N: break
    f0s.append(f[0]); f4s.append(f[1]); f8s.append(f[2]); ptrs.append(f[3]); dists.append(f[4])
    cnt += 1
print(f'\ntotal records: {cnt}')
print(f'f0 range {min(f0s)}..{max(f0s)}  monotone-asc: {all(f0s[i]<=f0s[i+1] for i in range(len(f0s)-1))}')
print(f'f4 range {min(f4s)}..{max(f4s)}  zero count: {sum(1 for v in f4s if v==0)}/{cnt}')
print(f'f8 range {min(f8s)}..{max(f8s)}  zero count: {sum(1 for v in f8s if v==0)}/{cnt}')
print(f'ptr+dist==next.ptr: {all(ptrs[i]+dists[i]==ptrs[i+1] for i in range(cnt-1))}')

# clip list @0x11580
def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: return None

clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', ad, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000: break
    clips.append((nm, ts, te))
print(f'\nclip list: {len(clips)} entries')
for i in range(12):
    print(f'  clip {i}: {clips[i][0]:36} [{clips[i][1]}..{clips[i][2]}] dur={clips[i][2]-clips[i][1]}')
print('  ...')
for i in range(len(clips)-3, len(clips)):
    print(f'  clip {i}: {clips[i][0]:36} [{clips[i][1]}..{clips[i][2]}] dur={clips[i][2]-clips[i][1]}')

# segments json from r24
segs = json.load(open('/home/z/my-project/scripts/s34_t1_segs.json'))
print(f'\nr24 segs json: {len(segs)} entries')
print('first 17: recTickEnd, ptr, dist vs clip windows:')
for i in range(min(17, len(segs), len(clips))):
    s = segs[i]
    print(f'  seg{i}: tickEnd={s["tickEnd"]} ptr=0x{s["ptr"]:x} dist={s["dist"]} | clip {clips[i][0]} [{clips[i][1]}..{clips[i][2]}]')
