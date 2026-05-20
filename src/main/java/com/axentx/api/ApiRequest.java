package com.axentx.api;

import java.util.Map;

public class ApiRequest {
    private String apiName;
    private String method;
    private String endpoint;
    private Map<String, String> headers;
    private String body;
    private String computedSignature;

    public ApiRequest(String apiName, String method, String endpoint, 
                      Map<String, String> headers, String body) {
        this.apiName = apiName;
        this.method = method;
        this.endpoint = endpoint;
        this.headers = headers;
        this.body = body;
    }

    // Getters
    public String getApiName() { return apiName; }
    public String getMethod() { return method; }
    public String getEndpoint() { return endpoint; }
    public Map<String, String> getHeaders() { return headers; }
    public String getBody() { return body; }
    public String getComputedSignature() { return computedSignature; }
    
    public void setComputedSignature(String signature) { 
        this.computedSignature = signature; 
    }
}