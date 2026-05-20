package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ConversationHistoryTest {

    @Test
    void testAddAndRetrieve() {
        ConversationHistory history = new ConversationHistory();
        history.addTurn("Hello", "Hi there!");
        history.addTurn("How are you?", "I'm fine, thanks.");

        List<ConversationHistory.Entry> entries = history.getAll();
        assertEquals(2, entries.size());

        assertEquals("Hello", entries.get(0).getUserMessage());
        assertEquals("Hi there!", entries.get(0).getAssistantReply());

        assertEquals("How are you?", entries.get(1).getUserMessage());
        assertEquals("I'm fine, thanks.", entries.get(1).getAssistantReply());
    }

    @Test
    void testClear() {
        ConversationHistory history = new ConversationHistory();
        history.addTurn("Test", "Response");
        assertEquals(1, history.size());
        history.clear();
        assertEquals(0, history.size());
        assertTrue(history.getAll().isEmpty());
    }

    @Test
    void testNullMessages() {
        ConversationHistory history = new ConversationHistory();
        assertThrows(IllegalArgumentException.class, () -> history.addTurn(null, "Reply"));
        assertThrows(IllegalArgumentException.class, () -> history.addTurn("Msg", null));
    }

    @Test
    void testThreadSafety() throws InterruptedException {
        ConversationHistory history = new ConversationHistory();

        // 10 threads each adding 100 turns
        Thread[] threads = new Thread[10];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    history.addTurn("msg", "reply");
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) t.join();

        assertEquals(1000, history.size());
    }
}