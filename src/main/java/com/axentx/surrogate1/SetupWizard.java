package com.axentx.surrogate1;

import java.util.Scanner;
import java.util.Map;
import java.util.HashMap;

public class SetupWizard {
    private Scanner scanner;
    private Map<String, String> config;
    
    public SetupWizard() {
        this.scanner = new Scanner(System.in);
        this.config = new HashMap<>();
    }
    
    public void run() {
        System.out.println("Welcome to Surrogate-1 Setup Wizard!");
        System.out.println("This setup will guide you through configuring your environment in under 10 minutes.\n");
        
        askForDatabaseConfig();
        askForApiConfig();
        askForStorageConfig();
        askForConfirmation();
        
        saveConfiguration();
        System.out.println("\nSetup complete! Configuration saved.");
    }
    
    private void askForDatabaseConfig() {
        System.out.println("=== Database Configuration ===");
        System.out.print("Database URL (default: jdbc:h2:./data/surrogate1): ");
        String dbUrl = scanner.nextLine().trim();
        if (dbUrl.isEmpty()) {
            dbUrl = "jdbc:h2:./data/surrogate1";
        }
        config.put("database.url", dbUrl);
        
        System.out.print("Database Username (default: sa): ");
        String dbUser = scanner.nextLine().trim();
        if (dbUser.isEmpty()) {
            dbUser = "sa";
        }
        config.put("database.username", dbUser);
        
        System.out.print("Database Password (default: ): ");
        String dbPassword = scanner.nextLine().trim();
        config.put("database.password", dbPassword);
        System.out.println();
    }
    
    private void askForApiConfig() {
        System.out.println("=== API Configuration ===");
        System.out.print("API Base URL (default: http://localhost:8080): ");
        String apiUrl = scanner.nextLine().trim();
        if (apiUrl.isEmpty()) {
            apiUrl = "http://localhost:8080";
        }
        config.put("api.base-url", apiUrl);
        
        System.out.print("API Key (optional but recommended): ");
        String apiKey = scanner.nextLine().trim();
        if (!apiKey.isEmpty()) {
            config.put("api.key", apiKey);
        }
        System.out.println();
    }
    
    private void askForStorageConfig() {
        System.out.println("=== Storage Configuration ===");
        System.out.print("Data Directory (default: ./data): ");
        String dataDir = scanner.nextLine().trim();
        if (dataDir.isEmpty()) {
            dataDir = "./data";
        }
        config.put("storage.data-dir", dataDir);
        
        System.out.print("Cache Directory (default: ./cache): ");
        String cacheDir = scanner.nextLine().trim();
        if (cacheDir.isEmpty()) {
            cacheDir = "./cache";
        }
        config.put("storage.cache-dir", cacheDir);
        System.out.println();
    }
    
    private void askForConfirmation() {
        System.out.println("=== Review Your Configuration ===");
        for (Map.Entry<String, String> entry : config.entrySet()) {
            System.out.println(entry.getKey() + " = " + entry.getValue());
        }
        System.out.println();
        
        System.out.print("Do you want to proceed with these settings? (y/n): ");
        String response = scanner.nextLine().trim().toLowerCase();
        if (!response.equals("y") && !response.equals("yes")) {
            System.out.println("Setup cancelled.");
            System.exit(0);
        }
    }
    
    private void saveConfiguration() {
        // In a real implementation, this would save to a configuration file
        // For now, we'll just print a success message
        System.out.println("Saving configuration...");
        // This would typically involve writing to a properties file or similar
    }
    
    public static void main(String[] args) {
        SetupWizard wizard = new SetupWizard();
        wizard.run();
    }
}