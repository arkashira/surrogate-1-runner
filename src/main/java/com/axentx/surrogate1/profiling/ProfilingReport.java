import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

public class ProfilingReport {

    private ConcurrentHashMap<String, Integer> readCounts;
    private ConcurrentHashMap<String, Integer> writeCounts;
    private ConcurrentHashMap<String, Integer> lockContentionCounts;

    public ProfilingReport(ConcurrentHashMap<String, Integer> readCounts, ConcurrentHashMap<String, Integer> writeCounts, ConcurrentHashMap<String, Integer> lockContentionCounts) {
        this.readCounts = readCounts;
        this.writeCounts = writeCounts;
        this.lockContentionCounts = lockContentionCounts;
    }

    public void generateReport() {
        Gson gson = new GsonBuilder().create();
        String reportJson = gson.toJson(this);

        try (FileWriter writer = new FileWriter("profiling_report.json")) {
            writer.write(reportJson);
        } catch (IOException e) {
            // Handle exception
        }
    }
}