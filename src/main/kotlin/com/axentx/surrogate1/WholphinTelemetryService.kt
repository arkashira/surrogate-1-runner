package com.axentx.surrogate1

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import kotlinx.coroutines.*
import java.util.ArrayDeque

class WholphinTelemetryService : Service() {
    
    companion object {
        private const val TAG = "WholphinTelemetryService"
        val EVENT_TYPES = listOf("flash_start", "flash_end", "buffer_start", "buffer_end")
    }
    
    private val eventQueue = ArrayDeque<Event>()
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    
    private val binder = object : IWholphinTelemetryService.Stub() {
        override fun getEvents(): List<Event> {
            synchronized(eventQueue) {
                return eventQueue.toList()
            }
        }
        
        override fun clearEvents() {
            synchronized(eventQueue) {
                eventQueue.clear()
            }
        }
    }
    
    override fun onBind(intent: Intent?): IBinder? {
        Log.d(TAG, "onBind called")
        return binder
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, "onStartCommand called with intent: $intent")
        
        scope.launch {
            capturePlaybackEvents()
        }
        
        return START_STICKY
    }
    
    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
        Log.d(TAG, "Service destroyed")
    }
    
    /**
     * Captures playback events from the media pipeline.
     * In production, this would hook into actual playback callbacks.
     */
    private suspend fun capturePlaybackEvents() {
        // Simulate event capture - replace with actual media pipeline hooks
        val events = EVENT_TYPES.map { eventType ->
            Event(eventType, System.currentTimeMillis())
        }
        
        synchronized(eventQueue) {
            events.forEach { event ->
                eventQueue.add(event)
                Log.d(TAG, "Captured event: ${event.type} at ${event.timestamp}")
            }
        }
    }
    
    /**
     * Public API for injecting events (for testing and external callers)
     */
    fun onEvent(eventType: String, timestamp: Long, eventId: String) {
        synchronized(eventQueue) {
            eventQueue.add(Event(eventType, timestamp, eventId))
        }
    }
    
    /**
     * Get current queue size without removing items
     */
    fun getQueueSize(): Int = synchronized(eventQueue) { eventQueue.size }
}