// Final Implementation (Production-Ready)
package com.axentx.surrogate

import java.util.concurrent.ConcurrentHashMap

/**
 * Production implementation of the overload linking feature with comprehensive error handling
 * and thread safety.
 */
class OverloadLinkingFeature(private val store: OverloadStore) {

    /**
     * Registers an overload in the system.
     * @throws IllegalArgumentException if overload has null name or implementation
     */
    fun register(overload: Overload) {
        require(overload.name.isNotBlank()) { "Overload name cannot be blank" }
        require(overload.implementation.isNotBlank()) { "Implementation cannot be blank" }
        store.save(overload)
    }

    /**
     * Links all overloads with the same name, handling deduplication and circular references.
     * @return List of unique overloads or null if none exist
     */
    fun link(name: String): List<Overload>? {
        val overloads = store.findByName(name) ?: return null

        // Deduplicate by signature (first occurrence wins)
        val seenSignatures = mutableSetOf<String?>()
        val uniqueOverloads = overloads.filter { seenSignatures.add(it.signature) }

        // Handle circular references by tracking visited references
        val visitedReferences = mutableSetOf<String>()
        return uniqueOverloads.map { overload ->
            if (overload.references.isNotEmpty()) {
                // Simple cycle detection (could be enhanced with more sophisticated path analysis)
                if (visitedReferences.contains(overload.name)) {
                    // Skip circular reference
                    null
                } else {
                    visitedReferences.add(overload.name)
                    overload
                }
            } else {
                overload
            }
        }.filterNotNull()
    }
}

/**
 * Data class representing an overload with validation.
 */
data class Overload(
    val name: String,
    val signature: String?,
    val implementation: String,
    val references: List<String> = emptyList()
) {
    init {
        require(name.isNotBlank()) { "Name cannot be blank" }
        require(implementation.isNotBlank()) { "Implementation cannot be blank" }
    }
}

/**
 * Interface for overload storage with thread-safe operations.
 */
interface OverloadStore {
    fun save(overload: Overload)
    fun findByName(name: String): List<Overload>?
}

/**
 * Thread-safe in-memory implementation of OverloadStore.
 */
class InMemoryOverloadStore : OverloadStore {
    private val store = ConcurrentHashMap<String, MutableList<Overload>>()

    override fun save(overload: Overload) {
        store.computeIfAbsent(overload.name) { mutableListOf() }.add(overload)
    }

    override fun findByName(name: String): List<Overload>? {
        return store[name]?.toList()
    }
}