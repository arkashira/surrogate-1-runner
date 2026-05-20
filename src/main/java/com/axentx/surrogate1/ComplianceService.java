package com.axentx.surrogate1;

import java.util.*;
import java.util.stream.Collectors;
import javax.mail.*;
import javax.mail.internet.*;
import javax.activation.*;

/**
 * Service responsible for detecting compliance issues in data records,
 * exposing them for the dashboard, and notifying stakeholders via email.
 *
 * <p>Compliance rules are intentionally simple for demonstration purposes:
 * <ul>
 *   <li>All records must contain a non-empty "id" field.</li>
 *   <li>All records must contain a non-empty "timestamp" field.</li>
 *   <li>All records must contain a "status" field equal to "ACTIVE" or "INACTIVE".</li>
 * </ul>
 *
 * <p>In a real system these rules would be configurable and more complex.
 */
public class ComplianceService {

    /**
     * Represents a single compliance issue found in a data record.
     */
    public static class ComplianceIssue {
        private final String recordId;
        private final String field;
        private final String message;

        public ComplianceIssue(String recordId, String field, String message) {
            this.recordId = recordId;
            this.field = field;
            this.message = message;
        }

        public String getRecordId() { return recordId; }
        public String getField() { return field; }
        public String getMessage() { return message; }

        @Override
        public String toString() {
            return String.format("Record %s: %s - %s", recordId, field, message);
        }
    }

    // In-memory store of the latest compliance issues
    private final List<ComplianceIssue> latestIssues = new ArrayList<>();

    /**
     * Detects compliance issues in the provided list of records.
     *
     * @param records list of records represented as Map<String, String>
     * @return list of detected issues
     */
    public List<ComplianceIssue> detectIssues(List<Map<String, String>> records) {
        List<ComplianceIssue> issues = new ArrayList<>();

        for (Map<String, String> record : records) {
            String id = record.getOrDefault("id", "").trim();
            String timestamp = record.getOrDefault("timestamp", "").trim();
            String status = record.getOrDefault("status", "").trim();

            if (id.isEmpty()) {
                issues.add(new ComplianceIssue(id, "id", "Missing or empty id field"));
            }
            if (timestamp.isEmpty()) {
                issues.add(new ComplianceIssue(id, "timestamp", "Missing or empty timestamp field"));
            }
            if (!status.equals("ACTIVE") && !status.equals("INACTIVE")) {
                issues.add(new ComplianceIssue(id, "status", "Invalid status value: " + status));
            }
        }

        // Persist latest issues for dashboard consumption
        synchronized (latestIssues) {
            latestIssues.clear();
            latestIssues.addAll(issues);
        }

        return issues;
    }

    /**
     * Returns the most recent set of compliance issues.
     *
     * @return list of issues
     */
    public List<ComplianceIssue> getLatestIssues() {
        synchronized (latestIssues) {
            return new ArrayList<>(latestIssues);
        }
    }

    /**
     * Sends an email notification containing the list of compliance issues.
     *
     * @param recipient email address to send the notification to
     * @throws MessagingException if the email cannot be sent
     */
    public void notifyViaEmail(String recipient) throws MessagingException {
        List<ComplianceIssue> issues = getLatestIssues();
        if (issues.isEmpty()) {
            // No issues, nothing to notify
            return;
        }

        // Basic email configuration – in production these would come from
        // environment variables or a configuration file.
        Properties props = new Properties();
        props.put("mail.smtp.host", "localhost");
        props.put("mail.smtp.port", "25");

        Session session = Session.getInstance(props, null);
        MimeMessage message = new MimeMessage(session);
        message.setFrom(new InternetAddress("noreply@axentx.com"));
        message.setRecipient(Message.RecipientType.TO, new InternetAddress(recipient));
        message.setSubject("Axentx Compliance Issues Detected");

        String body = issues.stream()
                .map(ComplianceIssue::toString)
                .collect(Collectors.joining("\n"));

        message.setText(body);
        Transport.send(message);
    }
}