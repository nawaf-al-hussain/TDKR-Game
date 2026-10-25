# s59 T5 — memory: ENVIRONMENT-DOMINATED (no real-GPU gpucheck block supplied this session)

No real-GPU block was pasted in this session's message, so per the task rule no further
memory work was done and no levers were tried. Standing result (s55/s56/s58): fine-harness
median peak ~560-592 MB (swiftshader native copies ~261 MB + zone-build transients), first
image 8.5-9.0 s, steady ~210 MB, empty three.js floor 93 MB; the texfree lever moved
nothing (s58). Targets <500 MB / <8 s remain NOT MET in this GPU-less environment; the
measurement floor is environment-dominated. The real-GPU check page stays ready:
integration_lazy.html?gpucheck=1 on a real GPU + paste-back for the CPU-model comparison.
