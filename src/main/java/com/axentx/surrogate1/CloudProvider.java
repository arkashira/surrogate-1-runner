import com.axentx.surrogate1.model.CloudProviderType;

public enum CloudProvider {
    AWS(CloudProviderType.AWS),
    AZURE(CloudProviderType.AZURE),
    GCP(CloudProviderType.GCP);

    private final CloudProviderType type;

    CloudProvider(CloudProviderType type) {
        this.type = type;
    }

    public CloudProviderType getType() {
        return type;
    }
}