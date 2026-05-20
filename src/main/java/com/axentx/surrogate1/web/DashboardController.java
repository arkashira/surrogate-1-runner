package com.axentx.surrogate1.web;

import com.axentx.surrogate1.service.PLService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.math.BigDecimal;

@Controller
public class DashboardController {

    @Autowired
    private PLService plService;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        BigDecimal pl = plService.getLast30DaysPL();
        model.addAttribute("pl", pl);
        model.addAttribute("plColor", pl.signum() == -1 ? "red" : "green");
        return "dashboard";
    }
}

// /opt/axentx/surrogate-1/src/main/resources/templates/dashboard.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        .green { color: green; }
        .red { color: red; }
    </style>
</head>
<body>
<h1>Profit & Loss: <span th:text="${pl}" th:class="${plColor}"></span></h1>
<a href="/pl-report">View Detailed P&L Report</a>
</body>
</html>

// /opt/axentx/surrogate-1/src/test/java/com/axentx/surrogate1/web/DashboardControllerTest.java
package com.axentx.surrogate1.web;

import com.axentx.surrogate1.service.PLService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(DashboardController.class)
class DashboardControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PLService plService;

    @Test
    void testDashboard() throws Exception {
        when(plService.getLast30DaysPL()).thenReturn(BigDecimal.valueOf(1000));
        mockMvc.perform(get("/dashboard"))
                .andExpect(status().isOk())
                .andExpect(view().name("dashboard"))
                .andExpect(model().attribute("pl", BigDecimal.valueOf(1000)))
                .andExpect(model().attribute("plColor", "green"));
    }
}

## Summary
- DashboardController updated to fetch and display P&L.
- dashboard.html template updated to display P&L and link to report.
- DashboardControllerTest created to verify P&L fetching and display.