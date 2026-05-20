import java.util.List;

public class ReportGenerator {
    public List<Vulnerability> generateReport() {
        // Simulate generating report data
        List<Vulnerability> vulnerabilities = List.of(
                new Vulnerability("VULN-1", "High", "Description of vulnerability 1"),
                new Vulnerability("VULN-2", "Medium", "Description of vulnerability 2")
        );
        return vulnerabilities;
    }
}