package com.axentx.surrogate1.reporting;

import java.util.List;
import java.util.Map;

public class ReportData {
    private List<String> vulnerabilities;
    private Map<String, Integer> vulnerabilityTrends;
    private Map<String, String> historicalData;

    public ReportData(List<String> vulnerabilities, Map<String, Integer> vulnerabilityTrends, Map<String, String> historicalData) {
        this.vulnerabilities = vulnerabilities;
        this.vulnerabilityTrends = vulnerabilityTrends;
        this.historicalData = historicalData;
    }

    public List<String> getVulnerabilities() {
        return vulnerabilities;
    }

    public void setVulnerabilities(List<String> vulnerabilities) {
        this.vulnerabilities = vulnerabilities;
    }

    public Map<String, Integer> getVulnerabilityTrends() {
        return vulnerabilityTrends;
    }

    public void setVulnerabilityTrends(Map<String, Integer> vulnerabilityTrends) {
        this.vulnerabilityTrends = vulnerabilityTrends;
    }

    public Map<String, String> getHistoricalData() {
        return historicalData;
    }

    public void setHistoricalData(Map<String, String> historicalData) {
        this.historicalData = historicalData;
    }
}