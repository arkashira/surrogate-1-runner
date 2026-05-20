package com.axentx.surrogate.models;

public class Alert {
    private AIModel model;
    private String riskDescription;
    private String mitigationAction;

    public Alert(AIModel model, String riskDescription, String mitigationAction) {
        this.model = model;
        this.riskDescription = riskDescription;
        this.mitigationAction = mitigationAction;
    }

    // Getters and setters
    public AIModel getModel() {
        return model;
    }

    public void setModel(AIModel model) {
        this.model = model;
    }

    public String getRiskDescription() {
        return riskDescription;
    }

    public void setRiskDescription(String riskDescription) {
        this.riskDescription = riskDescription;
    }

    public String getMitigationAction() {
        return mitigationAction;
    }

    public void setMitigationAction(String mitigationAction) {
        this.mitigationAction = mitigationAction;
    }
}