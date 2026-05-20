package com.axentx.wholphin.common

import java.time.Instant
import java.util.UUID
import java.util.concurrent.ConcurrentLinkedQueue

/**
 * Represents a playback event captured by the background worker.
 *
 * @property id Unique identifier for the event.
 * @property type Type of the event (flash start/end, buffer start/end).
 * @property timestamp The exact instant the event was recorded.
 * @property metadata Optional metadata associated with the event.
 */
data class PlaybackEvent(
    val id: UUID = UUID.randomUUID(),
    val type: PlaybackEventType,
    val timestamp: Instant = Instant.now(),
    val metadata: Map<String, Any> = emptyMap()
) {
    companion object {
        fun flashStart(metadata: Map<String, Any> = emptyMap()) =
            PlaybackEvent(type = PlaybackEventType.FLASH_START, metadata = metadata)

        fun flashEnd(metadata: Map<String, Any> = emptyMap()) =
            PlaybackEvent(type = PlaybackEventType.FLASH_END, metadata = metadata)

        fun bufferStart(metadata: Map<String, Any> = emptyMap()) =
            PlaybackEvent(type = PlaybackEventType.BUFFER_START, metadata = metadata)

        fun bufferEnd(metadata: Map<String, Any> = emptyMap()) =
            PlaybackEvent(type = PlaybackEventType.BUFFER_END, metadata = metadata)
    }
}

/**
 * Thread-safe local queue for playback events.
 */
class PlaybackEventQueue {
    private val queue = ConcurrentLinkedQueue<PlaybackEvent>()

    fun enqueue(event: PlaybackEvent) {
        queue.offer(event)
    }

    fun dequeue(): PlaybackEvent? = queue.poll()

    fun peek(): PlaybackEvent? = queue.peek()

    fun size(): Int = queue.size

    fun isEmpty(): Boolean = queue.isEmpty()

    fun drainAll(): List<PlaybackEvent> {
        val events = mutableListOf<PlaybackEvent>()
        while (true) {
            val event = queue.poll() ?: break
            events.add(event)
        }
        return events
    }

    fun clear() = queue.clear()
}