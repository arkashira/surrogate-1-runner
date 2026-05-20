
import com.axentx.cloud.CloudClient;
import com.axentx.cloud.models.SessionConfig;
import com.axentx.utils.CostOptimizer;

import java.util.List;

public class AIAGENTSESSIONMANAGER {

    private final CloudClient cloudClient;
    private final CostOptimizer costOptimizer;

    public AIAGENTSESSIONMANAGER(CloudClient cloudClient, CostOptimizer costOptimizer) {
        this.cloudClient = cloudClient;
        this.costOptimizer = costOptimizer;
    }

    public void optimizeSessionConfigurations() {
        List<SessionConfig> sessionConfigs = cloudClient.getAllSessionConfigs();
        for (SessionConfig sessionConfig : sessionConfigs) {
            SessionConfig optimizedConfig = costOptimizer.optimize(sessionConfig);
            cloudClient.updateSessionConfig(sessionConfig.getId(), optimizedConfig);
        }
    }
}