package com.axentx.surrogate1.kicad;

import com.axentx.surrogate1.workflow.Workflow;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class KicadWorkflowFactoryTest {
    @Test
    void testCreateWorkflow() {
        KicadWorkflowFactory factory = new KicadWorkflowFactory();
        Workflow workflow = factory.createWorkflow();
        assertNotNull(workflow);
        assertTrue(workflow instanceof KicadWorkflow);
    }
}