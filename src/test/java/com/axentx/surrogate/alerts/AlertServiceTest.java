package com.axentx.surrogate.alerts;

import com.axentx.surrogate.models.AIModel;
import com.axentx.surrogate.models.Alert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@SpringBootTest
public class AlertServiceTest {

    @Autowired
    private AlertService alertService;

    @Test
    public void testGenerateAlert() {
        AIModel model = new AIModel("test-model", "test-description");
        String riskDescription = "Test risk description";
        String mitigationAction = "Test mitigation action";

        alertService.generateAlert(model, riskDescription, mitigationAction);

        List<Alert> alerts = alertService.getAlerts();
        assertNotNull(alerts);
        assertEquals(1, alerts.size());

        Alert alert = alerts.get(0);
        assertEquals(model, alert.getModel());
        assertEquals(riskDescription, alert.getRiskDescription());
        assertEquals(mitigationAction, alert.getMitigationAction());
    }
}