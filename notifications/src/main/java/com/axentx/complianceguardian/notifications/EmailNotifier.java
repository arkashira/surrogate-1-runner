import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Component;

@Component
public class EmailNotifier {

    @Autowired
    private JavaMailSender javaMailSender;

    public void sendEmail(String to, String subject, String text) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom("complianceguardian@axentx.com");
        message.setTo(to);
        message.setSubject(subject);
        message.setText(text);
        javaMailSender.send(message);
    }

    public void sendNonComplianceNotification(String recipientEmail) {
        String subject = "Non-compliant AI Model Detected";
        String text = "Your AI model has been found to be non-compliant. Please take corrective action.";
        sendEmail(recipientEmail, subject, text);
    }
}