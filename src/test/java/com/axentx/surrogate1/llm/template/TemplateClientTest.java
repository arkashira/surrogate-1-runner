package com.axentx.surrogate1.llm.template;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

import static org.junit.jupiter.api.Assertions.*;

class TemplateClientTest {

    @Test
    void testAbstractClassHasRequiredMethods() {
        Class<?> clazz = TemplateClient.class;
        assertTrue(Modifier.isAbstract(clazz.getModifiers()), "TemplateClient should be abstract");

        Method sendPrompt = null;
        Method parseResponse = null;
        for (Method m : clazz.getDeclaredMethods()) {
            if (m.getName().equals("sendPrompt")) {
                sendPrompt = m;
            } else if (m.getName().equals("parseResponse")) {
                parseResponse = m;
            }
        }
        assertNotNull(sendPrompt, "sendPrompt method must exist");
        assertTrue(Modifier.isAbstract(sendPrompt.getModifiers()), "sendPrompt must be abstract");

        assertNotNull(parseResponse, "parseResponse method must exist");
        assertTrue(Modifier.isAbstract(parseResponse.getModifiers()), "parseResponse must be abstract");
    }
}