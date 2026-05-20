package com.axentx.surrogate.alerts;

import com.axentx.surrogate.models.AIModel;
import com.axentx.surrogate.models.Alert;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class AlertService {

    private final List<Alert> alerts = new ArrayList<>();

    public void generateAlert(AIModel model, String riskDescription, String mitigationAction) {
        Alert alert = new Alert(model, riskDescription, mitigationAction);
        alerts.add(alert);
        // In a real application, you would also send the alert to a notification system
    }

    public List<Alert> getAlerts() {
        return alerts;
    }
}