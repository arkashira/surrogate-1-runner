package com.axentx.surrogate1.notification;

import com.axentx.surrogate1.model.Anomaly;
import com.axentx.surrogate1.model.Notification;
import com.axentx.surrogate1.model.NotificationType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NotificationService {

    private final JavaMailSender javaMailSender;

    @Autowired
    public NotificationService(JavaMailSender javaMailSender) {
        this.javaMailSender = javaMailSender;
    }

    public void sendNotification(Anomaly anomaly) {
        Notification notification = createNotification(anomaly);
        sendEmailNotification(notification);
        sendInAppNotification(notification);
    }

    private Notification createNotification(Anomaly anomaly) {
        Notification notification = new Notification();
        notification.setType(NotificationType.ANOMALY_DETECTED);
        notification.setAnomaly(anomaly);
        notification.setMessage("Anomaly detected: " + anomaly.getDescription());
        return notification;
    }

    private void sendEmailNotification(Notification notification) {
        SimpleMailMessage mailMessage = new SimpleMailMessage();
        mailMessage.setTo("finance@example.com");
        mailMessage.setSubject("Anomaly Detected");
        mailMessage.setText(notification.getMessage());
        javaMailSender.send(mailMessage);
    }

    private void sendInAppNotification(Notification notification) {
        // Implement in-app notification logic here
        System.out.println("In-app notification sent: " + notification.getMessage());
    }
}