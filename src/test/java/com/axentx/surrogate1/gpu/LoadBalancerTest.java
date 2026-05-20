package com.axentx.surrogate1.gpu;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class LoadBalancerTest {

    private static final String PROP_KEY = "axentx.gpu.loadbalancer.mapping";

    @AfterEach
    void cleanup() {
        System.clearProperty(PROP_KEY);
    }

    @Test
    void testConfigureLoadBalancingSetsProperty() {
        LoadBalancer lb = new LoadBalancer();
        List<String> mockGpus = Arrays.asList("GPU-0", "GPU-1", "GPU-2");
        lb.configureLoadBalancing(mockGpus);

        String mapping = System.getProperty(PROP_KEY);
        assertEquals("0:GPU-0,1:GPU-1,2:GPU-2", mapping);
    }

    @Test
    void testConfigureLoadBalancingWithNoGpusDoesNotSetProperty() {
        LoadBalancer lb = new LoadBalancer();
        lb.configureLoadBalancing(Collections.emptyList());

        assertNull(System.getProperty(PROP_KEY));
    }
}