package com.axentx.surrogate1;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class RadioStreamRecorder {

    private List<String> availableStreams;

    public RadioStreamRecorder(List<String> availableStreams) {
        this.availableStreams = availableStreams;
    }

    public void selectStream(String streamUrl) {
        if (!availableStreams.contains(streamUrl)) {
            throw new IllegalArgumentException("Invalid stream URL");
        }
        // Logic to select the stream for recording
    }

    public void startRecording(String streamUrl, File outputFile) throws IOException {
        // Logic to start recording the selected stream into the specified file
    }

    public List<File> getRecordedStreams() {
        // Logic to return a list of recorded streams
        return null;
    }

    public void playRecordedStream(File recordedFile) {
        // Logic to play the recorded stream
    }
}