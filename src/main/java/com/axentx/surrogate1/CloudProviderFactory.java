import com.axentx.surrogate1.model.CloudProviderType;

public class CloudProviderFactory {
    public static CloudProvider createCloudProvider(CloudProviderType type) {
        switch (type) {
            case AWS:
                return CloudProvider.AWS;
            case AZURE:
                return CloudProvider.AZURE;
            case GCP:
                return CloudProvider.GCP;
            default:
                throw new UnsupportedOperationException("Unsupported cloud provider type");
        }
    }
}