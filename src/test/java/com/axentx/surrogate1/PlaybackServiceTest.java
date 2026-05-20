package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import javax.sound.sampled.LineUnavailableException;
import java.io.IOException;

class PlaybackServiceTest {
    @Test
    void testPlayRecording() {
        PlaybackService playbackService = new PlaybackService();
        try {
            playbackService.playRecording("test_audio.wav");
            assertTrue(playbackService.isPlaying());
            playbackService.stopPlayback();
            assertFalse(playbackService.isPlaying());
        } catch (LineUnavailableException | IOException | UnsupportedAudioFileException e) {
            fail("Exception should not be thrown: " + e.getMessage());
        }
    }

    @Test
    void testStopPlayback() {
        PlaybackService playbackService = new PlaybackService();
        playbackService.stopPlayback();
        assertFalse(playbackService.isPlaying());
    }
}