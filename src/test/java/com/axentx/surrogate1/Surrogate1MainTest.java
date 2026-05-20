package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Surrogate1MainTest {

    @Test
    public void testMain() {
        // This test is more about ensuring the main method runs without exceptions
        assertDoesNotThrow(() -> Surrogate1Main.main(new String[]{}));
    }
}