import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import static org.junit.Assert.assertTrue;

public class ReportExporterTest {
    @Test
    public void testExportToCSV() throws IOException {
        ReportExporter exporter = new ReportExporter();
        List<Vulnerability> vulnerabilities = new ReportGenerator().generateReport();
        exporter.exportReport(vulnerabilities, "csv");
        File file = new File("report.csv");
        assertTrue(file.exists());
    }

    @Test
    public void testExportToJson() throws IOException {
        ReportExporter exporter = new ReportExporter();
        List<Vulnerability> vulnerabilities = new ReportGenerator().generateReport();
        exporter.exportReport(vulnerabilities, "json");
        File file = new File("report.json");
        assertTrue(file.exists());
    }
}