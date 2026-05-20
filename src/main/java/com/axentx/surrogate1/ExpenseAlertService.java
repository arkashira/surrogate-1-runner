import com.slack.api.Slack;
import com.slack.api.methods.MethodsClient;
import com.slack.api.methods.request.chat.ChatPostMessageRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.mail.internet.MimeMessage;
import javax.mail.javamail.MimeMessageHelper;
import javax.mail.javamail.MimeMessageRecipientType;
import java.util.List;

import static com.axentx.surrogate1.utils.EmailUtils.sendEmail;

@Service
public class ExpenseAlertService {
    @Value("${slack.token}")
    private String slackToken;

    @Value("${slack.channel}")
    private String slackChannel;

    @Value("${email.from}")
    private String emailFrom;

    @Value("${email.to}")
    private String emailTo;

    public void sendAlert(String message) {
        sendEmail(emailFrom, emailTo, "Anomalous Expense Detected", message);
        sendSlackMessage(message);
    }

    private void sendSlackMessage(String message) {
        Slack slack = Slack.getInstance();
        MethodsClient methods = slack.methods(slackToken);

        ChatPostMessageRequest request = ChatPostMessageRequest.builder()
                .channel(slackChannel)
                .text(message)
                .build();

        methods.chatPostMessage(request);
    }
}