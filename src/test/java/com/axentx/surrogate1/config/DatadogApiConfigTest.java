package com.axentx.surrogate1.config;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class DatadogApiConfigTest {

    @Test
    void testConfiguration() {
        DatadogApiConfig config = new DatadogApiConfig();
        config.setEndpoint("http://test-endpoint");
        config.setApiKey("test-api-key");
        config.setAppKey("test-app-key");

        assertEquals("http://test-endpoint", config.getEndpoint());
        assertEquals("test-api-key", config.getApiKey());
        assertEquals("test-app-key", config.getAppKey());
    }
}