#!/usr/bin/env python3
"""Partial-fetch game_config/*.lvc* (and misc small config entries) from the
OBB zip release asset using HTTP Range requests (no 895MB download).
ZIP64-aware central directory parse from the tail of the file."""
import io, json, struct, subprocess, sys, zlib, os

# token comes from the environment (never commit tokens — GitHub push
# protection blocks releases tokens appearing in history)
TOKEN = os.environ.get("GH_TOKEN", "")
API = "https://api.github.com/repos/nawaf-al-hussain/TDKR-Game/releases/assets/617799396"
OUT = "/home/z/my-project/download/TDKR_assets/raw/game_config"
os.makedirs(OUT, exist_ok=True)

HDR = ["Authorization: token " + TOKEN, "Accept: application/octet-stream"]


def fetch(url, rng=None):
    cmd = ["curl", "-sL", "-H", HDR[0], "-H", HDR[1]]
    if rng:
        cmd += ["-r", rng]
    cmd += [url]
    return subprocess.run(cmd, capture_output=True).stdout


# resolve real URL (S3 signed), keep redirects
meta = subprocess.run(["curl", "-sI", "-H", HDR[0], "-H", HDR[1], API],
                      capture_output=True, text=True).stdout
real = None
for line in meta.splitlines():
    if line.lower().startswith("location:"):
        real = line.split(":", 1)[1].strip()
size = None
if real:
    hdr = subprocess.run(["curl", "-sI", real], capture_output=True, text=True).stdout
    for line in hdr.splitlines():
        if line.lower().startswith("content-length:"):
            size = int(line.split(":")[1])
if not size:
    raise SystemExit("cannot determine size")

print("zip size:", size)

# ---- read last 1 MB (EOCD + central dir); explicit range (suffix ranges rejected) ----
tail_len = min(1 << 20, size)
tail = fetch(real or API, f"{size - tail_len}-{size - 1}")
if len(tail) != tail_len:
    tail = fetch(API, f"{size - tail_len}-{size - 1}")
tail_off = size - tail_len
assert tail.rfind(b"PK\x05\x06") >= 0, f"no EOCD in {len(tail)}B tail ({tail[:60]!r})"
eocd = tail.rfind(b"PK\x05\x06")
cd_size, cd_off = struct.unpack_from("<II", tail, eocd + 12)
if cd_off == 0xFFFFFFFF or cd_size == 0xFFFFFFFF:  # zip64
    loc = tail.rfind(b"PK\x06\x07")
    z64 = tail.rfind(b"PK\x06\x06")
    assert z64 >= 0
    cd_size, cd_off = struct.unpack_from("<QQ", tail, z64 + 40)
print(f"central dir @ {cd_off:#x} size {cd_size:#x}")

if cd_off >= tail_off:
    cd = tail[cd_off - tail_off: cd_off - tail_off + cd_size]
else:
    cd = fetch(real, f"{cd_off}-{cd_off + cd_size - 1}")

want = {}
i = 0
entries = []
while i < len(cd) and cd[i:i + 4] == b"PK\x01\x02":
    (sig, vmade, vneed, flags, method, mtime, mdate, crc, csize, usize,
     nlen, elen, clen, disk, iattr, eattr, lho) = struct.unpack_from("<IHHHHHHIIIHHHHHII", cd, i)
    name = cd[i + 46:i + 46 + nlen].decode("utf8", "replace")
    extra = cd[i + 46 + nlen: i + 46 + nlen + elen]
    # zip64 extra
    if csize == 0xFFFFFFFF or usize == 0xFFFFFFFF or lho == 0xFFFFFFFF:
        j = 0
        while j < len(extra):
            eid, esz = struct.unpack_from("<HH", extra, j)
            if eid == 1:
                vals = []
                k = j + 4
                for cur in (usize, csize, lho):
                    if cur == 0xFFFFFFFF:
                        vals.append(struct.unpack_from("<Q", extra, k)[0]); k += 8
                    else:
                        vals.append(cur)
                usize, csize, lho = vals
                break
            j += 4 + esz
    entries.append((name, method, csize, usize, lho))
    i += 46 + nlen + elen + clen

print(f"{len(entries)} entries")
targets = [e for e in entries if "game_config/" in e[0]]
for name, method, csize, usize, lho in targets:
    print(f"  {name}  c={csize} u={usize} @ {lho:#x}")

# ---- fetch chosen entries by range ----
FETCH = [
    "com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla",
]


def fetch_entry(name, method, csize, usize, lho):
    hdr_len = 30 + 0  # probe: fetch first 512B to learn name/extra len
    head = fetch(real or API, f"{lho}-{lho + 511}")
    if head[:4] != b"PK\x03\x04":
        head = fetch(API, f"{lho}-{lho + 511}")
    nlen, elen = struct.unpack_from("<HH", head, 26)
    data_start = lho + 30 + nlen + elen
    print(f"fetching {name}: {csize}B @ {data_start:#x} method={method}")
    blob = fetch(real or API, f"{data_start}-{data_start + csize - 1}")
    if len(blob) != csize:
        blob = fetch(API, f"{data_start}-{data_start + csize - 1}")
    assert len(blob) == csize, f"{len(blob)} != {csize}"
    if method == 0:
        return blob
    return zlib.decompress(blob, -15)


for name, method, csize, usize, lho in entries:
    if name in FETCH:
        outp = os.path.join("/home/z/my-project/download/TDKR_assets/raw",
                            os.path.basename(name))
        data = fetch_entry(name, method, csize, usize, lho)
        open(outp, "wb").write(data)
        print("saved", outp, len(data), "bytes (usize", usize, ")")
