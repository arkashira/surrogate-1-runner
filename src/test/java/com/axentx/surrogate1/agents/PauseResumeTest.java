package com.axentx.surrogate1.agents;

import org.junit.Test;
import static org.junit.Assert.*;

public class PauseResumeTest {
    @Test
    public void testPauseResume() {
        PauseResume pauseResume = new PauseResume();
        assertFalse(pauseResume.isPaused());
        pauseResume.pause();
        assertTrue(pauseResume.isPaused());
        pauseResume.resume();
        assertFalse(pauseResume.isPaused());
    }
}