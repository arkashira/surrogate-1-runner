package com.axentx.surrogate1.subagents;

import com.axentx.surrogate1.workflow.WorkflowContext;

public interface Subagent {
    void execute(WorkflowContext context);
}