package com.axentx.surrogate1.controller;

import com.axentx.surrogate1.service.StrategyService;
import com.axentx.surrogate1.model.StrategyRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.ByteArrayInputStream;

@RestController
@RequestMapping("/api/strategies")
public class StrategyController {

    @Autowired
    private StrategyService strategyService;

    /**
     * Generates strategies based on the provided business details and goals.
     *
     * @param request The strategy request containing business details and goals.
     * @return A string indicating the generated strategies.
     */
    @PostMapping("/generate")
    public String generateStrategies(@RequestBody StrategyRequest request) {
        return strategyService.generateStrategies(request);
    }

    /**
     * Downloads the strategy content for a given strategy ID.
     *
     * @param strategyId The ID of the strategy to download.
     * @return A response entity containing the strategy content as an attachment.
     */
    @GetMapping("/download/{strategyId}")
    public ResponseEntity<InputStreamResource> downloadStrategy(@PathVariable String strategyId) {
        String strategyContent = strategyService.getStrategyContent(strategyId);
        InputStreamResource resource = new InputStreamResource(new ByteArrayInputStream(strategyContent.getBytes()));

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment;filename=" + strategyId + ".txt")
                .contentType(MediaType.TEXT_PLAIN)
                .body(resource);
    }
}