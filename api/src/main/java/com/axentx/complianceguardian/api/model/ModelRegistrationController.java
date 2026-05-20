package com.axentx.complianceguardian.api.model;

import com.axentx.complianceguardian.service.ModelRegistrationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/models")
public class ModelRegistrationController {

    @Autowired
    private ModelRegistrationService modelRegistrationService;

    @PostMapping
    public String registerModel(@RequestBody ModelRegistrationRequest request) {
        return modelRegistrationService.registerModel(request);
    }

    @GetMapping
    public List<ModelRegistrationResponse> getAllModels() {
        return modelRegistrationService.getAllModels();
    }

    @DeleteMapping("/{modelId}")
    public void removeModel(@PathVariable String modelId) {
        modelRegistrationService.removeModel(modelId);
    }
}