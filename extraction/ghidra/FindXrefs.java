// Find functions referencing given data addresses (string literals).
// Usage: run in headless -process mode; edit ADDRS below.
// @category TDKR.RE
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;

public class FindXrefs extends GhidraScript {
    static final String[] HEX_ADDRS = {
        "00b44cd0", ".lvc suffix A",
        "00b44fb4", ".lvc suffix B",
        "00b365fc", "shop.lvc",
        "00b3f9c8", "data/game_config.gla",
        "00b3ea64", "gol.bin",
        "00b3f628", "effects.bin",
    };

    @Override
    public void run() throws Exception {
        for (int i = 0; i < HEX_ADDRS.length; i += 2) {
            Address a = currentProgram.getAddressFactory().getAddress(HEX_ADDRS[i]);
            println("=== xrefs to " + a + " (" + HEX_ADDRS[i + 1] + ") ===");
            ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(a);
            boolean any = false;
            while (it.hasNext()) {
                Reference r = it.next();
                Function f = getFunctionContaining(r.getFromAddress());
                String fname = (f != null) ? f.getName() + " @ " + f.getEntryPoint() : "<no-func>";
                println("  from " + r.getFromAddress() + " (" + r.getReferenceType() + ") in " + fname);
                any = true;
            }
            if (!any) println("  (none)");
        }
    }
}
