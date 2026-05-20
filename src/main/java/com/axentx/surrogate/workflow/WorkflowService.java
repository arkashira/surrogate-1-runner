package com.axentx.surrogate.workflow;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class WorkflowService {

    @Autowired
    private WorkflowRepository workflowRepository;

    public List<Workflow> getAllWorkflows() {
        return workflowRepository.findAll();
    }

    public Workflow getWorkflowById(Long id) {
        return workflowRepository.findById(id).orElse(null);
    }

    public Workflow createWorkflow(Workflow workflow) {
        return workflowRepository.save(workflow);
    }

    public Workflow updateWorkflow(Long id, Workflow workflowDetails) {
        Workflow workflow = workflowRepository.findById(id).orElse(null);
        if (workflow != null) {
            workflow.setName(workflowDetails.getName());
            workflow.setDescription(workflowDetails.getDescription());
            workflow.setStatus(workflowDetails.getStatus());
            return workflowRepository.save(workflow);
        }
        return null;
    }

    public void deleteWorkflow(Long id) {
        workflowRepository.deleteById(id);
    }
}