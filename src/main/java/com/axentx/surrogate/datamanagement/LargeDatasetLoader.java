package com.axentx.surrogate.datamanagement;

import java.io.*;
import java.nio.channels.FileChannel;
import java.nio.file.*;
import java.util.concurrent.*;

public class LargeDatasetLoader {

    private static final int BUFFER_SIZE = 1024 * 1024; // 1MB buffer size

    public void loadDataset(String filePath) throws IOException {
        FileChannel sourceChannel = null;
        FileChannel destinationChannel = null;
        try {
            sourceChannel = FileChannel.open(Paths.get(filePath), StandardOpenOption.READ);
            destinationChannel = FileChannel.open(Paths.get("output.txt"), StandardOpenOption.WRITE, StandardOpenOption.CREATE);

            long position = 0;
            long count;
            while ((count = sourceChannel.size() - position) > 0) {
                count = Math.min(count, BUFFER_SIZE);
                sourceChannel.transferTo(position, count, destinationChannel);
                position += count;
            }
        } finally {
            if (sourceChannel != null) sourceChannel.close();
            if (destinationChannel != null) destinationChannel.close();
        }
    }

    public static void main(String[] args) {
        try {
            new LargeDatasetLoader().loadDataset(args[0]);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}