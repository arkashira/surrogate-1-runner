package com.axentx.surrogate1.reporting;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ReportDataTest {

    @Test
    public void testReportData() {
        List<String> vulnerabilities = Arrays.asList("vuln1", "vuln2");
        Map<String, Integer> vulnerabilityTrends = new HashMap<>();
        vulnerabilityTrends.put("vuln1", 10);
        vulnerabilityTrends.put("vuln2", 20);
        Map<String, String> historicalData = new HashMap<>();
        historicalData.put("date1", "data1");
        historicalData.put("date2", "data2");

        ReportData reportData = new ReportData(vulnerabilities, vulnerabilityTrends, historicalData);

        assertEquals(vulnerabilities, reportData.getVulnerabilities());
        assertEquals(vulnerabilityTrends, reportData.getVulnerabilityTrends());
        assertEquals(historicalData, reportData.getHistoricalData());
    }
}