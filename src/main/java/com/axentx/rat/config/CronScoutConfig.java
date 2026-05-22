import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CronScoutConfig {

    @Value("${surrogate-1.cron.log.file}")
    private String logFile;

    public String getLogFile() {
        return logFile;
    }
}