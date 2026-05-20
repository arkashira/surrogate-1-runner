package com.axentx.surrogate.controllers;

import com.axentx.surrogate.alerts.AlertService;
import com.axentx.surrogate.models.AIModel;
import com.axentx.surrogate.models.Alert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.List;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
public class AlertControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AlertService alertService;

    @Test
    public void testGetAlerts() throws Exception {
        AIModel model = new AIModel("test-model", "test-description");
        Alert alert = new Alert(model, "Test risk description", "Test mitigation action");
        List<Alert> alerts = Arrays.asList(alert);

        when(alertService.getAlerts()).thenReturn(alerts);

        mockMvc.perform(get("/api/alerts"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].model.name").value("test-model"))
                .andExpect(jsonPath("$[0].riskDescription").value("Test risk description"))
                .andExpect(jsonPath("$[0].mitigationAction").value("Test mitigation action"));
    }
}