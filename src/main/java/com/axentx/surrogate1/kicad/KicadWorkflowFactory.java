package com.axentx.surrogate1.kicad;

import com.axentx.surrogate1.workflow.Workflow;
import com.axentx.surrogate1.workflow.WorkflowFactory;

public class KicadWorkflowFactory implements WorkflowFactory {
    @Override
    public Workflow createWorkflow() {
        return new KicadWorkflow();
    }
}