package com.axentx.surrogate1

import com.axentx.surrogate1.types.KotlinSignature
import com.axentx.surrogate1.types.OverloadIdentifier
import java.util.regex.Pattern

/**
 * Resolves Kotlin function overloads and generates unique identifiers.
 * Parses function signatures, identifies parameter types, and creates
 * canonical overload references.
 */
class OverloadResolver {

    companion object {
        private val FUNCTION_SIGNATURE_PATTERN = Pattern.compile(
            "^\\s*(fun|val|var)\\s+(\\w+)\\s*\\(([^)]*)\\)(?:\\s*:\\s*(\\w+))?\\s*\\{?\\s*$"
        )
        private val PARAM_TYPE_PATTERN = Pattern.compile("\\w+(?:<[^>]+>)?")
    }

    /**
     * Parse a Kotlin function signature string into structured components.
     */
    fun parseSignature(signature: String): KotlinSignature? {
        val matcher = FUNCTION_SIGNATURE_PATTERN.matcher(signature)
        if (!matcher.matches()) {
            return null
        }

        val isFun = matcher.group(1) == "fun"
        val name = matcher.group(2) ?: ""
        val paramsStr = matcher.group(3) ?: ""
        val returnType = matcher.group(4) ?: ""

        val parameters = parseParameters(paramsStr)

        return KotlinSignature(
            isFun = isFun,
            name = name,
            parameters = parameters,
            returnType = returnType
        )
    }

    /**
     * Parse parameter string into list of parameter types.
     */
    private fun parseParameters(paramsStr: String): List<String> {
        val trimmed = paramsStr.trim()
        if (trimmed.isEmpty() || trimmed == "...") {
            return emptyList()
        }

        return PARAM_TYPE_PATTERN.matcher(trimmed).results()
            .map { it.group().trim() }
            .toList()
    }

    /**
     * Generate a unique identifier for a function overload.
     * Format: "name(param1, param2, ...)" with normalized types.
     */
    fun generateOverloadId(signature: KotlinSignature): OverloadIdentifier {
        val paramTypes = signature.parameters.joinToString(", ") { normalizeType(it) }
        val overloadKey = "${signature.name}($paramTypes)"
        
        return OverloadIdentifier(
            name = signature.name,
            signature = overloadKey,
            parameterCount = signature.parameters.size,
            returnType = signature.returnType.ifEmpty { "void" }
        )
    }

    /**
     * Normalize a type string for comparison purposes.
     */
    private fun normalizeType(type: String): String {
        return type
            .replace(" ", "")
            .replace("?", "")
            .replace("!", "")
            .replace(" ", "")
    }

    /**
     * Resolve a function call to the correct overload based on parameter types.
     */
    fun resolveOverload(
        targetSignature: KotlinSignature,
        availableOverloads: List<OverloadIdentifier>
    ): OverloadIdentifier? {
        val targetParamTypes = targetSignature.parameters.map { normalizeType(it) }
        
        return availableOverloads.find { overload ->
            val overloadParams = parseOverloadParams(overload.signature)
            if (overloadParams.size != targetParamTypes.size) {
                return@find false
            }
            
            (0 until targetParamTypes.size).all { i ->
                normalizeType(overloadParams[i]) == targetParamTypes[i]
            }
        }
    }

    /**
     * Extract parameter types from an overload identifier signature string.
     */
    private fun parseOverloadParams(signature: String): List<String> {
        val paramsStr = signature.substringAfter("(").substringBefore(")")
        return if (paramsStr.isEmpty()) emptyList()
        else PARAM_TYPE_PATTERN.matcher(paramsStr).results()
            .map { it.group().trim() }
            .toList()
    }
}