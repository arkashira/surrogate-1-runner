package com.axentx.surrogate1.rightsize;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(RightsizeController.class)
class RightsizeControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testGetRecommendationsEndpoint() throws Exception {
        mockMvc.perform(get("/api/rightsize"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].resourceId").value("vm-frontend-01"));
    }
}