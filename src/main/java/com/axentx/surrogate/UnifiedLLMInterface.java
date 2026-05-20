public class Main {
    public static void main(String[] args) {
        // Create a unified interface
        UnifiedLLMInterface unifiedInterface = new UnifiedLLMInterface();
        
        // Register a Claude provider
        ClaudeProvider claudeProvider = new ClaudeProvider("YOUR_API_KEY");
        unifiedInterface.registerProvider("claude", claudeProvider);
        
        // Set Claude as the default provider
        unifiedInterface.setDefaultProvider("claude");
        
        // Create an LLM request
        LLMRequest request = new LLMRequest("Hello, how are you?");
        
        // Send the request and get the response
        LLMResponse response = unifiedInterface.sendRequest(request);
        
        // Print the response content
        System.out.println(response.getContent());
    }
}