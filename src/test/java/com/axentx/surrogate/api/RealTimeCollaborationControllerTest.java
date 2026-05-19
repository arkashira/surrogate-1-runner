package com.axentx.surrogate.api;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(RealTimeCollaborationController.class)
public class RealTimeCollaborationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SimpMessagingTemplate messagingTemplate;

    @Test
    public void testJoinCollaboration_validRequest() throws Exception {
        mockMvc.perform(post("/api/collaboration/join")
                .contentType("application/json")
                .content("{\"userId\":\"123\",\"sessionId\":\"456\"}"))
                .andExpect(status().isOk());
        verify(messagingTemplate).convertAndSend(any(), any());
    }

    @Test
    public void testJoinCollaboration_invalidRequest() throws Exception {
        mockMvc.perform(post("/api/collaboration/join")
                .contentType("application/json")
                .content("{\"userId\":\"123\"}"))
                .andExpect(status().isBadRequest());
        verify(messagingTemplate, never()).convertAndSend(any(), any());
    }
}