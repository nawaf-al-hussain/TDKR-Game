# SESSION 64 — T6: memory & GPU status

- No real-GPU gpucheck block was supplied this session (city_bisect2.html
  ?gpucheck=1 output still pending from the user).
- Standing verdict unchanged: **environment-dominated, pending real GPU**. The s55
  breakdown (steady ~206 MB JS-side; native residual ~348 MB of which ~261 MB is
  swiftshader expanded-RGBA copies) is the model of record until a real-GPU run
  arrives. No time spent per the brief.
- The s53/s54/s55 levers (?texfree, ?poolchunk, lrumb16) remain in the tree,
  default-off, with measured receipts in the session notes.
