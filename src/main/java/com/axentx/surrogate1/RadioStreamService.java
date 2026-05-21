package com.axentx.surrogate1;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class RadioStreamService {
    private static final String RECORDINGS_DIR = "recordings/";

    public void recordStream(String url, String filename) throws IOException {
        new RadioStreamRecorder().recordStream(url, filename);
    }

    public List<String> getRecordedStreams() {
        File recordingsDir = new File(RECORDINGS_DIR);
        List<String> recordedStreams = new ArrayList<>();
        if (recordingsDir.exists() && recordingsDir.isDirectory()) {
            for (File file : recordingsDir.listFiles()) {
                if (file.isFile() && file.getName().endsWith(".wav")) {
                    recordedStreams.add(file.getName().substring(0, file.getName().length() - 4));
                }
            }
        }
        return recordedStreams;
    }
}