package com.axentx.surrogate.api;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import com.axentx.surrogate.service.SyntheticDataService;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(SyntheticDataController.class)
public class SyntheticDataControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SyntheticDataService syntheticDataService;

    @Test
    public void getSyntheticData_shouldReturnSyntheticData() throws Exception {
        when(syntheticDataService.generateSyntheticData("datadog")).thenReturn("{\"metric\": \"datadog.metric\", \"value\": 42}");

        mockMvc.perform(get("/api/synthetic-data")
                .param("integrationType", "datadog"))
                .andExpect(status().isOk())
                .andExpect(content().string("{\"metric\": \"datadog.metric\", \"value\": 42}"));
    }
}