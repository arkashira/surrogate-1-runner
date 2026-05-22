import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InsightEmailController {

    private final InsightEmailService insightEmailService;

    @Autowired
    public InsightEmailController(InsightEmailService insightEmailService) {
        this.insightEmailService = insightEmailService;
    }

    @GetMapping("/insight-email")
    public void sendInsightEmails() {
        insightEmailService.sendInsightEmails();
    }
}