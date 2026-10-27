# SESSION 63 — T6: memory & GPU status

- No real-GPU gpucheck block was supplied by the user this session
  (city_bisect2.html ?gpucheck=1 output still pending).
- Standing verdict unchanged: the memory profile on this machine is
  **environment-dominated** (swiftshader/llvmpipe GL copies dominate the peak; the
  s55 breakdown: steady ~206 MB JS-side, native residual ~348 MB of which ~261 MB is
  swiftshader expanded-RGBA copies), so any further tuning here would optimize the
  wrong machine. Recorded as **environment-dominated, pending real GPU**; no time
  spent this session per the brief.
- The s53/s54/s55 levers (?texfree, ?poolchunk, lrumb16) remain in the tree,
  default-off, with their measured receipts in the session notes.
