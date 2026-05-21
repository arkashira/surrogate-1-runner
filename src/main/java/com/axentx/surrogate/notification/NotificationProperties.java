package com.axentx.surrogate.notification;

import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "notification")
public class NotificationProperties {

    /**
     * Email address used as the sender.
     */
    private String from;

    /**
     * List of recipient email addresses.
     */
    private List<String> recipients;

    /**
     * Subject template, e.g. "Pipeline {pipeline} {status}"
     */
    private String subjectTemplate;

    /**
     * Body template, e.g. "Pipeline {pipeline} has {status}. View details: {url}"
     */
    private String bodyTemplate;

    // Getters and setters

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public List<String> getRecipients() {
        return recipients;
    }

    public void setRecipients(List<String> recipients) {
        this.recipients = recipients;
    }

    public String getSubjectTemplate() {
        return subjectTemplate;
    }

    public void setSubjectTemplate(String subjectTemplate) {
        this.subjectTemplate = subjectTemplate;
    }

    public String getBodyTemplate() {
        return bodyTemplate;
    }

    public void setBodyTemplate(String bodyTemplate) {
        this.bodyTemplate = bodyTemplate;
    }
}