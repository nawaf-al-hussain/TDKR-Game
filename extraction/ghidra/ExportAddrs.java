// Ghidra headless script: decompile functions at given vaddrs (Ghidra space).
// Usage: -postScript ExportAddrs.java 36874c,369ac0,...
// (real vaddr + 0x10000)
// @category TDKR.RE
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import java.io.*;

public class ExportAddrs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1) {
            println("usage: ExportAddrs.java <addrGhidraHex>[,<addr>...]");
            return;
        }
        String outDir = "/home/z/ghidra_out";
        new File(outDir).mkdirs();
        DecompInterface di = new DecompInterface();
        di.openProgram(currentProgram);
        for (String a : args) {
            for (String tok : a.split(",")) {
                if (tok.isBlank()) continue;
                long v = Long.parseLong(tok.trim(), 16);
                Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v);
                Function f = getFunctionContaining(addr);
                if (f == null) f = currentProgram.getFunctionManager().getFunctionAt(addr);
                if (f == null) {
                    println("no function at " + tok);
                    continue;
                }
                DecompileResults res = di.decompileFunction(f, 300, monitor);
                String fn = outDir + "/add_" + Long.toHexString(f.getEntryPoint().getOffset()) + ".c";
                if (res != null && res.decompileCompleted()) {
                    PrintWriter pw = new PrintWriter(new FileWriter(fn));
                    pw.println("// " + f.getName() + " @ " + f.getEntryPoint());
                    pw.println(res.getDecompiledFunction().getC());
                    pw.close();
                    println("wrote " + fn + " (" + f.getName() + ")");
                } else {
                    println("decompile FAILED " + tok);
                }
            }
        }
    }
}
