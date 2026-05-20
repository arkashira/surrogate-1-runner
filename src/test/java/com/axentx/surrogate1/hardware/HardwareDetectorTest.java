package com.axentx.surrogate1.hardware;

import org.junit.Test;
import static org.junit.Assert.*;

public class HardwareDetectorTest {

    @Test
    public void testDetectHardwareConfiguration() {
        String hardwareInfo = HardwareDetector.detectHardwareConfiguration();
        assertNotNull(hardwareInfo);
        assertFalse(hardwareInfo.isEmpty());
    }
}