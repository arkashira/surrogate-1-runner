package com.axentx.surrogate.tools;

import com.axentx.surrogate.tools.KiCAD9API;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class SurrogateTools {
    public static void generateDesignFiles(String projectPath) throws IOException {
        // Use KiCAD 9 native API format without Java dependencies
        String kicad9Json = KiCAD9API.generateBoardSpec(
            projectPath + "/board.kicad_pcb",
            projectPath + "/schematic.kicad_sch"
        );
        
        // Write output files directly without intermediate Java processing
        Files.write(Paths.get(projectPath + "/generated/surrogate_output.json"), 
                   kicad9Json.getBytes());
    }
}