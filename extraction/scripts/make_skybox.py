#!/usr/bin/env python3
"""Build an equirectangular night sky for the viewer from the game's own
GC_Skybox_02 (storm clouds + amber horizon glow).

The source is a dome texture: clouds top, orange glow bottom. An equirect
needs: zenith->mid = clouds, horizon band = amber glow, below = dark ground
fade. We resample the source accordingly (1024x512 output)."""
from PIL import Image
import numpy as np

SRC = '/home/z/my-project/download/TDKR_assets/textures_png/commons_tex/GC_Skybox_02.png'
OUT = '/home/z/my-project/work/site/skybox.jpg'

src = Image.open(SRC).convert('RGB')
a = np.asarray(src, np.float32) / 255.0
H, W, _ = a.shape  # 1024x1024

out_h, out_w = 512, 1024
canvas = np.zeros((out_h, out_w, 3), np.float32)

# source rows: clouds band = 0..0.72H, glow band = 0.72H..H
clouds = a[0:int(0.72 * H)]
glow = a[int(0.78 * H):]          # mostly the orange gradient

# --- equirect row mapping (DARK storm sky, glow at horizon) ---
# rows 0..0.38      : near-black zenith
# rows 0.38..0.62   : dark storm clouds
# rows 0.62..0.74   : lower clouds, slightly lit from below
# rows 0.74..0.80   : horizon glow (amber, peak at ~0.78)
# rows 0.80..0.86   : glow fades below horizon
# rows 0.86..1.0    : near-black nadir (city ground hides it)

r_dark_end = int(0.38 * out_h)
r_cloud_end = int(0.62 * out_h)
r_low_end = int(0.74 * out_h)
r_glow_peak = int(0.79 * out_h)
r_glow_end = int(0.86 * out_h)

# 0..38%: zenith — barely-visible clouds, very dark
band = np.asarray(Image.fromarray((clouds * 255).astype(np.uint8)).resize(
    (out_w, r_dark_end), Image.LANCZOS), np.float32) / 255.0
zen_dark = np.linspace(0.10, 0.22, r_dark_end)[:, None, None]
canvas[:r_dark_end] = band * zen_dark

# 38%->62%: storm clouds, dark
band2 = np.asarray(Image.fromarray((clouds[int(0.15 * clouds.shape[0]):] * 255).astype(np.uint8)).resize(
    (out_w, r_cloud_end - r_dark_end), Image.LANCZOS), np.float32) / 255.0
cloud_ramp = np.linspace(0.22, 0.48, r_cloud_end - r_dark_end)[:, None, None]
canvas[r_dark_end:r_cloud_end] = band2 * cloud_ramp

# 62%->74%: lower clouds with warm underlight creeping in
low = np.asarray(Image.fromarray((clouds[int(0.45 * clouds.shape[0]):] * 255).astype(np.uint8)).resize(
    (out_w, r_low_end - r_cloud_end), Image.LANCZOS), np.float32) / 255.0
canvas[r_cloud_end:r_low_end] = low * np.linspace(0.55, 0.8, r_low_end - r_cloud_end)[:, None, None]

# 74%->79%: clouds dissolving into the glow
mixzone = np.asarray(Image.fromarray((glow[:glow.shape[0] // 2] * 255).astype(np.uint8)).resize(
    (out_w, r_glow_peak - r_low_end), Image.LANCZOS), np.float32) / 255.0
canvas[r_low_end:r_glow_peak] = mixzone * 0.9

# 79%->86%: glow band fading downward (below horizon)
glowzone = np.asarray(Image.fromarray((glow[glow.shape[0] // 2:] * 255).astype(np.uint8)).resize(
    (out_w, r_glow_end - r_glow_peak), Image.LANCZOS), np.float32) / 255.0
canvas[r_glow_peak:r_glow_end] = glowzone * np.linspace(1.0, 0.22, r_glow_end - r_glow_peak)[:, None, None]

# 86%->100%: nadir — near black
canvas[r_glow_end:] = canvas[r_glow_end - 1:r_glow_end] * np.linspace(0.5, 0.06, out_h - r_glow_end)[:, None, None]

# subtle seam-safe horizontal wrap blur on cloud bands is unnecessary (LANCZOS
# edges already align since source is horizontal-tileable-ish); add tiny dither
# to avoid banding in the glow
dither = (np.random.rand(out_h, out_w, 1).astype(np.float32) - 0.5) / 255.0
canvas = np.clip(canvas + dither, 0, 1)

Image.fromarray((canvas * 255).astype(np.uint8)).save(OUT, 'JPEG', quality=88, optimize=True)
print('wrote', OUT)
