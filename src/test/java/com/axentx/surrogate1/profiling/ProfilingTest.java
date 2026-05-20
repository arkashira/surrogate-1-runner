import com.axentx.surrogate1.profiling.ProfilingAgent;
import com.axentx.surrogate1.profiling.ProfilingConfig;
import com.axentx.surrogate1.profiling.ProfilingReport;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

import static org.junit.Assert.*;

public class ProfilingTest {

    private ProfilingAgent profilingAgent;

    @Before
    public void setUp() {
        ProfilingConfig config = new ProfilingConfig();
        config.setEnableProfiling(true);
        profilingAgent = new ProfilingAgent(config);
    }

    @After
    public void tearDown() {
        profilingAgent.stopProfiling();
    }

    @Test
    public void testProfilingEnabled() {
        assertTrue(profilingAgent.isProfilingEnabled());
    }

    @Test
    public void testProfilingDisabled() {
        ProfilingConfig config = new ProfilingConfig();
        config.setEnableProfiling(false);
        ProfilingAgent agent = new ProfilingAgent(config);
        assertFalse(agent.isProfilingEnabled());
    }

    @Test
    public void testProfilingReport() throws IOException {
        ConcurrentHashMap<String, Integer> readCounts = new ConcurrentHashMap<>();
        ConcurrentHashMap<String, Integer> writeCounts = new ConcurrentHashMap<>();
        ConcurrentHashMap<String, Integer> lockContentionCounts = new ConcurrentHashMap<>();

        readCounts.put("collection1", 10);
        writeCounts.put("collection1", 5);
        lockContentionCounts.put("collection1", 2);

        ProfilingReport report = new ProfilingReport(readCounts, writeCounts, lockContentionCounts);
        report.generateReport();

        File reportFile = new File("profiling_report.json");
        assertTrue(reportFile.exists());

        // Clean up
        reportFile.delete();
    }
}