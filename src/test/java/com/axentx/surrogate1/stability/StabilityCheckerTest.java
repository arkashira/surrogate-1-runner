package com.axentx.surrogate1.stability;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class StabilityCheckerTest {

    @Test
    public void testCheckSystemStability() {
        StabilityChecker.adjustSystemStability(true);
        assertTrue(StabilityChecker.checkSystemStability());

        StabilityChecker.adjustSystemStability(false);
        assertFalse(StabilityChecker.checkSystemStability());
    }
}