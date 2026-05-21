package com.axentx.surrogate.notification;

import java.time.LocalDate;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
public class EmailNotificationService {

    private final JavaMailSender mailSender;
    private final NotificationProperties properties;

    // Tracks the last date an email was sent per pipeline (pipelineName -> LocalDate)
    private final Map<String, LocalDate> lastSentCache = new ConcurrentHashMap<>();

    public EmailNotificationService(JavaMailSender mailSender, NotificationProperties properties) {
        this.mailSender = mailSender;
        this.properties = properties;
    }

    /**
     * Sends an email notification about a pipeline status change, respecting the
     * throttling rule of at most one email per pipeline per day.
     *
     * @param pipelineName name of the pipeline
     * @param status       status string (e.g., "COMPLETED" or "FAILED")
     * @param dashboardUrl link to the dashboard for this run
     */
    public void notify(String pipelineName, String status, String dashboardUrl) {
        LocalDate today = LocalDate.now();

        // Throttle: if we already sent today for this pipeline, skip
        LocalDate lastSent = lastSentCache.get(pipelineName);
        if (today.equals(lastSent)) {
            return;
        }

        // Build email using configurable templates
        String subject = properties.getSubjectTemplate()
                .replace("{pipeline}", pipelineName)
                .replace("{status}", status);

        String body = properties.getBodyTemplate()
                .replace("{pipeline}", pipelineName)
                .replace("{status}", status)
                .replace("{url}", dashboardUrl);

        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(properties.getFrom());
        message.setTo(properties.getRecipients().toArray(new String[0]));
        message.setSubject(subject);
        message.setText(body);

        mailSender.send(message);

        // Record that we sent today
        lastSentCache.put(pipelineName, today);
    }
}