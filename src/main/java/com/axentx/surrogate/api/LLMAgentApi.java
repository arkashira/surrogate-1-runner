package com.axentx.surrogate.api;

import com.axentx.surrogate.service.LLMAgentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/llm-agent")
public class LLMAgentApi {

    @Autowired
    private LLMAgentService llmAgentService;

    @PostMapping("/{agentId}/request")
    public LLMResponse handleAgentRequest(
            @PathVariable String agentId,
            @RequestBody LLMRequest request) {
        return llmAgentService.processAgentRequest(agentId, request);
    }
}

class LLMRequest {
    private String prompt;
    private String context;
    // getters/setters
}

class LLMResponse {
    private String response;
    private String status;
    // getters/setters
}