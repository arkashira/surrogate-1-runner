package com.axentx.surrogate1.orchestration;

import com.axentx.surrogate1.subagents.Subagent;
import com.axentx.surrogate1.workflow.WorkflowContext;

import java.util.List;

public class OrchestrationLogic {

    public void executeWorkflow(List<Subagent> subagents, WorkflowContext context) {
        subagents.forEach(subagent -> subagent.execute(context));
        // Retain context across subagents by passing WorkflowContext as argument
    }
}