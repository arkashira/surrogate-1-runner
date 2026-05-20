package com.axentx.surrogate.pipeline;

import org.springframework.web.bind.annotation.*;
import java.util.concurrent.Future;

@RestController
@RequestMapping("/pipelines")
public class PipelineController {

    private final PipelineService pipelineService;

    public PipelineController(PipelineService pipelineService) {
        this.pipelineService = pipelineService;
    }

    @PostMapping("/{pipelineId}/pause")
    public void pausePipeline(@PathVariable String pipelineId) {
        pipelineService.pausePipeline(pipelineId);
    }

    @PostMapping("/{pipelineId}/cancel")
    public void cancelPipeline(@PathVariable String pipelineId) {
        pipelineService.cancelPipeline(pipelineId);
    }
}

interface PipelineService {
    void pausePipeline(String pipelineId);
    void cancelPipeline(String pipelineId);
}