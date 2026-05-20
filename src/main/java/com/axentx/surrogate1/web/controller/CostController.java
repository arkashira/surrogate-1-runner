package com.axentx.surrogate1.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.List;

/**
 * CostController exposes two endpoints:
 *  • /api/top-cost-drivers  – JSON REST API
 *  • /dashboard/top-cost-drivers – Thymeleaf page
 *
 * In a real system the data would come from a database or analytics service.
 * For this demo we return a static list of the top three cost drivers,
 * sorted by total cost (descending).
 */
public class CostController {

    /* --------------------------------------------------------------------- */
    /*  REST API                                                              */
    /* --------------------------------------------------------------------- */
    @RestController
    public static class Api {

        @GetMapping("/api/top-cost-drivers")
        public List<CostDriver> getTopCostDrivers() {
            return mockData();
        }
    }

    /* --------------------------------------------------------------------- */
    /*  Server‑side rendered page                                            */
    /* --------------------------------------------------------------------- */
    @Controller
    public static class Page {

        @GetMapping("/dashboard/top-cost-drivers")
        public String getTopCostDrivers(Model model) {
            model.addAttribute("topDrivers", mockData());
            return "topCostDrivers";
        }
    }

    /* --------------------------------------------------------------------- */
    /*  DTO                                                                    */
    /* --------------------------------------------------------------------- */
    public static class CostDriver {
        private final String vmType;
        private final String region;
        private final int totalCostCents;   // stored in cents
        private final int instanceCount;

        public CostDriver(String vmType, String region, int totalCostCents, int instanceCount) {
            this.vmType = vmType;
            this.region = region;
            this.totalCostCents = totalCostCents;
            this.instanceCount = instanceCount;
        }

        public String getVmType() { return vmType; }
        public String getRegion() { return region; }
        public int getTotalCostCents() { return totalCostCents; }
        public int getInstanceCount() { return instanceCount; }

        /** Human‑readable cost, e.g. "$1,200.00" */
        public String getTotalCostFormatted() {
            return String.format("$%,.2f", totalCostCents / 100.0);
        }

        /** Convenience for the Thymeleaf template */
        public String getDisplayString() {
            return String.format("%s in %s: %s, %d instances",
                    vmType, region, getTotalCostFormatted(), instanceCount);
        }
    }

    /* --------------------------------------------------------------------- */
    /*  Mock data generator                                                   */
    /* --------------------------------------------------------------------- */
    private static List<CostDriver> mockData() {
        return Arrays.asList(
                new CostDriver("m5.large", "us-east-1", 120_000, 5000),
                new CostDriver("c5.xlarge", "eu-west-2",  80_000, 3200),
                new CostDriver("t3.medium", "ap-southeast-1", 150_000, 2100)
        );
    }
}