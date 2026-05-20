package com.axentx.surrogate1.ui;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class UserExperience extends Application {
    
    @Override
    public void start(Stage primaryStage) {
        // Create UI components
        Button createWorkflowBtn = new Button("Create Workflow");
        Button manageWorkflowsBtn = new Button("Manage Workflows");
        Button settingsBtn = new Button("Settings");
        
        // Layout
        VBox root = new VBox(10);
        root.getChildren().addAll(createWorkflowBtn, manageWorkflowsBtn, settingsBtn);
        
        // Scene setup
        Scene scene = new Scene(root, 400, 300);
        scene.getStylesheets().add(getClass().getResource("/styles.css").toExternalForm());
        
        // Stage setup
        primaryStage.setTitle("Surrogate-1 Multi-Agent Workflow Manager");
        primaryStage.setScene(scene);
        primaryStage.setMinWidth(400);
        primaryStage.setMinHeight(300);
        primaryStage.show();
        
        // Event handlers for buttons
        createWorkflowBtn.setOnAction(e -> handleCreateWorkflow());
        manageWorkflowsBtn.setOnAction(e -> handleManageWorkflows());
        settingsBtn.setOnAction(e -> handleSettings());
    }
    
    private void handleCreateWorkflow() {
        // Implementation for creating workflow
        System.out.println("Creating new workflow...");
    }
    
    private void handleManageWorkflows() {
        // Implementation for managing workflows
        System.out.println("Managing workflows...");
    }
    
    private void handleSettings() {
        // Implementation for settings
        System.out.println("Opening settings...");
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}