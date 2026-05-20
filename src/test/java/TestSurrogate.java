package com.axentx.surrogate;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.Properties;

import static org.junit.jupiter.api.Assertions.*;

public class TestSurrogate {

    @Test
    public void testPropertiesLoad() throws IOException {
        // Load the test properties file from the classpath
        Properties props = new Properties();
        try (var stream = getClass().getClassLoader().getResourceAsStream("test.properties")) {
            assertNotNull(stream, "test.properties must be present on the test classpath");
            props.load(stream);
        }

        // Verify that the expected key/value pair exists
        assertEquals("testValue", props.getProperty("test.key"),
                "Property 'test.key' should have the value 'testValue'");
    }
}