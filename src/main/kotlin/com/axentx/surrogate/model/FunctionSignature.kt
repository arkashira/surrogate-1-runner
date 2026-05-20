package com.axentx.surrogate.model

/**
 * Represents the signature of a function, specifically focusing on parameter types
 * to distinguish overloads.
 */
data class FunctionSignature(
    val parameterTypes: List<String>
) {
    // Helper to display signature as a string, e.g., "(Int, String)"
    override fun toString(): String = parameterTypes.joinToString(", ", "(", ")")
}