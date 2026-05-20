package com.axentx.surrogate.gpu;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GPUTest {
    @Test
    public void testRender() {
        GPU gpu = new GPU();
        assertDoesNotThrow(() -> gpu.render(new Scene()));
    }

    @Test
    public void testSetResolution() {
        GPU gpu = new GPU();
        assertDoesNotThrow(() -> gpu.setResolution(3840, 2160));
    }

    @Test
    public void testSetFrameRate() {
        GPU gpu = new GPU();
        assertDoesNotThrow(() -> gpu.setFrameRate(120));
    }
}