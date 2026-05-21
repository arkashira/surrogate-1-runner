package com.axentx.surrogate1;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.List;

@RestController
public class RadioStreamController {
    private final RadioStreamService radioStreamService;

    public RadioStreamController(RadioStreamService radioStreamService) {
        this.radioStreamService = radioStreamService;
    }

    @PostMapping("/record")
    public void recordStream(@RequestParam String url, @RequestParam String filename) throws IOException {
        radioStreamService.recordStream(url, filename);
    }

    @GetMapping("/recordings")
    public List<String> getRecordedStreams() {
        return radioStreamService.getRecordedStreams();
    }
}