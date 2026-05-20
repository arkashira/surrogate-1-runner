package com.axentx.surrogate1.alerting;

import com.axentx.surrogate1.model.ComplianceViolation;
import org.springframework.stereotype.Service;

@Service
public class NotificationSystem {

    public void sendNotification(ComplianceViolation violation) {
        // Logic to send notification based on the violation
        // Example: Send email, trigger alert in monitoring tool, etc.
    }
}