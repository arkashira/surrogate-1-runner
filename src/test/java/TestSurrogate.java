
package com.axentx.surrogate1;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class Surrogate1Test {
    private Surrogate1 surrogate1 = new Surrogate1();

    @Test
    public void testBasicFunctionality() {
        String input = "some input";
        String expectedOutput = "expected output";
        String actualOutput = surrogate1.process(input);
        assertEquals(expectedOutput, actualOutput);
    }
}