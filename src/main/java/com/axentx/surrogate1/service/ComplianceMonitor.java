package com.axentx.surrogate1.service;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class ComplianceMonitor {

    private static final double THRESHOLD = 0.15; // 15%
    private ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

    public ComplianceMonitor() {
        startMonitoring();
    }

    private void startMonitoring() {
        scheduler.scheduleAtFixedRate(this::checkThreshold, 0, 1, TimeUnit.MINUTES);
    }

    private void checkThreshold() {
        double revenue = getRevenue(); // Placeholder method to fetch current revenue
        double expenses = getExpenses(); // Placeholder method to fetch current expenses

        double ratio = expenses / revenue;

        if (ratio > THRESHOLD) {
            triggerAlert(revenue, expenses, ratio);
            logViolation(revenue, expenses, ratio);
        }
    }

    private double getRevenue() {
        // Implementation to fetch current revenue
        return 100000; // Example value
    }

    private double getExpenses() {
        // Implementation to fetch current expenses
        return 16000; // Example value
    }

    private void triggerAlert(double revenue, double expenses, double ratio) {
        // Implementation to send email/SMS alerts
        System.out.println("ALERT: Expenses exceeded 15% of revenue! Revenue: " + revenue + ", Expenses: " + expenses + ", Ratio: " + ratio);
    }

    private void logViolation(double revenue, double expenses, double ratio) {
        // Implementation to log historical threshold violations
        System.out.println("LOG: Threshold violation detected. Revenue: " + revenue + ", Expenses: " + expenses + ", Ratio: " + ratio);
    }

    public static void main(String[] args) {
        new ComplianceMonitor();
    }
}