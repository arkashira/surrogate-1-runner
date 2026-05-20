package com.axentx.surrogate1.adaptation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class AdaptationSystemTest {

    @Test
    public void testStartAndStop() {
        AdaptationSystem adaptationSystem = new AdaptationSystem();
        adaptationSystem.start();
        assertTrue(adaptationSystem.executorService.isShutdown());
        adaptationSystem.stop();
        assertTrue(adaptationSystem.executorService.isTerminated());
    }
}