// Ghidra headless script: decompile RE-target functions of libKRHP.so
// @category TDKR.RE
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.io.*;
import java.util.*;

public class ExportTargets extends GhidraScript {
    static final String[] TARGETS = {
        "setfogcolor", "setfogdistance", "resetfog", "buildcolorgradingtexture",
        "colorgrading", "irradiancebaker", "changelightmap", "bakegroup",
        "batchbaker", "weathermanager", "footprint", "lightmapatlas",
        "globalobjects", "gol_", "loadglobalobject",
        // phase 2: preset/stream format + zone scene graph
        "templatelevelproperties", "saveload", "irradiancevolume", "zonesmanager",
        "dictionary",
        // phase 3: preset base classes + postprocess LUT loading
        "levelinit", "globalillum", "colorcorrection", "postprocess",
        // phase 4: level template load chain (lvc/DICT)
        "loadlevelinit", "requireloadlevel", "checkloadlevel", "loadlevelsstatus", "application"
    };

    @Override
    public void run() throws Exception {
        String outDir = "/home/z/ghidra_out";
        new File(outDir).mkdirs();

        DecompInterface di = new DecompInterface();
        di.openProgram(currentProgram);

        PrintWriter idx = new PrintWriter(new FileWriter(outDir + "/targets_index.txt"));
        PrintWriter all = new PrintWriter(new FileWriter(outDir + "/all_functions.txt"));

        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        int matched = 0;
        while (it.hasNext()) {
            Function f = it.next();
            String name = f.getName();
            all.println(f.getEntryPoint() + " " + name);
            String low = name.toLowerCase();
            String hit = null;
            for (String t : TARGETS) {
                if (low.contains(t)) { hit = t; break; }
            }
            if (hit == null) continue;
            DecompileResults res = di.decompileFunction(f, 120, monitor);
            if (res != null && res.decompileCompleted()) {
                String code = res.getDecompiledFunction().getC();
                String fname = hit + "__" + Long.toHexString(f.getEntryPoint().getOffset()) + ".c";
                PrintWriter pw = new PrintWriter(new FileWriter(outDir + "/" + fname));
                pw.println("// " + name + " @ " + f.getEntryPoint());
                pw.println(code);
                pw.close();
                idx.println(f.getEntryPoint() + " " + name + " -> " + fname);
                matched++;
            } else {
                idx.println(f.getEntryPoint() + " " + name + " -> DECOMPILE_FAILED");
            }
        }
        idx.close();
        all.close();
        println("ExportTargets: matched=" + matched);
    }
}
