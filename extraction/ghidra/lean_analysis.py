# Ghidra headless pre-script: disable slow analyzers to fit tight disk/RAM.
# Function names come from the symtab (41.5k FUNC symbols), so heavy discovery
# passes add little for our decompile targets but hours of time + GB of DB.
# @category TDKR.RE
opts = {
    "Decompiler Parameter ID": "false",
    "Shared Return Calls": "false",
    "Non-Returning Functions - Discovered": "false",
    "Aggressive Instruction Finder": "false",
    "Embedded Media": "false",
    "Embedded Images": "false",
}
for k, v in opts.items():
    try:
        setAnalysisOption(currentProgram, k, v)
        print("lean_analysis: %s -> %s" % (k, v))
    except Exception as e:
        print("lean_analysis FAIL %s: %s" % (k, e))
print("lean_analysis done")
