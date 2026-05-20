package com.axentx.surrogate1.alerting;

import com.axentx.surrogate1.model.ComplianceViolation;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AlertingSystem {

    private final NotificationSystem notificationSystem;

    public AlertingSystem(NotificationSystem notificationSystem) {
        this.notificationSystem = notificationSystem;
    }

    public void sendAlerts(List<ComplianceViolation> violations) {
        for (ComplianceViolation violation : violations) {
            notificationSystem.sendNotification(violation);
        }
    }
}