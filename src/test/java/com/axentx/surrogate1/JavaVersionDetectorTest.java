package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class JavaVersionDetectorTest {

    @Test
    public void testGetJavaVersion() {
        String version = JavaVersionDetector.getJavaVersion();
        assertNotNull(version);
        assertFalse(version.isEmpty());
    }

    @Test
    public void testIsJavaVersionSupported() {
        assertTrue(JavaVersionDetector.isJavaVersionSupported("1.8.0_202"));
        assertTrue(JavaVersionDetector.isJavaVersionSupported("11.0.1"));
        assertTrue(JavaVersionDetector.isJavaVersionSupported("17.0.1"));
        assertFalse(JavaVersionDetector.isJavaVersionSupported("1.7.0_201"));
    }
}