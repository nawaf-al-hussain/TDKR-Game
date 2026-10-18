#!/usr/bin/env python3
"""S34 T1: walk segment records (stride 0x1c from 0xcd00), enumerate tables,
match clip order (clip k = segment k), find _008_run's table + data extents."""
import struct, json
AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

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

# walk records from 0xcd00
segs = []
o = 0xcd00
while o + 0x1c <= N:
    te_, p1, p2, ptr, dist, p3, te2 = [u32a(o + 4*i) for i in range(7)]
    if te_ != te2 or p1 or p2 or p3 or ptr == 0 or dist == 0 or dist > 0x100000:
        break
    if not (0x1000 < ptr < N and ptr < 0x2900000):
        break
    segs.append(dict(rec=o, tickEnd=te_, ptr=ptr, dist=dist))
    o += 0x1c
print(f'{len(segs)} segment records walked (clips: {len(clips)})')
for i, s in enumerate(segs[:12]):
    nm = clips[i][0] if i < len(clips) else '?'
    print(f'  seg{i:3d} @0x{s["rec"]:06x} tickEnd={s["tickEnd"]} ptr=0x{s["ptr"]:06x} '
          f'dist=0x{s["dist"]:05x}  clip={nm}')
print('  ...')
for i, s in enumerate(segs[-4:]):
    j = len(segs) - 4 + i
    print(f'  seg{j:3d} @0x{s["rec"]:06x} tickEnd={s["tickEnd"]} ptr=0x{s["ptr"]:06x} '
          f'dist=0x{s["dist"]:05x}  clip={clips[j][0] if j < len(clips) else "?"}')

# chain check
ok = all(segs[i]['ptr'] + segs[i]['dist'] == segs[i+1]['ptr'] for i in range(len(segs)-1))
print(f'\nchain ptr+dist==next.ptr: {ok}')

# find run segment
for i, (nm, ts, te) in enumerate(clips):
    if nm == '_008_run':
        if i < len(segs):
            s = segs[i]
            print(f'\n_008_run = seg{i}: ptr=0x{s["ptr"]:06x} dist=0x{s["dist"]:05x} '
                  f'tickEnd={s["tickEnd"]}')
            # table entries count: read entries until len==0 terminator pattern
            ptr = s['ptr']
            ne = 0
            while ne < 400:
                ln = u32a(ptr + 8*ne + 4)
                if ln == 0: ne += 1; break
                if ln > 0x2000: break
                ne += 1
            print(f'  entries: {ne}, table bytes 0x{ne*8:x}, data starts '
                  f'0x{ptr + ne*8 + 8:06x}, dist ends 0x{ptr + s["dist"]:06x}')
            json.dump(dict(seg_index=i, ptr=ptr, dist=s['dist'], tickEnd=s['tickEnd'],
                           nentries=ne, data=ptr + ne*8 + 8,
                           data_end=ptr + s['dist']),
                      open('/home/z/my-project/scripts/s34_t1_runseg.json', 'w'))
        else:
            print(f'\n_008_run at clip {i} beyond walked segments')
        break
json.dump(segs, open('/home/z/my-project/scripts/s34_t1_segs.json', 'w'))
