import com.axentx.surrogate1.profiling.ProfilingConfig;
import com.axentx.surrogate1.profiling.ProfilingReport;

import java.util.concurrent.ConcurrentHashMap;

public class ProfilingAgent {

    private ProfilingConfig config;
    private boolean isProfilingEnabled;
    private ConcurrentHashMap<String, Integer> readCounts;
    private ConcurrentHashMap<String, Integer> writeCounts;
    private ConcurrentHashMap<String, Integer> lockContentionCounts;

    public ProfilingAgent(ProfilingConfig config) {
        this.config = config;
        this.isProfilingEnabled = config.isEnableProfiling();
        this.readCounts = new ConcurrentHashMap<>();
        this.writeCounts = new ConcurrentHashMap<>();
        this.lockContentionCounts = new ConcurrentHashMap<>();
    }

    public boolean isProfilingEnabled() {
        return isProfilingEnabled;
    }

    public void startProfiling() {
        // Start profiling
    }

    public void stopProfiling() {
        // Stop profiling
    }

    public void updateReadCount(String collectionName, int count) {
        readCounts.put(collectionName, count);
    }

    public void updateWriteCount(String collectionName, int count) {
        writeCounts.put(collectionName, count);
    }

    public void updateLockContentionCount(String collectionName, int count) {
        lockContentionCounts.put(collectionName, count);
    }

    public ProfilingReport generateReport() {
        return new ProfilingReport(readCounts, writeCounts, lockContentionCounts);
    }
}