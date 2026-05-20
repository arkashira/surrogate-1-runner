package com.axentx.surrogate.model

/**
 * Represents a specific overload of a function.
 */
data class FunctionOverload(
    val functionName: String,
    val signature: FunctionSignature
)