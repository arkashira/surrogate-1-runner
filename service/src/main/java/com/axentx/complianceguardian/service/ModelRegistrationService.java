package com.axentx.complianceguardian.service;

import com.axentx.complianceguardian.api.model.ModelRegistrationRequest;
import com.axentx.complianceguardian.api.model.ModelRegistrationResponse;
import com.axentx.complianceguardian.repository.ModelRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class ModelRegistrationService {

    @Autowired
    private ModelRepository modelRepository;

    public String registerModel(ModelRegistrationRequest request) {
        String modelId = UUID.randomUUID().toString();
        // TODO: Save model details to the database
        return modelId;
    }

    public List<ModelRegistrationResponse> getAllModels() {
        // TODO: Fetch all models from the database
        return List.of();
    }

    public void removeModel(String modelId) {
        // TODO: Remove model from the database
    }
}