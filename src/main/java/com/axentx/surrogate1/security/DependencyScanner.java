import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.apache.maven.model.Dependency;
import org.apache.maven.model.Model;
import org.apache.maven.model.io.xpp3.MavenXpp3Reader;
import org.codehaus.plexus.util.xml.pull.XmlPullParserException;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class DependencyScanner {
    private static final String VULNERABILITY_API_URL = "https://api.npmjs.org/downloads/point/last-week";
    private static final String DEPENDENCY_FILE = "pom.xml";

    public static void main(String[] args) {
        scanDependencies();
    }

    public static void scanDependencies() {
        File file = new File(DEPENDENCY_FILE);
        if (file.exists()) {
            try {
                MavenXpp3Reader reader = new MavenXpp3Reader();
                Model model = reader.read(file);
                List<Dependency> dependencies = model.getDependencies();
                List<Vulnerability> vulnerabilities = new ArrayList<>();

                for (Dependency dependency : dependencies) {
                    String groupId = dependency.getGroupId();
                    String artifactId = dependency.getArtifactId();
                    String version = dependency.getVersion();

                    String url = VULNERABILITY_API_URL + "?package=" + groupId + ":" + artifactId + "&version=" + version;
                    String response = sendGetRequest(url);

                    if (response != null) {
                        Gson gson = new GsonBuilder().create();
                        Vulnerability vulnerability = gson.fromJson(response, Vulnerability.class);

                        if (vulnerability != null) {
                            vulnerabilities.add(vulnerability);
                        }
                    }
                }

                logVulnerabilities(vulnerabilities);
            } catch (IOException | XmlPullParserException e) {
                System.out.println("Error reading dependency file: " + e.getMessage());
            }
        } else {
            System.out.println("Dependency file not found.");
        }
    }

    private static String sendGetRequest(String url) {
        try {
            Scanner scanner = new Scanner(new java.net.URL(url).openStream());
            scanner.useDelimiter("\\A");
            return scanner.next();
        } catch (IOException e) {
            System.out.println("Error sending GET request: " + e.getMessage());
            return null;
        }
    }

    private static void logVulnerabilities(List<Vulnerability> vulnerabilities) {
        for (Vulnerability vulnerability : vulnerabilities) {
            System.out.println("Vulnerability found: " + vulnerability.getName() + " - " + vulnerability.getSeverity());
        }
    }

    private static class Vulnerability {
        private String name;
        private String severity;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getSeverity() {
            return severity;
        }

        public void setSeverity(String severity) {
            this.severity = severity;
        }
    }
}