package com.axentx.surrogate.workflow;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/workflows")
public class WorkflowController {

    @Autowired
    private WorkflowService workflowService;

    @GetMapping
    public List<Workflow> getAllWorkflows() {
        return workflowService.getAllWorkflows();
    }

    @GetMapping("/{id}")
    public Workflow getWorkflowById(@PathVariable Long id) {
        return workflowService.getWorkflowById(id);
    }

    @PostMapping
    public Workflow createWorkflow(@RequestBody Workflow workflow) {
        return workflowService.createWorkflow(workflow);
    }

    @PutMapping("/{id}")
    public Workflow updateWorkflow(@PathVariable Long id, @RequestBody Workflow workflowDetails) {
        return workflowService.updateWorkflow(id, workflowDetails);
    }

    @DeleteMapping("/{id}")
    public void deleteWorkflow(@PathVariable Long id) {
        workflowService.deleteWorkflow(id);
    }
}