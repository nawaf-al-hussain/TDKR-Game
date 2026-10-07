# Ghidra headless post-script: decompile RE-target functions of libKRHP.so
# Targets: fog (CWeatherManager), ColorGrading LUT (CPostProcessManager),
#          IrradianceBaker (runtime footprint bakes), ChangeLightMap (CZone),
#          BakeGroup loaders, Lua API registration
# @category TDKR.RE
import os
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT_DIR = "/home/z/ghidra_out"
LIST_FILE = os.path.join(OUT_DIR, "targets_index.txt")
ALL_FUNCS = os.path.join(OUT_DIR, "all_functions.txt")

# substring-match (lowercase) against function name
TARGETS = [
    "setfogcolor",
    "setfogdistance",
    "resetfog",
    "buildcolorgradingtexture",
    "colorgrading",
    "irradiancebaker",
    "changelightmap",
    "bakegroup",
    "batchbaker",
    "weathermanager",
    "footprint",
    "lightmapatlas",
]

if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

fm = currentProgram.getFunctionManager()
di = DecompInterface()
di.openProgram(currentProgram)
monitor = ConsoleTaskMonitor()

matched = 0
index_lines = []
all_lines = []
for f in fm.getFunctions(True):
    name = f.getName()
    addr = f.getEntryPoint().toString()
    all_lines.append("%s %s" % (addr, name))
    low = name.lower()
    hit = None
    for t in TARGETS:
        if t in low:
            hit = t
            break
    if hit:
        res = di.decompileFunction(f, 120, monitor)
        if res.decompileCompleted():
            code = res.getDecompiledFunction().getC()
            fname = "%s__%x.c" % (hit, f.getEntryPoint().getOffset())
            with open(os.path.join(OUT_DIR, fname), "w") as fh:
                fh.write(code)
            index_lines.append("%s %s -> %s" % (addr, name, fname))
            matched += 1
        else:
            index_lines.append("%s %s -> DECOMPILE_FAILED" % (addr, name))

with open(LIST_FILE, "w") as fh:
    fh.write("\n".join(index_lines))
with open(ALL_FUNCS, "w") as fh:
    fh.write("\n".join(all_lines))

print("ExportTargets: matched=%d functions" % matched)
