import com.axentx.surrogate1.config.ConfigLoader;

public class Client {
    private String provider;
    private String apiKey;

    public Client(String provider, String apiKey) {
        this.provider = provider;
        this.apiKey = apiKey;
    }

    public Client(String provider) {
        Map<String, String> config = ConfigLoader.loadConfig();
        ConfigLoader.validateConfig(config);
        this.provider = provider;
        this.apiKey = config.get(provider);
    }

    public String getProvider() {
        return provider;
    }

    public String getApiKey() {
        return apiKey;
    }
}