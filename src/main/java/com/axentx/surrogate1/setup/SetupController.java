package com.axentx.surrogate1.setup;

import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Controller
@RequestMapping("/setup")
public class SetupController {

    /**
     * Serves the static setup wizard HTML page.
     */
    @GetMapping(produces = MediaType.TEXT_HTML_VALUE)
    public ResponseEntity<Resource> getSetupPage() {
        Resource resource = new ClassPathResource("static/setup.html");
        return ResponseEntity.ok()
                .contentType(MediaType.TEXT_HTML)
                .body(resource);
    }

    /**
     * Receives step‑completion notifications from the wizard.
     * Returns a simple JSON payload confirming the step was recorded.
     *
     * @param step identifier of the completed step (e.g., "step2")
     * @return JSON with step name and status
     */
    @PostMapping(path = "/step", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public ResponseEntity<Map<String, String>> completeStep(@RequestParam String step) {
        // In a full implementation we would persist progress; here we just echo success.
        return ResponseEntity.ok(Map.of(
                "step", step,
                "status", "completed"
        ));
    }
}