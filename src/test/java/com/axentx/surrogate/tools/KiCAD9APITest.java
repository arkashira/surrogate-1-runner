package com.axentx.surrogate.tools;

import org.junit.jupiter.api.Test;
import java.io.IOException;
import static org.junit.jupiter.api.Assertions.*;

public class KiCAD9APITest {
    @Test
    public void testBoardSpecGeneration() throws IOException {
        String testOutput = KiCAD9API.generateBoardSpec(
            "test/resources/test_board.kicad_pcb",
            "test/resources/test_schematic.kicad_sch"
        );
        
        assertNotNull(testOutput);
        assertTrue(testOutput.contains("\"kicad_version\":9"));
        assertFalse(testOutput.contains("java"));
    }
}