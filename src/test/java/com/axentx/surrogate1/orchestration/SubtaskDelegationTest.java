package com.axentx.surrogate1.orchestration;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class SubtaskDelegationTest {

    @Test
    public void testDelegateSubtask() {
        String subtaskName = "testSubtask";
        boolean[] executed = {false};

        Runnable subtask = () -> {
            executed[0] = true;
        };

        SubtaskDelegation.delegateSubtask(subtaskName, subtask);

        assertTrue(executed[0], "Subtask should have been executed");
    }
}