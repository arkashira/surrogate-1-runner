package com.axentx.surrogate.utils

object LinkGenerator {

    /**
     * Generates a deterministic, URL-safe, and HTML-compliant identifier for a function overload.
     * 
     * Handles:
     * - Fully qualified names (replaces . with _)
     * - Generics (replaces < and > with _)
     * - Array brackets (strips [ and ])
     * 
     * Example: "exampleFunction(List<Int>)" -> "exampleFunction_List_Int_"
     */
    fun generateUniqueLink(functionName: String, paramTypes: List<String>): String {
        val sanitizedParams = paramTypes.joinToString("_") { type ->
            type
                .replace(".", "_")
                .replace("[\\[\\]]".toRegex(), "") // strip array brackets
                .replace("<", "_")
                .replace(">", "_")
                .replace(" ", "")
        }
        
        return if (sanitizedParams.isBlank()) {
            functionName
        } else {
            "${functionName}_$sanitizedParams"
        }
    }
}