import com.axentx.surrogate1.model.AccessControl;
import com.axentx.surrogate1.model.CloudProviderType;

public class RemediationService {
    public void remediateSecurityIncident(AccessControl accessControl, CloudProviderType type) {
        CloudProvider provider = CloudProviderFactory.createCloudProvider(type);
        AccessControlUpdater updater = new AccessControlUpdater();
        updater.updateAccessControls(provider, accessControl);
        updater.rollbackChanges(provider);
    }
}