package com.axentx.surrogate.api;

import com.axentx.surrogate.service.LLMAgentService;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
public class LLMAgentApiTest {

    @Mock
    private LLMAgentService llmAgentService;

    @InjectMocks
    private LLMAgentApi llmAgentApi;

    private MockMvc mockMvc;

    public void setup() {
        mockMvc = MockMvcBuilders.standaloneSetup(llmAgentApi).build();
    }

    @Test
    public void testHandleAgentRequest() throws Exception {
        String agentId = "test-agent";
        String json = "{\"prompt\":\"test\",\"context\":\"ctx\"}";
        
        mockMvc.perform(post("/api/v1/llm-agent/" + agentId + "/request")
                .contentType("application/json")
                .content(json))
                .andExpect(status().isOk());
    }
}