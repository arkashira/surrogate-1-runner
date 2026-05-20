package com.axentx.surrogate1.notification;

import java.util.Map;
import java.util.Properties;
import java.util.concurrent.CompletableFuture;
import javax.mail.*;
import javax.mail.internet.*;

/**
 * Email-based alert channel implementation
 */
public class EmailAlertChannel implements AlertChannel {

    private final String channelName = "email";
    private final String smtpHost;
    private final int smtpPort;
    private final String username;
    private final String password;
    private final String fromAddress;
    private final String[] toAddresses;
    private final boolean enabled;

    public EmailAlertChannel(String smtpHost, int smtpPort, String username,
                            String password, String fromAddress, String[] toAddresses) {
        this.smtpHost = smtpHost;
        this.smtpPort = smtpPort;
        this.username = username;
        this.password = password;
        this.fromAddress = fromAddress;
        this.toAddresses = toAddresses;
        this.enabled = (smtpHost != null && !smtpHost.isEmpty() &&
                       toAddresses != null && toAddresses.length > 0);
    }

    @Override
    public CompletableFuture<Boolean> send(String title, String message, Map<String, String> metadata) {
        CompletableFuture<Boolean> future = CompletableFuture.completedFuture(true);

        if (!isEnabled()) {
            future = CompletableFuture.completedFuture(false);
            return future;
        }

        Properties props = new Properties();
        props.put("mail.smtp.host", smtpHost);
        props.put("mail.smtp.port", String.valueOf(smtpPort));
        Session session = Session.getInstance(props, null);

        try {
            MimeMessage mimeMessage = new MimeMessage(session);
            mimeMessage.setFrom(new InternetAddress(fromAddress));
            mimeMessage.setRecipients(Message.RecipientType.TO, InternetAddress.parse(String.join(",", toAddresses), false));
            mimeMessage.setSubject(title);
            Multipart multipart = new MimeMultipart();
            BodyPart messageBodyPart = new MimeBodyPart();
            messageBodyPart.setContent(message, "text/html; charset=utf-8");
            multipart.addBodyPart(messageBodyPart);

            for (Map.Entry<String, String> entry : metadata.entrySet()) {
                BodyPart metadataBodyPart = new MimeBodyPart();
                metadataBodyPart.setContent(entry.getValue(), "text/plain; charset=utf-8");
                metadataBodyPart.setHeader("Name", entry.getKey());
                multipart.addBodyPart(metadataBodyPart);
            }

            mimeMessage.setContent(multipart);

            Transport.send(mimeMessage);
            future = CompletableFuture.completedFuture(true);
        } catch (MessagingException e) {
            future = CompletableFuture.completedFuture(false);
            throw new RuntimeException("Failed to send email alert", e);
        }

        return future;
    }

    @Override
    public String getChannelName() {
        return channelName;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }
}