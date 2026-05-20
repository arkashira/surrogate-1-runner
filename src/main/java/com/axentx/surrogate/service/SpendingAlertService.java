package com.axentx.surrogate.service;

import com.axentx.surrogate.model.SpendingAnomaly;
import com.axentx.surrogate.repository.SpendingAnomalyRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SpendingAlertService {

    @Autowired
    private SpendingAnomalyRepository spendingAnomalyRepository;

    @Autowired
    private EmailService emailService;

    @Autowired
    private NotificationService notificationService;

    public void checkForAnomalies() {
        List<SpendingAnomaly> anomalies = spendingAnomalyRepository.findRecentAnomalies();

        for (SpendingAnomaly anomaly : anomalies) {
            sendAlert(anomaly);
        }
    }

    private void sendAlert(SpendingAnomaly anomaly) {
        String emailContent = constructEmailContent(anomaly);
        emailService.sendEmail(anomaly.getRecipientEmail(), "Unexpected Spending Spike Alert", emailContent);

        String notificationContent = constructNotificationContent(anomaly);
        notificationService.sendNotification(anomaly.getUserId(), "Unexpected Spending Spike Alert", notificationContent);
    }

    private String constructEmailContent(SpendingAnomaly anomaly) {
        return "Dear " + anomaly.getUserName() + ",\n\n" +
                "We have detected an unexpected spending spike in your cloud account.\n\n" +
                "Details:\n" +
                "Amount: " + anomaly.getAmount() + "\n" +
                "Date: " + anomaly.getDate() + "\n" +
                "Service: " + anomaly.getService() + "\n\n" +
                "Suggested Actions:\n" +
                "1. Review your recent activities and usage.\n" +
                "2. Check for any unauthorized access or usage.\n" +
                "3. Contact our support team if you need further assistance.\n\n" +
                "Best regards,\n" +
                "Axentx Support Team";
    }

    private String constructNotificationContent(SpendingAnomaly anomaly) {
        return "Unexpected spending spike detected:\n" +
                "Amount: " + anomaly.getAmount() + "\n" +
                "Date: " + anomaly.getDate() + "\n" +
                "Service: " + anomaly.getService() + "\n\n" +
                "Please review and take necessary actions.";
    }
}