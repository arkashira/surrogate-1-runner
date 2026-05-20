package com.axentx.surrogate1.kicad;

import com.axentx.surrogate1.workflow.WorkflowException;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class KicadWorkflowTest {
    @Test
    void testExecute() {
        KicadWorkflow workflow = new KicadWorkflow();
        assertDoesNotThrow(() -> workflow.execute());
    }

    @Test
    void testValidate() {
        KicadWorkflow workflow = new KicadWorkflow();
        assertDoesNotThrow(() -> workflow.validate());
    }
}