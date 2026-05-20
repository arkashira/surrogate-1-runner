package com.axentx.surrogate1

/**
 * Represents a telemetry event from the Wholphin playback pipeline.
 */
data class Event(
    val type: String,
    val timestamp: Long,
    val eventId: String = java.util.UUID.randomUUID().toString()
)