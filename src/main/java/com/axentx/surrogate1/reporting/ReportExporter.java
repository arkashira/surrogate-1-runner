import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

public class ReportExporter {
    public void exportReport(List<Vulnerability> vulnerabilities, String format) throws IOException {
        switch (format) {
            case "csv":
                exportToCSV(vulnerabilities);
                break;
            case "json":
                exportToJson(vulnerabilities);
                break;
            default:
                throw new UnsupportedOperationException("Unsupported export format: " + format);
        }
    }

    private void exportToCSV(List<Vulnerability> vulnerabilities) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter("report.csv"))) {
            writer.println("Vulnerability ID,Severity,Description");
            for (Vulnerability vulnerability : vulnerabilities) {
                writer.println(vulnerability.getId() + "," + vulnerability.getSeverity() + "," + vulnerability.getDescription());
            }
        }
    }

    private void exportToJson(List<Vulnerability> vulnerabilities) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter("report.json"))) {
            writer.println("[");
            for (int i = 0; i < vulnerabilities.size(); i++) {
                Vulnerability vulnerability = vulnerabilities.get(i);
                writer.println("  {");
                writer.println("    \"id\": \"" + vulnerability.getId() + "\",");
                writer.println("    \"severity\": \"" + vulnerability.getSeverity() + "\",");
                writer.println("    \"description\": \"" + vulnerability.getDescription() + "\"");
                if (i < vulnerabilities.size() - 1) {
                    writer.println("  },");
                } else {
                    writer.println("  }");
                }
            }
            writer.println("]");
        }
    }
}

class Vulnerability {
    private String id;
    private String severity;
    private String description;

    public Vulnerability(String id, String severity, String description) {
        this.id = id;
        this.severity = severity;
        this.description = description;
    }

    public String getId() {
        return id;
    }

    public String getSeverity() {
        return severity;
    }

    public String getDescription() {
        return description;
    }
}