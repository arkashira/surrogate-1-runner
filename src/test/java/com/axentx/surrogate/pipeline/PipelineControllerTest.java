package com.axentx.surrogate.pipeline;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(PipelineController.class)
class PipelineControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PipelineService pipelineService;

    @Test
    void shouldPausePipeline() throws Exception {
        mockMvc.perform(post("/pipelines/1/pause"))
                .andExpect(status().isOk());

        verify(pipelineService).pausePipeline("1");
    }

    @Test
    void shouldCancelPipeline() throws Exception {
        mockMvc.perform(post("/pipelines/1/cancel"))
                .andExpect(status().isOk());

        verify(pipelineService).cancelPipeline("1");
    }
}