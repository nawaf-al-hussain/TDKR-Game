// Ghidra headless pre-script: disable slow analyzers (tight disk/RAM budget).
// Function names come from the symtab (41.5k FUNC symbols); heavy discovery
// passes add little for our decompile targets but hours of time + GB of DB.
// @category TDKR.RE
import ghidra.app.script.GhidraScript;

public class LeanAnalysis extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[][] opts = {
            {"Decompiler Parameter ID", "false"},
            {"Shared Return Calls", "false"},
            {"Non-Returning Functions - Discovered", "false"},
            {"Aggressive Instruction Finder", "false"},
            {"Embedded Media", "false"},
            {"Embedded Images", "false"},
        };
        for (String[] o : opts) {
            try {
                setAnalysisOption(currentProgram, o[0], o[1]);
                println("LeanAnalysis: " + o[0] + " -> " + o[1]);
            } catch (Exception e) {
                println("LeanAnalysis FAIL " + o[0] + ": " + e);
            }
        }
        println("LeanAnalysis done");
    }
}
