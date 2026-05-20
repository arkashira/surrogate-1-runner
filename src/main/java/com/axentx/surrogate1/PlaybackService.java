package com.axentx.surrogate1;

import java.io.File;
import java.io.IOException;
import javax.sound.sampled.*;
import java.nio.file.Path;
import java.nio.file.Paths;

public class PlaybackService {
    private Clip clip;
    private boolean isPlaying = false;

    public void playRecording(String filePath) throws LineUnavailableException, IOException, UnsupportedAudioFileException {
        File audioFile = new File(filePath);
        AudioInputStream audioStream = AudioSystem.getAudioInputStream(audioFile);
        AudioFormat format = audioStream.getFormat();
        DataLine.Info info = new DataLine.Info(Clip.class, format);

        if (!AudioSystem.isLineSupported(info)) {
            throw new LineUnavailableException("Audio format not supported");
        }

        clip = (Clip) AudioSystem.getLine(info);
        clip.open(audioStream);
        clip.start();
        isPlaying = true;
    }

    public void stopPlayback() {
        if (clip != null && isPlaying) {
            clip.stop();
            clip.close();
            isPlaying = false;
        }
    }

    public boolean isPlaying() {
        return isPlaying;
    }
}