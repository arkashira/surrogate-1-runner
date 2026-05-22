import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class EmailConfig {

    @Value("${surrogate-1.email.template}")
    private String emailTemplate;

    public String getEmailTemplate() {
        return emailTemplate;
    }
}