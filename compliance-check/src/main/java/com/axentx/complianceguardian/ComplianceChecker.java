import com.axentx.complianceguardian.notifications.EmailNotifier;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ComplianceChecker {

    @Autowired
    private EmailNotifier emailNotifier;

    public void checkCompliance() {
        // Perform compliance check logic here
        // ...

        // If non-compliant, send email notification
        String recipientEmail = "sysadmin@example.com";
        emailNotifier.sendNonComplianceNotification(recipientEmail);
    }
}