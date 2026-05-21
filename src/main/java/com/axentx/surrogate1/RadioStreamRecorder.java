package com.axentx.surrogate1;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;

public class RadioStreamRecorder {
    private static final String RECORDINGS_DIR = "recordings/";

    public void recordStream(String url, String filename) throws IOException {
        File recordingsDir = new File(RECORDINGS_DIR);
        if (!recordingsDir.exists()) {
            recordingsDir.mkdir();
        }

        File outputFile = new File(recordingsDir, filename + ".wav");
        try (AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new URL(url))) {
            AudioFormat format = audioInputStream.getFormat();
            byte[] audioBytes = new byte[format.getFrameSize()];
            int bytesRead;
            try (FileOutputStream outputStream = new FileOutputStream(outputFile)) {
                while ((bytesRead = audioInputStream.read(audioBytes)) != -1) {
                    outputStream.write(audioBytes, 0, bytesRead);
                }
            }
        }
    }
}