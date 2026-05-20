package com.axentx.surrogate1

import java.util.ArrayDeque

/**
 * Thread-safe event queue for telemetry data.
 * Uses ArrayDeque for O(1) add/remove operations.
 */
class EventQueue {
    
    private val queue = ArrayDeque<Event>()
    private val lock = Any()
    
    fun add(event: Event) {
        synchronized(lock) {
            queue.add(event)
        }
    }
    
    fun addAll(events: List<Event>) {
        synchronized(lock) {
            queue.addAll(events)
        }
    }
    
    fun getEvents(): List<Event> {
        synchronized(lock) {
            return queue.toList()
        }
    }
    
    fun getAndClear(): List<Event> {
        synchronized(lock) {
            val events = queue.toList()
            queue.clear()
            return events
        }
    }
    
    fun size(): Int = synchronized(lock) { queue.size }
    
    fun isEmpty(): Boolean = synchronized(lock) { queue.isEmpty() }
    
    fun clear() {
        synchronized(lock) {
            queue.clear()
        }
    }
}